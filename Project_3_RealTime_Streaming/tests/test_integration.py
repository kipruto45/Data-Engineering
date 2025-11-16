"""Integration tests for Kafka producer and consumer"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from streaming.kafka_producer import TransactionProducer
from streaming.kafka_consumer import TransactionConsumer


class TestTransactionProducer:
    """Test Kafka producer functionality"""
    
    @patch('streaming.kafka_producer.KafkaProducer')
    def test_producer_initialization(self, mock_kafka_producer_class):
        """Test producer initialization"""
        mock_producer_instance = Mock()
        mock_kafka_producer_class.return_value = mock_producer_instance
        
        producer = TransactionProducer(bootstrap_servers='localhost:9092', topic='transactions')
        
        assert producer.topic == 'transactions'
        assert producer.producer is not None
        mock_kafka_producer_class.assert_called_once()
    
    def test_generate_transaction(self, sample_transaction):
        """Test transaction generation"""
        with patch('streaming.kafka_producer.KafkaProducer'):
            producer = TransactionProducer()
            
            transaction = producer.generate_transaction()
            
            # Verify required fields
            required_fields = ['transaction_id', 'sender', 'receiver', 'amount', 
                             'timestamp', 'transaction_type', 'status', 'provider', 'fee']
            for field in required_fields:
                assert field in transaction
            
            # Verify data types
            assert isinstance(transaction['transaction_id'], str)
            assert isinstance(transaction['amount'], float)
            assert transaction['amount'] > 0
            assert transaction['status'] in ['success', 'failed']
            assert transaction['transaction_type'] in ['transfer', 'withdrawal', 'deposit']
    
    @patch('streaming.kafka_producer.KafkaProducer')
    def test_send_transaction_success(self, mock_kafka_producer_class, sample_transaction):
        """Test successful transaction sending"""
        mock_producer_instance = Mock()
        mock_future = Mock()
        mock_metadata = Mock(topic='transactions', partition=0, offset=1)
        mock_future.get.return_value = mock_metadata
        mock_producer_instance.send.return_value = mock_future
        mock_kafka_producer_class.return_value = mock_producer_instance
        
        producer = TransactionProducer()
        result = producer.send_transaction(transaction=sample_transaction)
        
        assert result is True
        mock_producer_instance.send.assert_called_once()
    
    @patch('streaming.kafka_producer.KafkaProducer')
    def test_send_batch(self, mock_kafka_producer_class):
        """Test batch transaction sending"""
        mock_producer_instance = Mock()
        mock_future = Mock()
        mock_metadata = Mock(topic='transactions', partition=0, offset=1)
        mock_future.get.return_value = mock_metadata
        mock_producer_instance.send.return_value = mock_future
        mock_kafka_producer_class.return_value = mock_producer_instance
        
        producer = TransactionProducer()
        success_count = producer.send_batch(count=50)
        
        assert success_count == 50
        assert mock_producer_instance.send.call_count == 50
    
    @patch('streaming.kafka_producer.KafkaProducer')
    def test_producer_close(self, mock_kafka_producer_class):
        """Test producer close"""
        mock_producer_instance = Mock()
        mock_kafka_producer_class.return_value = mock_producer_instance
        
        producer = TransactionProducer()
        producer.close()
        
        mock_producer_instance.close.assert_called_once()


class TestTransactionConsumer:
    """Test Kafka consumer functionality"""
    
    @patch('streaming.kafka_consumer.KafkaConsumer')
    def test_consumer_initialization(self, mock_kafka_consumer_class):
        """Test consumer initialization"""
        mock_consumer_instance = Mock()
        mock_kafka_consumer_class.return_value = mock_consumer_instance
        
        consumer = TransactionConsumer(
            bootstrap_servers='localhost:9092',
            topic='transactions',
            group_id='transaction-group'
        )
        
        assert consumer.topic == 'transactions'
        assert consumer.group_id == 'transaction-group'
        assert consumer.message_count == 0
        mock_kafka_consumer_class.assert_called_once()
    
    @patch('streaming.kafka_consumer.KafkaConsumer')
    def test_process_successful_message(self, mock_kafka_consumer_class):
        """Test processing successful transaction message"""
        mock_consumer_instance = Mock()
        mock_kafka_consumer_class.return_value = mock_consumer_instance
        
        consumer = TransactionConsumer()
        
        message = {
            'transaction_id': 'TXN001',
            'sender': '254712345678',
            'receiver': '254712345679',
            'amount': 5000.00,
            'status': 'success',
            'transaction_type': 'transfer'
        }
        
        result = consumer.process_message(message)
        
        assert result is True
        assert consumer.stats['total_messages'] == 1
        assert consumer.stats['successful'] == 1
        assert consumer.stats['total_amount'] == 5000.00
    
    @patch('streaming.kafka_consumer.KafkaConsumer')
    def test_process_failed_message(self, mock_kafka_consumer_class):
        """Test processing failed transaction message"""
        mock_consumer_instance = Mock()
        mock_kafka_consumer_class.return_value = mock_consumer_instance
        
        consumer = TransactionConsumer()
        
        message = {
            'transaction_id': 'TXN002',
            'sender': '254712345678',
            'receiver': '254712345679',
            'amount': 3000.00,
            'status': 'failed',
            'transaction_type': 'withdrawal'
        }
        
        result = consumer.process_message(message)
        
        assert result is True
        assert consumer.stats['total_messages'] == 1
        assert consumer.stats['failed'] == 1
        assert consumer.stats['total_amount'] == 0  # Failed txn doesn't add to total
    
    @patch('streaming.kafka_consumer.KafkaConsumer')
    def test_get_stats(self, mock_kafka_consumer_class):
        """Test stats retrieval"""
        mock_consumer_instance = Mock()
        mock_kafka_consumer_class.return_value = mock_consumer_instance
        
        consumer = TransactionConsumer()
        
        # Process some messages
        consumer.stats['total_messages'] = 100
        consumer.stats['successful'] = 85
        consumer.stats['failed'] = 15
        consumer.stats['total_amount'] = 50000.00
        consumer.message_count = 100
        
        stats = consumer.get_stats()
        
        assert stats['messages_processed'] == 100
        assert stats['stats']['total_messages'] == 100
        assert stats['stats']['successful'] == 85
        assert stats['stats']['failed'] == 15
        assert 'timestamp' in stats
    
    @patch('streaming.kafka_consumer.KafkaConsumer')
    def test_consumer_close(self, mock_kafka_consumer_class):
        """Test consumer close"""
        mock_consumer_instance = Mock()
        mock_kafka_consumer_class.return_value = mock_consumer_instance
        
        consumer = TransactionConsumer()
        consumer.close()
        
        mock_consumer_instance.close.assert_called_once()


class TestKafkaIntegration:
    """Integration tests for producer and consumer"""
    
    @patch('streaming.kafka_producer.KafkaProducer')
    @patch('streaming.kafka_consumer.KafkaConsumer')
    def test_producer_consumer_flow(self, mock_consumer_class, mock_producer_class):
        """Test full producer-consumer flow"""
        # Setup producer
        mock_producer_instance = Mock()
        mock_future = Mock()
        mock_metadata = Mock(topic='transactions', partition=0, offset=1)
        mock_future.get.return_value = mock_metadata
        mock_producer_instance.send.return_value = mock_future
        mock_producer_class.return_value = mock_producer_instance
        
        # Setup consumer
        mock_consumer_instance = Mock()
        mock_consumer_class.return_value = mock_consumer_instance
        
        # Send transaction
        producer = TransactionProducer()
        transaction = {
            'transaction_id': 'TXN20240001',
            'sender': '254712345678',
            'receiver': '254712345679',
            'amount': 1500.00,
            'status': 'success',
            'transaction_type': 'transfer'
        }
        
        send_result = producer.send_transaction(transaction=transaction)
        
        # Process on consumer side
        consumer = TransactionConsumer()
        process_result = consumer.process_message(transaction)
        
        assert send_result is True
        assert process_result is True
        assert consumer.stats['successful'] == 1
        assert consumer.stats['total_amount'] == 1500.00
    
    @patch('streaming.kafka_producer.KafkaProducer')
    @patch('streaming.kafka_consumer.KafkaConsumer')
    def test_throughput_validation(self, mock_consumer_class, mock_producer_class):
        """Test throughput with multiple messages"""
        mock_producer_instance = Mock()
        mock_future = Mock()
        mock_metadata = Mock(topic='transactions', partition=0, offset=1)
        mock_future.get.return_value = mock_metadata
        mock_producer_instance.send.return_value = mock_future
        mock_producer_class.return_value = mock_producer_instance
        
        mock_consumer_instance = Mock()
        mock_consumer_class.return_value = mock_consumer_instance
        
        producer = TransactionProducer()
        consumer = TransactionConsumer()
        
        # Send and process 100 transactions
        for i in range(100):
            transaction = {
                'transaction_id': f'TXN{i:05d}',
                'sender': '254712345678',
                'receiver': '254712345679',
                'amount': 1000.00,
                'status': 'success' if i % 10 else 'failed',
                'transaction_type': 'transfer'
            }
            producer.send_transaction(transaction=transaction)
            consumer.message_count += 1  # Increment counter
            consumer.process_message(transaction)
        
        stats = consumer.get_stats()
        
        assert stats['messages_processed'] == 100
        assert stats['stats']['total_messages'] == 100
        # 10 failed (when i % 10 == 0), 90 successful
        assert stats['stats']['successful'] == 90
        assert stats['stats']['failed'] == 10

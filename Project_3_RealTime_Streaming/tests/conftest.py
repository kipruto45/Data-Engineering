"""Pytest configuration for Project 3 tests"""

import pytest
import sys
import os
from unittest.mock import Mock, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def mock_kafka_producer():
    """Mock Kafka producer for testing"""
    producer = Mock()
    producer.send = MagicMock(return_value=Mock(get=Mock(return_value=Mock(
        topic='transactions',
        partition=0,
        offset=0
    ))))
    producer.flush = MagicMock()
    producer.close = MagicMock()
    return producer

@pytest.fixture
def mock_kafka_consumer():
    """Mock Kafka consumer for testing"""
    consumer = Mock()
    consumer.close = MagicMock()
    return consumer

@pytest.fixture
def sample_transaction():
    """Sample transaction data for testing"""
    return {
        'transaction_id': 'TXN20240001',
        'sender': '254712345678',
        'receiver': '254712345679',
        'amount': 1000.00,
        'timestamp': '2024-01-01T12:00:00',
        'transaction_type': 'transfer',
        'status': 'success',
        'provider': 'Safaricom',
        'fee': 10.00
    }

from django.core.management.base import BaseCommand
from voting.crypto import generate_rsa_keypair, private_key_path, public_key_path


class Command(BaseCommand):
    help = "Generate RSA keypair for vote encryption (stored in VOTE_KEYS_DIR)"

    def add_arguments(self, parser):
        parser.add_argument("--bits", type=int, default=2048, help="Key size in bits")
        parser.add_argument("--private-file", type=str, default=None, help="Private key filename (writes to VOTE_KEYS_DIR if provided)")
        parser.add_argument("--public-file", type=str, default=None, help="Public key filename (writes to VOTE_KEYS_DIR if provided)")

    def handle(self, *args, **options):
        bits = options.get("bits")
        priv_file = options.get("private_file")
        pub_file = options.get("public_file")
        priv, pub = generate_rsa_keypair(bits=bits, private_path=priv_file, public_path=pub_file)
        self.stdout.write(self.style.SUCCESS(f"Generated keys:\n private: {priv}\n public: {pub}"))

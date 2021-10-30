from os.path import exists, join
from cryptography.fernet import Fernet
from json import dumps
import random

ENCRYPTED = 'encrypted'
DECRYPTED = 'decrypted'
UNKOWN = 'unknown'


class Credentials:
    def __init__(self, args):
        self.username = args.username
        self.password = args.password
        self.text_state = self.get_text_state(args)

        self.set_and_validate_output_dir(args)

        if not self.has_error():
            self.get_or_create_key(args)

    def get_text_state(self, args):
        if args.encrypt:
            return DECRYPTED
        elif args.decrypt:
            return ENCRYPTED
        else:
            return UNKOWN

    def set_and_validate_output_dir(self, args):
        self.outputdir = args.output
        if not exists(self.outputdir):
            self.error = f'Invalid argument: output directory {self.outputdir} does not exist'

    def get_or_create_key(self, args):
        if self.text_state == ENCRYPTED:
            if args.keypath:
                if exists(args.keypath):
                    self.keypath = args.keypath
                    self.unique_identifier = self.keypath.split('.key')[-1]
                else:
                    self.error = f'Invalid argument: key file {args.keypath} does not exist'
            else:
                self.error = 'Missing argument: for decryption, please specify path to key file with "-k" or "--keypath"'
        elif self.text_state == DECRYPTED:
            self.create_new_key_file()
        else:
            self.error = 'Missing argument: please specify encryption (with "-e" or "--encrypt") or decryption (with "-d" or "--decrypt")'

    def has_error(self) -> bool:
        return hasattr(self, 'error')

    def create_new_key_file(self):
        # Create a filename that doesn't already exist in the output dir
        unique_identifier = random.randint(1, 99999)
        while (exists(join(self.outputdir, f'.key{unique_identifier}'))):
            unique_identifier = random.randint(1, 99999)

        # Store unique ID so we know which output goes with which key
        self.unique_identifier = unique_identifier
        self.keypath = join(self.outputdir, f'.key{unique_identifier}')

        # Generate and write new key to new key file in output dir
        with open(self.keypath, 'w') as key_file:
            key_file.write(Fernet.generate_key().decode())

    def load_key(self) -> str:
        with open(self.keypath, 'r') as key_file:
            return key_file.read()

    def encrypt(self):
        f = Fernet(self.load_key())
        self.username = f.encrypt(self.username.encode()).decode()
        self.password = f.encrypt(self.password.encode()).decode()

    def decrypt(self):
        f = Fernet(self.load_key())
        self.username = f.decrypt(self.username.encode()).decode()
        self.password = f.decrypt(self.password.encode()).decode()

    def write_to_file(self):
        output_filename = f'decrypted-{self.unique_identifier}.json' \
            if self.text_state == ENCRYPTED \
            else f'encrypted-{self.unique_identifier}.json'

        with open(join(self.outputdir, output_filename), 'w') as output_file:
            output_file.write(dumps({
                'username': self.username,
                'password': self.password
            }))

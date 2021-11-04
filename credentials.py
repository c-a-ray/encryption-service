from os.path import exists, join
from os import getcwd, path, urandom
from cryptography.fernet import Fernet
from json import dumps
from secrets import token_hex

ENCRYPT = 'encrypt'
DECRYPT = 'decrypt'


class Credentials:
    def __init__(self, args, path_to_keys):
        self.path_to_keys = path_to_keys
        self.action = self.determine_action(args)

        self.errors = list()

        if self.action == None:
            self.errors.append(
                'Missing argument: please specify an action (encrypt, decrypt, or clean-up)')

        if args.username:
            self.username = args.username
        else:
            self.errors.append(
                f'Missing argument: expected a username to {self.action}')

        if args.password:
            self.password = args.password
        else:
            self.errors.append(
                f'Missing argument: expected a password to {self.action}')

        self.set_and_validate_output_dir(args)

        if not self.has_error():
            self.get_or_create_key(args)

    def determine_action(self, args):
        if args.encrypt:
            return ENCRYPT
        elif args.decrypt:
            return DECRYPT
        else:
            return None

    def set_and_validate_output_dir(self, args):
        if args.output:
            self.outputdir = args.output
            if not exists(self.outputdir):
                self.errors.append(
                    f'Invalid argument: output directory {self.outputdir} does not exist')
        else:
            self.outputdir = getcwd()
            print(
                f'No output directory specified. Writing output to CWD ({self.outputdir})')

    def get_or_create_key(self, args):
        if self.action == ENCRYPT:
            self.create_new_key_file()
        elif self.action == DECRYPT:
            if args.uniqueid:
                self.uniqueid = args.uniqueid
                self.key_path = join(
                    self.path_to_keys, f'.{self.uniqueid}')
                if not exists(self.key_path):
                    self.errors.append(
                        f'Invalid argument:{self.uniqueid} is not valid unique ID')
            else:
                self.errors.append(
                    f'Missing argument: to decrypt, provide the unique ID that was provided after encryption')

    def has_error(self) -> bool:
        return len(self.errors) > 0

    def print_errors(self):
        for err in self.errors:
            print(err)

    def create_new_key_file(self):
        self.uniqueid = token_hex(16)
        self.key_path = join(self.path_to_keys, f'.{self.uniqueid}')
        while (exists(self.key_path)):
            self.uniqueid = token_hex(16)
            self.key_path = join(self.path_to_keys, f'.{self.uniqueid}')

        with open(self.key_path, 'w') as key_file:
            key_file.write(Fernet.generate_key().decode())

    def load_key(self) -> str:
        with open(self.key_path, 'r') as key_file:
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
        text_state = 'encrypted' if self.action == ENCRYPT else 'decrypted'
        output_filename = 'crypto-service-results.json'
        output_data = {
            'uid': self.uniqueid,
            'text_state': text_state,
            'username': self.username,
            'password': self.password,
        }

        with open(join(self.outputdir, output_filename), 'w') as output_file:
            output_file.write(dumps(output_data))

from os.path import exists, join
from os import getcwd, mkdir
from json import dumps
from secrets import token_hex
from shutil import rmtree
from constants import DECRYPT, ENCRYPT


class Config:
    def __init__(self, path_to_keys):
        self.errors = list()
        self.path_to_keys = path_to_keys

    def set_keys_dir(self):
        try:
            if not exists(self.path_to_keys):
                mkdir(self.path_to_keys)
        except OSError as e:
            self.errors.append(f'Error creating keys directory: {e.strerror}')

    def set_output_dir(self, args):
        if args.output:
            self.outputdir = args.output
            if not exists(self.outputdir):
                self.errors.append(
                    f'Invalid argument: output directory {self.outputdir} does not exist')
        else:
            self.outputdir = getcwd()
            print(
                f'No output directory specified. Writing output to {self.outputdir}')

    def create_new_uid(self):
        self.new_uid = token_hex(16)
        self.new_key_path = join(self.path_to_keys, f'.{self.new_uid}')
        while (exists(self.new_key_path)):
            self.new_uid = token_hex(16)
            self.new_key_path = join(self.path_to_keys, f'.{self.new_uid}')

    def create_new_key_file(self, credentials):
        with open(self.new_key_path, 'w') as key_file:
            key_file.write(credentials.get_new_key())

    def set_username_uid(self, username_uid):
        self.username_uid = username_uid

    def set_password_uid(self, password_uid):
        self.password_uid = password_uid

    def find_keys(self):
        if hasattr(self, 'username_uid'):
            self.username_key_path = join(
                self.path_to_keys, f'.{self.username_uid}')
            if not exists(self.username_key_path):
                self.errors.append(
                    f'Invalid argument: provided username UID {self.username_uid} is not a valid unique ID')

        if hasattr(self, 'password_uid'):
            self.password_key_path = join(
                self.path_to_keys, f'.{self.password_uid}')
            if not exists(self.password_key_path):
                self.errors.append(
                    f'Invalid argument: provided password UID {self.password_uid} is not a valid unique ID')

    def load_new_key(self) -> str:
        return self.load_key(self.new_key_path)

    def load_username_key(self) -> str:
        return self.load_key(self.username_key_path)

    def load_password_key(self) -> str:
        return self.load_key(self.password_key_path)

    def load_key(self, key_path: str) -> str:
        with open(key_path, 'r', encoding='utf-8') as key_file:
            return key_file.read()

    def write_output(self, credentials, output_filename: str):
        output_data: dict = self.create_output_data(credentials)
        with open(join(self.outputdir, output_filename), 'w') as output_file:
            try:
                output_file.write(dumps(output_data))
            except Exception as e:
                print(f'Failed to create output file: {e}')

    def create_output_data(self, credentials) -> dict:
        output_data: dict = {}
        if credentials.action == ENCRYPT:
            output_data = {'text_state': 'encrypted'}
            if hasattr(credentials, 'username'):
                output_data['username'] = credentials.username
                output_data['uuid'] = self.new_uid
            if hasattr(credentials, 'password'):
                output_data['password'] = credentials.password
                output_data['puid'] = self.new_uid
        elif credentials.action == DECRYPT:
            output_data = {'text_state': 'decrypted'}
            if hasattr(credentials, 'username'):
                output_data['username'] = credentials.username
                output_data['uuid'] = self.username_uid
            if hasattr(credentials, 'password'):
                output_data['password'] = credentials.password
                output_data['puid'] = self.password_uid
        return output_data

    def run_cleanup(self):
        action_verified = input(f"""
            WARNING: You specified '-c' or '--cleanup'.
            If you proceed, any encrypted text will no longer be able to be decrypted.
            Are you sure you want to delete all key files? 
            Enter 'YES" to continue or 'NO' to stop.

            """)
        if action_verified == 'YES':
            try:
                rmtree(self.path_to_keys)
            except OSError as e:
                print(
                    f'Error removing directory {self.path_to_keys}: {e.strerror}')
            else:
                print(f'Successfully removed directory {self.path_to_keys}')
        else:
            print('Canceling clean-up')

    def has_error(self):
        return len(self.errors) > 0

    def print_errors(self):
        for err in self.errors:
            print(err)

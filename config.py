from os.path import exists, join
from os import getcwd, mkdir
from json import dumps
from secrets import token_hex
from shutil import rmtree
from credentials import ENCRYPT


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
        self.uniqueid = token_hex(16)
        self.key_path = join(self.path_to_keys, f'.{self.uniqueid}')
        while (exists(self.key_path)):
            self.uniqueid = token_hex(16)
            self.key_path = join(self.path_to_keys, f'.{self.uniqueid}')

    def create_new_key_file(self, credentials):
        with open(self.key_path, 'w') as key_file:
            key_file.write(credentials.get_new_key())

    def find_key(self, args):
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

    def load_key(self):
        with open(self.key_path, 'r') as key_file:
            return key_file.read()

    def write_output(self, credentials, output_filename):
        text_state = 'encrypted' if credentials.action == ENCRYPT else 'decrypted'
        output_data = {
            'uid': self.uniqueid,
            'text_state': text_state,
            'username': credentials.username,
            'password': credentials.password,
        }

        with open(join(self.outputdir, output_filename), 'w') as output_file:
            try:
                output_file.write(dumps(output_data))
            except Exception as e:
                print(f'Failed to create output file: {e}')

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

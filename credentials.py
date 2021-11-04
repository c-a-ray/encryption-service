from cryptography.fernet import Fernet

ENCRYPT = 'encrypt'
DECRYPT = 'decrypt'


class Credentials:
    def __init__(self, args):
        self.errors = list()

        self.action = self.determine_action(args)
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

    def determine_action(self, args):
        if args.encrypt:
            return ENCRYPT
        elif args.decrypt:
            return DECRYPT
        else:
            return None

    def get_new_key(self):
        return Fernet.generate_key().decode()

    def encrypt(self, cfg):
        f = Fernet(cfg.load_key())
        self.username = f.encrypt(self.username.encode()).decode()
        self.password = f.encrypt(self.password.encode()).decode()

    def decrypt(self, cfg):
        f = Fernet(cfg.load_key())
        self.username = f.decrypt(self.username.encode()).decode()
        self.password = f.decrypt(self.password.encode()).decode()

    def has_error(self):
        return len(self.errors) > 0

    def print_errors(self):
        for err in self.errors:
            print(err)

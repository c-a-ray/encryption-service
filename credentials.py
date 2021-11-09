from cryptography.fernet import Fernet
from constants import ENCRYPT, DECRYPT
from config import Config


class Credentials:
    def __init__(self, args, cfg: Config):
        self.errors = list()

        self.action = self.determine_action(args)
        if self.action == None:
            self.errors.append(
                'Missing argument: please specify an action (encrypt, decrypt, or clean-up)')
            return

        if not args.username and not args.password:
            self.errors.append('No username or password was provided')
            return

        if args.username:
            self.username = args.username
            if self.action == DECRYPT:
                if args.usernameuid:
                    cfg.set_username_uid(args.usernameuid)
                else:
                    self.errors.append(
                        'To decrypt a username, specify the UID associated with that username')

        if args.password:
            self.password = args.password
            if self.action == DECRYPT:
                if args.passworduid:
                    cfg.set_password_uid(args.passworduid)
                else:
                    self.errors.append(
                        'To decrypt a password, specify the UID associated with that password')

    def determine_action(self, args):
        if args.encrypt:
            return ENCRYPT
        elif args.decrypt:
            return DECRYPT
        else:
            return None

    def get_new_key(self):
        return Fernet.generate_key().decode()

    def encrypt(self, cfg: Config):
        f = Fernet(cfg.load_new_key())
        if hasattr(self, 'username'):
            self.username = f.encrypt(self.username.encode()).decode()
        if hasattr(self, 'password'):
            self.password = f.encrypt(self.password.encode()).decode()

    def decrypt(self, cfg: Config):
        if hasattr(self, 'username'):
            f = Fernet(cfg.load_username_key())
            self.username = f.decrypt(self.username.encode()).decode()
        if hasattr(self, 'password'):
            f = Fernet(cfg.load_password_key())
            self.password = f.decrypt(self.password.encode()).decode()

    def has_error(self):
        return len(self.errors) > 0

    def print_errors(self):
        for err in self.errors:
            print(err)

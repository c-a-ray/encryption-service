from args import get_args

ENCRYPTED = 'encrypted'
DECRYPTED = 'decrypted'
UNKOWN = 'unknown'


class Credentials:
    def __init__(self, args):
        self.username = args.username
        self.password = args.password
        self.text_state = self.get_text_state(args)

    def encrypt(self):
        pass

    def decrypt(self):
        pass

    def get_text_state(self, args):
        if args.encrypt:
            return ENCRYPTED
        elif args.decrypt:
            return DECRYPTED
        else:
            return UNKOWN

    def write_to_file(self):
        pass


def main():
    creds = Credentials(get_args())
    if creds.text_state == DECRYPTED:
        creds.encrypt()
    elif creds.text_state == ENCRYPTED:
        creds.decrypt()

    creds.write_to_file()

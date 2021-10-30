from credentials import Credentials, ENCRYPTED, DECRYPTED
from args import get_args


def run_crypto_service():
    creds = Credentials(get_args())
    if creds.has_error():
        print(creds.error)
        return

    if creds.text_state == DECRYPTED:
        creds.encrypt()
    elif creds.text_state == ENCRYPTED:
        creds.decrypt()

    creds.write_to_file()


run_crypto_service()

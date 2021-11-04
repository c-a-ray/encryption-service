from credentials import DECRYPT, ENCRYPT, Credentials
from args import get_args
from os.path import join, exists, expanduser
from os import mkdir
from shutil import rmtree


def run_crypto_service():
    path_to_keys = join(expanduser('~'), '.crypto-service-keys')
    if not exists(path_to_keys):
        mkdir(path_to_keys)

    args = get_args()
    if args.cleanup:
        run_cleanup(path_to_keys)
        return

    creds = Credentials(args, path_to_keys)
    if creds.has_error():
        creds.print_errors()
        return

    if creds.action == ENCRYPT:
        creds.encrypt()
    elif creds.action == DECRYPT:
        creds.decrypt()

    creds.write_to_file()


def run_cleanup(path_to_keys):
    action_verified = input(f"""
        WARNING: You specified '-c' or '--cleanup'.
        If you proceed, any encrypted text will no longer be able to be decrypted.
        Are you sure you want to delete all key files? 
        Enter 'YES" to continue or 'NO' to stop.

        """)
    if action_verified == 'YES':
        try:
            rmtree(path_to_keys)
        except OSError as e:
            print(f'Error removing directory {path_to_keys}: {e.strerror}')
        else:
            print(f'Successfully removed directory {path_to_keys}')
    else:
        print("Exiting...")


run_crypto_service()

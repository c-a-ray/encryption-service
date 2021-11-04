from os.path import join, expanduser
from credentials import DECRYPT, ENCRYPT, Credentials
from config import Config
from args import get_args

KEYS_DIRECTORY = '.crypto-service-keys'
OUTPUT_FILENAME = 'crypto-service-results.json'


def run_crypto_service():
    path_to_keys = join(expanduser('~'), KEYS_DIRECTORY)
    args = get_args()

    cfg = Config(path_to_keys)
    if args.cleanup:
        cfg.run_cleanup()
        return

    cfg.set_keys_dir()
    cfg.set_output_dir(args)
    if cfg.has_error():
        cfg.print_errors()
        return

    credentials = Credentials(args)
    if credentials.has_error():
        credentials.print_errors()
        return

    if credentials.action == ENCRYPT:
        cfg.create_new_uid()
        cfg.create_new_key_file(credentials)
        credentials.encrypt(cfg)
    elif credentials.action == DECRYPT:
        cfg.find_key(args)
        if cfg.has_error():
            cfg.print_errors()
            return
        credentials.decrypt(cfg)

    cfg.write_output(credentials, OUTPUT_FILENAME)


run_crypto_service()

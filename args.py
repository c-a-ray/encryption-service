from argparse import ArgumentParser


def get_args():
    parser = ArgumentParser()

    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument('-e', '--encrypt', action='store_true',
                              help='Use to encrypt credentials')
    action_group.add_argument('-d', '--decrypt', action='store_true',
                              help='Use to decrypt credentials')
    action_group.add_argument('-c', '--cleanup', action='store_true',
                              help='Use to delete all key files in ~/.crypto-service-keys')

    parser.add_argument('-u', '--username', type=str,
                        help='Specify a username to encrypt or decrypt')
    parser.add_argument('-p', '--password', type=str,
                        help='Specify a password to encrypt or decrypt')

    parser.add_argument('-uid', '--uniqueid', type=str,
                        help='To decrypt, specify the unique ID returned after encrypting')

    parser.add_argument('-o', '--output', type=str,
                        help='Specify path to output directory')

    return parser.parse_args()

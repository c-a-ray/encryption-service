from argparse import ArgumentParser


def get_args():
    parser = ArgumentParser()

    m_group = parser.add_mutually_exclusive_group()
    m_group.add_argument('-e', '--encrypt', action='store_true',
                         help='Use to encrypt credentials')
    m_group.add_argument('-d', '--decrypt', action="store_true",
                         help='Use to decrypt credentials')

    parser.add_argument('-u', '--username', type=str, required=True,
                        help='Specify a username to encrypt or decrypt')
    parser.add_argument('-p', '--password', type=str, required=True,
                        help='Specify a password to encrypt or decrypt')

    parser.add_argument('-k', '--keypath', type=str,
                        help='Specify path to key file (for decryption only)')

    parser.add_argument('-o', '--output', type=str,
                        required=True, help='Specify path to output directory')

    return parser.parse_args()

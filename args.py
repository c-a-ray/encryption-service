from argparse import ArgumentParser


def get_args():
    parser = ArgumentParser()

    m_group = parser.add_mutually_exclusive_group()
    m_group.add_argument('-e', '--encrypt', action='store_true',
                         help='use to encrypt credentials')
    m_group.add_argument('-d', '--decrypt', action="store_true",
                         help='use to decrypt credentials')

    parser.add_argument('-u', '--username', type=str, required=True,
                        help='specify a username to encrypt or decrypt')
    parser.add_argument('-p', '--password', type=str, required=True,
                        help='specify a password to encrypt or decrypt')

    return parser.parse_args()

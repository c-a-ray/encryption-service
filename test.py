"""
test.py:
    Testing script for crypto-service.
    Runs three tests:
        - Encrypt and then decrypt a single username
        - Encrypt and then decrypt a single password
        - Encrypt and then decrypt a username/password pair
"""

from subprocess import run
from time import sleep
from os.path import join
from os import remove, getcwd
from json import load

RESULTS_FILENAME: str = 'crypto-service-results.json'
USERNAME: str = "fakeUsername"
PASSWORD: str = "fakePa$$word123"
OUTPUT_DIR_PATH: str = join(getcwd(), 'output')
SLEEP_LENGTH: float = 0.05


def encrypt_username() -> dict:
    print('Encrypting username')

    run(['python3', '-m', 'crypto-service',
        '-e', '-u', f'{USERNAME}', '-o', f'{OUTPUT_DIR_PATH}'], check=True)
    sleep(SLEEP_LENGTH)

    path_to_results: str = join(OUTPUT_DIR_PATH, RESULTS_FILENAME)
    with open(path_to_results, encoding='utf-8') as results_file:
        results = load(results_file)

    success: bool = True
    if results['text_state'] != 'encrypted' or results['username'] == USERNAME:
        print('Error: Text is not encrypted')
        success = False

    return {
        'success': success,
        'username': results['username'],
        'uuid': results['uuid']
    }


def decrypt_username(encrypted_username: str, uuid: str) -> bool:
    print('Decrypting username')

    run(['python3', '-m', 'crypto-service', '-d', '-u',
        f'{encrypted_username}', '-uuid', f'{uuid}', '-o', f'{OUTPUT_DIR_PATH}'], check=True)
    sleep(SLEEP_LENGTH)

    path_to_results: str = join(OUTPUT_DIR_PATH, RESULTS_FILENAME)
    with open(path_to_results, encoding='utf-8') as results_file:
        results = load(results_file)

    success: bool = True
    if results['text_state'] != 'decrypted':
        success = False
        print('Error: Text state is not decrypted')
    if results['username'] != USERNAME:
        success = False
        print('Error: Decrypted username does not match original')
    if results['uuid'] != uuid:
        success = False
        print('Error: Returned UUID does not match original')

    return success


def encrypt_password():
    print('Encrypting password')

    run(['python3', '-m', 'crypto-service',
        '-e', '-p', f'{PASSWORD}', '-o', f'{OUTPUT_DIR_PATH}'], check=True)
    sleep(SLEEP_LENGTH)

    path_to_results: str = join(OUTPUT_DIR_PATH, RESULTS_FILENAME)
    with open(path_to_results, encoding='utf-8') as results_file:
        results = load(results_file)

    success: bool = True
    if results['text_state'] != 'encrypted' or results['password'] == PASSWORD:
        print('Error: Text is not encrypted')
        success = False

    return {
        'success': success,
        'password': results['password'],
        'puid': results['puid']
    }


def decrypt_password(encrypted_password: str, puid: str) -> bool:
    print('Decrypting password')

    run(['python3', '-m', 'crypto-service', '-d', '-p',
        f'{encrypted_password}', '-puid', f'{puid}', '-o', f'{OUTPUT_DIR_PATH}'], check=True)
    sleep(SLEEP_LENGTH)

    path_to_results: str = join(OUTPUT_DIR_PATH, RESULTS_FILENAME)
    with open(path_to_results, encoding='utf-8') as results_file:
        results = load(results_file)

    success: bool = True
    if results['text_state'] != 'decrypted':
        success = False
        print('Error: Text state is not decrypted')
    if results['password'] != PASSWORD:
        success = False
        print('Error: Decrypted password does not match original')
    if results['puid'] != puid:
        success = False
        print('Error: Returned PUID does not match original')

    return success


def encrypt_credentials() -> dict:
    print('Encrypting username/password pair')

    run(['python3', '-m', 'crypto-service', '-e', '-u',
        f'{USERNAME}', '-p', f'{PASSWORD}', '-o', f'{OUTPUT_DIR_PATH}'], check=True)
    sleep(SLEEP_LENGTH)

    path_to_results: str = join(OUTPUT_DIR_PATH, RESULTS_FILENAME)
    with open(path_to_results, encoding='utf-8') as results_file:
        results = load(results_file)

    success: bool = True
    if results['text_state'] != 'encrypted' or results['username'] == USERNAME or results['password'] == PASSWORD:
        print('Error: Text is not encrypted')
        success = False

    return {
        'success': success,
        'username': results['username'],
        'uuid': results['uuid'],
        'password': results['password'],
        'puid': results['puid']
    }


def decrypt_credentials(encrypted_username: str, uuid: str, encrypted_password: str, puid: str) -> bool:
    print('Decrypting username/password pair')

    run(['python3', '-m', 'crypto-service', '-d', '-u', f'{encrypted_username}', '-uuid', f'{uuid}',
        '-p', f'{encrypted_password}', '-puid', f'{puid}', '-o', f'{OUTPUT_DIR_PATH}'], check=True)
    sleep(SLEEP_LENGTH)

    path_to_results: str = join(OUTPUT_DIR_PATH, RESULTS_FILENAME)
    with open(path_to_results, encoding='utf-8') as results_file:
        results = load(results_file)

    success: bool = True
    if results['text_state'] != 'decrypted':
        success = False
        print('Error: Text state is not decrypted')
    if results['username'] != USERNAME:
        success = False
        print('Error: Decrypted username does not match original')
    if results['uuid'] != puid:
        success = False
        print('Error: Returned UUID does not match original')
    if results['password'] != PASSWORD:
        success = False
        print('Error: Decrypted password does not match original')
    if results['puid'] != puid:
        success = False
        print('Error: Returned PUID does not match original')

    return success


def run_single_username_test() -> bool:
    print('Running test: Encrypt/Decrypt Single Username')
    results: dict = encrypt_username()
    if results['success'] is False:
        return False
    success = decrypt_username(results['username'], results['uuid'])
    return success


def run_single_password_test() -> bool:
    print('Running test: Encrypt/Decrypt Single Password')
    results: dict = encrypt_password()
    if results['success'] is False:
        return False
    success = decrypt_password(results['password'], results['puid'])
    return success


def run_credentials_test() -> bool:
    print('Running test: Encrypt/Decrypt Username/Password Pair')
    results: dict = encrypt_credentials()
    if results['success'] is False:
        return False
    success = decrypt_credentials(
        results['username'], results['uuid'], results['password'], results['puid'])
    return success


def run_tests():
    success = run_single_username_test()
    if not success:
        print("\nFAIL\n")
        return
    success = run_single_password_test()
    if not success:
        print("\nFAIL\n")
        return
    success = run_credentials_test()
    if not success:
        print("\nFAIL\n")
        return

    print('\nSUCCESS\n')


run_tests()
remove(join(OUTPUT_DIR_PATH, RESULTS_FILENAME))

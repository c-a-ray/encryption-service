import subprocess
from time import sleep
import os
import json

RESULTS_FILENAME = 'crypto-service-results.json'
USERNAME = "fakeUsername"
PASSWORD = "fakePa$$word123"
OUTPUT_DIR_PATH = os.path.join(os.getcwd(), 'output')
SLEEP_LENGTH = .05


def run_encryption_test():
    # Send the credentials to crypto-service and wait for it to finish
    print(
        f"Sending request to encrypt username '{USERNAME}' and password '{PASSWORD}'\n")
    subprocess.run(["python3", "-m", "crypto-service", "-e", "-u",
                   f"{USERNAME}", "-p", f"{PASSWORD}", "-o", f"{OUTPUT_DIR_PATH}"])
    sleep(SLEEP_LENGTH)

    # Read the results from the output file
    path_to_results = os.path.join(OUTPUT_DIR_PATH, RESULTS_FILENAME)
    with open(path_to_results) as results_file:
        results = json.load(results_file)

    # Store the encrypted username and password
    text_state = results["text_state"]
    uid = results["uid"]
    encrypted_username = results["username"]
    encrypted_password = results["password"]

    # Verify that the text_state is 'encrypted'
    success = False
    if text_state == "encrypted":
        success = True
        print("Successfully encrypted username and password")
        print(f"UID: {uid}")
        print(f"Encrypted username: {encrypted_username}")
        print(f"Encrypted password: {encrypted_password}\n")

    # Delete results file
    os.remove(path_to_results)

    # Return encrypted results so we can decrypt them
    return {
        'success': success,
        'uid': uid,
        'username': encrypted_username,
        'password': encrypted_password
    }


def run_decryption_test(encrypted_username, encrypted_password, uid):
    # Send encrypted credentials and path to key file to crypto-service and wait for it to finish
    subprocess.run(["python3", "-m", "crypto-service", "-d", "-uid", f"{uid}",  "-u",
                   f"{encrypted_username}", "-p", f"{encrypted_password}", "-o", f"{OUTPUT_DIR_PATH}"])
    sleep(SLEEP_LENGTH)

    # Read results file
    path_to_results = os.path.join(OUTPUT_DIR_PATH, RESULTS_FILENAME)
    with open(path_to_results) as results_file:
        results = json.load(results_file)

    # Store decrypted username and password
    text_state = results["text_state"]
    result_username = results["username"]
    result_password = results["password"]

    # Verify that the text_state is 'decrypted'
    success = False
    if text_state == "decrypted":
        success = True
        print("Successfully decrypted username and password")
        print(f"Decrypted username: {result_username}")
        print(f"Decrypted password: {result_password}\n")

    # Remove results file
    os.remove(path_to_results)

    # Just a check that the decrypted credentials match the original
    if result_username == USERNAME:
        print("Decrypted username matches original")
    else:
        print("Decrypted username does not match original")

    if result_password == PASSWORD:
        print("Decrypted password matches original")
    else:
        print("Decrypted password does not match original")

    return {'success': success}


encryption_results = run_encryption_test()
decryption_results = run_decryption_test(
    encryption_results['username'], encryption_results['password'], encryption_results['uid'])

if decryption_results['success'] == True:
    print("\nTEST SUCCESSFUL")
else:
    print("\nTEST FAILED")

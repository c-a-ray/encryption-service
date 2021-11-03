import subprocess
from time import sleep
import os
import json

#############
# Encrypt
#############

# Credentials to encrypt
username = "username"
password = "password"

# This directory must already exist (and I don't think the "./" works on Windows)
output_dir_path = "./output"

# Send the credentials to crypto-service and wait for it to finish
subprocess.run(["python3", "-m", "crypto-service", "-e", "-u",
               f"{username}", "-p", f"{password}", "-o", f"{output_dir_path}"])
sleep(1)

# Find the output file
results_filename = ""
for (dirpath, dirnames, filenames) in os.walk(output_dir_path):
    for file in filenames:
        if file[0:9] == "encrypted":
            results_filename = file

# Extract the uniqueID
uniqueID = os.path.basename(os.path.normpath(
    results_filename)).replace("encrypted-", "").replace(".json", "")

# Create path to keyfile
path_to_keyfile = os.path.join(output_dir_path, f".key{uniqueID}")

# Read the results from the output file
path_to_results = os.path.join(output_dir_path, results_filename)
with open(path_to_results) as results_file:
    results = json.load(results_file)

# Store the encrypted username and password
encrypted_username = results["username"]
encrypted_password = results["password"]

# Delete results file
os.remove(path_to_results)

#####################################################################################
# Store encrypted username, password, and path to key file (or just unique ID) in DB
#####################################################################################


#############
# Decrypt
#############

# Send encrypted credentials and path to key file to crypto-service and wait for it to finish
subprocess.run(["python3", "-m", "crypto-service", "-d", "-u",
               f"{encrypted_username}", "-p", f"{encrypted_password}", "-o", f"{output_dir_path}", "-k", f"{path_to_keyfile}"])
sleep(1)

# Construct decrypted results filename with unique ID (always in the form decrypted-uniqueID.json)
results_filename = f"decrypted-{uniqueID}.json"

# Read results file
path_to_results = os.path.join(output_dir_path, results_filename)
with open(path_to_results) as results_file:
    results = json.load(results_file)

# Store decrypted username and password
result_username = results["username"]
result_password = results["password"]

# Remove results file
os.remove(path_to_results)

# Just a check that the decrypted credentials match the original
if result_username == username:
    print("Decrypted username matches original")
else:
    print("Decrypted username does not match original")

if result_password == password:
    print("Decrypted password matches original")
else:
    print("Decrypted password does not match original")

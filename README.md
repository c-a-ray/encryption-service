### General Usage:

`crypto-service.py [-h] [-e | -d | -c] [-u USERNAME] [-p PASSWORD] [-uid UNIQUEID] [-o OUTPUT]`

- One of the following three flags must be specified:
  - Encrypt credentials with '-e' or '--encrypt'
  - Decrypt credentials with '-d' or '--decrypt'
  - Delete key files directory with '-c' or '--cleanup'
- A username must be specified after the '-u' (or '--username' flag)
- A password must be specified after the '-p' (or '--password' flag)
- An output directory (where the results will be written) can be specified after '-o' or '--output'
  - If no output directory is specified, the the the output file is written to the current working directory
- For both encryption and decryption, results are written to a file named 'crypto-service-results.json'
  - This file will have four fields:
    - 'uid': a unique identifier
    - 'username': the encrypted or decrypted username
    - 'password': the encrypted or decrypted password
    - 'text_state': if the username/password in the results are encrypted, this will be 'encrypted. If they are decrypted, it will be 'decrypted'
- Every time a set of credentials are encrypted, a hidden key file is generated and stored in a hidden directory called '.crypto-service-keys' in the user's home directory
  - Using the clean-up flag will delete this directory and all of the keys in it. Credentials encrypted with these keys will no longer be decryptable
- When encrypting, a new 32-digit hexadecimal 'uid' (unique identifier) is generated and included in the JSON output
- When decrypting, the 'uid' returned from encryption must be passed to crypto-service after a '-uid' or '--uniqueid' flag

### Encryption:

To encrypt a username/password pair, use the `-e` or `--encrypt` flag

##### Example usage:

`python3 -m crypto-service --encrypt --username '{username}' --password '{password}'`

or

`python3 -m crypto-service -e -u '{username}' -p '{password}'`

### Decryption:

To decrypt an encrypted username/password pair, use the `-d` or `--decrypt` flag

##### Example usage:

`python3 -m crypto-service --decrypt --uniqueid '{uid}' --username '{encrypted-username}' --password '{encrypted-password}'`

or

`python3 -m crypto-service -d -uid '{uid}' -u '{encrypted-username}' -p '{encrypted-password}'`

When decrypting, the unique ID returned with the encrypted credentials must also be provided.

### Clean-up

Because encryption keys are stored locally on whichever machine is running the program, a clean-up option has been included to delete the directory containing all of the key files.

##### Example usage:

`python3 -m crypto-service --cleanup`

or

`python3 -m crypto-service -c`

#### Example of encrypting and decrypting a username/password pair:

1. To encrypt, user runs:
   `python3 -m crypto-service -e -u 'myFakeUsername' -p 'myFakePa$$word'`
2. Since no output directory was specified, results are written to the current working directory, in a file called `crypto-service-results.json`
   - This file will contain the encrypted username, password, and a UID. All three of these must be stored.
3. To decrypt, user runs:
   `python3 -m crypto-service -d -uid '{uid}' -u '{encrypted username}' -p '{encrypted password}'`
4. The decrypted username/password pair is written to `crypto-service-results.json`

#### Additional notes

- The calling program will need to wait after calling crypto-service before opening the output file
  - Benchmark tests indicate that this program consistently completes in far less than .01 seconds
  - A 0.5 second sleep may be prudent. A test showed that the program successfully ran 1,000 times in less than 0.5 seconds.
- A testing script `test.py` is included in the repo. This script acts as a proof-of-concept for how a program would interact with crypto-service programmatically

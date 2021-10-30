### General Usage:

`python3 -m crypto-service [-h] [-e | -d] -u USERNAME -p PASSWORD [-k KEYPATH] -o OUTPUT`

    - Either '-e' (or '--encrypt') or '-d' (or '--decrypt') must be specified
    - A username must be specified after the '-u' (or '--username' flag)
    - A password must be specified after the '-p' (or '--password' flag)
    - For decryption, the path to the key file used to encrypt must be specified after a '-k' or '--keypath' flag
    - For both encryption and decryption, the path to the desired output directory must be specified after a '-o' or '--output' flag

### Encryption:

To encrypt a username/password pair, use the `-e` or `--encrypt` flag

Example usage:
`python3 -m crypto-service --encrypt --username 'username' --password 'password' --output './output/'`

or

`python3 -m crypto-service -e -u 'username' -p 'password' -o './output/'`

When encrypting, a new key file is generated in the specified output directory with the form `.key{uniqueID}` where `{uniqueID}` is a unique pseudo-random integer between 1 and 99999 (e.g. `output/.key12345`). An output JSON file with the encrypted credentials is also stored in the output directory with the form `encrypted-{uniqueID}.json`where`{uniqueID}` is the same integer as the generated key file. This allows the user to match the encrypted credentials to the appropriate key file, which will be needed to decrypt the ciphertext.

### Decryption:

To decrypt an encrypted username/password pair, use the `-d` or `--decrypt` flag

Example usage:
`python3 -m crypto-service --decrypt --username '{encrypted-username}' --password '{encrypted-password}' --output './output/' --keypath './output/.key{uniqueID}'`

or

`python3 -m crypto-service -d -u '{encrypted-username}' -p '{encrypted-password}' -o './output/' -k './output/.key{uniqueID}'`

When decrypting, the key file originally used to encrypt the text must be specified. You can determine which key file
this is by matching the uniqueID from the output JSON file with the uniqueID appended to the key file's name.

#### Example of encrypting and decrypting a username/password pair:

1. To encrypt, user runs:
   `python3 -m crypto-service -e -u 'username' -p 'password' -o './output/'`
2. A new key is generated and stored in `output/.key12345`
3. The encrypted username/password pair are written to `output/encrypted-12345.json`
4. To decrypt, user runs:
   `python3 -m crypto-service -d -u '{encrypted username from encrypted-12345.json}' -p '{encrypted password from encrypted-12345.json}' -o './output/' -k './output/.key12345'`

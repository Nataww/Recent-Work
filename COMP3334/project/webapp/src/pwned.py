import requests
import hashlib

def is_pwned(password):

    # Calculate the SHA-256 hash of the password
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

    # Take the first 5 characters of the hash (prefix)
    hash_prefix = sha1_hash[:5]

    # Make the API request to check if the password has been pwned
    api_url = f"https://api.pwnedpasswords.com/range/{hash_prefix}"
    response = requests.get(api_url)

    # Check if the response was successful
    if response.status_code == 200:
        # Split the response by lines
        hashes = response.text.splitlines()

        # Check if the full hash of the password is present in the response
        for hash in hashes:
            if hash.split(':')[0] == sha1_hash[5:]:
                return True
        else:
            return False
    else:
        return True
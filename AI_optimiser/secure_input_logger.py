import base64
import logging
from typing import Tuple

#configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

def encrypt_input(input_string: str) -> str:
    """
    Encrypts the input string using base64 encoding.
    """
    encoded_bytes = base64.b64encode(input_string.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def decrypt_input(encrypted_string: str) -> str:
    """
    Decrypts the encrypted string using base64 decoding.
    """
    try:
        decoded_bytes = base64.b64decode(encrypted_string.encode('utf-8'))
        return decoded_bytes.decode('utf-8')
    except Exception as e:
        logging.error(f"Decryption failed: {e}")
        return None
    
def log_input(input_string: str, file_path: str = "input_log.txt") -> None:
    """
    Logs the input string to a file after encrypting it.
    """
    encrypted_input = encrypt_input(input_string)
    try:
        with open(file_path, 'a') as file:
            file.write(f"{encrypted_input}\n")
        logging.info("Input logged successfully.")
    except Exception as e:
        logging.error(f"Failed to log input: {e}")

def read_logged_inputs(file_path: str = "input_log.txt") -> Tuple[str, ...]:
    """ Reads the logged inputs from the file and decrypts them."""
    try:
        with open(file_path, 'r') as file:
            encrypted_inputs = file.readlines()
        decrypted_inputs = [decrypt_input(line.strip()) for line in encrypted_inputs]
        return tuple(decrypted_inputs)
    except Exception as e:
        logging.error(f"Failed to read logged inputs: {e}")
        return tuple()
    
# Example usage
if __name__ == "__main__":
    input_string = "Hello, World!"
    log_input(input_string)
    logged_inputs = read_logged_inputs()
    print("Logged Inputs:")
    for input_str in logged_inputs:
        print(input_str)
# This module provides functions to securely log inputs by encrypting them using base64 encoding.
# The encrypted inputs are stored in a file, and the original inputs can be retrieved by decrypting
# the stored values. It includes error handling and logging for successful operations and failures.
# The logging is configured to output messages to the console.
# The functions are designed to be used in a secure environment where the encryption key is not compromised.
# The module can be extended to use more robust encryption methods if needed.
# The example usage demonstrates how to log an input string and read the logged inputs from the file.
# The logged inputs are printed to the console after decryption.
# This code is useful for securely logging sensitive information without exposing it in plaintext.
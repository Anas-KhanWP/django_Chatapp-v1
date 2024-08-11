from cryptography.fernet import Fernet

# Generate a key and store it securely
key = Fernet.generate_key()

# Print the key (store this securely, e.g., in an environment variable)
print(key.decode())

# Use the key for encryption/decryption
cipher_suite = Fernet(key)

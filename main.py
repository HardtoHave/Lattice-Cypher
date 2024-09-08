import numpy as np
from scipy.stats import norm

# Parameters for LWE
n = 256  # Dimension of the lattice
q = 32768  # Modulus for finite field (ensure it's large enough for ASCII values)
sigma = 0.1  # Standard deviation for Gaussian noise


# Generate Gaussian noise
def discrete_gaussian_noise(sigma, size):
    return np.rint(norm.rvs(scale=sigma, size=size)).astype(int)


# Key generation
def generate_keys(n, q, sigma):
    s = np.random.randint(0, q, size=n)  # Secret key
    A = np.random.randint(0, q, size=(n, n))  # Public matrix
    e = discrete_gaussian_noise(sigma, n)  # Gaussian noise
    b = (np.dot(A, s) + e) % q  # Public key vector
    return (A, b), s  # Public key: (A, b), Secret key: s


# Encrypt a single integer (ASCII of a character)
def encrypt_integer(m, public_key, q, sigma):
    A, b = public_key
    r = np.random.randint(0, 2, size=n)  # Random binary vector for encryption
    c1 = (np.dot(r, A)) % q  # First part of ciphertext
    c2 = (np.dot(r, b) + m) % q  # Second part of ciphertext
    return c1, c2


# Decrypt a single integer
def decrypt_integer(ciphertext, secret_key, q):
    c1, c2 = ciphertext
    s = secret_key
    result = (c2 - np.dot(c1, s)) % q

    # Adjust result to fit into the ASCII range (0-255)
    if result > q // 2:
        result -= q

    # Ensure result falls within the valid ASCII range
    result = max(0, min(result, 255))  # Clamp to ASCII range (0-255)
    return int(result)


# Encrypt a string message
def encrypt_message(message, public_key, q, sigma):
    encrypted_message = []
    for char in message:
        m = ord(char)  # Convert character to its ASCII value
        encrypted_char = encrypt_integer(m, public_key, q, sigma)
        encrypted_message.append(encrypted_char)
    return encrypted_message


# Decrypt a string message
def decrypt_message(encrypted_message, secret_key, q):
    decrypted_message = ""
    for ciphertext in encrypted_message:
        decrypted_char = decrypt_integer(ciphertext, secret_key, q)
        decrypted_message += chr(decrypted_char)  # Convert ASCII back to character
    return decrypted_message


# Example usage
# Step 1: Key generation
public_key, secret_key = generate_keys(n, q, sigma)

# Step 2: Encrypt a string message
message = "Hello, LWE!!@QWASZfdisongasgjkhujlfasundyigknrDLSVMjshjbfKD"
encrypted_message = encrypt_message(message, public_key, q, sigma)

# Step 3: Decrypt the message
decrypted_message = decrypt_message(encrypted_message, secret_key, q)

# Output the results
print(f"Original message: {message}")
print(f"Decrypted message: {decrypted_message}")

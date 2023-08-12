import numpy as np
import socket
import time

def apply_noise(bit, error_prob):
    if np.random.rand() < error_prob:
        return 1 - bit
    return bit

def apply_noise_to_hamming(hamming_code, error_prob):
    hamming_code_with_noise = [apply_noise(int(bit), error_prob) for bit in hamming_code]
    return hamming_code_with_noise

def emisor_bits_with_noise(data_bits, error_prob):
    n = len(data_bits)
    m = 1
    while 2 ** m < n + m + 1:
        m += 1

    if not np.all(np.logical_or(data_bits == 0, data_bits == 1)):
        raise ValueError("Los bits de datos deben ser 0 o 1")

    hamming_code = np.zeros(n + m, dtype=int)
    j = 0

    for i in range(n + m):
        if i & (i + 1) != 0:
            hamming_code[i] = data_bits[j]
            j += 1

    for i in range(m):
        xor_val = np.bitwise_xor.reduce(hamming_code[np.arange(1, n + m + 1) & (2 ** i) == 2 ** i])
        hamming_code[2 ** i - 1] = xor_val

    noise_index = np.random.randint(0, len(hamming_code))
    hamming_code_with_noise = np.array([apply_noise(bit, error_prob) if idx == noise_index else bit for idx, bit in enumerate(hamming_code)])

    return hamming_code_with_noise.tolist()

def run_single_test(input_word, error_prob):
    ascii_data = [ord(char) for char in input_word]
    binary_data = [format(code, '08b') for code in ascii_data]
    data_bits = np.array([int(bit) for code in binary_data for bit in code])

    hamming_code_str = emisor_bits_with_noise(data_bits, error_prob)
    received_hamming_code = apply_noise_to_hamming(hamming_code_str, error_prob)

    start_time = time.time()

    host = '127.0.0.1'
    port = 12345
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(''.join(map(str, received_hamming_code)).encode())

    end_time = time.time()
    processing_time = end_time - start_time

    return hamming_code_str, processing_time

def run_tests(num_tests, error_prob):
    test_results = []

    for _ in range(num_tests):
        input_word = chr(np.random.randint(32, 127))
        original_hamming, received_hamming = run_single_test(input_word, error_prob)
        error_detected = 1 if original_hamming != received_hamming else 0
        test_results.append({
            "Input Word": input_word,
            "Error Detected": error_detected
        })

    return test_results

try:
    num_tests = 100  # Número de pruebas a realizar
    error_prob = 0.01  # Probabilidad de error

    test_results = run_tests(num_tests, error_prob)

   

except ValueError as e:
    print("\nError:", str(e))

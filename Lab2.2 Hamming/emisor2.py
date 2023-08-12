import numpy as np
import socket

def apply_noise(bit, error_prob):
    if np.random.rand() < error_prob:
        return 1 - bit
    return bit

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

    # Decide un índice aleatorio para aplicar el ruido
    noise_index = np.random.randint(0, len(hamming_code))
    hamming_code_with_noise = np.array([apply_noise(bit, error_prob) if idx == noise_index else bit for idx, bit in enumerate(hamming_code)])

    return hamming_code_with_noise.tolist()

try:
    input_word = input("Ingrese una palabra o letra: ")
    error_prob = float(input("Ingrese la probabilidad de error (entre 0 y 1): "))

    if error_prob < 0 or error_prob > 1:
        raise ValueError("La probabilidad de error debe estar entre 0 y 1")

    ascii_data = [ord(char) for char in input_word]
    binary_data = [format(code, '08b') for code in ascii_data]
    data_bits = np.array([int(bit) for code in binary_data for bit in code])

    print("\nLetra o palabra convertida a ASCII:")
    print(ascii_data)

    print("\nASCII convertido a bits:")
    print(binary_data)

    hamming_code_str = emisor_bits_with_noise(data_bits, error_prob)

    print("\nSecuencia de código de Hamming original:")
    print(''.join(map(str, hamming_code_str)))

    hamming_code_with_noise = [apply_noise(int(bit), error_prob) for bit in hamming_code_str]

    print("\nSecuencia de código de Hamming a enviar con ruido:")
    print(''.join(map(str, hamming_code_with_noise)))

    host = '127.0.0.1'
    port = 12345
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(''.join(map(str, hamming_code_with_noise)).encode())

except ValueError as e:
    print("\nError:", str(e))
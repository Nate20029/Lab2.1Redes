import numpy as np
import socket

def emisor_bits(data_bits):
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

    return hamming_code.tolist()

try:
    input_word = input("Ingrese una palabra o letra: ")
    ascii_data = [ord(char) for char in input_word]
    binary_data = [format(code, '08b') for code in ascii_data]
    data_bits = np.array([int(bit) for code in binary_data for bit in code])

    print("\nLetra o palabra convertida a ASCII:")
    print(ascii_data)

    print("\nASCII convertido a bits:")
    print(binary_data)

    hamming_code = emisor_bits(data_bits)
    hamming_code_str = ''.join(map(str, hamming_code))

    print("\nSecuencia de código de Hamming a enviar:")
    print(hamming_code_str)

    host = '127.0.0.1'
    port = 12345
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(hamming_code_str.encode())

except ValueError as e:
    print("\nError:", str(e))

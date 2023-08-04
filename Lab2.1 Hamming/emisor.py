import numpy as np

def emisor_bits(data_bits):
    n = len(data_bits)
    m = 1
    while 2 ** m < n + m + 1:
        m += 1

    # Verificar que los bits de datos sean 0 o 1 usando NumPy
    if not np.all(np.logical_or(data_bits == 0, data_bits == 1)):
        raise ValueError("Los bits de datos deben ser 0 o 1")

    # Crear un array para los bits de código de Hamming con bits de paridad en 0
    hamming_code = np.zeros(n + m, dtype=int)
    j = 0

    # Colocar los bits de datos en las posiciones en el código de Hamming
    for i in range(n + m):
        if i & (i + 1) != 0:  # Verificar si i + 1 no es una potencia de 2 (bit de paridad)
            hamming_code[i] = data_bits[j]
            j += 1

    # Calcular los bits de paridad 
    for i in range(m):
        xor_val = np.bitwise_xor.reduce(hamming_code[np.arange(1, n + m + 1) & (2 ** i) == 2 ** i])
        hamming_code[2 ** i - 1] = xor_val

    return hamming_code.tolist()

try:
    # Obtener la secuencia de bits del usuario
    data_bits_str = input("Ingrese la trama de bits (ejemplo: 1010): ")
    data_bits = np.array([int(bit) for bit in data_bits_str])  # Convertir la lista a un array NumPy

    # Calcular y mostrar el código de Hamming
    hamming_code = emisor_bits(data_bits)
    print("Código de Hamming:", ''.join(map(str, hamming_code))) # Mostrar el código sin comas

except ValueError as e:
    print("Error:", str(e))

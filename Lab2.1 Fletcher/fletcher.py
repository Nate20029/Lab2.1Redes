def calculate_fletcher_checksum(data, block_size):
    # Padiar la data con ceros para que matchee con el tamaño del bloquesillo
    padded_data = data.ljust(block_size, '0')

    # Inicializar la suma y calcular el checksum
    sum1 = sum2 = 0
    for i in range(0, len(padded_data), block_size):
        block = padded_data[i:i+block_size]
        sum1 = (sum1 + int(block, 2)) % 255
        sum2 = (sum2 + sum1) % 255

    # checksum bits
    checksum_bits = bin(sum1)[2:].zfill(8) + bin(sum2)[2:].zfill(8)
    return data + checksum_bits

# Emisor
input_data = input("Ingresa la trama en binario (e.g., '110101'): ")
block_size = int(input("Ingresa el tamaño del bloque (8, 16 o 32): "))

result = calculate_fletcher_checksum(input_data, block_size)
print("Trama enviada:", result)

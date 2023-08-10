import socket
import random

# Capa de Ruido
def apply_noise(data, error_probability):
    noisy_data = ''
    for bit in data:
        if random.random() < error_probability:
            noisy_data += '0' if bit == '1' else '1'
        else:
            noisy_data += bit
    return noisy_data

# Algoritmo de Fletcher Checksum
def fletcher_checksum(data):
    sum1 = sum2 = 0
    for bit in data:
        sum1 = (sum1 + int(bit, 2)) % 255
        sum2 = (sum2 + sum1) % 255
    return sum1, sum2

# Capa de Transmisión
def send_data(data):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))  # Loopback IP
    client_socket.send(data.encode())
    client_socket.close()

# Capa de Aplicación
message = input("Ingrese el mensaje a enviar: ")
error_probability = float(input("Ingrese la probabilidad de error (0-1): "))

# Codificar el mensaje
encoded_message = ''.join(format(ord(char), '08b') for char in message)

# Verifica si la probabilidad de error es válida
if error_probability < 0 or error_probability > 1:
    print("La probabilidad de error debe estar entre 0 y 1.")
    exit()

# Limitar la cantidad máxima de errores introducidos
max_allowed_errors = int(len(encoded_message) * error_probability)
if max_allowed_errors >= len(encoded_message):
    print("La probabilidad de error es demasiado alta para corregir.")
    exit()

# Aplicar ruido a la trama
noisy_message = apply_noise(encoded_message, error_probability)

# Calcular el checksum de Fletcher
sum1, sum2 = fletcher_checksum(encoded_message)
checksum = format(sum1, '08b') + format(sum2, '08b')

# Agregar el checksum a la trama
final_message = noisy_message + checksum

# Enviar la trama al receptor
send_data(final_message)

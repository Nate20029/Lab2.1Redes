import socket
import random
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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

# Función para realizar una prueba
def run_single_test(message, error_probability):
    # Codificar el mensaje
    encoded_message = ''.join(format(ord(char), '08b') for char in message)

    # Verificar si la probabilidad de error es válida
    if error_probability < 0 or error_probability > 1:
        print("La probabilidad de error debe estar entre 0 y 1.")
        return None

    # Limitar la cantidad máxima de errores introducidos
    max_allowed_errors = int(len(encoded_message) * error_probability)
    if max_allowed_errors >= len(encoded_message):
        print("La probabilidad de error es demasiado alta para corregir.")
        return None

    # Aplicar ruido a la trama
    noisy_message = apply_noise(encoded_message, error_probability)

    # Calcular el checksum de Fletcher
    sum1, sum2 = fletcher_checksum(encoded_message)
    checksum = format(sum1, '08b') + format(sum2, '08b')

    # Agregar el checksum a la trama
    final_message = noisy_message + checksum

    # Enviar la trama al receptor
    send_data(final_message)
    
    return final_message

# Función para realizar pruebas múltiples
def run_tests(num_tests):
    test_results = []

    for _ in range(num_tests):
        message_size = random.randint(1, 100)  # Tamaño del mensaje aleatorio
        message = ''.join(random.choice(['0', '1']) for _ in range(message_size))
        error_probability = random.uniform(0, 0.01)  # Probabilidad de error aleatoria
        
        # Enviar mensaje al emisor y recibir respuesta del receptor
        start_time = time.time()
        received_message = run_single_test(message, error_probability)
        end_time = time.time()

        if received_message is not None:
            elapsed_time = end_time - start_time
            test_results.append({
                "Message Size": message_size,
                "Error Probability": error_probability,
                "Elapsed Time": elapsed_time,
                "Received Message": received_message
            })

    return test_results

# Ejecutar pruebas
num_tests = 100  # Número de pruebas a realizar
test_results = run_tests(num_tests)

# Convertir los resultados en un DataFrame de Pandas
df = pd.DataFrame(test_results)

# Guardar los resultados en un archivo CSV
df.to_csv("test_results.csv", index=False)

# Análisis estadístico y generación de gráficas
error_detection_rate = df["Received Message"].apply(lambda x: "Se detectaron errores" in x).mean()

# Recibir resultados del receptor
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 12345))  # Loopback IP
client_socket.send("Results".encode())

# Esperar la respuesta del receptor
response = client_socket.recv(1024).decode()

client_socket.close()

# Procesar los resultados del receptor
response_parts = response.split(":")[1].split(",")
received_error_detection_count = int(response_parts[0])
received_no_error_detection_count = int(response_parts[1])

# Gráfica 1: Tamaño de Mensaje vs. Tiempo de Procesamiento
plt.figure(figsize=(10, 6))
plt.scatter(df["Message Size"], df["Elapsed Time"], c=df["Error Probability"], cmap="coolwarm", alpha=0.7)
plt.xlabel("Tamaño del Mensaje")
plt.ylabel("Tiempo de Procesamiento")
plt.title("Tamaño de Mensaje vs. Tiempo de Procesamiento")
plt.colorbar(label="Probabilidad de Error")
plt.show()

# Generar gráfica de errores
labels = ['Detección de Errores', 'Sin Detección de Errores']
counts = [received_error_detection_count, received_no_error_detection_count]

plt.bar(labels, counts, color=['red', 'green'])
plt.xlabel('Resultados')
plt.ylabel('Cantidad de Pruebas')
plt.title('Resultados de Detección de Errores vs. Sin Detección de Errores')
plt.show()

error_detection_rate = received_error_detection_count / num_tests
print("Tasa de detección de errores:", error_detection_rate)
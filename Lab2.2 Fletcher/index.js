const net = require('net');

let totalTests = 0;
let errorDetectionCount = 0;
let noErrorDetectionCount = 0;
let waitingForResult = false; // Bandera para esperar resultados

// Algoritmo de Fletcher Checksum
function fletcherChecksum(data) {
  let sum1 = 0, sum2 = 0;
  for (let bit of data) {
    sum1 = (sum1 + parseInt(bit, 2)) % 255;
    sum2 = (sum2 + sum1) % 255;
  }
  return { sum1, sum2 };
}

// Decodificar mensaje de ASCII binario a caracteres
function decodeMessage(binaryData) {
  let decodedMessage = '';
  for (let i = 0; i < binaryData.length; i += 8) {
    const byte = binaryData.substr(i, 8);
    const charCode = parseInt(byte, 2);
    decodedMessage += String.fromCharCode(charCode);
  }
  return decodedMessage;
}

// Capa de Transmisión
const server = net.createServer((socket) => {
    let receivedData = '';
  
    socket.on('data', (data) => {
      receivedData += data.toString();
  
      if (receivedData === "Results") {
        // Enviar los resultados al emisor
        const responseMessage = `Results:${errorDetectionCount},${noErrorDetectionCount}`;
        socket.write(responseMessage);
        waitingForResult = true;
      }
  
      if (waitingForResult) {
        // Procesar la solicitud de resultados del emisor
        waitingForResult = false;
        return; // No procesar más datos después de enviar resultados
      }

    // Extraer el checksum de los últimos 16 bits
    const checksum = receivedData.slice(-16);
    const dataWithoutChecksum = receivedData.slice(0, -16);
    
    // Verificar el checksum
    const calculatedChecksum = fletcherChecksum(dataWithoutChecksum);
    const receivedChecksum = {
      sum1: parseInt(checksum.slice(0, 8), 2),
      sum2: parseInt(checksum.slice(8), 2)
    };

    totalTests++;

    if (calculatedChecksum.sum1 === receivedChecksum.sum1 &&
        calculatedChecksum.sum2 === receivedChecksum.sum2) {
      // Capa de Presentación
      const decodedMessage = decodeMessage(dataWithoutChecksum);
      // Capa de Aplicación
      console.log("Mensaje recibido sin errores:", decodedMessage);
      noErrorDetectionCount++;
    } else {
      // Mostrar el mensaje incorrecto y el mensaje original
      const incorrectMessage = dataWithoutChecksum.slice(0, -16);
      console.log("Mensaje incorrecto recibido:", decodeMessage(incorrectMessage));
      console.log("Mensaje original:", decodeMessage(dataWithoutChecksum));
      errorDetectionCount++;
    }

    console.log(`Total de pruebas: ${totalTests}`);
    console.log(`Pruebas con detección de errores: ${errorDetectionCount}`);
    console.log(`Pruebas sin detección de errores: ${noErrorDetectionCount}`);
  });

  // Esperar activamente la cadena "Results"
  socket.on('end', () => {
    if (receivedData === "Results") {
      // Enviar los resultados al emisor
      const responseMessage = `Results:${errorDetectionCount},${noErrorDetectionCount}`;
      socket.write(responseMessage);
      waitingForResult = false;
    }
  });
});

server.listen(12345, '127.0.0.1');  // Loopback IP

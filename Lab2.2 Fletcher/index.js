const net = require('net');

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
    // Extraer el checksum de los últimos 16 bits
    const checksum = receivedData.slice(-16);
    const dataWithoutChecksum = receivedData.slice(0, -16);
    
    // Verificar el checksum
    const calculatedChecksum = fletcherChecksum(dataWithoutChecksum);
    const receivedChecksum = {
      sum1: parseInt(checksum.slice(0, 8), 2),
      sum2: parseInt(checksum.slice(8), 2)
    };

    if (calculatedChecksum.sum1 === receivedChecksum.sum1 &&
        calculatedChecksum.sum2 === receivedChecksum.sum2) {
      // Capa de Presentación
      const decodedMessage = decodeMessage(dataWithoutChecksum);
      // Capa de Aplicación
      console.log("Mensaje recibido sin errores:", decodedMessage);
    } else {
      console.log("Se detectaron errores en el mensaje recibido.");
    }
  });
});

server.listen(12345, '127.0.0.1');  // Loopback IP

const readline = require('readline');

function calculate_fletcher_checksum(data, block_size) {
  // Padiar la data con ceros para que matchee con el tamaño del bloquesillo
  const padded_data = data.padEnd(block_size, '0');

  
  //Inicializar la suma y calcular el checksum
  let sum1 = 0;
  let sum2 = 0;
  for (let i = 0; i < padded_data.length; i += block_size) {
    const block = padded_data.slice(i, i + block_size);
    sum1 = (sum1 + parseInt(block, 2)) % 255;
    sum2 = (sum2 + sum1) % 255;
  }

  // Checksum bits
  const checksum_bits = (sum1.toString(2).padStart(8, '0') +
                         sum2.toString(2).padStart(8, '0'));

  return data + checksum_bits;
}

function validate_fletcher_checksum(data, block_size) {
  // Extraer los checksum bits
  const received_data = data.slice(0, -16);
  const received_checksum = data.slice(-16);

  // Calcular el checksum esperado
  const expected_checksum = calculate_fletcher_checksum(received_data, block_size).slice(-16);

  // Verficiacion si es el esperado
  if (received_checksum === expected_checksum) {
    return { valid: true, corrected_data: received_data };
  } else {
    return { valid: false };
  }
}

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Receptor
rl.question("Ingresa la cadena mostrada por el emisor: ", (input_data) => {
  rl.question("Ingresa el tamaño del bloque (8, 16 o 32): ", (block_size) => {
    const validation_result = validate_fletcher_checksum(input_data, parseInt(block_size, 10));
    if (validation_result.valid) {
      console.log("No se detectaron errores. Trama recibida:", validation_result.corrected_data);
    } else {
      console.log("Se detectaron errores. La trama se descarta por detectar errores.");
    }
    rl.close();
  });
});


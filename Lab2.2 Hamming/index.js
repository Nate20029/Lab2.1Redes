const net = require('net');

// Función para detectar y corregir errores en el código de Hamming
function detectAndCorrectErrors(hammingCode) {
    const m = Math.floor(Math.log2(hammingCode.length + 1));
    const errorBits = [];
    let parityBitSum = 0;

    for (let i = 0; i < m; i++) {
        const parityIndex = Math.pow(2, i) - 1;

        for (let j = parityIndex; j < hammingCode.length; j = j + (2 * parityIndex) + 2) {
            for (let k = 0; k <= parityIndex && j + k < hammingCode.length; k++) {
                parityBitSum ^= hammingCode[j + k];
            }
        }

        if (parityBitSum !== 0) {
            errorBits.push(parityIndex);
        }
        
        parityBitSum = 0;
    }

    if (errorBits.length > 0) {
        console.log(`Se encontraron errores en los bits: ${errorBits.join(', ')}`);
        for (const errorBit of errorBits) {
            hammingCode[errorBit] ^= 1;
        }
    } else {
        console.log('No se encontraron errores en el código de Hamming.');
    }

    return hammingCode;
}

// Función para decodificar el código de Hamming a binario
function decodeHammingToBinary(hammingCode) {
    const m = Math.floor(Math.log2(hammingCode.length + 1));
    const dataBits = [];

    for (let i = 0; i < hammingCode.length; i++) {
        if ((i & (i + 1)) !== 0) {
            dataBits.push(hammingCode[i]);
        }
    }

    return dataBits;
}

// Función para convertir binario a valores ASCII
function binaryToASCII(binaryArray) {
    const asciiValues = [];

    for (let i = 0; i < binaryArray.length; i += 8) {
        const byte = binaryArray.slice(i, i + 8).join('');
        const decimalValue = parseInt(byte, 2);
        asciiValues.push(decimalValue);
    }

    return asciiValues;
}

// Función para convertir valores ASCII a texto
function asciiToText(asciiValues) {
    let text = '';

    for (const asciiValue of asciiValues) {
        const char = String.fromCharCode(asciiValue);
        text += char;
    }

    return text;
}

// Crear un servidor TCP para recibir el código de Hamming con ruido
const server = net.createServer((socket) => {
    console.log('Cliente conectado');
    let hammingCodeWithNoise = '';

    socket.on('data', (data) => {
        hammingCodeWithNoise += data.toString();
    });

    socket.on('end', () => {
        console.log('\nSecuencia de código de Hamming con ruido recibida:');
        console.log(hammingCodeWithNoise);
    
        const receivedCode = hammingCodeWithNoise.split('').map(Number);
    
        // Detectar y corregir errores en el código de Hamming
        const correctedCode = detectAndCorrectErrors(receivedCode);
        console.log('\nSecuencia de código de Hamming corregida:');
        console.log((correctedCode.join('')));
    
        // Decodificar el código de Hamming a binario
        const decodedBinary = decodeHammingToBinary(correctedCode);
        console.log('\nCódigo de Hamming decodificado a binario:');
        console.log(decodedBinary.join(''));
    
        // Convertir binario a valores ASCII
        const asciiValues = binaryToASCII(decodedBinary);
        console.log('\nValores ASCII:');
        console.log(asciiValues.join(', '));
    
        // Convertir valores ASCII a texto
        const decodedText = asciiToText(asciiValues);
        console.log('\nTexto decodificado:');
        console.log(decodedText);
    });
});

const port = 12345;
server.listen(port, () => {
    console.log(`Servidor escuchando en el puerto ${port}`);
});
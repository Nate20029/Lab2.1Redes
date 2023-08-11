const net = require('net');

function decodeHamming(encodedBits) {
    const n = encodedBits.length;
    let m = 1;
    while (Math.pow(2, m) < n + m + 1) {
        m++;
    }

    const decodedBits = new Array(n - m);

    let j = 0;
    for (let i = 0; i < n; i++) {
        if ((i & (i + 1)) !== 0) {
            decodedBits[j] = encodedBits[i];
            j++;
        }
    }

    for (let i = 0; i < m; i++) {
        let xorVal = 0;
        for (let k = 0; k < n; k++) {
            if (((k + 1) & (1 << i)) === (1 << i)) {
                xorVal ^= encodedBits[k];
            }
        }
        if (xorVal !== 0) {
            console.log(`Error en el bit de paridad ${i + 1}`);
        }
    }

    return decodedBits;
}

const server = net.createServer(socket => {
    let receivedData = '';

    socket.on('data', data => {
        receivedData += data.toString();
    });

    socket.on('end', () => {
        const receivedBits = receivedData.split('').map(bit => parseInt(bit, 10));
        const decodedBits = decodeHamming(receivedBits);
        
        const asciiCodes = [];
        for (let i = 0; i < decodedBits.length; i += 8) {
            const byte = decodedBits.slice(i, i + 8);
            const asciiCode = parseInt(byte.join(''), 2);
            asciiCodes.push(asciiCode);
        }

        console.log('\nCodigo de Hamming Recibido:');
        console.log(receivedBits.join(''));

        console.log('\nCodigo de Hamming decodificado (ASCII a binario):');
        console.log(decodedBits.join(''));

        console.log('\nValor binario a decimal:');
        for (let i = 0; i < decodedBits.length; i += 8) {
            const byte = decodedBits.slice(i, i + 8);
            console.log(byte.join('') + ' -> ' + parseInt(byte.join(''), 2));
        }

        console.log('\nValor decimal a letra o palabra:');
        for (const asciiCode of asciiCodes) {
            console.log(asciiCode + ' -> ' + String.fromCharCode(asciiCode));
        }

        const receivedText = String.fromCharCode(...asciiCodes);
        console.log('\nTexto recibido:');
        console.log(receivedText);
    });
});

const port = 12345;
server.listen(port, () => {
    console.log(`Servidor escuchando en el puerto ${port}`);
});

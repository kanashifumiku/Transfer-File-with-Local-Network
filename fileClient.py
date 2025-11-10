# UTS PRAKTIKUM KOMUNIKASI DATA SEMESTER 1
# DOSEN PENGAMPU: RIAN RAHMANDA PUTRA, S.Kom.,M.Kom.
# OLEH: ABDUS SALIM TRI OCTA ISLAMI, ALIEF HIDAYATULLAH, MUHAMMAD ALPINO
import socket
import os

print('==================\nPROGRAM TRANSFER FILE TCP (CLIENT)\n==================')

# bagian handshake
print('IP Local: 127.0.0.1')
ip = input('Masukkan IP Server\n> ')
port = int(input('Masukkan PORT\n>'))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((ip, port))
    print('Terhubung dengan Server!')
except ConnectionRefusedError as e:
    print('Error: Server tidak tersedia! Pastikan server telah diaktifkan')
    exit()
#server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bagian metadata
metadata = client.recv(1024).decode()
if '|' not in metadata:
    print('Transaksi Dibatalkan Server')
    client.close()
    exit()

filename, size = metadata.split('|')
filenames = os.path.basename(filename)
size = int(size)
print(f'\nServer mengirim file\nNama: {filenames}\nUkuran: {size} bytes')
konfir = input('Terima berkas? y/n\n> ').strip().lower()
if konfir == 'y':
    client.sendall(b'ACK')
else:
    client.sendall(b'NACK')
    print('Transaksi dibatalkan!')
    client.close()
    exit()

dirFile = 'Masukan'
os.makedirs(dirFile, exist_ok=True)
berkasDiterima = os.path.join(dirFile, filenames)

# bagian terima berkas dari peladen
received = 0
with open(berkasDiterima, "wb") as f:
    while True:
        data = client.recv(1024)
        if not data:
            break
        f.write(data)
        received += len(data)
        progresDl = (received/size)*100
        print(f'\rProgres Download: {progresDl:.2f}%', end='')

print('\n-----\nBerkas Berhasil diterima.')
print(f'Berkas tersimpan di {berkasDiterima}')
client.close()

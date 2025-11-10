# UTS PRAKTIKUM KOMUNIKASI DATA SEMESTER 1
# DOSEN PENGAMPU: RIAN RAHMANDA PUTRA, S.Kom.,M.Kom.
# OLEH: ABDUS SALIM TRI OCTA ISLAMI, ALIEF HIDAYATULLAH, MUHAMMAD ALPINO
import socket
import os

print('==================\nPROGRAM TRANSFER FILE TCP (SERVER)\n==================')

# bagian handshake
print('IP Local: 127.0.0.1')
ip = input('Masukkan IP Server\n> ')
port = int(input('Masukkan PORT\n>'))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((ip, port))
server.listen(1)

print("Menunggu Koneksi ...")
conn, addr = server.accept()
print(f"Terhubung dengan {addr}\n")

# bagian input berkas
def masukan():
    while True:
        filename = input('Masukkan nama berkas yang akan anda kirim!(ketik exit untuk batal)\n> ')
        if filename.lower() == 'exit':
            conn.close()
            server.close()
            print('Transaksi dibatalkan')
            exit()
        if not os.path.exists(filename):
            print('Error: Nama berkas yang Anda masukkan tidak ada di direktori! Periksa ulang nama file Anda.\n------')

        else:
            return filename

# bagian metadata
def infoData(filename, size, conn):
    try:
        metadata = f"{filename}|{size}"
        conn.sendall(metadata.encode())
        print('Metadata telah terkirim! Menunggu konfirmasi dari Client')
        acc = conn.recv(1024).decode()
        if acc == 'ACK':
            print(f'Dikonfirmasi')
            mulaiProses(filename, conn, size)
        else:
            print('Transaki Dibatalkan Client')
            conn.close
            return
    except FileNotFoundError:
        print(f'Error: Berkas yang Anda masukkan tidak ada di direktori! Periksa ulang masukkan Anda.')
        exit()

# bagian kirim berkas ke klien
def mulaiProses(filename, conn, size):
    try:
        sent = 0
        with open(filename, "rb") as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                conn.sendall(data)
                sent += len(data)
                progresTf = (sent/size)*100
                print(f'\rProgres Transfer: {progresTf:.2f}%', end='')
        print("\nBerkas berhasil dikirim!")
    except FileNotFoundError as e:
        print(f'Error: Berkas yang Anda masukkan tidak ada di direktori! Periksa ulang masukkan Anda.')

# main (gak tau mau ditulis apa)
filename = masukan()
size = os.path.getsize(filename)
infoData(filename, size, conn)

conn.close()
server.close()

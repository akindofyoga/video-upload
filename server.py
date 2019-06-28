import json
import os
import socket
import struct


MAGIC_NUMBER = bytes([66])
HOST = ''
PORT = 8089
FILENAME = 'filename'


class SocketContainer:
    def __init__(self, conn):
        self.conn = conn

    def recv_n_bytes(self, n):
        """ Convenience method for receiving exactly n bytes from
        socket (assuming it's open and connected).
        """

        # based on https://docs.python.org/3.4/howto/sockets.html
        chunks = []
        bytes_recd = 0
        while bytes_recd < n:
            chunk = self.conn.recv(n - bytes_recd)
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd += len(chunk)
        return b''.join(chunks)

    def consume_magic_number(self):
        response = self.recv_n_bytes(1)
        return response == MAGIC_NUMBER


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(10)
    conn, _ = s.accept()
    print('Device connected')

    socket_container = SocketContainer(conn)
    while True:
        found_magic = socket_container.consume_magic_number()
        if not found_magic:
            raise Exception('Client did not send magic number')

        header_size = struct.unpack("!I", socket_container.recv_n_bytes(4))[0]
        header_raw = socket_container.recv_n_bytes(header_size)
        header = json.loads(header_raw.decode('ascii'))

        video_size = struct.unpack("!I", socket_container.recv_n_bytes(4))[0]

        filename = os.path.basename(header[FILENAME])

        with open(filename, 'wb') as video_file:
            video_file.write(socket_container.recv_n_bytes(video_size))


if __name__ == '__main__':
    main()

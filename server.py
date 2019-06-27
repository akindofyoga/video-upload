import socket


HOST=''
PORT=8089


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(10)

    conn, addr=s.accept()
    data_size = struct.unpack("!I", recv_n_bytes(conn, 4))[0]

    with open('video.mp4', 'wb') as video_file:
        # based on https://docs.python.org/3/howto/sockets.html#using-a-socket
        bytes_recd = 0
        while bytes_recd < data_size:
            chunk = conn.recv(data_size - bytes_recd)
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            video_file.write(chunk)
            bytes_recd += len(chunk)



if __name__ == '__main__':
    main()

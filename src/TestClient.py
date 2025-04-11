import socket, json

if __name__ == "__main__":
    HOST, PORT = "localhost", 8968

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        msg = input("String to send to the server: \n")
        message = {
            "words": msg
        }
        messagePacked = json.dumps(message).encode('utf-8')
        sock.sendall(bytes(messagePacked))
        print("Sent message \"{}\"".format(message))
        response = json.loads(sock.recv(1024).decode('utf-8'))
        print("Received message \"{}\"".format(response))

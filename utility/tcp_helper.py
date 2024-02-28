import socket
import json

tcp_host = 'localhost'
tcp_port = int(8080)


def tcp_client(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((tcp_host, tcp_port))

            message_str = f'{message}\n'
            client_socket.send(message_str.encode('utf-8'))

            data = client_socket.recv(1024)
            data_to_json = json.loads(data.decode('utf-8'))

            print(data_to_json)
            return data_to_json
        except Exception as err:
            print(f"Error: {err}")
            return None

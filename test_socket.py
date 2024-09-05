import socket
import json
import os


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('3.18.29.6', 12345)
client_socket.connect(server_address)


def get_clients(client_socket):
    command = {
        'cmd': 'ls_clients'
    }
    
    client_socket.sendall(json.dumps(command).encode())
    response = client_socket.recv(1024)
    response = json.loads(response.decode())
    
    return response['result']


print(get_clients(client_socket))


def send_command(client_socket, command):

# Send a message to the server
    try:
        # lấy các clients đang kết nối
        """ command = {
            'cmd': 'ls_clients'
        }
        
        client_socket.sendall(json.dumps(command).encode())
        response = client_socket.recv(1024)
        
        print(response.decode()) """
        
        
        
        command = {
            'cmd': 'python',
            'clients': ['118.70.190.129'],
            'code': 'import webbrowser; webbrowser.open("https://www.google.com")'
        }
        
        client_socket.sendall(json.dumps(command).encode())
        
        
        client_socket.shutdown(socket.SHUT_WR)
        
    finally:
        client_socket.close()
    
    
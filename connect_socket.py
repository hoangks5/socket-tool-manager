import socket
import json
import time


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12345)
client_socket.connect(server_address)

def get_clients(client_socket):
    # Send command to the server
    command = {
        'cmd': 'ls_clients'
    }
    client_socket.sendall(json.dumps(command).encode())
    # Receive response from server
    response = client_socket.recv(1024)
    response = json.loads(response.decode())
    return response['result']


def send_command(client_socket, command):

# Send a message to the server
    try:

        """ command = {
            'cmd': 'python',
            'clients': ['118.70.190.129'],
            'code': 'import webbrowser; webbrowser.open("https://www.google.com")'
        }
        
        client_socket.sendall(json.dumps(command).encode()) """
        
        
        client_socket.shutdown(socket.SHUT_WR)
        
    finally:
        client_socket.close()
    
    

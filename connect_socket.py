import socket
import json
import time

def check_server(ip, port):
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the server
    server_address = (ip, port)
    try:
        client_socket.connect(server_address)
        return True
    except Exception as e:
        return False
    finally:
        client_socket.close()
    

def get_clients():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('3.18.29.6', 12345)
    client_socket.connect(server_address)
    # Send command to the server
    command = {
        'cmd': 'ls_clients'
    }
    print('Sending command to server:', command)
    client_socket.sendall(json.dumps(command).encode())
    # Receive response from server
    response = client_socket.recv(1024)
    response = json.loads(response.decode())
    print('Received response from server:', response)
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
    
    

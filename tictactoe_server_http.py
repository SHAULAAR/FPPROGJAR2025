import socket
import threading
from http import HttpServer

httpserver = HttpServer()

def handle_client(conn, addr):
    print(f"Connection from {addr}")
    try:
        data = conn.recv(4096).decode(errors='ignore')
        print("Received request:", data)
        if data:
            response = httpserver.proses(data)
            conn.sendall(response)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', 8889))
    server_socket.listen(5)
    print("[Server] Tic-Tac-Toe HTTP server ready on port 8889")
    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__=="__main__":
    run_server()

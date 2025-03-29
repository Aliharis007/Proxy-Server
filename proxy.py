import socket
import sys
import multiprocessing
import re
import signal
import ssl
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MAX_CLIENTS = 100
activeProcesses = []

def handleClient(clientSocket):
    try:
        request = clientSocket.recv(4096).decode(errors='ignore')
        
        if not request:
            clientSocket.close()
            return

        firstLine = request.split("\n")[0]
        method, url, _ = firstLine.split(" ")

        if method != "GET":
            clientSocket.send(b"HTTP/1.0 501 Not Implemented\r\n\r\n")
            clientSocket.close()
            return

        match = re.match(r"http[s]?://([^:/]+)(?::(\d+))?(/.*)?", url)
        if not match:
            clientSocket.send(b"HTTP/1.0 400 Bad Request\r\n\r\n")
            clientSocket.close()
            return

        host, port, path = match.groups()
        port = int(port) if port else (443 if url.startswith("https") else 80)
        path = path if path else "/"

        logging.info(f"[+] Forwarding request to {host}:{port}{path}")

        try:
            remoteSocket = socket.create_connection((host, port))
            if url.startswith("https"):
                context = ssl.create_default_context()
                remoteSocket = context.wrap_socket(remoteSocket, server_hostname=host)
        except socket.error:
            clientSocket.send(b"HTTP/1.0 502 Bad Gateway\r\n\r\n")
            clientSocket.close()
            return

        requestHeader = f"GET {path} HTTP/1.0\r\nHost: {host}\r\nConnection: close\r\nUser-Agent: Python-Proxy/1.0\r\n\r\n"
        remoteSocket.send(requestHeader.encode())

        while (data := remoteSocket.recv(4096)):
            clientSocket.send(data)

        remoteSocket.close()
        clientSocket.close()
    except Exception as e:
        logging.error(f"Error: {e}")
        clientSocket.close()

def startProxy(port):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(("0.0.0.0", port))
    serverSocket.listen(MAX_CLIENTS)
    logging.info(f"[*] Proxy Server listening on port {port}...")

    while True:
        if len(activeProcesses) >= MAX_CLIENTS:
            logging.warning("[!] Max clients reached. Waiting...")
            continue

        clientSocket, addr = serverSocket.accept()
        logging.info(f"[*] New Connection from {addr}")

        process = multiprocessing.Process(target=handleClient, args=(clientSocket,))
        process.daemon = True
        process.start()
        activeProcesses.append(process)
        activeProcesses[:] = [p for p in activeProcesses if p.is_alive()]

def shutdownProxy(signalReceived, frame):
    logging.info("[!] Shutting down proxy...")
    for p in activeProcesses:
        p.terminate()
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python proxy.py <port>")
        sys.exit(1)
    
    port = int(sys.argv[1])
    signal.signal(signal.SIGINT, shutdownProxy)
    startProxy(port)

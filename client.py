from time import sleep
import socket

class Client:

    def __init__(self, ip, port, protocol):
    # __init__ method
    #   Args: 
    #   - IP address
    #   - Port
    #   - Protocol (TCP/UDP)
        self.client = None           # Client TCP
        self._protocol = protocol
        self.start(ip, port)
       
    def start(self, ip, port):
    # Method to start the socket communication with the Ground Station
        try:
            if self._protocol == "TCP":
                # Creiamo il client:
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # Connessione al server:
                addr = (ip, port)
                self.client.connect(addr)
                print(f"\nConnected to TCP server: {addr}...")
            elif self._protocol == "UDP":
                # Creiamo il client:
                self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error as error:
            print(f"\n{error}")
            print("Trying to start again...")
            sleep(5)
            self.start(ip, port)

    def end(self):
    # Metodo per chiudere la connessione:
        try:
            print("Closing connection with " + self._protocol + " server...\n")
            self.client.close()
        except socket.error as error:
            print(f"\n{error}")
        else:
            if self._protocol == "TCP":
                print("Uplink ended")
            elif self._protocol == "UDP":
                print("Downlink ended\n")

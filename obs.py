from telemetry import TlmSender, ArduinoSerial
from telecommands import TlcReceiver
from client import Client

class OnBoardSoftware:

    def __init__(self, ip, portTCP, portUDP, inoPort, baudRate):
    # __init__ method
    #   Args: 
    #   - IP address
    #   - Port for TCP communication
    #   - Port for UDP communication
    #   - Port for serial communication
    #   - Baud rate for arduino
        self._ip = ip                # Indirizzo IP del server
        self._portTCP = portTCP      # Porta per la connessione TCP
        self._portUDP = portUDP      # Porta per la connessione TCP
        self._inoPort = inoPort      # Porta seriale di Arduino
        self._baudRate = baudRate    # Rate per la comunicazione seriale (Arduino Uno!)
    
    def start(self):
    # Method to start the socket communication with the Ground Station
        # Creiamo il client UDP:
        downlink = Client(self._ip, self._portUDP, "UDP")
        # Creiamo il client TCP:
        uplink = Client(self._ip, self._portTCP, "TCP")
        # Connessione seriale con arduino:
        ino = ArduinoSerial(self._inoPort, self._baudRate)
        # Creiamo i vari threads:
        if uplink.client is not None and downlink.client is not None and ino.ser is not None:
            # Creiamo un thread per mandare la telemetria:
            sender = TlmSender(client = downlink.client, addr = (self._ip, self._portUDP), ser = ino.ser)
            # Creiamo un thread per ricevere telecomandi:
            receiver = TlcReceiver(client = uplink.client, threadToStop = sender)
            # Facciamo partire i threads:
            sender.start()
            receiver.start()
            sender.join()
            receiver.join()
            # Chiudiamo il downlink:
            downlink.end()
            # Chiudiamo l'uplink:
            uplink.end()

from telemetry import TlmReceiver
from telecommands import TlcSender
from server import Server

class GroundStation:

    def __init__(self, ip, portTCP, portUDP):
    # __init__ method
    #   Args: 
    #   - IP address
    #   - Port
        self._ip = ip                # Indirizzo IP del server
        self._portTCP = portTCP      # Porta per la connessione TCP
        self._portUDP = portUDP      # Porta per la connessione TCP

    def start(self):
    # Method to start the socket communication with the On Board Computer
        # Creo il server UDP:
        downlink = Server(self._ip, self._portUDP, "UDP")
        # Creo il server TCP:
        uplink = Server(self._ip, self._portTCP, "TCP")
        # Creiamo un thread per ricevere telemetria:
        receiver = TlmReceiver(server = downlink.server)
        # Creiamo un thread per mandare telecomandi:
        sender = TlcSender(client = uplink.client, threadToStop = receiver)
        # Iniziamo i threads:
        receiver.start()
        sender.start()
        # Chiudiamo i threads:
        receiver.join()
        sender.join()
        # Chiudiamo il downlink:
        downlink.end()
        # Chiudiamo l'uplink:
        uplink.end()

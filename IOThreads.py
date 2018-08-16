import threading
import Constants
import Helpers

class OutputThread(threading.Thread):
    def __init__(self, clientSocket, persistConnection = False):
        super(OutputThread, self).__init__()
        self.clientSocket = clientSocket
        self.persistConnection = persistConnection

    def run(self):
        if self.persistConnection:
            httpResponse = """HTTP/1.1 200 OK\nServer: TK Servers\nContent-Type: text/html\nContent-Length: 15\nAccept-Ranges: bytes\n\nsdfkjsdnbfkjbsf"""
        else:
            httpResponse = """HTTP/1.1 200 OK\nServer: TK Servers\nContent-Type: text/html\nConnection: close\nContent-Length: 15\nAccept-Ranges: bytes\n\nsdfkjsdnbfkjbsf"""
        bytesToSend = bytes(httpResponse, "utf-8")
        # Sends to the clientSocket file descriptor in C, ignore the messed up structure
        self.clientSocket.send(bytesToSend)


class InputThread(threading.Thread):
    def __init__(self, clientSocket, mainThread):
        super(InputThread, self).__init__()
        self.clientSocket = clientSocket
        self.mainThread = mainThread

    def run(self):
        # This thread will continue running if the request includes connection keep-alive header
        persistThread = True
        while persistThread:
            req = self.clientSocket.recv(1024)
            reqDict = Helpers.parseHttpRequest( req.decode("utf-8") )

            # Parse the http request and check if connection is keep alive, if it is keep the thread running to listen for input, else end while loop
            # If can't find 'Connection', check 'connection'
            if reqDict.get("Connection", reqDict.get("connection", None)) == "keep-alive":
                persistThread = True
            else:
                persistThread = False

            # Add the input to the event queue to be picked up by the InputEventListener
            self.mainThread.inputEventQueue.append(
                {'type': Constants.INPUT_RECEIVED, 'req': reqDict,'clientSocket': self.clientSocket, "persistConnection": persistThread})


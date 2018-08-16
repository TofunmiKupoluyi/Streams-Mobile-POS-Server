import threading
import time
import socket

# Personal modules
import Constants
import EventHandlers

# This is the thread that contains the main execution of the program, maintains event queues


class MainThread(threading.Thread):
    def __init__(self):
        super(MainThread, self).__init__()
        self.connectionEventQueue = []
        self.inputEventQueue = []

    # This is the main execution of the program -- creates and binds the socket and maintains the connection loop
    def run(self):
        # Creates the socket
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind(('', 3003))
        serverSocket.listen(5)

        # Connection loop -- the main thread essentially waits for client connection
        while 1:
            clientSocket, address = serverSocket.accept()
            self.connectionEventQueue.append(
                {"type": Constants.CONNECTION_RECEIVED, "clientSocket": clientSocket})


# This is a thread that runs continuously and checks if there are any events that need to be handled
class ConnectionEventListener(threading.Thread):
    def __init__(self, mainThread):
        super(ConnectionEventListener, self).__init__()
        self.mainThread = mainThread

    def run(self):
        # Runs for as long as program is up
        while 1:
            for i in mainThread.connectionEventQueue:
                # Get the first item in the queue
                eventReceived = mainThread.connectionEventQueue.pop(0)
                # Calling the connection event handler
                EventHandlers.connectionEventHandler(eventReceived, mainThread)


class InputEventListener(threading.Thread):
    def __init__(self, mainThread):
        super(InputEventListener, self).__init__()
        self.mainThread = mainThread

    def run(self):
        while 1:
            for i in mainThread.inputEventQueue:
                # Get the first item in the queue
                eventReceived = mainThread.inputEventQueue.pop(0)
                # Calling the input event handler, event received contains the client socket
                EventHandlers.inputEventHandler(eventReceived, mainThread)



# Instantiating the threads
mainThread = MainThread()
connectionEventListener = ConnectionEventListener(mainThread)
inputEventListener = InputEventListener(mainThread)

# Scheduler moves between the threads, starting both threads
mainThread.start()
connectionEventListener.start()
inputEventListener.start()

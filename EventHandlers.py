import IOThreads

def connectionEventHandler(eventReceived, mainThread):
    clientSocket = eventReceived["clientSocket"]
    IOThreads.InputThread( clientSocket, mainThread ).start()

def inputEventHandler(eventReceived, mainThread):
    clientSocket = eventReceived["clientSocket"]
    IOThreads.OutputThread( clientSocket, eventReceived["persistConnection"] ).start()

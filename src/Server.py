# Written by Nolan Casey, 2025

import socketserver, threading, json
from WordPrediction import WordPrediction
from Autocorrect import Autocorrect

predictor: WordPrediction = None
autocorrect: Autocorrect = None

class ThreadedTCPHandler(socketserver.BaseRequestHandler):
    def handle(self: socketserver.BaseRequestHandler):
        print("Client connected")
        data: dict[str, str] = json.loads(self.request.recv(4294967296).decode('utf-8'))
        predictions = []
        mode = ""
        if data["words"][-1] in " .,:;!?-\n":
            mode = "prediction"
            predictions = predictor.predict(data["words"], 3)
        else:
            mode = "correction"
            words = data["words"].rsplit(" ", 1)
            predictions = autocorrect.correct(words[-1])
        response: dict = {
            "mode": mode,
            "word1": predictions[0],
            "word2": predictions[1],
            "word3": predictions[2]
        }
        responsePacked = json.dumps(response).encode('utf-8')
        self.request.sendall(responsePacked)
        print("<Server> Message replied")

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "", 8968
    predictor = WordPrediction()
    predictor.load()
    autocorrect = Autocorrect()
    with ThreadedTCPServer((HOST, PORT), ThreadedTCPHandler) as server:
        serverThread = threading.Thread(target=server.serve_forever)
        serverThread.daemon = True
        serverThread.start()
        server.serve_forever()

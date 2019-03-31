import time
import requests
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST_NAME = '0.0.0.0'
PORT_NUMBER = 8000

def generator():
        trains = []
        sortedTrains = []
        #text = '["Trains"'
        r = requests.get('https://api.tfl.gov.uk/StopPoint/940GZZLUWPL/Arrivals')
        #print(len(r.json()))
        for i in range(len(r.json())):
            train = r.json()[i]
            #print(train)
            try:
                if(train["direction"] == "inbound"):
                    dict = {
                        "destination": train["destinationName"],
                        "timeToStation": train["timeToStation"]}
                    #print(dict)
                    trains.append(dict)

            except KeyError:
                pass

        sortedTrains = sorted(trains[:3], key=lambda k: k['timeToStation'])
        #sortedTrains.insert(0, text)
        #print(sortedTrains)
        #b = bytearray()
        #b.extend(map(ord, json.dumps(sortedTrains)))
        #print(json.dumps(sortedTrains).encode())
        return(sortedTrains)

class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps(generator()).encode())
        return

    def handle_http(self, status_code):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        return

    def respond(self):
        response = self.generator()
        self.wfile.write(bytes(response))


if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))

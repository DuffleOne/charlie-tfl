import time
import requests
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

HOST_NAME = '0.0.0.0'
PORT_NUMBER = 8000


# https://tfl.cha.rles.tech/940GZZLUWPL/district/inbound/3
# Whitechapel ID: 940GZZLUWPL
# 


def generator(url):
        stopID = url[0]
        lineID = url[1]
        direction = url[2]
        numTrains = int(url[3])
        trains = []
        sortedTrains = []
        response = []
        #text = '["Trains"'
        r = requests.get('https://api.tfl.gov.uk/StopPoint/{}/Arrivals'.format(stopID))
        print(numTrains)
        for i in range(len(r.json())):
            train = r.json()[i]
            #print(train)
            try:
                if(train["lineId"] == lineID):
                        if(train["direction"] == direction):
                                dict = {
                                "destination": train["destinationName"],
                                "timeToStation": train["timeToStation"]}
                    #print(dict)
                                trains.append(dict)

            except KeyError:
                pass

        sortedTrains = sorted(trains[:numTrains], key=lambda k: k['timeToStation'])        
        return(sortedTrains)

class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        url = str(urlparse(self.path).path)
        url = (url[:0] + url[(1):]).split("/")
        if(len(url))==4:
                self.wfile.write(json.dumps(generator(url)).encode())
                return
        else:
                self.wfile.write(json.dumps('[{"Bad Request":1}]').encode())
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

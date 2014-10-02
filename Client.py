__author__ = 'prier'

import requests

r = requests.get("http://127.0.0.1:21212/orders")
print r.status_code
print r.headers
print r.encoding
print r.text

'''def client(string):
    HOST, PORT = 'localhost', 21212
    # SOCK_STREAM == a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.setblocking(0)  # optional non-blocking
    sock.connect((HOST, PORT))

    #print "sending data => [%s]" % (string)

    sock.sendall("GET http://127.0.0.1/ HTTP/1.0\n\n")
    reply = sock.recv(16384)
    sock.close()

    #sock.send(string)
    #reply = sock.recv(16384)  # limit reply to 16K
    print "reply => \n [%s]" % (reply)
    sock.close()
    return reply

def main():
    client()

if __name__ == "__main__":
    main()'''

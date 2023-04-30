import os
import json
import socket
import struct
from socketserver import UDPServer, BaseRequestHandler


METHODS_LIST = os.getenv('METHODS_LIST', '').split(';')
MCAST_GRP = os.getenv('MCAST_GRP', '')
MCAST_PORT = int(os.getenv('MCAST_PORT', 9889))
SERVICE_PORT = int(os.getenv('SERVICE_PORT', 2000))


class UdpProxy(BaseRequestHandler):
    def handle(self) -> None:
        data, sock_in = self.request
        data = json.loads(data.strip().decode())
        if data['method'] == 'get_result':
            sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock_out.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
            mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
            sock_out.setsockopt(
                socket.IPPROTO_IP, 
                socket.IP_ADD_MEMBERSHIP, 
                mreq)
            if data['param'] == 'all':
                sock_out.sendto(b'get_result', (MCAST_GRP, MCAST_PORT))
                ans_count = 0
                result = []
                while ans_count < len(METHODS_LIST):
                    data, _ = sock_out.recvfrom(1024)
                    result.append(json.loads(data.decode()))
                    ans_count += 1
                sock_in.sendto(json.dumps({'results': result}).encode(), self.client_address)
            elif data['param'] in METHODS_LIST:
                sock_out.sendto(b'get_result', (data['param'], SERVICE_PORT))
                result = sock_out.recv(1024)
                sock_in.sendto(result, self.client_address)
            else:
                sock_in.sendto(b'{"status":"error", "info":"no such param!"}', self.client_address)
            sock_out.close()
        else:
            sock_in.sendto(b'{"status":"error", "info":"no such method!"}', self.client_address)


if __name__ == '__main__':
    OUTTER_HOST, OUTTER_PORT = os.getenv("HOST", "0.0.0.0"), int(os.getenv("PORT", 2000))
    with UDPServer((OUTTER_HOST, OUTTER_PORT), UdpProxy) as server:
        server.serve_forever()

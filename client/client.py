import os
import json
import socket


METHODS_LIST = "avro;json;msgpack;native;proto;xml;yaml".split(';')


def main():
    while True:
        request_method = input('input request method (avro, json, msgpack, native, proto, xml, yaml or all): ')
        if request_method not in METHODS_LIST and request_method != 'all':
            print('no such method!')
            break
        proxy_addr = ("localhost", int(os.getenv('SERVICE_PORT', 2000)))
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            send_data = json.dumps({'method': 'get_result', 'param': request_method}).encode()
            sock.sendto(send_data, proxy_addr)
            result = json.loads(sock.recv(1024))
            if request_method == 'all':
                for method_res in sorted(
                        filter(lambda x: x['status'] == 'ok', result['results']), 
                        key=lambda x: x['result']):
                    if method_res['status'] == 'ok':
                        print(method_res['result'], end='')
            else:
                if result['status'] == 'ok':
                    print(result['result'])


if __name__ == '__main__':
    main()

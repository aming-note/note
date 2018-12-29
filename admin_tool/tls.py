import os
import socket
import threading
import re
import time
import random
import ssl
from M2Crypto import X509, EVP, RSA, ASN1

CACerFile = 'ca.cer'

CAKeyFile = 'ca.key'

StoreFolder = 'certs/'

mutex = threading.Lock()


def gen_rand_serial(len):
    num = ''
    nlist = random.sample(['1', '2', '3', '4', '5', '6', '7', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f'], len)
    for n in nlist:
        num += str(n)
        return int(num.encode('hex'), 16)


def mk_cert():
    serial = gen_rand_serial(4)
    cert = X509.X509()
    cert.set_serial_number(serial)
    cert.set_version(2)
    mk_cert_valid(cert)
    cert.add_ext(X509.new_extension('nsComment', 'SSL sever'))
    return cert


def mk_cert_valid(cert, days=180):
    t = long(time.time())
    now = ASN1.ASN1_UTCTIME()
    now.set_time(t - 24 * 60 * 60)
    expire = ASN1.ASN1_UTCTIME()
    expire.set_time(t + days * 24 * 60 * 60)
    cert.set_not_before(now)
    cert.set_not_after(expire)


def mk_request(bits, cn='localhost'):
    pk = EVP.PKey()
    x = X509.Request()
    rsa = RSA.gen_key(bits, 65537, lambda: None)
    pk.assign_rsa(rsa)
    x.set_pubkey(pk)
    name = x.get_subject()
    name.C = "CN"
    name.CN = cn
    name.ST = 'TS'
    name.O = 'TS'
    name.OU = 'TS'
    x.sign(pk, 'sha1')
    return x, pk


def mk_self_cert(cacert_file, ca_key_file, cn):
    cert_req, pk2 = mk_request(2048, cn=cn)

    if cacert_file and ca_key_file:
        cacert = X509.load_cert(cacert_file)
        pk1 = EVP.load_key(ca_key_file)
    else:
        cacert = None
        pk1 = None

    cert = mk_cert()
    cert.set_subject(cert_req.get_subject())
    cert.set_pubkey(cert_req.get_pubkey())

    if cacert and pk1:
        cert.set_issuer(cacert.get_issuer())
        cert.sign(pk1, 'sha256')
    else:
        cert.set_issuer(cert.get_subject())
        cert.sign(pk2, 'sha256')

    with open(StoreFolder + cn + '.cer', 'w') as f:
        f.write(cert.as_pem())
    with open(StoreFolder + cn + '.key', 'w') as f:
        f.write(pk2.as_pem(None))


def RecviceMessage(ss):
    head = ''
    method = ''
    isFrist = True
    while (True):
        try:
            buf = ss.recv(2048)
            if (len(buf) > 0):
                head += buf
            else:
                break
            if isFrist:
                i = head.find(' ')
                method = head[0:i]
                isFrist = False
        except Exception as e:
            print("Recvice Browser Data Fail")
            break

        if ("\r\n\r\n" in head):
            patten = method + '+( http| https)(://)+([^/])+(/)'
            reobj = re.compile(patten)
            result, number = reobj.subn(method + ' /', head)
            req = result.replace("Proxy-Connection:", "Connection:")
            print(req)

            if method == "CONNECT":
                # t = threading.Thread(target=FakeHttps,args=(result,ss))
                # t.start()
                FakeHttps(result, ss)
            else:
                # t = threading.Thread(target=ForWardHttp,args=(result,ss))
                # t.start()
                ForWardHttp(result, ss)


def ForWardHttp(msg, ss):
    host = ''
    port = 80
    patten2 = r'(Host: )+(\S+)'
    searchObj2 = re.search(patten2, msg, re.M | re.I)
    if searchObj2:
        host = searchObj2.group(2)
        # print host
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if (isinstance(ss, ssl.SSLSocket)):
        sock = ssl.wrap_socket(sock)
        port = 443

    try:
        ip = socket.gethostbyname(host)
        sock.connect((ip, port))
    except Exception as e:
        print(e, "Connect Fail")
        return

    sock.send(msg)
    while (True):
        try:
            rec = sock.recv(2048)
            if (len(rec) > 0):
                ss.send(rec)
            else:
                break

        except Exception as e:
            print(e, 'Recvice Data Fail')
            sock.close()
            ss.close()
            break


def FakeHttps(result, ss):
    index = result.find(':')

    Host = result[len('CONNECT '):index]

    ss.send('HTTP/1.1 200 Connection Established\r\n\r\n')

    mutex.acquire()
    mk_self_cert(CACerFile, CAKeyFile, Host)  # Make a self signed certificate
    mutex.release()
    # os.system('FakeSSL.exe '+Host)
    conn = ssl.wrap_socket(ss, keyfile=StoreFolder + Host + ".key", certfile=StoreFolder + Host + ".cer",
                           server_side=True)

    RecviceMessage(conn)


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 8080))
    sock.listen(50)
    while (True):
        clientSock, address = sock.accept()
        t = threading.Thread(target=RecviceMessage, args=(clientSock,))
        t.start()
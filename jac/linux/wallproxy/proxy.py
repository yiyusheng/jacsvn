#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Based on GAppProxy by Du XiaoGang <dugang@188.com>

import BaseHTTPServer, SocketServer, socket, errno, re, time, util
try:
    import ssl
    ssl_enabled = True
except:
    ssl_enabled = False

class LocalProxyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    partSize = 1024000
    FR_Headers = ('', 'host', 'vary', 'via', 'x-forwarded-for',
            'proxy-authorization', 'proxy-connection', 'upgrade', 'keep-alive')

    def send_response(self, code, message=None):
        self.log_request(code)
        if message is None:
            if code in self.responses:
                message = self.responses[code][0]
            else:
                message = 'WallProxy Notify'
        if self.request_version != 'HTTP/0.9':
            self.wfile.write("%s %d %s\r\n" % (self.protocol_version, code, message))

    def end_error(self, code, message=None, data=None):
        if not data:
            self.send_error(code, message)
        else:
            self.send_response(code, message)
            self.wfile.write(data)
        self.connection.close()

    def do_CONNECT(self):
        if not ssl_enabled:
            return self.end_error(501, 'Local proxy error, HTTPS needs Python2.6 or later')

        # for ssl proxy
        host, _, port = self.path.rpartition(':')
        keyFile, crtFile = util.getCertificate(host)
        self.send_response(200)
        self.end_headers()
        try:
            ssl_sock = ssl.wrap_socket(self.connection, keyFile, crtFile, True)
        except ssl.SSLError, e:
            print 'SSLError: ' + str(e)
            return

        # rewrite request line, url to abs
        first_line = ''
        while True:
            data = ssl_sock.read()
            # EOF?
            if data == '':
                # bad request
                ssl_sock.close()
                self.connection.close()
                return
            # newline(\r\n)?
            first_line += data
            if '\n' in first_line:
                first_line, data = first_line.split('\n', 1)
                first_line = first_line.rstrip('\r')
                break
        # got path, rewrite
        method, path, ver = first_line.split()
        if path.startswith('/'):
            path = 'https://%s%s' % (host if port=='443' else self.path, path)
        # connect to local proxy server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not util.LISTEN_ADDR[0]:
            sock.connect(('127.0.0.1', util.LISTEN_ADDR[1]))
        else:
            sock.connect(util.LISTEN_ADDR)
        sock.send('%s %s %s\r\n%s' % (method, path, ver, data))

        # forward https request
        ssl_sock.settimeout(1)
        while True:
            try:
                data = ssl_sock.read(8192)
            except ssl.SSLError, e:
                if str(e).lower().find('timed out') == -1:
                    # error
                    sock.close()
                    ssl_sock.close()
                    self.connection.close()
                    return
                # timeout
                break
            if data != '':
                sock.send(data)
            else:
                # EOF
                break

        ssl_sock.setblocking(True)
        # simply forward response
        while True:
            data = sock.recv(8192)
            if data != '':
                ssl_sock.write(data)
            else:
                # EOF
                break
        # clean
        sock.close()
        ssl_sock.shutdown(socket.SHUT_WR)
        ssl_sock.close()
        self.connection.close()

    def _RangeFetch(self, handler, proxy, m, data):
        m = map(int, m.groups())
        start = m[0]
        end = m[2] - 1
        if 'range' in self.headers:
            req_range = re.search(r'(\d+)?-(\d+)?', self.headers['range'])
            if req_range:
                req_range = [u and int(u) for u in req_range.groups()]
                if req_range[0] is None:
                    if req_range[1] is not None:
                        if m[1]-m[0]+1==req_range[1] and m[1]+1==m[2]:
                            return False
                        if m[2] >= req_range[1]:
                            start = m[2] - req_range[1]
                else:
                    start = req_range[0]
                    if req_range[1] is not None:
                        if m[0]==req_range[0] and m[1]==req_range[1]:
                            return False
                        if end > req_range[1]:
                            end = req_range[1]
            data['headers']['content-range'] = 'bytes %d-%d/%d' % (start, end, m[2])
        elif start == 0:
            data['code'] = 200
            del data['headers']['content-range']
        data['headers']['content-length'] = end-start+1
        partSize = LocalProxyHandler.partSize
        self.send_response(data['code'])
        for k,v in data['headers'].iteritems():
            self.send_header(k.title(), v)
        self.end_headers()
        if start == m[0]:
            self.wfile.write(data['content'])
            start = m[1] + 1
            partSize = len(data['content'])
        failed = 0
        print '>>>>>>>>>>>>>>> Range Fetch started'
        while start <= end:
            self.headers['Range'] = 'bytes=%d-%d' % (start, start + partSize - 1)
            retval, data = handler(proxy, self.path, self.command, self.headers)
            if retval!=0 or data['code']!=206:
                time.sleep(4)
                continue
            m = re.search(r'bytes\s+(\d+)-(\d+)/(\d+)', data['headers'].get('content-range',''))
            if not m or int(m.group(1))!=start:
                if failed >= 1:
                    break
                failed += 1
                continue
            start = int(m.group(2)) + 1
            print '>>>>>>>>>>>>>>> %s %d' % (data['headers']['content-range'], end)
            failed = 0
            self.wfile.write(data['content'])
        print '>>>>>>>>>>>>>>> Range Fetch ended'
        self.connection.close()
        return True

    def do_METHOD(self):
        if self.path.startswith('/'):
            host = self.headers['host']
            if host.endswith(':80'):
                host = host[:-3]
            self.path = 'http://%s%s' % (host , self.path)
        handler, proxy = util.findProxy(self.client_address[0], self.path, self.command, dict(self.headers))
        if handler is None:
            return self.end_error(*proxy)

        payload_len = int(self.headers.get('content-length', 0))
        if payload_len > 0:
            payload = self.rfile.read(payload_len)
        else:
            payload = ''

        for k in LocalProxyHandler.FR_Headers:
            try:
                del self.headers[k]
            except KeyError:
                pass

        retval, data = handler(proxy, self.path, self.command, self.headers, payload)
        try:
            if retval == -1:
                return self.end_error(502, str(data))
            # Proxy Fetch
            if isinstance(data, dict):
                if data['code']==206 and self.command=='GET':
                    m = re.search(r'bytes\s+(\d+)-(\d+)/(\d+)', data['headers'].get('content-range',''))
                    if m and self._RangeFetch(handler, proxy, m, data):
                        return
                self.send_response(data['code'])
                for k,v in data['headers'].iteritems():
                    self.send_header(k.title(), v)
                self.end_headers()
                self.wfile.write(data['content'])
            # Direct Fetch
            else:
                resp = data
                self.send_response(resp.code)
                # Write resp.headers directly to avoid set-cookie bug
                self.wfile.write(resp.headers)
                self.end_headers()
                data = resp.read(8192)
                while data != '':
                    self.wfile.write(data)
                    data = resp.read(8192)
                resp.close()
        except socket.error, (err, _):
            # Connection closed before proxy return
            if err == errno.EPIPE or err == 10053: return
        self.connection.close()

    do_GET = do_METHOD
    do_HEAD = do_METHOD
    do_PUT = do_METHOD
    do_POST = do_METHOD
    do_DELETE = do_METHOD

class ThreadingHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    pass

if __name__ == '__main__':
    print '---------------------------------------------------'
    print 'ListenAddress: %s:%d' % util.LISTEN_ADDR
    print 'HTTPS Enabled: %s' % ('YES' if ssl_enabled else 'NO')
    print 'OpenSSLModule: %s' % ('YES' if util.crypto else 'NO')
    print 'Proxies Count: GAE(%d) PHP(%d) DIRECT(%d)' % (len(util.GAE_PROXY), len(util.PHP_PROXY), len(util.DIRECT_PROXY))
    print '---------------------------------------------------'
    httpd = ThreadingHTTPServer(util.LISTEN_ADDR, LocalProxyHandler)
    if util.RELOAD:
        from threading import Thread
        def repeat():
            while util.RELOAD:
                time.sleep(util.RELOAD)
                util.checkConf()
        Thread(target=repeat).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        util.RELOAD = 0
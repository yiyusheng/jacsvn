#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Functions called by proxy.py

# patch by lyricconch 20100925 (performance of autoproxy)

from __future__ import with_statement

__author__ = 'base64.decodestring("d3d3LmVodXN0QGdtYWlsLmNvbQ==")'
__version__ = '0.3.7'

try:
    from OpenSSL import crypto
except ImportError:
    crypto = None
import os, sys, re, itertools, random, struct
import urlparse, urllib2, socket, zlib, httplib

def getModulePath():
    if hasattr(sys, 'frozen'):
        return os.path.dirname(sys.executable)
    return os.path.dirname(__file__)

def _createKeyPair(type=None, bits=1024):
    if type is None:
        type = crypto.TYPE_RSA
    pkey = crypto.PKey()
    pkey.generate_key(type, bits)
    return pkey

def _createCertRequest(pkey, digest='sha1', **subj):
    req = crypto.X509Req()
    subject = req.get_subject()
    for k,v in subj.iteritems():
        setattr(subject, k, v)
    req.set_pubkey(pkey)
    req.sign(pkey, digest)
    return req

def _createCertificate(req, (issuerKey, issuerCert), serial, (notBefore, notAfter), digest='sha1'):
    cert = crypto.X509()
    cert.set_serial_number(serial)
    cert.gmtime_adj_notBefore(notBefore)
    cert.gmtime_adj_notAfter(notAfter)
    cert.set_issuer(issuerCert.get_subject())
    cert.set_subject(req.get_subject())
    cert.set_pubkey(req.get_pubkey())
    cert.sign(issuerKey, digest)
    return cert

def _loadPEM(pem, type):
    handlers = ('load_privatekey', 'load_certificate_request', 'load_certificate')
    return getattr(crypto, handlers[type])(crypto.FILETYPE_PEM, pem)

def _dumpPEM(obj, type):
    handlers = ('dump_privatekey', 'dump_certificate_request', 'dump_certificate')
    return getattr(crypto, handlers[type])(crypto.FILETYPE_PEM, obj)

def _makeCA():
    pkey = _createKeyPair(bits=2048)
    subj = {'countryName': 'CN', 'stateOrProvinceName': 'Internet',
            'localityName': 'Cernet', 'organizationName': 'WallProxy',
            'organizationalUnitName': 'WallProxy Root', 'commonName': 'WallProxy CA'}
    req = _createCertRequest(pkey, **subj)
    cert = _createCertificate(req, (pkey, req), 0, (0, 60*60*24*7305))  #20 years
    return (_dumpPEM(pkey, 0), _dumpPEM(cert, 2))

def _makeCert(host, (cakey, cacrt), serial):
    pkey = _createKeyPair()
    subj = {'countryName': 'CN', 'stateOrProvinceName': 'Internet',
            'localityName': 'Cernet', 'organizationName': host,
            'organizationalUnitName': 'WallProxy Branch', 'commonName': host}
    req = _createCertRequest(pkey, **subj)
    cert = _createCertificate(req, (cakey, cacrt), serial, (0, 60*60*24*7305))
    return (_dumpPEM(pkey, 0), _dumpPEM(cert, 2))

def _quoteData(s):
    return str(s).replace('\x10', '\x100').replace('=','\x101').replace('&','\x102')

def encodeData(dic):
    res = []
    for k,v in dic.iteritems():
        res.append('%s=%s' % (_quoteData(k), _quoteData(v)))
    return '&'.join(res)

def _unquoteData(s):
    unquote_map = {'0':'\x10', '1':'=', '2':'&'}
    res = s.split('\x10')
    for i in xrange(1, len(res)):
        item = res[i]
        try:
            res[i] = unquote_map[item[0]] + item[1:]
        except KeyError:
            res[i] = '\x10' + item
    return ''.join(res)

def decodeData(qs, keep_blank_values=False, strict_parsing=False):
    pairs = qs.split('&')
    dic = {}
    for name_value in pairs:
        if not name_value and not strict_parsing:
            continue
        nv = name_value.split('=', 1)
        if len(nv) != 2:
            if strict_parsing:
                raise ValueError, "bad query field: %r" % (name_value,)
            if keep_blank_values:
                nv.append('')
            else:
                continue
        if len(nv[1]) or keep_blank_values:
            dic[_unquoteData(nv[0])] = _unquoteData(nv[1])
    return dic

def _xor(data, key):
    key = [ord(i) for i in key]
    data = [ord(d)^k for d,k in itertools.izip(data, itertools.cycle(key))]
    return ''.join(map(chr, data))
xor = lambda data, key: key and _xor(data, key) or data

def proxyFetch(proxy, url, method='GET', headers='', payload=''):
    if not isinstance(proxy, list):
        proxy = [proxy, proxy]
    #length = len(proxy)
    #proxy = list(itertools.islice(itertools.cycle(proxy), 2 if length<=2 else length))
    proxy = list(proxy) #Get a copy of proxy because of list.pop
    if len(proxy) == 1: proxy *= 2
    params = zlib.compress(encodeData({'url':url, 'method':method,
            'headers':headers, 'payload':payload}))
    errors = []
    length = len(proxy)
    for i in range(1, 3):
        server = proxy.pop(random.randint(0, length-i))
        data = xor(params, server['key'])
        req = urllib2.Request(server['url'], data, HEADERS)
        try:
            resp = server['proxy'].open(req)
            data = resp.read()
            resp.close()
        except urllib2.HTTPError, e:
            try:
                errors.append('%d: %s' % (e.code, httplib.responses[e.code]))
            except KeyError:
                errors.append(str(e.code))
            continue
        except urllib2.URLError, e:
            errors.append(str(e.reason))
            continue
        except Exception, e:
            errors.append(repr(e))
            continue
        try:
            data = xor(data, server['key'])
            if data[0] == '0':
                raw_data = data[1:]
            elif data[0] == '1':
                raw_data = zlib.decompress(data[1:])
            else:
                raise ValueError('Data format not match(%s)' % server['url'])
            data = {}
            data['code'], hlen, clen = struct.unpack('>3I', raw_data[:12])
            if len(raw_data) != 12+hlen+clen:
                raise ValueError('Data length not match')
            data['content'] = raw_data[12+hlen:]
            if data['code'] == 555:     #Urlfetch Failed
                raise ValueError(data['content'])
            data['headers'] = decodeData(raw_data[12:12+hlen])
            return (0, data)
        except Exception, e:
            errors.append(str(e))
    return (-1, errors)

def directFetch(proxy, url, method='GET', headers=None, payload=None):
    #headers and payload may be ''
    if not payload: payload = None
    if not headers: headers = {}
    req = urllib2.Request(url, payload, headers)
    req.get_method = lambda: method
    try:
        resp = proxy.open(req)
        return (0, resp)
    except urllib2.HTTPError, e:
        try:
            return (-1, '%d: %s' % (e.code, httplib.responses[e.code]))
        except KeyError:
            return (-1, e.code)
    except urllib2.URLError, e:
        return (-1, e.reason)
    except Exception, e:
        return (-1, repr(e))

def findProxy(remote, url, method, headers):
    proxy = FindProxyForURL(remote, url, method, headers)
    if not proxy:
        return (None, (417, 'Selected proxy has not been configured yet'))
    #Reject for some reason
    if isinstance(proxy, tuple):
        return (None, proxy)
    if isinstance(proxy, list):
        tester = proxy[random.randint(0, len(proxy)-1)]
    else:
        tester = proxy
    if isinstance(tester, dict):
        return (proxyFetch, proxy)
    else:
        return (directFetch, tester)

def parseURL(url):
    url = urlparse.urlparse(url)
    try:
        return url.scheme, url.hostname, url.port
    except ValueError:
        netloc = url.netloc.rsplit('@', 1)[-1].lower()
    try:
        #netloc may be IPv6 address like [::1]:8086
        p1 = netloc.rindex(']')
        p2 = netloc.rindex(':')
        if p1 > p2:
            return url.scheme, netloc[1:p1], None
        return url.scheme, netloc[1:p1], int(netloc[p2+1:])
    except:
        return url.scheme, netloc, None

def dnsDomainIs(host, domain):
    return host == domain or host.endswith('.' + domain)

def _parseAutoProxyList(ruleList):
    rules_hash =  [{}, {}]
    rules_share = [[], []]

    for line in ruleList.splitlines()[1:]:
        # Ignore the first line ([AutoProxy x.x]), empty lines and comments
        line = line.strip()
        if line and line[0] not in ('[', '!'):
            rule_type = 1
            # Exceptions
            if line.startswith('@@'):
                line = line[2:]
                rule_type = 0
            # Regular expressions
            if line.startswith('/') and line.endswith('/'):
                line = line[1:-1]
            # Other cases
            else:
                # Remove multiple wildcards
                line = re.sub(r'\*+', r'*', line)
                # Remove anchors following separator placeholder
                line = re.sub(r'\^\|$', r'^', line, 1)
                # Escape special symbols
                line = re.sub(r'(\W)', r'\\\1', line)
                # Replace wildcards by .*
                line = re.sub(r'\\\*', r'.*', line)
                # Process separator placeholders
                line = re.sub(r'\\\^', r'(?:[^\w\-.%\u0080-\uFFFF]|$)', line)
                # Process extended anchor at expression start
                line = re.sub(r'^\\\|\\\|', r'^[\w\-]+:\/+(?!\/)(?:[^\/]+\.)?', line, 1)
                # Process anchor at expression start
                line = re.sub(r'^\\\|', '^', line, 1)
                # Process anchor at expression end
                line = re.sub(r'\\\|$', '$', line, 1)
                # Remove leading wildcards
                line = re.sub(r'^(\.\*)', '', line, 1)
                # Remove trailing wildcards
                line = re.sub(r'(\.\*)$', '', line, 1)

            if line:
                i = line.find(r'\?')
                keys = RULE_OPTIMIZE.findall(line if i==-1 else line[:i])
                hash_key = max(filter(lambda x: x not in ('http','com'), keys),
                        key=lambda x: len(x)).lower() if keys else None
                if hash_key:
                    if hash_key in rules_hash[rule_type]:
                        rules_hash[rule_type][hash_key].append(line)
                    else:
                        rules_hash[rule_type][hash_key] = [line]
                else:
                    rules_share[rule_type].append(line)

    # Remove repeated rules
    cnt_hash = [0, 0]
    for i in (0, 1):
        for k,v in rules_hash[i].iteritems():
            rules_hash[i][k] = [re.compile(r) for r in list(set(v))]
            cnt_hash[i] += len(rules_hash[i][k])
    for i, v in enumerate(rules_share):
        rules_share[i] = [re.compile(r) for r in list(set(v))]
    print 'Rules count: %d:%d %d:%d %d %d' % (len(rules_hash[0]), cnt_hash[0],
        len(rules_hash[1]), cnt_hash[1], len(rules_share[0]), len(rules_share[1]))
    return rules_hash + rules_share

def _initAutoProxyList():
    if not AUTOPROXY_LIST:
        return None
    ruleLists = []
    print 'Fetching AutoProxy List:'
    for url in AUTOPROXY_LIST:
        ruleList = None
        print '  %s...' % url,
        if not url.startswith('file'):
            retval, data = proxyFetch(GAE_PROXY, url)
            if retval == 0:
                ruleList = data['content']
        #Local file or proxyFetch failed
        if not ruleList:
            try:
                resp = urllib2.urlopen(url)
                ruleList = resp.read()
                resp.close()
            except:
                pass

        if ruleList:
            try:
                #ruleList may have encoded with base64
                ruleList = ruleList.decode('base64')
            except:
                pass
            print '%d bytes' % len(ruleList)
            ruleLists.append(ruleList)
        else :
            print 'Failed'
    ruleLists = '\n'.join(ruleLists)
    print 'Converting rules to compiledRegex...'
    return  _parseAutoProxyList(ruleLists)

def inAutoProxy(url):
    if not AUTOPROXY_LIST:
        return False

    D_HASH, P_HASH, D_SHARE, P_SHARE = AUTOPROXY_LIST
    i = url.find('?')
    token = url if i==-1 else url[:i]
    tokens = filter(lambda x: x not in ('http','com'),
            RULE_OPTIMIZE.findall(token.lower()))

    for token in tokens:
        if token in D_HASH:
            for regex in D_HASH[token]:
                if regex.search(url):
                    return False
    for regex in D_SHARE:
        if regex.search(url):
            return False
    for token in tokens:
        if token in P_HASH:
            for regex in P_HASH[token]:
                if regex.search(url):
                    return True
    for regex in P_SHARE:
        if regex.search(url):
            return True
    return False

def readFile(filename):
    try:
        with open(filename, 'rb') as f:
            return f.read()
    except IOError:
        return None

def writeFile(filename, content):
    with open(filename, 'wb') as f:
        f.write(str(content))

def getCertificate(host):
    if not crypto:
        keyFile = os.path.join(base_dir, 'cert/ca.key')
        crtFile = os.path.join(base_dir, 'cert/ca.crt')
        return (keyFile, crtFile)
    keyFile = os.path.join(base_dir, 'cert/%s.key' % host)
    crtFile = os.path.join(base_dir, 'cert/%s.crt' % host)
    if not os.path.isfile(keyFile) or not os.path.isfile(crtFile):
        global SERIAL
        SERIAL += 1
        key, crt = _makeCert(host, CA, SERIAL)
        writeFile(keyFile, key)
        writeFile(crtFile, crt)
        writeFile(os.path.join(base_dir, 'cert/serial'), SERIAL)
    return (keyFile, crtFile)

def _checkCA():
    global CA, SERIAL
    #Check cert directory
    cert_dir = os.path.join(base_dir, 'cert')
    if not os.path.isdir(cert_dir):
        if os.path.isfile(cert_dir):
            os.remove(cert_dir)
        os.mkdir(cert_dir)
    #Check CA file
    cakeyFile = os.path.join(base_dir, 'cert/ca.key')
    cacrtFile = os.path.join(base_dir, 'cert/ca.crt')
    serialFile = os.path.join(base_dir, 'cert/serial')
    cakey = readFile(cakeyFile)
    cacrt = readFile(cacrtFile)
    SERIAL = readFile(serialFile)
    try:
        CA = (_loadPEM(cakey, 0), _loadPEM(cacrt, 2))
        SERIAL = int(SERIAL)
    except:
        cakey, cacrt = _makeCA()
        SERIAL = 0
        #Remove old certifications, because ca and cert must be in pair
        for name in os.listdir(cert_dir):
            path = os.path.join(cert_dir, name)
            if os.path.isfile(path):
                os.remove(path)
        writeFile(cakeyFile, cakey)
        writeFile(cacrtFile, cacrt)
        writeFile(serialFile, SERIAL)
        CA = (_loadPEM(cakey, 0), _loadPEM(cacrt, 2))

def _checkConf(confFile):
    global LISTEN_ADDR, GAE_PROXY, PHP_PROXY, DIRECT_PROXY
    global AUTOPROXY_LIST, RULE_OPTIMIZE, RELOAD, HEADERS
    LISTEN_ADDR = ('127.0.0.1', 8086)
    GAE_PROXY = []
    PHP_PROXY = []
    DIRECT_PROXY = [{}]
    AUTOPROXY_LIST = None
    RULE_OPTIMIZE = r'[\w%]{2,}'
    RELOAD = 5
    HEADERS = {'Content-Type':'application/octet-stream'}
    try:
        execfile(confFile, globals())
        if isinstance(AUTOPROXY_LIST, str):
            AUTOPROXY_LIST = (AUTOPROXY_LIST,)
        _checkProxy()
        RULE_OPTIMIZE = re.compile(RULE_OPTIMIZE)
        AUTOPROXY_LIST = _initAutoProxyList()
        #Test FindProxyForURL
        FindProxyForURL('127.0.0.1', 'http://wallproxy/', 'GET', {})
    except Exception, e:
        print 'checkConf() Error: %s' % e
        sys.exit(-1)

def checkConf(STATIC=[]):
    confFile = os.path.join(base_dir, 'proxy.conf')
    lastmtime = os.path.getmtime(confFile)
    if not STATIC:
        STATIC.append(lastmtime)
        _checkConf(confFile)
    elif STATIC[0] != lastmtime:
        STATIC[0] = lastmtime
        _checkConf(confFile)
        print 'Config reloaded'

#All status code should reply to browser in directFetch, I don't care how to deal with them
class DirectHTTPErrorProcessor(urllib2.HTTPErrorProcessor):
    def http_response(self, request, response):
        return response
    https_response = http_response

def _checkProxy():
    global GAE_PROXY, PHP_PROXY, DIRECT_PROXY
    proxies = []
    try:
        raw_proxies = []
        for server in GAE_PROXY + PHP_PROXY:
            if isinstance(server['proxy'], urllib2.OpenerDirector):
                continue
            if not server['url']:
                raise KeyError('url')
            try:
                server['proxy'] = proxies[raw_proxies.index(server['proxy'])]
            except ValueError:
                raw_proxies.append(server['proxy'])
                server['proxy'] = urllib2.build_opener(#urllib2.HTTPHandler(debuglevel=1),
                        urllib2.ProxyHandler(server['proxy']))
                proxies.append(server['proxy'])
        #GAE_PROXY is important
        if not GAE_PROXY:
            GAE_PROXY = PHP_PROXY
        raw_proxies = []
        for i in range(len(DIRECT_PROXY)):
            if isinstance(DIRECT_PROXY[i], urllib2.OpenerDirector):
                continue
            try:
                DIRECT_PROXY[i] = proxies[raw_proxies.index(DIRECT_PROXY[i])]
            except ValueError:
                raw_proxies.append(DIRECT_PROXY[i])
                DIRECT_PROXY[i] = urllib2.build_opener(DirectHTTPErrorProcessor(),
                        urllib2.ProxyHandler(DIRECT_PROXY[i]))
                proxies.append(DIRECT_PROXY[i])
    except (TypeError, KeyError), e:
        raise ValueError('GAE_PROXY or PHP_PROXY or DIRECT_PROXY format Error: %s' % e)

base_dir = getModulePath()
if crypto: _checkCA()
checkConf()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Functions called by proxy.py

# patch by lyricconch 20100925 (performance of autoproxy)

__author__ = 'base64.decodestring("d3d3LmVodXN0QGdtYWlsLmNvbQ==")'
__version__ = '0.3.7'

try:
    from OpenSSL import crypto
except ImportError:
    crypto = None
import os, sys, re, itertools, random, struct
import urlparse, urllib2, socket, zlib, httplib, time, mutex

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
    global RULE_OPTIMIZE
    from re import sub,compile
    rules_hash =  [{},{}]
    rules_shash = [{},{}]
    rules_share = [[],[]]

    for line in ruleList.splitlines()[1:]:
        line = line.strip()
        if not line or line[0] in ('[', '!'):
            continue
        useProxy = True
        if line.startswith('@@'):
            line = line[2:]
            useProxy = False
        # Regular expressions
        if line.startswith('/') and line.endswith('/'):
            line = line[1:-1]
            rule_regex = line
            # [...] =>  .
            rule_hash = sub(r'\[[^]]+\]', '.', line)
            # {a,b} =>  *
            rule_hash = sub(r'\{[^}]+\}', '*', rule_hash)
            # (?!...) (?=...) =>
            rule_hash = sub(r'\(\?[!=][^)]\)', '*', rule_hash)
            # (?:...) (...) =>(...)
            rule_hash = sub(r'\((\?:)?([^)]+)\)','\2', rule_hash)
            # * ? + => *
            rule_hash = sub(r'(?<!\\)[*?+]','*' ,rule_hash)
            # ^ $ ^| =>
            rule_hash = sub(r'^\^', '', rule_hash)
            rule_hash = sub(r'\$$', '', rule_hash)
            # \w \W \d \D \s \S=> .
            rule_hash = sub(r'\\[wWdDsS]','.',rule_hash)
            # . .* => *
            rule_hash = sub(r'(?<!\\)\.\*?','*', rule_hash)
            # \. => .
            rule_hash = sub(r'(?<!\\)\\(\W)',r'\1', rule_hash)
        else:
            rule_hash = line
            # Remove multiple wildcards
            rule_regex = sub(r'\*+', r'*', line)
            # Remove anchors following separator placeholder
            rule_regex = sub(r'\^\|$', r'^', rule_regex, 1)
            # Escape special symbols
            rule_regex = sub(r'(\W)', r'\\\1', rule_regex)
            # Replace wildcards by .*
            rule_regex = sub(r'\\\*', r'.*', rule_regex)
            # Process separator placeholders
            rule_regex = sub(r'\\\^', r'(?:[^\w\-.%\u0080-\uFFFF]|$)', rule_regex)
            # Process extended ahefnchor at expression start
            rule_regex = sub(r'^\\\|\\\|', r'^[\w\-]+:\/+(?!\/)(?:[^\/]+\.)?', rule_regex, 1)
            # Process anchor at expression start
            rule_regex = sub(r'^\\\|', '^', rule_regex, 1)
            # Process anchor at expression end
            rule_regex = sub(r'\\\|$', '$', rule_regex, 1)
            # Remove leading wildcards
            rule_regex = sub(r'^(\.\*)', '', rule_regex, 1)
            # Remove trailing wildcards
            rule_regex = sub(r'(\.\*)$', '', rule_regex, 1)
        if rule_regex != '':
            value = compile(rule_regex)
            keys = filter(lambda x:x.find('*')==-1, re.findall(RULE_OPTIMIZE,rule_hash))
            keys.sort(lambda x,y:len(x)-len(y))
            best_key = keys[-1] if keys else None;
            rule_type = 1 if useProxy else 0

            hashed = False
            while keys:
                key = keys.pop()
                if key not in rules_hash[rule_type]:
                    rules_hash[rule_type][key] = value
                    hashed = True
                    break
            if not hashed :
                if best_key :
                    if best_key in rules_shash[rule_type] :
                        rules_shash[rule_type][best_key].append(value)
                    else:
                        rules_shash[rule_type][best_key]=[value]
                else:
                    rules_share[rule_type].append(value)

    dh = len(rules_hash[0].keys())
    dk = len(rules_shash[0].keys())
    de = reduce(lambda x,y: x+len(y),rules_shash[0].itervalues(),0)
    ds = len(rules_share[0])
    ph = len(rules_hash[1].keys())
    pk = len(rules_shash[1].keys())    
    pe = reduce(lambda x,y: x+len(y),rules_shash[1].itervalues(),0)
    ps = len(rules_share[1])
    da = dh + de + ds
    pa = ph + pe + ps

    print '  optimize_param**: %s\ttotal: %d\tdirect: %d proxy: %d' % (RULE_OPTIMIZE , da+pa , da, pa)
    print '  direct_hash(very fast): %6d / %2.2f%%' % (dh, 100*dh/(da+0.01))
    print '  direct_shash(fast)    : %6d / %2.2f%% \tkeys: %6d / %2.2f%%' % (de,100*de/(da+0.01),dk,100*dk/(de+0.01))
    print '  direct_share(slow)    : %6d*/ %2.2f%%' % (ds, 100*ds/(da+0.01))
    print '  proxy_hash(vary fast) : %6d / %2.2f%%' % (ph, 100*ph/(pa+0.01))
    print '  proxy_shash(fast)     : %6d / %2.2f%% \tkeys: %6d / %2.2f%%' % (pe,100*pe/(pa+0.01),pk,100*pk/(pe+0.01))
    print '  proxy_share(slow)     : %6d*/ %2.2f%%' % (ps, 100*ps/(pa+0.01))
    print '  ** : dont change this unless u know how it works.  * : lower is better.' 
    
    del sub, compile
    return (rules_hash[0],rules_shash[0],rules_share[0],
        rules_hash[1],rules_shash[1],rules_share[1])

def _initAutoProxyList():
    if not AUTOPROXY_LIST:
        return None;
    import base64
    print 'getting autoproxy data from sources:'
    ruleListTotal = ""
    for url in AUTOPROXY_LIST:
        ruleList = None
        print '  ' + url + '... ',
        if not url.startswith('file'):
            retval, data = proxyFetch(GAE_PROXY, url)
            if retval == 0:
                ruleList = data['content']
        #Local file or proxyFetch failed
        if not ruleList:
            retval, resp = directFetch(DIRECT_PROXY[0], url)
            if retval == 0:
                ruleList = resp.read()
                resp.close()
        if ruleList:
            try:
                #ruleList may have encoded with base64
                ruleList = base64.decodestring(ruleList)
            except:
                pass
            ruleListTotal += ruleList+'\n';
            print str(len(ruleList)) + 'bytes.'
        else :
            print 'Failed'
    del base64
    print "converting autoproxy data to hashed compiledRegex ..."
    return  _parseAutoProxyList(ruleListTotal)

def inAutoProxy(url ):
    global RULE_STATIC, RULE_OPTIMIZE
    if not RULE_STATIC :
        return False

    D_HASH,D_SHASH,D_SHARE,P_HASH,P_SHASH,P_SHARE = RULE_STATIC
    tokens = re.findall(RULE_OPTIMIZE,url)

    for regex in D_SHARE :
        if regex.search(url) :
            return False
    for token in tokens :
        if token in D_SHASH :
            for regex in D_SHASH[token] :
                if regex.search(url):
                    return False;
        if token in D_HASH :
            if D_HASH[token].search(url) :
                return False

    for token in tokens :
        if token in P_HASH :
            if P_HASH[token].search(url) :
                return True
        if token in P_SHASH :
            for regex in P_SHASH[token] :
                if regex.search(url) :
                    return True;
    for regex in P_SHARE :
        if regex.search(url) :
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
    global LISTEN_ADDR, GAE_PROXY, PHP_PROXY, DIRECT_PROXY, AUTOPROXY_LIST, RELOAD, HEADERS
    global RULE_STATIC, RULE_OPTIMIZE
    LISTEN_ADDR = ('127.0.0.1', 8086)
    GAE_PROXY = []
    PHP_PROXY = []
    DIRECT_PROXY = [{}]
    AUTOPROXY_LIST = None
    RELOAD = 5
    HEADERS = {'Content-Type':'application/octet-stream'}
    try:
        execfile(confFile, globals())
        if isinstance(AUTOPROXY_LIST, str):
            AUTOPROXY_LIST = (AUTOPROXY_LIST,)
        _checkProxy()
        #Test FindProxyForURL
        FindProxyForURL('127.0.0.1', 'http://wallproxy/', 'GET', {})
        RULE_OPTIMIZE = r'[\w%*]{3,}' if not RULE_OPTIMIZE else RULE_OPTIMIZE
        RULE_STATIC = _initAutoProxyList()
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
RULE_OPTIMIZE = None
RULE_STATIC = None
if crypto: _checkCA()
checkConf()
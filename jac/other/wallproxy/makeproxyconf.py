## Created by Randomwalk.
## Based on scripts from Lyricconch in Wallproxy.

import urllib2, json, re

PAC = '''
# -*- coding: utf-8 -*-

LISTEN_ADDR = ('127.0.0.1', 8086)

GAE_PROXY = [{
    'url': 'http://jacaegdl.appspot.com/fetch.php',
    'key': '',
    'proxy': {},
}]

PHP_PROXY = [{
    'url': 'http://35free.net/jacteefan/fetch.php',
    'key': '',
    'proxy': {},
}]

DIRECT_PROXY = [{}]

HEADERS = {'Content-Type':'application/octet-stream', 'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.0 Safari/534.10'}

RULE_STATIC_EXCLUDE = %s

#FOR CERNET
FreeIPs = %s

#FOR CERNET END
def FindProxyForURL(remote, url, method, headers):
    scheme, host, port = parseURL(url)
    #return PHP_PROXY
    #if dnsDomainIs(host, 'launchpad.net'):
        #return DIRECT_PROXY[0]
    if host == 'wallproxy':
        return GAE_PROXY
    #lookup dns
    ipinfo = socket.getaddrinfo(host,port)
    if ipinfo:
        ip = ipinfo[0][4][0]
    else:
	return goWallProxy(method, host, port, headers)
    if ip:
        #return PHP_PROXY
        #ipv6
        if ip.find(':') != -1:
	    return DIRECT_PROXY[0]
        #local
        if isInNet(ip,'127.0.0.0','255.0.0.0'):
            return DIRECT_PROXY[0]
        if isInNet(ip,'10.0.0.0','255.0.0.0'):
            return DIRECT_PROXY[0]
        if isInNet(ip,'192.168.0.0','255.255.0.0'):
            return DIRECT_PROXY[0]
        if isInNet(ip,'172.16.0.0','255.240.0.0'):
            return DIRECT_PROXY[0]
        if isInNet(ip,'169.254.0.0','255.255.0.0'):
            return DIRECT_PROXY[0]
        #FOR CERNET
        ip_l = ip2long(ip)
        bytes = ip.split('.')
        if bytes[0] in FreeIPs:
            for ipgm in FreeIPs[bytes[0]]:
                if ip_l&ipgm[1] == ipgm[0]&ipgm[1]:
                    return DIRECT_PROXY[0]
    else:
        return goWallProxy(method, host, port, headers)
    if inProxyExclude(url):
        #return PHP_PROXY
        #return goWallProxy(method, host, port, headers)
        return DIRECT_PROXY[0]
    #return PHP_PROXY
    return goWallProxy(method, host, port, headers)

def ip2long(ip):
    seg = map(int,ip.split('.'))
    return (seg[0]<<24)+(seg[1]<<16)+(seg[2]<<8)+seg[3]

def isInNet(host, pattern, mask):
    host_l = ip2long(host)
    pattern_l = ip2long(pattern)
    mask_l = ip2long(mask)
    return host_l&mask_l==pattern_l&mask_l

def  inProxyExclude(url):
    D_SHASH = RULE_STATIC_EXCLUDE[0]
    D_SHARE = RULE_STATIC_EXCLUDE[1]
    P_SHASH = RULE_STATIC_EXCLUDE[2]
    P_SHARE = RULE_STATIC_EXCLUDE[3]
    tokens = re.findall(r'[\w%%*]{3,}',url)
    for regex in D_SHARE :
        if re.search(regex,url) :
            return False
    for token in tokens :
        if token in D_SHASH :
            for regex in D_SHASH[token] :
                if re.search(regex,url):
                    return False;

    for token in tokens :
        if token in P_SHASH :
            for regex in P_SHASH[token] :
                if re.search(regex,url) :
                    return True;
    for regex in P_SHARE :
        if re.search(regex,url) :
            return True

    return False

def goWallProxy(method, host, port, headers):
    if method not in ('GET', 'HEAD', 'PUT', 'POST', 'DELETE'):
        return (405, 'Local proxy error, Method not allowed')
    if method == 'DELETE' or int(headers.get('content-length', 0)) > 0x100000:
        #return PHP_PROXY
        return DIRECT_PROXY[0]
    if port is None or (port >= 80 and port <= 90) or (port >= 440 and port <= 450) or port >= 1024:
        return GAE_PROXY
    #return PHP_PROXY
    return DIRECT_PROXY[0]
'''

def _getAutoProxyList():
    RULE_OPTIMIZE = r'[\w%*]{3,}'
    sub = re.sub
    rules_shash = [{},{}]
    rules_share = [[],[]]
    
    print "Reading Autoproxy List...."
    #o = urllib2.urlopen('http://jacsvn.googlecode.com/svn/jac/other/wallproxy/gfwlist.txt')
    o = file('gfwlist.txt','r')
    ruleList = o.read()
    o.close()

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
            # value = compile(rule_regex)
            value = rule_regex
            keys = filter(lambda x:x.find('*')==-1, re.findall(RULE_OPTIMIZE,rule_hash))
            keys.sort(lambda x,y:len(x)-len(y))
            best_key = keys[-1] if keys else None;
            rule_type = 1 if useProxy else 0

            if best_key:
                if best_key in rules_shash[rule_type]:
                    rules_shash[rule_type][best_key].append(value)
                else:
                    rules_shash[rule_type][best_key]=[value]
            else:
                rules_share[rule_type].append(value)
    return json.dumps((rules_shash[0],rules_share[0],rules_shash[1],rules_share[1]))

def _getIPTableForCERNET():
    URLs = (r'CERNET.txt', 
            #r'http://jacsvn.googlecode.com/svn/jac/other/wallproxy/CERNET.txt', 
            )
            # If other free lists are privided by your own school, replace URLs above with yours.
            # The format of your own list should be the same as that of the lists above. Or just modify the regex below.
    iptable = []
    ips = []
    
    print "Reading CERNET Free IP List...."
    for i in URLs:
        #o = urllib2.urlopen(i)
        o = file(i,'r')
        s = o.read()
        o.close()
        ips.extend(re.findall('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\s+[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\s+([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)',s))
    for i in ips:
        ip_seg = map(int,i[0].split('.'))
        mask_seg = map(int,i[1].split('.'))
        iptable.append((ip_seg[0],\
                ((ip_seg[0]<<24)+(ip_seg[1]<<16)+(ip_seg[2]<<8)+ip_seg[3],\
                (mask_seg[0]<<24)+(mask_seg[1]<<16)+(mask_seg[2]<<8)+mask_seg[3])))
    hashed = {}
    for i in iptable:
        if i[0] in hashed:
            hashed[i[0]].append(i[1])
        else:
            hashed[i[0]] = [i[1]]
    return json.dumps(hashed)


if __name__=="__main__":
    pac = PAC%(_getAutoProxyList(),_getIPTableForCERNET())
    print "Writing to file 'proxy.conf'...."
    f = file('proxy.conf','w')
    f.write(pac)
    f.close()
    print "Done!"
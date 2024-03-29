## Created by Randomwalk.
## Based on scripts from Lyricconch in Wallproxy.

import urllib2, json, re

PAC = '''
// Created by Randomwalk.
// Based on scripts from Lyricconch in Wallproxy.

GAEPROXY = 'PROXY 127.0.0.1:48100';
DIRECT = 'DIRECT';
RULE_EXCLUDE = %s;

//// FOR CERNET END
function inRuleList(url){
    D_SHASH = RULE_EXCLUDE[0];
    D_SHARE = RULE_EXCLUDE[1];
    P_SHASH = RULE_EXCLUDE[2];
    P_SHARE = RULE_EXCLUDE[3];
    tokens = url.match(/[\w%%*]{3,}/g);
    for (var regex in D_SHARE){
        if (eval('/'+D_SHARE[regex]+'/').test(url))
            return false;
    }
    for (var i in tokens){
        token = tokens[i];
        if (token in D_SHASH)
            for (regex in D_SHASH[token])
                if (eval('/'+D_SHASH[token][regex]+'/').test(url))
                    return false;
    }
    for (var i in tokens){
        token = tokens[i];
        if (token in P_SHASH)
            for (regex in P_SHASH[token])
                if (eval('/'+P_SHASH[token][regex]+'/').test(url))
                    return true;
    }
    for (var regex in P_SHARE){
        if (eval('/'+P_SHARE[regex]+'/').test(url))
            return true;
    }
    return false;
}
function FindProxyForURL(url, host){
    if (inRuleList(url))
        return DIRECT;
    
    return GAEPROXY;
    //// FOR CERNET END
    //// DISABLE FOR CERNET: return DIRECT;
}

'''

def _getRuleList():
    RULE_OPTIMIZE = r'[\w%*]{3,}'
    sub = re.sub
    rules_shash = [{},{}]
    rules_share = [[],[]]
    
    print "Reading Rule List...."
    #o = urllib2.urlopen('http://jacsvn.googlecode.com/svn/jac/other/PAC/gfwlist.txt')
    o = file('excludelist.txt','r')
    #o = urllib2.urlopen(source)
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

if __name__=="__main__":
    #ule_exclude = 'http://jacsvn.googlecode.com/svn/jac/other/PAC/excludelist.txt'
    pac = PAC%(_getRuleList())
    print "Writing to file 'proxy.conf'...."
    f = file('jac.pac','w')
    f.write(pac)
    f.close()
    print "Done!"
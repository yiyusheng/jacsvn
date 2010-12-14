
// Created by Randomwalk.
// Based on scripts from Lyricconch in Wallproxy.

GAEPROXY = 'PROXY 127.0.0.1:48100';
DIRECT = 'DIRECT';
RULE_EXCLUDE = [{}, [], {"baidu": ["^[\\w\\-]+:\\/+(?!\\/)(?:[^\\/]+\\.)?baidu\\.com"], "iciba": ["^[\\w\\-]+:\\/+(?!\\/)(?:[^\\/]+\\.)?iciba\\.com"], "renren": ["^[\\w\\-]+:\\/+(?!\\/)(?:[^\\/]+\\.)?renren\\.com"], "whnet": ["^[\\w\\-]+:\\/+(?!\\/)(?:[^\\/]+\\.)?whnet\\.edu\\.cn"], "hust": ["^[\\w\\-]+:\\/+(?!\\/)(?:[^\\/]+\\.)?hust\\.edu\\.cn"], "114": ["^[\\w\\-]+:\\/+(?!\\/)(?:[^\\/]+\\.)?202\\.114\\.9\\.43"]}, []];

//// FOR CERNET END
function inRuleList(url){
    D_SHASH = RULE_EXCLUDE[0];
    D_SHARE = RULE_EXCLUDE[1];
    P_SHASH = RULE_EXCLUDE[2];
    P_SHARE = RULE_EXCLUDE[3];
    tokens = url.match(/[\w%*]{3,}/g);
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



// Created by Randomwalk.
// Based on scripts from Lyricconch in Wallproxy.

GAEPROXY = 'PROXY 127.0.0.1:48100';
DIRECT = 'DIRECT';
RULE_STATIC = 
[{}, [], {"renren": ["^[\\w\\-]+:\\/+(?!\\/)(?:[^\\/]+\\.)?renren\\.com"], "youku": ["^[\\w\\-]+:\\/+(?!\\/)(?:[^\\/]+\\.)?youku\\.com"], "iciba": ["^[\\w\\-]+:\\/+(?!\\/)(?:[^\\/]+\\.)?iciba\\.com"]}, []];
//// FOR CERNET
FreeIPs = 
{"1": [[20119552, 4294901760], [28835840, 4294836224]], "137": [[2310864896, 4294901760]], "140": [[2356215808, 4294901760]], "143": [[2404974592, 4294901760]], "144": [[2429943808, 4294901760]], "147": [[2466775040, 4294901760]], "149": [[2500272147, 4294967295]], "152": [[2556755968, 4294901760], [2556952576, 4294901760]], "27": [[462684160, 4294705152]], "158": [[2659450880, 4294901760], [2662727680, 4294901760]], "159": [[2682388480, 4294901760]], "161": [[2714697728, 4294901760]], "162": [[2724790272, 4294901760]], "166": [[2792292352, 4294901760]], "167": [[2810904576, 4294901760]], "168": [[2829058048, 4294901760]], "175": [[2938765312, 4294836224], [2938896384, 4294901760], [2948136960, 4294901760], [2948202496, 4294836224]], "49": [[825491456, 4294705152], [829947904, 4294705152], [831258624, 4294836224]], "192": [[3226888192, 4294967040]], "180": [[3026190336, 4294966784], [3027632128, 4294901760], [3028877312, 4294959104], [3029860352, 4294443008], [3030384640, 4293918720], [3025403904, 4294836224], [3033071616, 4294901760], [3033530368, 4294836224]], "94": [[1593132032, 4294966272]], "182": [[3059482624, 4294901760]], "183": [[3070230528, 4290772992], [3081240576, 4294836224], [3081371648, 4294901760], [3081502720, 4294705152]], "202": [[3389324288, 4294966272], [3389975299, 4294967295], [3389976102, 4294967295], [3391746048, 4294963200], [3391852544, 4294963200], [3393524594, 4294967295], [3395006464, 4294963200], [3395156992, 4294966272], [3397086720, 4294967040], [3399004160, 4294963200], [3399393280, 4294959104], [3400790016, 4294963200], [3389292544, 4294959104], [3391488000, 4294901760], [3391668224, 4294959104], [3391954944, 4294959104], [3393929216, 4294959104], [3394506752, 4294966784], [3395223552, 4294959104], [3395289088, 4293918720], [3396337664, 4294443008], [3396861952, 4294836224], [3397001216, 4294963200], [3397320704, 4294950912], [3397353472, 4294934528], [3397517312, 4294959104], [3397574656, 4294959104], [3397636096, 4294963200], [3401408512, 4294959104], [3401580544, 4293918720], [3394889728, 4294965248], [3391870976, 4294966784], [3399528448, 4294963200], [3399835648, 4294965248], [3399837696, 4294966272]], "58": [[974258176, 4294836224], [974389248, 4294901760], [974520320, 4294836224], [975047816, 4294967295], [975235072, 4294966272], [976605184, 4294963200], [976945423, 4294967295], [976945424, 4294967294], [976977920, 4294934528], [977010688, 4294705152], [977403904, 4294836224], [977567744, 4294934528], [978550784, 4294934528], [979632128, 4294836224], [980680704, 4294705152], [981467136, 4294443008], [986710016, 4294963200], [986908416, 4294967168], [986910464, 4294967040], [986925056, 4294967040], [986927104, 4294967040], [986941696, 4294967232], [986942720, 4294967040], [986972160, 4294836224], [987103232, 4294901760], [987195904, 4294967040], [987332608, 4294934528], [987365376, 4294934528], [989242112, 4294967040], [989331456, 4294443008], [974192640, 4294901760], [974651392, 4294836224], [983171072, 4294836224], [985661440, 4293918720], [988807168, 4294836224]], "59": [[993001472, 4294836224], [993132544, 4294901760], [993394688, 4294901760], [993858816, 4294967040], [993886208, 4294959104], [994017280, 4294965248], [996868096, 4294901760], [996933632, 4294836224], [999751680, 4294934528], [1001357312, 4294963200], [1001382912, 4294966272], [991952896, 4293918720], [994050048, 4293918720]], "60": [[1017511936, 4294901760], [1017643008, 4294901760], [1019091968, 4294967040], [1019092736, 4294967040], [1019094528, 4294966784], [1019151072, 4294967280], [1019346944, 4294836224], [1020133376, 4294836224], [1020264448, 4294443008], [1020915430, 4294967295], [1020915566, 4294967295], [1020915712, 4294963200], [1022820352, 4294934528], [1006632960, 4292870144], [1010761728, 4294901760], [1019144192, 4294967040], [1019146496, 4294967040]], "61": [[1023693312, 4294966784], [1023719710, 4294967295], [1023720448, 4294967040], [1025343488, 4294934528], [1029160960, 4294950912], [1036538254, 4294967295], [1025245184, 4294963200], [1026555904, 4294443008], [1031798784, 4290772992], [1038614528, 4294705152], [1038876672, 4294836224], [1039138816, 4294705152]], "63": [[1062786229, 4294967295]], "64": [[1089052672, 4294959104], [1074913936, 4294967295], [1078430208, 4294967168], [1074003968, 4294950912]], "65": [[1094057984, 4294836224]], "66": [[1113980928, 4294963200], [1123631104, 4294959104], [1115767721, 4294967295], [1116056320, 4294967040], [1113515008, 4294967040], [1121601536, 4294967040]], "67": [[1136665520, 4294967295], [1138000721, 4294967295], [1138000743, 4294967295], [1138000744, 4294967294], [1138000746, 4294967295]], "69": [[1167290368, 4294967040]], "70": [[1176829952, 4294901760]], "72": [[1208926208, 4294950912]], "74": [[1249705984, 4294901760], [1244387495, 4294967295], [1244387496, 4294967295], [1244387572, 4294967294], [1244387575, 4294967295], [1244388096, 4294967040]], "203": [[3419414528, 4294959104], [3411228672, 4294965248], [3411410944, 4294959104], [3411427328, 4294959104], [3411550208, 4294959104], [3411591168, 4294959104], [3411750440, 4294967295], [3411769344, 4294965248], [3412000768, 4294965248], [3412352000, 4294966272], [3412377600, 4294963200], [3413579776, 4294965248], [3414303008, 4294967264], [3414618112, 4294966272], [3414619136, 4294967040], [3416060867, 4294967295], [3416060868, 4294967294], [3417276416, 4294959104], [3418071040, 4294959104], [3418619904, 4294966272], [3418620928, 4294967040], [3418621696, 4294967040], [3411087360, 4294963200], [3411533824, 4294959104], [3411869696, 4294901760], [3414196224, 4294959104], [3418357760, 4294959104], [3419357184, 4294950912], [3419373568, 4294934528], [3419406336, 4294959104], [3419668480, 4294963200], [3411330313, 4294967295], [3419529216, 4294959104]], "207": [[3475898368, 4294901760], [3477377753, 4294967295], [3477383168, 4294967040], [3477384427, 4294967295], [3477385728, 4294967168], [3477386176, 4294967264]], "209": [[3512041472, 4294934528], [3518971904, 4294950912]], "210": [[3524149248, 4294959104], [3524161536, 4294966784], [3524165376, 4294967040], [3528949760, 4294950912], [3535388672, 4294950912], [3523543040, 4294959104], [3524001792, 4294836224], [3524173824, 4294959104], [3524182016, 4294950912], [3524198400, 4294934528], [3524231168, 4294950912], [3524591616, 4294901760], [3524657152, 4294901760], [3524853760, 4294934528], [3524886528, 4294950912], [3524919296, 4294836224], [3525050368, 4294705152], [3525312512, 4293918720], [3526557696, 4294901760], [3526623232, 4294836224], [3527933952, 4294705152], [3528196096, 4294836224], [3528327168, 4294901760], [3528450048, 4294959104], [3528589312, 4294836224], [3535822848, 4294959104]], "211": [[3549741056, 4294959104], [3544186880, 4294443008], [3545235456, 4293918720], [3546284032, 4294443008], [3548905472, 4294443008], [3549429760, 4293918720], [3550478336, 4294443008]], "213": [[3586626560, 4294966784], [3586633216, 4294967168]], "216": [[3639549952, 4294959104]], "218": [[3664576512, 4294901760], [3673751552, 4294901760], [3657433088, 4292870144], [3661103104, 4294443008], [3661627392, 4292870144], [3663724544, 4294705152], [3664248832, 4294705152], [3664510976, 4294901760], [3670016000, 4293918720], [3673161728, 4294443008]], "219": [[3679584256, 4294901760], [3678928896, 4294901760], [3682598912, 4292870144], [3688366080, 4294443008], [3688890368, 4293918720], [3690070016, 4294836224], [3690201088, 4294705152]], "220": [[3698327552, 4294705152], [3701080064, 4294901760], [3706126336, 4294950912], [3706159104, 4294934528], [3706208256, 4294950912], [3706847232, 4294836224], [3701473280, 4292870144], [3703570432, 4293918720], [3706322944, 4294901760], [3707240448, 4294705152], [3707502592, 4294901760]], "221": [[3715760128, 4294836224], [3719299072, 4294443008], [3721728512, 4294967040], [3707764736, 4293918720], [3716284416, 4294836224], [3716743168, 4294901760], [3719036928, 4294705152], [3720347648, 4294443008], [3720871936, 4294705152], [3721134080, 4294836224], [3721396224, 4294705152], [3721658368, 4294901760], [3721789440, 4294836224], [3721920512, 4294443008], [3722444800, 4293918720]], "222": [[3732733952, 4294901760], [3732930560, 4294705152], [3740794880, 4294836224], [3725590528, 4293918720], [3726639104, 4292870144], [3728736256, 4292870144], [3733192704, 4294705152], [3733454848, 4294443008], [3735027712, 4294705152], [3735552000, 4294443008], [3736076288, 4293918720], [3737124864, 4293918720], [3738173440, 4294443008], [3738697728, 4294836224], [3738828800, 4294901760], [3739090944, 4294836224], [3740270592, 4294443008]], "223": [[3741450240, 4294836224], [3749707776, 4294836224]], "110": [[1849163776, 4294443008], [1850408960, 4294901760], [1850474496, 4294959104], [1850482688, 4294963200], [1851785216, 4292870144], [1856839680, 4294963200], [1856847872, 4294959104], [1856880640, 4294959104], [1857028096, 4294443008], [1857912832, 4294950912], [1858076672, 4292870144], [1849688064, 4294836224]], "111": [[1866711040, 4294963200], [1869742080, 4294836224], [1869873152, 4294836224], [1874460672, 4294836224], [1876772352, 4294966784]], "112": [[1883242496, 4294836224], [1883389952, 4294959104], [1883398144, 4294965248], [1884981248, 4294966272], [1884982272, 4294966784], [1884982784, 4294967040], [1885008896, 4294967040], [1885046016, 4294967040], [1885307192, 4294967288], [1885309568, 4294967168], [1885310080, 4294967168], [1885335552, 4294966272], [1886322688, 4294901760], [1887436800, 4294705152], [1887240192, 4294901760]], "113": [[1897398272, 4294705152], [1897857024, 4294934528], [1900019712, 4292870144], [1902116864, 4293918720], [1903165440, 4294443008], [1904017408, 4294901760], [1904082944, 4294901760], [1904279552, 4294901760], [1904738304, 4294963200], [1905131520, 4294901760], [1912078336, 4294705152], [1899364352, 4294836224]], "114": [[1917845504, 4294901760], [1919918080, 4294963200], [1919983616, 4294963200], [1920058368, 4294966272], [1920059392, 4294966272], [1920270336, 4294901760], [1927217152, 4294901760], [1927282688, 4294901760], [1927610368, 4294901760], [1928134656, 4294901760], [1928331264, 4293918720], [1926496256, 4294836224], [1926627328, 4294901760]], "115": [[1932263424, 4294836224], [1932525568, 4293918720], [1937510400, 4294966272], [1940520960, 4294836224], [1941241856, 4294901760], [1941307392, 4294901760], [1944983296, 4294967040], [1945942528, 4294966784], [1930952704, 4294705152], [1939472384, 4294836224], [1939603456, 4294836224], [1939734528, 4294901760]], "116": [[1946419200, 4294705152], [1947205632, 4293918720], [1950011392, 4294963200], [1950679040, 4294901760], [1950744576, 4294963200], [1951137792, 4294836224], [1958820018, 4294967295], [1959550976, 4294959104], [1959616512, 4294959104], [1960132608, 4294950912], [1960148992, 4294934528], [1960312832, 4294705152], [1960968192, 4294901760], [1961623552, 4294901760], [1962016768, 4294836224], [1962147840, 4294836224], [1962718976, 4294967040], [1962719232, 4294967040], [1962835968, 4294934528], [1947009024, 4294901760], [1949827072, 4294836224]], "117": [[1963458560, 4294443008], [1964435200, 4294967040], [1964615776, 4294967288], [1964849664, 4294967040], [1964965888, 4294901760], [1966420109, 4294967295], [1966420112, 4294967295], [1966866432, 4294901760], [1967652864, 4294836224], [1967849472, 4294901760], [1968144384, 4294959104], [1968439296, 4294836224], [1968793600, 4294966784], [1968832512, 4294901760], [1968963584, 4294901760], [1969487872, 4294836224], [1969688717, 4294967295], [1971060736, 4294705152], [1971322880, 4290772992]], "118": [[1984131072, 4294963200], [1985268736, 4294967040], [1986400256, 4294963200], [1987824128, 4294967040], [1987831808, 4294966272], [1987836416, 4294966784], [1987836928, 4294967040], [1987837952, 4294959104], [1988362240, 4294901760], [1989148672, 4294705152], [1992425472, 4294959104], [1992556544, 4294705152], [1993080832, 4294705152], [1994391552, 4294705152], [1995702272, 4294705152], [1992949760, 4294836224], [1994653696, 4294836224], [1994784768, 4294901760]], "119": [[1997144064, 4294967040], [1998879744, 4294967040], [1999034368, 4294965248], [2001457152, 4294963200], [2001600512, 4294836224], [2002878976, 4294967040], [2002880000, 4294967040], [2004353024, 4294443008], [2004877312, 4293918720], [2005925888, 4294705152], [2007072768, 4294966272], [2007076864, 4294963200], [2007101440, 4294965248], [2007493376, 4294967040], [2013069312, 4294901760], [2013134848, 4294836224], [1999298560, 4294959104]], "120": [[2015363072, 4294443008], [2015887360, 4294705152], [2021949440, 4294934528], [2021982208, 4294901760], [2022047744, 4294836224], [2026164736, 4294966784], [2026174976, 4294966784], [2026175744, 4294967040], [2026176000, 4294967040], [2019426304, 4294836224]], "121": [[2030305280, 4294836224], [2030567424, 4294443008], [2031091712, 4293918720], [2032140288, 4294705152], [2032403456, 4294966272], [2032404480, 4294965248], [2032406528, 4294965248], [2032467968, 4294934528], [2033504256, 4294963200], [2033844224, 4294934528], [2034499584, 4294705152], [2035253248, 4294950912], [2036711424, 4294950912], [2043088475, 4294967295], [2043215872, 4294901760], [2043412480, 4294705152], [2044723200, 4294963200], [2045247488, 4294901760], [2045378560, 4294901760], [2033188864, 4294836224], [2033491968, 4294959104], [2042626048, 4294705152], [2046296064, 4294705152], [2030047232, 4294963200]], "122": [[2047509504, 4294966272], [2047510528, 4294965248], [2047512576, 4294963200], [2047516672, 4294966272], [2047549440, 4294959104], [2051440640, 4294965248], [2051443200, 4294967040], [2053111808, 4294836224], [2055733248, 4294443008], [2057043968, 4294705152], [2059403264, 4294705152], [2059943936, 4294950912], [2061500416, 4294836224], [2061692928, 4294967040], [2061824640, 4294967168], [2061828096, 4294901760], [2060189696, 4294705152], [2061532672, 4294967040]], "123": [[2063859712, 4294705152], [2064121856, 4294443008], [2066849792, 4294967040], [2067439616, 4294959104], [2067857408, 4294901760], [2069364736, 4294836224], [2070144000, 4294967040], [2070151168, 4294959104], [2070257664, 4294959104], [2070265856, 4294950912], [2070364416, 4294967040], [2070364704, 4294967264], [2070375528, 4294967294], [2070937600, 4293918720], [2071986176, 4294443008], [2072641536, 4294836224], [2073034752, 4294705152], [2073296896, 4294901760], [2073481216, 4294965248], [2073483264, 4294966272], [2073485312, 4294959104], [2073537536, 4294966272], [2073538560, 4294963200], [2073559040, 4294443008], [2074869760, 4294705152], [2075426816, 4294967040], [2076442624, 4294836224], [2078932992, 4294966784], [2078933504, 4294967040]], "124": [[2081292288, 4294836224], [2081423360, 4294836224], [2082258944, 4294950912], [2082275328, 4294934528], [2083127296, 4294934528], [2084569088, 4294836224], [2084700160, 4294934528], [2084765696, 4294901760], [2084831232, 4294705152], [2085093376, 4294705152], [2085421056, 4294934528], [2086141952, 4294705152], [2087845888, 4294836224], [2088042496, 4294901760], [2088697856, 4294901760], [2088763392, 4294443008], [2090871296, 4294967040], [2090901504, 4294966784], [2090926080, 4294901760], [2090991616, 4294836224], [2091122688, 4294705152], [2091646976, 4294705152], [2092957696, 4294836224], [2093481984, 4294443008], [2095120384, 4294901760], [2095310336, 4294967040], [2095619840, 4294967040], [2095710208, 4294836224], [2096758784, 4294836224], [2083006720, 4294967040]], "125": [[2099249152, 4293918720], [2101347840, 4294967040], [2101350524, 4294967295], [2101350526, 4294967295], [2101772288, 4294934528], [2101936128, 4294901760], [2102190080, 4294959104], [2102198272, 4294901760], [2102263808, 4294836224], [2102394880, 4294443008], [2102919168, 4294901760], [2103066624, 4294966272], [2103177216, 4294966272], [2103178240, 4294966784], [2103180595, 4294967295], [2103443456, 4294836224], [2103574528, 4294901760], [2108358656, 4294901760], [2110783488, 4294963200], [2110980096, 4294901760], [2111307776, 4294443008]]};
//// FOR CERNET END
function inAutoProxy(url){
    D_SHASH = RULE_STATIC[0];
    D_SHARE = RULE_STATIC[1];
    P_SHASH = RULE_STATIC[2];
    P_SHARE = RULE_STATIC[3];
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
    if (inAutoProxy(url))
        return DIRECT;
    
    //// FOR CERNET
    if(isPlainHostName(host)) return DIRECT;
    var ip = dnsResolve(host);
    // no dns result
    if(!ip) return GAEPROXY;
    // ipv6
    if(shExpMatch(ip, '*:*')) return DIRECT;
    // local
    if(isInNet(ip,'127.0.0.0','255.0.0.0')) return DIRECT;
    else if(isInNet(ip,'10.0.0.0','255.0.0.0')) return DIRECT;
    else if(isInNet(ip,'192.168.0.0','255.255.0.0')) return DIRECT;
    else if(isInNet(ip,'172.16.0.0','255.240.0.0')) return DIRECT;
    else if(isInNet(ip,'169.254.0.0','255.255.0.0')) return DIRECT;
    var bytes = ip.split('.');
    if (bytes[0] in FreeIPs){
        var ipvalue = ((bytes[0] & 0xff) << 24) |((bytes[1] & 0xff) << 16) |
                     ((bytes[2] & 0xff) <<  8) |(bytes[3] & 0xff);
        for (var i in FreeIPs[bytes[0]]){
            if ((ipvalue&FreeIPs[bytes[0]][i][1])==(FreeIPs[bytes[0]][i][0]&FreeIPs[bytes[0]][i][1]))
                return DIRECT;
        }
    }
    return GAEPROXY;
    //// FOR CERNET END
    //// DISABLE FOR CERNET: return DIRECT;
}


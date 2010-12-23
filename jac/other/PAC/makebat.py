## Created by Randomwalk.
## Based on scripts from Lyricconch in Wallproxy.

import urllib2, json, re

PAC = '''
set GW=192.168.225.1

%s

'''

def _getIPTableForCERNET():
    URLs = (r'CERNET.txt', 
            #r'http://jacsvn.googlecode.com/svn/jac/other/PAC/CERNET.txt', 
            )
            # If other free lists are privided by your own school, replace URLs above with yours.
            # The format of your own list should be the same as that of the lists above. Or just modify the regex below.
    ips = []
    routes = ''
    
    print "Reading CERNET Free IP List...."
    for i in URLs:
        #o = urllib2.urlopen(i)
        o = file(i,'r')
        s = o.read()
        o.close()
        ips.extend(re.findall('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\s+[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\s+([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)',s))
    for i in ips:
        routes += 'route -p add ' + i[0] + ' mask ' + i[1] + ' %GW% METRIC 15\n'

    return routes


if __name__=="__main__":
    pac = PAC%(_getIPTableForCERNET())
    print "Writing to file 'proxy.conf'...."
    f = file('CERNET.bat','w')
    f.write(pac)
    f.close()
    print "Done!"
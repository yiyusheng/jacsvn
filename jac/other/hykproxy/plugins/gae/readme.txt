hyk-proxy 0.9.1  Read Me
Release 2010/06/16
http://hyk-proxy.googlecode.com 

This file is part of hyk-proxy.                                   
                                                                  
hyk-proxy is free software: you can redistribute it and/or modify 
it under the terms of the GNU General Public License as           
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.                   
                                                                  
hyk-proxy is distributed in the hope that it will be useful,      
but WITHOUT ANY WARRANTY; without even the implied warranty of    
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the     
GNU General Public License for more details.                      
                                                                  
You should have received a copy of the GNU General Public License 
along with hyk-proxy(client & server & plugin).  If not, see <http://www.gnu.org/licenses/>.

Dependencies
------------
1. You need to install JRE/JDK(1.6+).
2. You need to install Google App Engine SDK(Java) (use the latest version)
3. You may need intall seattle SDK if you want to use seattle platform

INSTALL:
GAE server part����GAE server���֣�
 1. unzip hyk-proxy-server-[version].zip
    ����Ŀ¼�½�ѹhyk-proxy-server-[version].zip
 2. cd hyk-proxy-server-[version] 
    �����ѹ��Ŀ¼
 3. modify war/WEB-INF/appengine-web.xml, change the element '<application>hyk-proxy-demo</application>'
    �޸�war/WEB-INF/appengine-web.xml�� ��'<application>'ֵ��Ϊ�Լ�������appid
 4. execute appcfg update (make sure you are in the directory 'hyk-proxy-server-[version]')
    ִ��appcfg.cmd/appcfg.sh update war�ϴ�

Seattle server part:
 1. Login seattle
 2. apply some resources
 3. run your application
    
Client part: ��Client���֣�
  1. unzip hyk-proxy-client-[version].zip
    ����Ŀ¼�½�ѹhyk-proxy-client-[version].zip
  2. cd hyk-proxy-client-[version] 
    �����ѹ��Ŀ¼
  3. modify etc/hyk-proxy-client.conf.xml, refer the comment for more information
    ����ע���޸�etc/hyk-proxy-client.conf.xml
  4. execute bin/start.bat(start.sh) to start the local server, execute bin/stop.bat to stop it
    ִ��bin/start.bat(start.sh)����local server��bin/stop.bat(stop.sh)ֹͣ

 

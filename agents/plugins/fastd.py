#!/usr/bin/env python3
import subprocess
import json
import os
import sys
import ipaddress
import re

def main():

    class Fastd(object):
        """
        Bindings for the fastd-status utility
        """
        def __init__(self, unix_sockpath=None, int=False):
            self.unix_sockpath = unix_sockpath
            self.int = int
            if self.unix_sockpath is not None and not os.path.exists(self.unix_sockp
ath):
                raise RuntimeError('fastd: invalid unix socket path given')

        def _fetch(self, section):
            cmd = ['/usr/local/bin/fastd-status', self.unix_sockpath]

            output = subprocess.check_output(cmd)

            if int:
              return json.loads(output.decode("utf-8"))[section]
            else:
              return json.loads(output.decode("utf-8"))[section].values()


        def peers(self):
            return self._fetch('peers')

        def statistics(self):
            return self._fetch('statistics')

        def uptime(self, int=True):
            return self._fetch('uptime')

    def count_online_peers(peers):
        count = 0

        for peer, value in peers.items():
            if value['connection']:
                count += 1

        return count

    def is_valid_ipv4_address(ipv4):
        try:
            iparray = re.findall(r'[0-9]+(?:\.[0-9]+){3}', ipv4)
            ipstring = ""
            for i in iparray:
                ipstring = ipstring + i
            ip = ipaddress.ip_address(ipstring)
        except ValueError:
            return False
        except IndexError:
            return False
        return True

    def is_valid_ipv6_address(ipv6):
        try:
            iparray = re.findall(r'(?:(?:[0-9A-Fa-f]{1,4}:){6}(?:[0-9A-Fa-f]{1,4}:[0
-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|
[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|::(?:[0-9A-Fa-f]{1,4}:){5}(?:[0-9A-Fa-f]{
1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[
0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f
]{1,4}:){4}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0
-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{22[0-4][0-9]|25[0-5]))|(?:[0-9A-F
a-f]{1,4}:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){3}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f
]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-
9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,2}[0-9A-Fa-{1,4})?::(?:
[0-9A-Fa-f]{1,4}:){2}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0
-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])
)|(?:(?:[0-9A-Fa-f]{1,4}:){,3}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}:(?:[0-9A-Fa-f]{1,
4}:[0-9Aa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-
9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:){,4}[0-9A-Fa-f
]{1,4})?::(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-
4][0-9]|25[0-5])\\.){3}(?:[0]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A
-Fa-f]{1,4}:){,5}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}|(?:(?:[0-9A-Fa-f]{1,4}:){,6}[0
-9A-Fa-f]{1,4})?::)', ipv6)
            ipstring = ""
            for i in iparray:
                ipstring = ipstring + i
            ip = ipaddress.ip_address(ipstring)
        except ValueError:
            return False
        return True

    def count_ip_address(peers, ipversion):
        v4count = 0
        v6count = 0

        for peer, value in peers.items():
            if value['connection']:
                ip = str(value['address'])
                if is_valid_ipv4_address(ip):
                    v4count += 1
                elif is_valid_ipv6_address(ip):
                    v6count += 1

        if ipversion == "4":
            return v4count
        elif ipversion == "6":
            return v6count

    def get_fastd_infos(socket, name):
        fastd_instance = Fastd(socket)
        fastd_db = {
            'peers': fastd_instance.peers(),
            'statistics': fastd_instance.statistics(),
            'uptime': fastd_instance.uptime()
        }

        fastd_peers = fastd_db['peers']
        fastd_stats = fastd_db['statistics']
        fastd_uptime = fastd_db['uptime']

        peer_count_all = len((fastd_peers).items())
        v4_peers = count_ip_address(fastd_peers, "4")
        v6_peers = count_ip_address(fastd_peers, "6")

        print(name + ' peers_all ' + str(peer_count_all))
        print(name + ' peers_online ' + str(count_online_peers(fastd_peers)))
        print(name + ' peers_ipv4 ' + str(v4_peers))
        print(name + ' peers_ipv6 ' + str(v6_peers))
        print(name + ' uptime ' + str(fastd_uptime))
        print(name + ' tx_bytes ' + str(fastd_stats['tx']['bytes']))
        print(name + ' tx_packets ' + str(fastd_stats['tx']['packets']))
        print(name + ' tx_error_bytes ' + str(fastd_stats['tx_error']['bytes']))
        print(name + ' tx_error_packets ' + str(fastd_stats['tx_error']['packets']))
        print(name + ' tx_dropped_bytes ' + str(fastd_stats['tx_dropped']['bytes']))
        print(name + ' tx_dropped_packets ' + str(fastd_stats['tx_dropped']['packets']))
        print(name + ' rx_bytes ' + str(fastd_stats['rx']['bytes']))
        print(name + ' rx_packets ' + str(fastd_stats['rx']['packets']))

    sockets = [
        {
            'name'   : 'mainz',
            'socket' : '/var/run/fastd-mz.status',
        },
        {
            'name'   : 'wiesbaden',
            'socket' : '/var/run/fastd-wi.status',
        },
    ]

    print('<<<fastd>>>')
    for socket in sockets:
        get_fastd_infos(socket['socket'], socket['name'])


if __name__ == '__main__':
    main()

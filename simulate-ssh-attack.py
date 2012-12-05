#!/usr/bin/python
'''Script generating random SSH failures.'''
import os
import sys
from attack import basic_options, anomaly, syslog_printer
from random import randint

ATTACKED_USERS = '''apache oracle root mysql postgres nagios icinga nginx
admin administrator me myself ego 98ypo8hm ityfbyt
hgvmjgf'''.split()

def parse_opts():
    '''Parses the command line'''
    parser = basic_options()
    parser.add_option("-s", "--source-ips", "--attackers",
                      dest="attackers", help="IPs to inject in the 'attack'")
    return parser.parse_args()

if __name__ == '__main__':
    (options, args) = parse_opts()

    @anomaly(options.begin, options.end, options.rate, options.nodes)
    @syslog_printer
    def ssh_attacker(ips):
        pid = randint(2, 65536)
        ip = ips[randint(0, len(ips)-1)]
        port = randint(0, 65536)
        user = ATTACKED_USERS[randint(0, len(ATTACKED_USERS)-1)]
        return "sshd[%(pid)d]: Failed password for %(user)s from %(ip)s port %(port)d ssh2" % {
            "pid" : pid, "ip" : ip, "port" : port, "user" : user }

    ssh_attacker(options.attackers.split(","))

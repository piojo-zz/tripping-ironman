#!/usr/bin/python
#!/usr/bin/python
'''Script generating lots of messages for some stupid programs'''
import os
import sys
from attack import basic_options, anomaly, syslog_printer
from random import randint

BERSERKER_MESSAGES = [
    "bwctl[%d] 2012-12-04T20:51:47.123971+01:00 master9 bwctld[28455]: FILE=time.c, LINE=180, NTP: STA_NANO should be set. Make sure ntpd is running, and your NTP configuration is good",
    "powmaster.pl[%d]: Unable to contact Home(magikarp.cubone.gent.vsc):Can't locate IO/Select.pm:   Too many open files at /usr/lib64/perl5/IO/Socket.pm line 116.#012#012" ]

def parse_opts():
    '''Parses the command line'''
    parser = basic_options()
    return parser.parse_args()

if __name__ == '__main__':
    (options, args) = parse_opts()

    @anomaly(options.begin, options.end, options.rate, options.nodes)
    @syslog_printer
    def perfsonar_errors():
        '''Perfsonar errors are funny.  They insert a lot of shit into
        the logs, with two possible messages, one of them much more
        frequent than the other.'''
        pid = randint(2, 65536)
        program = randint(0,5)
        if program != 0:
            program = 1
        return BERSERKER_MESSAGES[program] % pid

    perfsonar_errors()

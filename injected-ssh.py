#!/usr/bin/python
#!/usr/bin/python
'''Script generating lots of messages for some stupid programs'''
import os
import sys
from attack import basic_options, anomaly, syslog_printer, message_burst
from random import randint

TROUBLESOME_MESSAGES = [ 'sshd[%d]: error: Bind to port 22 on 0.0.0.0 failed: Address already in use.',
                        'sshd[%d]: error: Bind to port 22 on :: failed: Address already in use.',
                        'sshd[%d]: fatal: Cannot bind any address.' ]

def parse_opts():
    '''Parses the command line'''
    parser = basic_options()
    return parser.parse_args()


if __name__ == '__main__':
    (options, args) = parse_opts()


    @anomaly(options.begin, options.end, options.rate, options.nodes)
    @message_burst(len(TROUBLESOME_MESSAGES))
    @syslog_printer
    def generate_ssh_errors(iteration, pid):
        return TROUBLESOME_MESSAGES[iteration] % pid


    generate_ssh_errors()

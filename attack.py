#!/usr/bin/python
'''Basic library for all the repository.

Generates the common command line options and decorates the anomalous
message.
'''

import os
import sys
from optparse import OptionParser
from random import randint
import time
from datetime import datetime

def basic_options():
    '''Return an option parser with the basic parameters: begin of the
    anomaly, , end of the anomaly, hosts involved and rate.'''
    parser = OptionParser()
    parser.add_option("-r", "--rate", dest="rate",
                      help="Anomalous message rate, in messages per minute")
    parser.add_option("-b", "--begin", dest="begin",
                      help="Begin of the anomaly")
    parser.add_option("-e", "--end", dest="end", help="End of the anomaly")
    parser.add_option("-n", "--nodes", dest="nodes",
                      help="Nodes involved in the anomaly")
    return parser

class anomaly(object):
    '''Decorator for an anomaly generator. Takes as arguments the
    begin and the end of the anomaly, the rate of messages it produces
    and the hosts involved in it.  It assumes the anomaly is uniformly
    distributed among all hosts'''

    def __init__(self, begin, end, rate, hosts):
        '''Trivial class constructor'''
        dt = datetime.strptime(begin, "%Y/%m/%d-%H:%M:%S")
        self.begin = time.mktime(dt.timetuple())
        dt = datetime.strptime(end, "%Y/%m/%d-%H:%M:%S")
        self.end = time.mktime(dt.timetuple())
        self.rate = 60.0/int(rate)
        self.hosts = hosts.split(",")
        self.now = self.begin
        self.nhosts = len(self.hosts)-1

    def __call__(self, f):
        '''Wrapper function for the decorator'''
        def wrapped_f(*args, **kwargs):
            while self.now <= self.end:
                if randint(0,1) == 1:
                    host = randint(0, self.nhosts)
                    f(self.now, self.hosts[host], *args, **kwargs)
                self.now += self.rate
        return wrapped_f

def syslog_printer(f):
    '''Decorator. Prints the string returned by the decorated function
    as if it were a Syslog entry, with an rsyslog-like timestamp and a
    host name. The program/tag field is part of the return of the
    decorated function.'''
    def wrapped_f(timestamp, host, *args, **kwargs):
        date=time.strftime("%Y-%m-%dT%H:%M:%S.00000+01:00", time.localtime(timestamp))
        print "%s %s %s" % (date, host, f(*args, **kwargs))
    return wrapped_f

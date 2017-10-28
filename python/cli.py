#!/usr/bin/env python2.7

"""
Boilerplate for a python CLI
"""

import sys
import logging
import argparse
import Queue
import threading

DEFAULTS = dict(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] - %(message)s',
    log='cli.log'
)

def get_logger():
    """Wrapper for logger creation"""
    logger = logging.getLogger('cli')
    logger.setLevel(DEFAULTS['level'])

    formatter = logging.Formatter(DEFAULTS['format'])
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_args(argv, logger):
    """Wrapper for argument parsing"""
    parser = argparse.ArgumentParser(description='CLI Boilerplate')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')
    parser.add_argument('-q', '--quiet', action='store_true', help='Suppress informational logging')
    parser.add_argument('-l', '--log', nargs='?', const=DEFAULTS['log'],
                        help='Output logs to the specified file or to "%s" if none specified' %
                        DEFAULTS['log'])
    args = parser.parse_args(argv)

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    if args.quiet:
        logger.setLevel(logging.WARN)

    if args.log:
        formatter = logging.Formatter(DEFAULTS['format'])
        file_handler = logging.FileHandler(args.log)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return args


class CLI(object):
    """
    A CLI that handles input in a separate thread
    """

    def __init__(self, args, logger):
        self.args = args
        self.logger = logger

        self.event = threading.Event()
        self.queue = Queue.Queue()
        self.thread = threading.Thread(target=self.process, args=())

    def start(self):
        """Start collecting user input"""

        self.thread.start()

        while True:
            try:
                cmd = raw_input()
                self.queue.put(cmd)
            except KeyboardInterrupt:
                self.logger.info('Stopping on CTRL-C')
                self.event.set()
                break

    def process(self):
        """Collect and enqueue user input"""
        while not self.event.is_set():
            try:
                cmd = self.queue.get(timeout=0.1)
                if cmd:
                    self.logger.info('received "%s"', cmd)
            except Queue.Empty:
                pass


def main():
    """Execution"""
    logger = get_logger()
    args = get_args(sys.argv[1:], logger)
    cli = CLI(args, logger)
    cli.start()


if __name__ == '__main__':
    main()

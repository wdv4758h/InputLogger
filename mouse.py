#!/usr/bin/env python3

# Modify from PyUserInput/examples/mouse.py

import daemon                               # python-daemon
from pymouse import PyMouse, PyMouseEvent   # PyUserInput (need python3-xlib for X11)

import logging
import sys
from socket import gethostname
from signal import signal, SIGINT


class MouseLoggingEvent(PyMouseEvent):
    def __init__(self):
        super().__init__()
        FORMAT = '%(asctime)-15s ' + gethostname() + ' touchlogger %(levelname)s %(message)s'
        logging.basicConfig(filename='/var/log/mouse.log', level=logging.DEBUG, format=FORMAT)

    def move(self, x, y):
        logging.info('{{ "event": "move", "x": {}, "y": {} }}'.format(x, y))

    def click(self, x, y, button, press):
        if press:
            logging.info('{{ "event": "click", "type": "press", "x": {}, "y": {} }}'.format(x, y))
        else:
            logging.info('{{ "event": "click", "type": "release", "x": {}, "y": {} }}'.format(x, y))


def main():

    with daemon.DaemonContext():

        ########################################
        # Setting Signal Handler For SIGINT
        ########################################

        def stop(signum, frame):
            cleanup_stop_thread()
            sys.exit()

        signal(SIGINT, stop)

        ########################################

        try:
            e = MouseLoggingEvent()
            e.capture = False
            e.daemon = False
            e.start()
        except ImportError:
            logging.info('{ "event": "exception", "type": "ImportError", "value": "Mouse events unsupported" }')
            sys.exit()

        ########################################
        # Logging Screen Size
        ########################################

        m = PyMouse()

        try:
            size = m.screen_size()
            logging.info('{{ "event": "start", "type": "size", "value": {} }}'.format(size))
        except:
            logging.info('{ "event": "exception", "type": "size", "value": "undetermined problem" }')
            sys.exit()

        ########################################

        try:
            e.join()
        except KeyboardInterrupt:
            e.stop()
            sys.exit()


if __name__ == '__main__':
    main()

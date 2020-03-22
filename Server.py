import logging
import os
import subprocess
from datetime import datetime, timedelta
from threading import Thread
from time import sleep


class Server:
    def __init__(self):
        self._executable = "nogui.cmd"

    def initial_start(self):
        self._start()
        thread = Thread(target=self._threaded_sleep)
        thread.start()
        self._initCommandLine()

    def _command(self, cmd):
        logging.info('Writing server command')
        self._process.stdin.write(str.encode('%s\n' % cmd))
        self._process.stdin.flush()

    def _initCommandLine(self):
        while True:
            command = input("$ ")
            if command == "backup":
                self._backup()
            else:
                self._command(command)

    def _start(self):
        logging.info('Starting server')
        self._process = subprocess.Popen(self._executable, stdin=subprocess.PIPE)
        logging.info("Server started.")

    def _stop_backup(self):
        logging.info('Stopping server')
        self._command(
            "say Server will close in 1 minute for backup, it will be back online in 1 minute.")
        sleep(30)
        self._command(
            "say Server will close in 30 seconds for backup, it will be back online in 1 minute.")
        sleep(20)
        for i in range(10, 0, -1):
            self._command(
                "say Server will close in " + str(i) + " seconds for backup, it will be back online in 1 minute.")
            sleep(1)
        self._command("stop")
        logging.info('Server stopped')

    def _backup(self):
        server._stop_backup()
        sleep(10)
        os.system("7z a -tzip backup/" +
                  str(datetime.now().strftime('%Y-%m-%d-%H-%M-%S')) + ".zip Chamantopia")
        sleep(5)
        server._start()

    def _threaded_sleep(self):
        while True:
            now = datetime.now()
            # to = now + timedelta(seconds=1)
            to = now + timedelta(days=1)
            to = to.strftime("%Y-%m-%d") + "-7-0-0"
            to = datetime.strptime(to, '%Y-%m-%d-%H-%M-%S')
            print("I will now sleep until " + str(to))
            sleep((to - now).seconds)
            server._backup()


server = Server()
server.initial_start()

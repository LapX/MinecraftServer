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

        sleep_thread = Thread(target=self._threaded_sleep)
        sleep_thread.start()

        player_command_thread = Thread(target=self._threaded_player_command)
        player_command_thread.start()

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
            elif command == "restart":
                self._restart()
            else:
                self._command(command)

    def _start(self):
        logging.info('Starting server')
        self._process = subprocess.Popen(self._executable, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
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

    def _stop(self):
        logging.info('Stopping server')
        self._command(
            "say Server will close in 1 minute, it will be back online in 30 seconds.")
        sleep(30)
        self._command(
            "say Server will close in 30 seconds, it will be back online in 30 seconds.")
        sleep(20)
        for i in range(10, 0, -1):
            self._command(
                "say Server will close in " + str(i) + " seconds, it will be back online in 30 seconds.")
            sleep(1)
        self._command("stop")
        logging.info('Server stopped')

    def _backup(self):
        self._stop_backup()
        sleep(10)
        os.system("7z a -tzip E:/BackupMinecraft/" +
                  str(datetime.now().strftime('%Y-%m-%d-%H-%M-%S')) + ".zip ChamanWorld")
        sleep(5)
        self._start()

    def _restart(self):
        self._stop()
        sleep(5)
        self._start()

    def _threaded_sleep(self):
        while True:
            now = datetime.now()
            to = now + timedelta(days=1)
            to = to.strftime("%Y-%m-%d") + "-7-0-0"
            to = datetime.strptime(to, '%Y-%m-%d-%H-%M-%S')
            print("I will now sleep until " + str(to))
            sleep((to - now).seconds)
            self._backup()

    def _threaded_player_command(self):
        for line in iter(self._process.stdout.readline, ""):
            message = str(line).replace("b'", '')

            if "!day" in message:
                self._command("time set day")
            elif "!midnight" in message:
                self._command("time set midnight")
            elif "!night" in message:
                self._command("time set night")
            elif "!noon" in message:
                self._command("time set noon")
            elif "!help" in message:
                self._command(
                    "say Put a ! followed by your command to set the time. Either day, midnight, night or noon")

            print(message)


server = Server()
server.initial_start()

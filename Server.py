import logging
import os
import subprocess
from datetime import datetime, timedelta
from time import sleep


class Server:
    def __init__(self):
        self.executable = "nogui.cmd"

    def command(self, cmd):
        logging.info('Writing server command')
        self.process.stdin.write(str.encode('%s\n' % cmd))
        self.process.stdin.flush()

    def start(self):
        logging.info('Starting server')
        self.process = subprocess.Popen(self.executable, stdin=subprocess.PIPE)
        logging.info("Server started.")

    def stop(self):
        logging.info('Stopping server')
        self.command(
            "say Server will close in 1 minute for backup, it will be back online in 1 minute.")
        sleep(30)
        self.command(
            "say Server will close in 30 seconds for backup, it will be back online in 1 minute.")
        sleep(20)
        for i in range(10, 0, -1):
            self.command(
                "say Server will close in " + str(i) + " seconds for backup, it will be back online in 1 minute.")
            sleep(1)
        self.command("stop")
        logging.info('Server stopped')

    def backup(self):
        server.stop()
        sleep(10)
        os.system("7z a -tzip backup/" +
                  str(datetime.now().strftime('%Y-%m-%d-%H-%M-%S')) + ".zip Chamantopia")
        sleep(5)
        server.start()


server = Server()
server.start()
while True:
    now = datetime.now()
    to = now + timedelta(days=1)
    to = to.strftime("%Y-%m-%d") + "-7-0-0"
    to = datetime.strptime(to, '%Y-%m-%d-%H-%M-%S')
    print("I will now sleep until " + str(to))
    sleep((to - now).seconds)
    server.backup()

from typing import List
import threading
import time
import subprocess
import shlex
import logging


class ClientThread(threading.Thread):
    """
    Thread representing a client
    """

    def __init__(self, commands: List[str], time_step_len_seconds: float) -> None:
        """
        Initializes the client thread

        :param commands: the sequence of commands that the client will execute
        :param time_step_len_seconds: the length of a time-step in seconds
        """
        threading.Thread.__init__(self)
        self.commands = commands
        self.time_step_len_seconds = time_step_len_seconds

    def run(self) -> None:
        """
        The main function of the client. It executes a sequence of commands and then terminates

        :return: None
        """
        for cmd in self.commands:
            args = shlex.split(cmd)
            try:
                p = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False)
                p.communicate(timeout=10)
                p.wait(timeout=10)
            except subprocess.TimeoutExpired:
                logging.warning(f"[Client] command {cmd} timed out. Killing process.")
                p.kill()
                p.communicate()
            except Exception as e:
                logging.error(f"[Client] Error executing command {cmd}: {e}")
            time.sleep(self.time_step_len_seconds)

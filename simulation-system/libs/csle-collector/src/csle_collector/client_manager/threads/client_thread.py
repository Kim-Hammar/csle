from typing import List
import threading
import time
import subprocess
import os
import signal
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
            try:
                p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True,
                                     start_new_session=True)
                p.communicate(timeout=15)
            except subprocess.TimeoutExpired:
                logging.warning(f"[Client] command {cmd} timed out. Killing process group.")
                try:
                    os.killpg(os.getpgid(p.pid), signal.SIGKILL)
                    p.communicate()  # Clean up resources
                except Exception as kill_err:
                    logging.error(f"Failed to kill process group: {kill_err}")

            except Exception as e:
                logging.error(f"[Client] Error executing command {cmd}: {e}")
            time.sleep(self.time_step_len_seconds)

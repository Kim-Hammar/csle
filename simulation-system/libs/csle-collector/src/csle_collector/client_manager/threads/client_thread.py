from typing import List
import threading
import time
import subprocess
import os
import signal
import random


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
        self.daemon = True

    def run(self) -> None:
        """
        The main function of the client. It executes a sequence of commands and then terminates

        :return: None
        """
        time.sleep(random.uniform(0, 2.0))
        for cmd in self.commands:
            p = None
            try:
                p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                     shell=True, start_new_session=True)
                p.communicate(timeout=15)

            except subprocess.TimeoutExpired:
                if p:
                    try:
                        os.killpg(os.getpgid(p.pid), signal.SIGKILL)
                    except (ProcessLookupError, OSError):
                        pass
            except Exception:
                if p:
                    try:
                        os.killpg(os.getpgid(p.pid), signal.SIGKILL)
                    except:
                        pass
            finally:
                if p:
                    try:
                        p.wait(timeout=1)
                    except:
                        try:
                            os.killpg(os.getpgid(p.pid), signal.SIGKILL)
                            p.wait()
                        except:
                            pass
            jitter = random.uniform(0, 1.0)
            time.sleep(self.time_step_len_seconds + jitter)

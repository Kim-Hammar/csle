from typing import List, Optional, Any
import threading
import time
import subprocess
import random
import os
import signal


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
        # Jitter start time to desynchronize threads immediately upon creation
        time.sleep(random.uniform(0, 5.0))

        for cmd in self.commands:
            # Small random delay to prevent threads hitting the OS process table lock simultaneously.
            time.sleep(random.uniform(0, 0.5))

            p = None
            try:
                p = subprocess.Popen(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    shell=True,
                    start_new_session=True
                )
                p.communicate(timeout=15)

            except subprocess.TimeoutExpired:
                self._kill_and_reap(p)

            except Exception:
                self._kill_and_reap(p)

            finally:
                if p and p.poll() is None:
                    self._kill_and_reap(p)

            # Add jitter o keep threads desynchronized
            jitter = random.uniform(0, 1.0)
            time.sleep(self.time_step_len_seconds + jitter)

    def _kill_and_reap(self, p: Optional[subprocess.Popen[Any]]) -> None:
        """
        Robustly kills a process group and waits for it, avoiding infinite hangs.

        :param p: the process group to kill
        :return: None
        """
        if p is None:
            return
        try:
            if p.poll() is None:
                os.killpg(os.getpgid(p.pid), signal.SIGKILL)
        except (ProcessLookupError, OSError):
            pass
        try:
            p.wait(timeout=1.0)
        except subprocess.TimeoutExpired:
            pass

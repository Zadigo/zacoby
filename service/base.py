import errno
import os
import platform
import socket
import time
from subprocess import PIPE, Popen
from urllib.parse import urljoin

import requests
from zacoby.logging.logger import default_logger


class Service:
    """
    Starts a new service using the provided
    executable web driver

    Parameters
    ----------

        - executable (exe): path to the browser executable to run
          e.g. msedgedriver.exe

        - host (str): the host on which to start the service

        - port (int): the port on which to bind the service
    """
    def __init__(self, executable, host, port, environ=None):
        self.executable = executable
        self.process = None
        self.host = host
        self.port = port
        self.logging = default_logger(self.__class__.__name__)

        if environ is None:
            environ = os.environ

        self.environ = environ

    def __del__(self):
        try:
            self.stop()
        except Exception:
            pass

    @property
    def browser_url(self):
        return f"http://{self.join_host_port('localhost', self.port)}"

    @staticmethod
    def _can_still_connect(port, host='localhost'):
        s = None
        state = False
        try:
            s = socket.create_connection((host, port), 1)
            state = True
        except socket.error:
            state = False
        else:
            if s:
                s.close()
        default_logger('Service').info(f'The port is up and running ({port})')
        return state

    def _process_is_running(self):
        code = self.process.poll()
        print(code)
        if code is not None:
            raise Exception('The service was exited')

    def _check_connection_state(self):
        can_connect = False
        for _ in range(30):
            can_connect = self._can_still_connect(self.port)
            if not can_connect:
                break
            time.sleep(1)
        return can_connect

    def shutdown_remote_connection(self):
        try:
            requests.get(urljoin(self.browser_url, '/shutdown'))
        except:
            return False
        else:
            return True

    def start(self, host=None):
        """Start a new service"""
        log_file = open(os.devnull, 'rb')
        cmd = [self.executable, f'--port={self.port}']

        if host is not None:
            cmd.extend([f'--host={host}'])

        try:
            self.process = Popen(
                cmd, env=self.environ, 
                    close_fds=True if platform.system() != 'Windows' else False, 
                        stdout=log_file, stderr=log_file, stdin=PIPE
            )
        except TypeError:
            raise
        except OSError as e:
            if e.errno == errno.ENOENT:
                raise Exception('The executable could not be accessed')
            elif e.errno == errno.EACCES:
                raise Exception('Does the executable have the appropritate access rights?')
            else:
                raise
        except Exception:
            raise

        self.logging.info(f'Service started')

        count = 0

        while True:
            self._process_is_running()
            if self._can_still_connect(self.port):
                break
            count += 1
            time.sleep(1)
            if count == 5:
                raise Exception('Could not create a Service instance because the process failed')

    def stop(self):
        """Stop the current service"""
        self.shutdown_remote_connection()
        self.logging.info('Service stopped')
        streams = [
            self.process.stderr,
            self.process.stdin,
            self.process.stdout
        ]
        try:
            if self.process:
                try:
                    for stream in streams:
                        if stream is not None:
                            stream.close()
                except Exception:
                    raise
                else:
                    self.process.terminate()
                    self.process.wait()
                    self.process.kill()
                    self.process = None
        except OSError:
            return False
        else:
            self.logging.info('Process stopped')
            return True

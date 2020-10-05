import errno
import os
import platform
import socket
import time
from subprocess import PIPE, Popen
from urllib.parse import urljoin

import requests


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
    def _can_still_connect(self, port, host='localhost'):
        s = None
        try:
            s = socket.create_connection((host, port), 1)
        except socket.error:
            return False
        else:
            if s:
                s.close()
                return False

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

    def start(self):
        """Start a new service"""
        print('The service was started')
        cmd = [self.executable, f'--port={self.port}']
        try:
            self.process = Popen(
                cmd, env=self.environ, 
                    close_fds=platform.system(), 
                        stdout=None, stderr=None, stdin=PIPE
            )
        except TypeError:
            raise
        except OSError as e:
            if e.errno == errno.ENOENT:
                pass
            elif e.errno == errno.EACCES:
                pass
            else:
                raise
        except Exception:
            raise

        while True:
            print('Service is running')
            time.sleep(1)

    def stop(self):
        """Stop the current service"""
        print('The service was stopped')
        self.shutdown_remote_connection()
        streams = [
            self.process.stderr,
            self.process.stdin,
            self.process.stdout
        ]
        try:
            if self.process:
                try:
                    for stream in streams:
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
            return True

    def _join_host_port(self, host, port):
        return f'{host}:{port}'

import errno
import os
import socket
import platform
from subprocess import PIPE, Popen
from zacoby.logger import create_default_logger
from zacoby import exceptions
from zacoby.signals import signal


class Service:
    def __init__(self, executable_or_dir, host, port, filename=None, environ=None):
        self.logger = create_default_logger(self.__class__.__name__)
        if not os.path.exists(executable_or_dir):
            raise FileNotFoundError(f"Could not find the driver on path {executable_or_dir}")

        if os.path.isdir(executable_or_dir):
            base, _, files = list(os.walk(executable_or_dir))[0]
            if filename is None:
                executable_or_dir = os.path.join(base, files[-1])
            else:
                filtered_file = list(filter(lambda x: filename in x, files))
                if not filtered_file:
                    raise FileNotFoundError(f"Could not find the driver in directory: {executable_or_dir}")
                executable_or_dir = os.path.join(base, filtered_file[-1])
            
        if not os.access(executable_or_dir, os.X_OK):
            raise Exception('The file you provided is not executable')
        
        self.executable = executable_or_dir
        self.host = host
        self.port = port
        self.environ = environ or os.environ
        self.process = None
        self.logger.info('Service started...')

    # def __call__(self, sender, signal, name=None, **kwargs):
    #     print('The browser was opened at:', sender.host, sender.port)
    #     if name == 'start':
    #         if self.host is None:
    #             self.host = sender.host
    #         self.start()

    #     if name == 'stop':
    #         return self.stop()

    # NOTE: Cuts off the service before
    # doing anything like get requests
    # def __del__(self):
    #     self.stop()
    #     self.logger.info('Service terminated')

    def _poll_process_is_running(self):
        code = self.process.poll()
        if code is not None:
            raise Exception('The service was exited')
        print(code)

    def _can_sill_connect(self, host='localhost'):
        try:
            s = socket.create_connection((host, self.port), 1)
            state = True
        except socket.error:  
            state = False
        else:
            if s:
                s.close()
        finally:
            print(state)
            return state

    def start(self, host=None):
        host = host or self.host

        cmd = [self.executable, f'--port={self.port}']
        if self.host is not None:
            cmd.extend([f"--host={host}"])
 
        close_fds = True if platform.system() else False
        log_file = open(os.devnull, 'rb')

        try:
            process = Popen(
                cmd, env=self.environ,
                    close_fds=close_fds,
                        stdout=log_file, stderr=log_file, stdin=PIPE
            )
        except TypeError:
            raise
        except OSError as e:
            if e.errno == errno.ENOENT:
                raise Exception('The executable could not be accessed')
            if e.errno == errno.EACCES:
                raise Exception(
                    'Does the executable have the appropritate access rights?')
            raise exceptions.ServiceError()
        except Exception:
            raise exceptions.ServiceError()
        else:
            self.process = process

        count = 0

        while True:
            self._poll_process_is_running()
            if self._can_sill_connect():
                break
            count += 1
            if count == 5:
                raise Exception('Could not create a new service instance because the process broke')

    def stop(self):
        if self.process is not None:
            streams = [
                self.process.stderr,
                self.process.stdin,
                self.process.stdout
            ]

            for stream in streams:
                if stream is not None:
                    try:
                        try:
                            stream.close()
                        except Exception as e:
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

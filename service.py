import errno
import os
import platform
import socket
from subprocess import PIPE, Popen

from pydispatch import dispatcher

from zacoby import exceptions, global_logger


class Service:
    """
    Class that creates a new service by running the
    the executable.
    """
    def __init__(self, executable_or_dir, host: str, 
                 port: int, filename: str=None, environ: dict=None):
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
        # signal.send(signal=dispatcher.Any, sender=self)
        global_logger.info('Service configured...')

    # NOTE: Cuts off the service before
    # doing anything like get requests
    def __del__(self):
        print('Service terminated')
        # self.stop()
        # logger.info('Service terminated')

    def _poll_process_is_running(self):
        code = self.process.poll()
        if code is not None:
            raise Exception('The service was exited')

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
            return state

    def start(self, host=None, debug_mode=False):
        print('Started service')
        # host = host or self.host

        # cmd = [self.executable, f'--port={self.port}']
        # if self.host is not None:
        #     cmd.extend([f"--host={host}"])
 
        # close_fds = True if platform.system() else False
        # log_file = open(os.devnull, 'rb')

        # if not debug_mode:
        #     try:
        #         process = Popen(
        #             cmd, env=self.environ,
        #                 close_fds=close_fds,
        #                     stdout=log_file, stderr=log_file, stdin=PIPE
        #         )
        #     except TypeError:
        #         raise
        #     except OSError as e:
        #         if e.errno == errno.ENOENT:
        #             raise Exception('The executable could not be accessed')
        #         if e.errno == errno.EACCES:
        #             raise Exception(
        #                 'Does the executable have the appropritate access rights?')
        #         raise exceptions.ServiceError()
        #     except Exception:
        #         raise exceptions.ServiceError()
        #     else:
        #         self.process = process

        #     count = 0

        #     while True:
        #         self._poll_process_is_running()
        #         if self._can_sill_connect():
        #             break
        #         count += 1
        #         if count == 5:
        #             raise Exception('Could not create a new service instance because the process broke')
        # else:
        #     global_logger.warn('You are running the spider in DEBUG mode')

    def stop(self):
        print('Stopped service')
        # if self.process is not None:
        #     streams = [
        #         self.process.stderr,
        #         self.process.stdin,
        #         self.process.stdout
        #     ]

        #     for stream in streams:
        #         if stream is not None:
        #             try:
        #                 try:
        #                     stream.close()
        #                 except Exception as e:
        #                     raise
        #                 else:
        #                     self.process.terminate()
        #                     self.process.wait()
        #                     self.process.kill()
        #                     self.process = None
        #             except OSError:
        #                 return False
        #             else:
        #                 return True

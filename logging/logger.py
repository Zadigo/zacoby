import logging


class Logger:
    def __init__(self, filename=None, name=None, default='stream'):
        logging_defaults = ['stream', 'file']
        if default not in logging_defaults:
            raise ValueError(f"'{default}' is not in the logging defaults")

        if name is None:
            name = 'Zacoby'

        if filename is None:
            filename = 'zacoby.log'

        logger = logging.Logger(name)

        formatter = logging.Formatter(
            '%(asctime)s :: %(levelname)s - %(name)s - %(message)s',
            datefmt='%Y-%m-%d %H:%m'
        )

        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(filename)
        
        stream_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        if default == 'stream':
            logger.addHandler(stream_handler)
        elif default == 'file':
            logger.addHandler(file_handler)
        elif default == 'both':
            logger.addHandler(stream_handler)
            logger.addHandler(file_handler)

        self.logger = logger

    def __call__(self, name, filename=None, default='stream'):
        self.__init__(filename=filename, name=name, default=default)
        return self.logger

default_logger = Logger()

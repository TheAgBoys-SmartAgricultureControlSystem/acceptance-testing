import logging

formatter = logging.Formatter('%(asctime)s - %(processName)s:%(levelname)s - %(funcName)s: %(message)s')


def setup_logger(name, log_file, level=logging.INFO, filemode='a'):
	handler = logging.FileHandler(log_file)
	handler.setFormatter(formatter)

	logger = logging.getLogger(name)
	logger.setLevel(level)
	logger.addHandler(handler)

	return logger


gui_logger = setup_logger('gui_logger', 'gui_gui.log')

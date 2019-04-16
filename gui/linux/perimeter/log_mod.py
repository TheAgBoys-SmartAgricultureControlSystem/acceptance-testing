import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path, PurePath
import glob
import os

log_folder = "/home/pi/Downloads/gui/acceptance-testing-master/gui/log/"
init_log = log_folder + 'gui_init.log'
# print(init_log)
nodeStatus_log = log_folder + 'gui_nodeStatus.log'
stream_log = log_folder + 'gui_stream.log'
settings_log = log_folder + 'gui_settings.log'
gui_log = log_folder + 'gui_gui.log'
upload_log = log_folder + 'gui_upload.log'
irrigation_log = log_folder + 'gui_irrigation.log'

formatter = logging.Formatter('%(asctime)s - %(processName)s:%(levelname)s - %(funcName)s: %(message)s')


def setup_logger(name, log_file, level=logging.INFO, filemode='a'):
	handler = TimedRotatingFileHandler(log_file, when='W6', interval=1, backupCount=3, utc=False)
	handler.setFormatter(formatter)

	logger = logging.getLogger(name)
	logger.setLevel(level)
	logger.addHandler(handler)

	return logger


gui_logger = setup_logger('gui_logger', gui_log)


from pathlib import Path
import glob
import os
import subprocess
import log_mod

log_folderstream = Path("D:/MyDocuments/Dropbox/University/Fall_18/Capstone/code/acceptance-testing/gui/log/")

upload_logger = log_mod.setup_logger('upload_logger', log_mod.upload_log)
initial_log = True
bt_address = "64:A2:F9:3C:FA:D9"


def transmit_latest_stream_log():
	global initial_log
	try:
		if initial_log:
			filenameslistfirst = glob.glob(str(log_folderstream / 'gui_stream.log'))
			latest_log = max(filenameslistfirst, key=os.path.getctime)
			initial_log = False
			subprocess.check_call(["obexftp", "-b", bt_address, "-c", "/PHONE_MEMORY/ftp", "-p", latest_log])
		else:
			filenameslist = glob.glob(str(log_folderstream / 'gui_stream.log.*'))
			latest_log = max(filenameslist, key=os.path.getctime)
			subprocess.check_call(["obexftp", "-b", bt_address, "-c", "/PHONE_MEMORY/ftp", "-p", latest_log])
	except subprocess.CalledProcessError as e:
		upload_logger.error("Subprocess Error: ", e)
	except subprocess.TimeoutExpired:
		upload_logger.error("Subprocess Timed Out")


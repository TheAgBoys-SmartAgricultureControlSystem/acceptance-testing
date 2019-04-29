# acceptance testing - final
[TOC]

#### Dependencies

- Source code found in Wireless_Communication/ is compiled in Code Composer Studio (C code) using the 	Simplelink CC1352 SDK v2.30 for the concentrator code and v2.40 for the node code. Currently the node 	code runs on the v2.30 SDK. The rfWsnNode and rfWsnConcentrator example projects are used as a base for the source files. The wsn_final.zip file contains the projects used for the final production code.
- Source code found in gui/ is compiled in PyCharm using Python 3.6.6 and designed to work on 3.5. The pyserial module must be installed for the GUI to run properly. Run `$ python3 threaded_serial_gui_concentrator.py` to run the GUI. A serial port must be open but unused for the GUI to run properly.
	- Code in linux/ is the final production code for use on a Raspberry Pi 3
		- /geofencing.py requires the GDAL library and the python symlink module installed. This 				depends on the platform
		- /irrigation_control.py requires the RPI.GPIO module found exclusively on the RPI
		- /uploader.py requires obexftp to be installed on the system. This is a linux only program
	- Code in windows/ is the debug code for use on windows and doesnt have RPI-based dependencies

#### acceptance-testing.md directory

    acceptance-testing.md/
            GPS/
				GPS Integration Test/
					/main_nortos.c
            gui/
				linux/
					perimeter/
						/entryvalidation.py
						/geofencing.py
						/irrigation_control.py
						/log_mod.py
						/uploader.py
					/threaded_serial_gui_concentrator.py
					/entryvalidation.py
					/geofencing.py
					/irrigation_control.py
					/log_mod.py
					/uploader.py
				windows/
					perimeter/
						/entryvalidation.py
						/geofencing.py
						/irrigation_control.py
						/log_mod.py
						/uploader.py
					/threaded_serial_gui_concentrator.py
					/entryvalidation.py
					/geofencing.py
					/irrigation_control.py
					/log_mod.py
					/uploader.py
            Structures/
				PCB/
					Gerber/
				Sensor Module/
					Assembly.SLDASM/
					Casingrev3.STL/
					Casingrev2 - Casing_lid.STL/
            Wireless_Communication/
				CCS_RF_Tx/
					rf node and concentrator code/
						concentrator/
							/*
						gpsnode/
							/*
						node/
							/*
            ...


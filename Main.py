"""
PyDroidTools
Experiments with Python and ADB/fastboot tools

"""
import os # Allows the execution of shell commands

print("--------------------\nInstalling core components...\nPlease wait\n-----------------------------")
os.system("pip install wget")

import wget # Allows URL downloads
import time

# Static URL from Google Server
adb_windows ="https://dl.google.com/android/repository/platform-tools-latest-windows.zip"

# Packages names
windows = "platform-tools-latest-windows.zip"

user = 0 # For keyboard input 

while user != 5:
	user = int(input(
		"""
	██████╗░██╗░░░██╗██████╗░██████╗░░█████╗░██╗██████╗░████████╗░█████╗░░█████╗░██╗░░░░░░██████╗
	██╔══██╗╚██╗░██╔╝██╔══██╗██╔══██╗██╔══██╗██║██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██║░░░░░██╔════╝
	██████╔╝░╚████╔╝░██║░░██║██████╔╝██║░░██║██║██║░░██║░░░██║░░░██║░░██║██║░░██║██║░░░░░╚█████╗░
	██╔═══╝░░░╚██╔╝░░██║░░██║██╔══██╗██║░░██║██║██║░░██║░░░██║░░░██║░░██║██║░░██║██║░░░░░░╚═══██╗
	██║░░░░░░░░██║░░░██████╔╝██║░░██║╚█████╔╝██║██████╔╝░░░██║░░░╚█████╔╝╚█████╔╝███████╗██████╔╝
	╚═╝░░░░░░░░╚═╝░░░╚═════╝░╚═╝░░╚═╝░╚════╝░╚═╝╚═════╝░░░░╚═╝░░░░╚════╝░░╚════╝░╚══════╝╚═════╝░
	\nChoose one of the following options: \n-------------------------------\n[1] Download ADB-FASTBOOT Tools\n[2] Check for ADB Devices\n[3] Check for FASTBOOT Devices\n[4] Get Android Phone Logcat\n[5] Exit\n"""))

	if user == 1:
		print("Erasing previous files...")
		os.system("rmdir /S /Q platform-tools")

		print("Downloading", windows, "from Google server, please wait...")
		windows = wget.download(adb_windows,windows) #Download the platform-tools-latest-windows.zip from Google server

		print("\nExtracting the downloaded",windows,"file...")
		from zipfile import ZipFile
		with ZipFile('platform-tools-latest-windows.zip') as zipObj:
			zipObj.extractall() #Extracts the downloaded file into a subdir called /platform-tools

		print("Erasing temp files...")
		os.system("del /f platform-tools-latest-windows.zip ")


	elif user == 2:
		print("\n---------------- ADB Devices Found ---------------\nIf your device is not listed, check your USB cable")
		os.system("cd platform-tools & adb.exe devices")
		time.sleep(5)

	elif user == 3:
		print("\n---------------- FASTBOOT Devices Found ---------------\nIf your device is not listed, check your USB cable")
		os.system("cd platform-tools & fastboot.exe devices")
		time.sleep(5)

	elif user == 4:
		print("Plug your device to your PC USB port and wait\nA logcat file will be generated into your /PyDroidTools folder")
		os.system("cd platform-tools & adb.exe logcat -d -b main -b system -b events -v time > logcat.txt")

	else:
		print("Bye")





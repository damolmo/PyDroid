"""
PyDroidTools
Experiments with Python and ADB/fastboot tools

"""
import os

print("--------------------\nInstalling core components...\nPlease wait\n-----------------------------")
os.system("pip install wget")
os.system("pip install wheel")

try:
    import lzma
except ImportError:
    from backports import lzma

import wget # Allows URL downloads
import time # Allows to sleep the code execution
import lzma # Allows .xz extraction for gsi files
import sys
import tarfile

# Static URLs
adb_windows ="https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
pydroidtools = "https://github.com/daviiid99/PyDroidTools/raw/main/Main.py"

# Packages names
windows = "platform-tools-latest-windows.zip"
gsi_image = "system.img.xz"

user = 0 # For keyboard input 

while user != 9:
	user = int(input(
		"""
	██████╗░██╗░░░██╗██████╗░██████╗░░█████╗░██╗██████╗░████████╗░█████╗░░█████╗░██╗░░░░░░██████╗
	██╔══██╗╚██╗░██╔╝██╔══██╗██╔══██╗██╔══██╗██║██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██║░░░░░██╔════╝
	██████╔╝░╚████╔╝░██║░░██║██████╔╝██║░░██║██║██║░░██║░░░██║░░░██║░░██║██║░░██║██║░░░░░╚█████╗░
	██╔═══╝░░░╚██╔╝░░██║░░██║██╔══██╗██║░░██║██║██║░░██║░░░██║░░░██║░░██║██║░░██║██║░░░░░░╚═══██╗
	██║░░░░░░░░██║░░░██████╔╝██║░░██║╚█████╔╝██║██████╔╝░░░██║░░░╚█████╔╝╚█████╔╝███████╗██████╔╝
	╚═╝░░░░░░░░╚═╝░░░╚═════╝░╚═╝░░╚═╝░╚════╝░╚═╝╚═════╝░░░░╚═╝░░░░╚════╝░░╚════╝░╚══════╝╚═════╝░
	\nChoose one of the following options: \n-------------------------------\n[0] Upgrade PyDroidTools\n[1] Download Platform-Tools\n[2] Check for ADB Devices\n[3] Check for Fastboot Devices\n[4] Get Android Device Logcat\n[5] Flash a GSI\n[6] Unlock Android Bootloader\n[7] Remove Android App (Bloatware)\n[8] Dump Thermal config file\n[9] Exit\n--------------------------------\n"""))

	if user == 0:
		print("\nErasing previous version of PyDroidTools...")
		os.system("del /f Main.py ")

		print("\nDownloading latest PyDroidTools, please wait...")
		release = wget.download(pydroidtools, "Main.py")

		print("\nExiting from previous PyDroidTools version and launching new version...")
		user = 5
		os.system("python Main.py")


	elif user == 1:
		print("\nErasing previous files...")
		os.system("rmdir /S /Q platform-tools")

		print("\nDownloading %s from Google server, please wait..." % windows)
		windows = wget.download(adb_windows,windows) #Download the platform-tools-latest-windows.zip from Google server

		print("\nExtracting the downloaded %s file..." % windows)
		from zipfile import ZipFile
		with ZipFile('platform-tools-latest-windows.zip') as zipObj:
			zipObj.extractall() #Extracts the downloaded file into a subdir called /platform-tools

		print("\nErasing temp files...")
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
		print("\nPlug your device to your PC USB port and wait\nA logcat file will be generated into your /PyDroidTools folder")
		os.system("cd platform-tools & adb.exe logcat -d -b main -b system -b events -v time > ../logcat.txt")

	elif user == 5:
		url = input("\nEnter your GSI URL (Recommended GitHub:\n")
		gsi = wget.download(url,gsi_image) # Download the GSI
		with lzma.open('system.img.xz', mode='rt', encoding='utf-8', errors='ignore') as image:
		 for line in image:
		 	print(image)

		os.system("cd platform-tools & fastboot.exe devices")
		print("\nFlashing the Generic System Image...")
		os.system("cd platform-tools & fastboot.exe flash system.img")

		print("\nErasing temp files...")
		os.system("del /f system.img.xz ")
		os.system("del /f system.img")

	elif user == 6:
		print("\nWARNING!!\nBootloader Unlock will ONLY work with Google Pixel and Android One Devices\nIf you're using an unlockable device, enable\nSettings > System > Developer Options > OEM unlock > Enable\nAnd plug-in your Android device")
		os.system("cd platform-tools & fastboot.exe flashing unlock")
		time.sleep(10)

	elif user == 7:
		print("\nTo remove a preinstalled Android App, go to the settings of your app and search the package name\nExample 'com.android.vending'\n")
		app = input("Enter App package name:\n")
		os.system("cd platform-tools & adb.exe uninstall --user 0 %s " % app)

	elif user == 8:
		os.system("cd platform-tools & adb.exe root & adb.exe shell thermal-engine -o > ../thermal-engine.conf")
		print("\nDumped Device Thermal configuration to /PyDroidTools")
		time.sleep(3)

	else:
		print("\nBye")





"""
PyDroidTools
Experiments with Python and ADB/fastboot tools

"""
import os

#======================== Beginning of dependencies ==============
print("-----------------------------\nInstalling core components...\nPlease wait\n-----------------------------")
os.system("pip install wheel")
os.system("pip install wget")
# =================== End of dependencies ===========================================


# ======================= Beginning of Imports ===================
try:
    import lzma
except ImportError:
    from backports import lzma

import wget # Allows URL downloads
import time # Allows to sleep the code execution
import lzma # Allows .xz extraction for gsi files
import sys
import tarfile
from pathlib import Path
import zipfile
from datetime import datetime
DATE_FORMAT = '%y%m%d'
import subprocess
import subprocess
# ==================== End of imports ================================


# ============================ Beginning of Functions ====================

def date_str():
    """returns the today string year, month, day"""
    return '{}'.format(datetime.now().strftime(DATE_FORMAT))

def zip_name(path):
    cur_dir = Path(path).resolve()
    parent_dir = cur_dir.parents[0]
    zip_filename = '{}/{}_{}.zip'.format(parent_dir, cur_dir.name, date_str())
    p_zip = Path(zip_filename)
    n = 1
    while p_zip.exists():
        zip_filename = ('{}/{}_{}_{}.zip'.format(parent_dir, cur_dir.name,
                                             date_str(), n))
        p_zip = Path(zip_filename)
        n += 1
    return zip_filename


def all_files(path):
    for child in Path(path).iterdir():
        yield str(child)
        if child.is_dir():
            for grand_child in all_files(str(child)):
                yield str(Path(grand_child))

def zip_dir(path):
    zip_filename = zip_name(path)
    zip_file = zipfile.ZipFile(zip_filename, 'w')
    print('create:', zip_filename)
    for file in all_files(path):
        print('adding... ', file)
        zip_file.write(file)
    zip_file.close()

def check_device():
	try:
		my_device_model = subprocess.check_output("cd platform-tools & adb shell getprop ro.product.model", shell=True, )
		my_device_model = my_device_model.decode("utf-8")
		my_device_model = str(my_device_model)
		my_device_model = my_device_model.replace(" ", "")

	except subprocess.CalledProcessError as e:
		my_device_model = str("No ADB device found")

	return my_device_model

# ======================== End of Functions ================================

# =================== Beginning of variables=============
# Static URLs
adb_windows ="https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
pydroidtools = "https://github.com/daviiid99/PyDroidTools/raw/main/Main.py"

# Packages names
windows = "platform-tools-latest-windows.zip"
gsi_image = "system.img"
ota_package = "android_ota.zip"

user = 0 # For keyboard input 

# ==================== End of variables ===================


# ================= Beginning of Main ======================
while user != "":
	my_device_model = check_device()
	if my_device_model == "No ADB device found" :
		user = input(
			"""
 ----------------------------------------------
| █▀█ █▄█ █▀▄ █▀█ █▀█ █ █▀▄ ▀█▀ █▀█ █▀█ █░░ █▀ |
| █▀▀ ░█░ █▄▀ █▀▄ █▄█ █ █▄▀ ░█░ █▄█ █▄█ █▄▄ ▄█ |
|----------------------------------------------|\n|Current Device : %s          |\n|----------------------------------------------|\n|Choose one of the following options:          |\n|----------------------------------------------|\n|[0] Upgrade PyDroidTools                      |\n|[1] Download Platform-Tools                   |\n|[2] Check for ADB Devices                     |\n|[3] Check for Fastboot Devices                |\n|[4] Get Android Device Logcat                 |\n|[5] Flash a Generic System Image              |\n|[6] Unlock Android Bootloader                 |\n|[7] Remove Android App (Bloatware)            |\n|[8] Install Android App                       |\n|[9] Dump Thermal config file                  |\n|[10] Android Device Backup                    |\n|[11] Backup current Android boot.img          |\n|[12] Send file over ADB                       |\n|[13] Sideload OTA file                        |\n|----------------------------------------------|\n|Press enter to exit...                        |\n|----------------------------------------------|    \n| Version 1.0                       ©daviiid99 |\n ----------------------------------------------    \n""" % my_device_model)

	else:
		user = input(
			"""
 ----------------------------------------------
| █▀█ █▄█ █▀▄ █▀█ █▀█ █ █▀▄ ▀█▀ █▀█ █▀█ █░░ █▀ |
| █▀▀ ░█░ █▄▀ █▀▄ █▄█ █ █▄▀ ░█░ █▄█ █▄█ █▄▄ ▄█ |
|----------------------------------------------|\n|Current Device : %s|----------------------------------------------|\n|Choose one of the following options:          |\n|----------------------------------------------|\n|[0] Upgrade PyDroidTools                      |\n|[1] Download Platform-Tools                   |\n|[2] Check for ADB Devices                     |\n|[3] Check for Fastboot Devices                |\n|[4] Get Android Device Logcat                 |\n|[5] Flash a Generic System Image              |\n|[6] Unlock Android Bootloader                 |\n|[7] Remove Android App (Bloatware)            |\n|[8] Install Android App                       |\n|[9] Dump Thermal config file                  |\n|[10] Android Device Backup                    |\n|[11] Backup current Android boot.img          |\n|[12] Send file over ADB                       |\n|[13] Sideload OTA file                        |\n|----------------------------------------------|\n|Press enter to exit...                        |\n|----------------------------------------------|    \n| Version 1.0                       ©daviiid99 |\n ----------------------------------------------    \n""" % my_device_model)
	match user:

		case "0":
			print("\nErasing previous version of PyDroidTools...")
			os.system("del /f Main.py ")

			print("\nDownloading latest PyDroidTools, please wait...")
			release = wget.download(pydroidtools, "Main.py")

			print("\nExiting from previous PyDroidTools version and launching new version...")
			user = ""
			os.system("python Main.py")


		case "1":
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


		case "2":
			print("\n---------------- ADB Devices Found ---------------\nIf your device is not listed, check your USB cable")
			os.system("cd platform-tools & adb.exe devices")
			time.sleep(5)

		case "3":
			print("\n---------------- FASTBOOT Devices Found ---------------\nIf your device is not listed, check your USB cable")
			os.system("cd platform-tools & fastboot.exe devices")
			time.sleep(5)

		case "4":
			logcat = "logcat" + "-" + my_device_model + ".txt"
			logcat = logcat.replace("\n.txt", ".txt")
			print("\nPlug your device to your PC USB port and wait\nA logcat file will be generated into your /PyDroidTools folder")
			os.system("cd platform-tools & adb.exe logcat -d -b main -b system -b events -v time > ../%s" % logcat)

		case "5":
			resource = input("\nChoose an option to get the GSI file: \n[1] Local\n[2] URL\n")

			if resource == "1":
				print("\nPut your gsi file into your /PyDroidTools Folder and press enter..")
				empty = input("")
				gsi = input("\nEnter the filename of your GSI (without the .img extension) : \n")
				gsi = gsi + ".img"

			else:
				url = input("\nEnter your GSI URL (Recommended GitHub:\n")
				gsi = wget.download(url,gsi_image) # Download the GSI
				gsi = gsi_image

			user = input("\nSelect the slot to flash the Generic System Image : \n[1] Slot system_a\n[3] Slot system_b\n")

			if user == "1" :
				os.system("cd platform-tools & fastboot.exe devices")
				print("\nFlashing the Generic System Image...")
				os.system("cd platform-tools & fastboot.exe flash system_a %s" % gsi)

			else :
				os.system("cd platform-tools & fastboot.exe devices")
				print("\nFlashing the Generic System Image...")
				os.system("cd platform-tools & fastboot.exe flash system_b %s" % gsi)

			print("\nErasing temp files...")
			os.system("del /f system.img")

		case "6":
			print("\nWARNING!!\nBootloader Unlock will ONLY work with Google Pixel and Android One Devices\nIf you're using an unlockable device, enable\nSettings > System > Developer Options > OEM unlock > Enable\nAnd plug-in your Android device")
			os.system("cd platform-tools & fastboot.exe flashing unlock")
			time.sleep(10)

		case "7":
			print("\nTo remove a preinstalled Android App, go to the settings of your app and search the package name\nExample 'com.android.vending'\nOr list all apps packages")
			ask = input("\n[1] List all apps packages\n[2] Enter app package\n")

			if ask == "1" :
				os.system("cd platform-tools & adb.exe shell pm list packages")
				app = input("Enter App package name:\n")
				os.system("cd platform-tools & adb.exe uninstall --user 0 %s " % app)

			else :
				app = input("Enter App package name:\n")
				os.system("cd platform-tools & adb.exe uninstall --user 0 %s " % app)

		case "8":
			print("Place the .APK files into your /PyDroidTools dir and wait ...")
			time.sleep(3)
			user = input("\nEnter app name (without the .apk extension): \n")
			os.system("cd platform-tools & adb.exe install -r ../%s.apk " % user)

			ask = input("Remove the installed file?:\n (Y/N)")
			if ask.upper() == "Y":
				os.system("del /f %s.apk" % user)


		case "9":
			os.system("cd platform-tools & adb.exe shell thermal-engine -o > ../thermal-engine.conf")
			print("\nDumped Device Thermal configuration to /PyDroidTools")
			time.sleep(3)

		case "10":
			allowed = []
			print("This will allow you to backup selected files from your Android Device to a compressed .zip file\n")
			dcim = input("Include /DCIM folder ?\nThis folder includes Camera photos\n (Y/N)")
			if  dcim.upper() == "Y":
				allowed.append("DCIM")

			pictures = input("Include /Pictures folder ?\nThis folder includes photos from Social Apps like Twitter, WhatsApp,...\n (Y/N)")
			if  pictures.upper() == "Y":
				allowed.append("Pictures")

			downloads = input("Include /Download folder ?\nThis folder includes all your browser downloads\n (Y/N)")
			if  downloads.upper() == "Y":
				allowed.append("Download")

			music = input("Include /Music folder ?\nThis folder includes .mp3 files\n (Y/N)")
			if  music.upper() == "Y":
				allowed.append("Music")

			documents = input("Include /Documents folder ?\nThis folder includes all your documents\n (Y/N)")
			if  documents.upper() == "Y":
				allowed.append("Documents")

			os.system("mkdir backup")

			for dirs in allowed:
				os.system("cd platform-tools & adb.exe pull sdcard/%s ../backup " % dirs )

			print("\nDone downloading the files from your devices... \nCreating a zip file...")

			zipdir = zip_dir("backup")

			print("\nErasing temp files...")
			os.system("rmdir /S /Q backup")

			print("\nBackup completed succesfully!")
			time.sleep(2)

		case "11":
			my_device_model_img = check_device() + ".img"
			my_device_model_img = my_device_model_img.replace("\n.img", ".img")
			ask = input("Choose device partitions type: \n[1] A-only partition (2011-2017 devices\n[2] A|B Partitions (2017-2022 devices)\n[3] Check for all partitions (unknown partitions)\n")
			if ask == "1" :
				os.system("cd platform-tools & adb.exe root & adb.exe pull dev/block/bootdevice/by-name/boot ../boot_%s" % my_device_model_img)

			elif ask == "2" :
				os.system("cd platform-tools & adb.exe root & adb.exe pull dev/block/bootdevice/by-name/boot_a ../boot_a_%s" % my_device_model_img)
				os.system("cd platform-tools & adb.exe root & adb.exe pull dev/block/bootdevice/by-name/boot_b ../boot_b_%s" % my_device_model_img)

			else :
				os.system("cd platform-tools & adb.exe root & adb.exe pull dev/block/bootdevice/by-name/boot ../boot_%s" % my_device_model_img)
				os.system("cd platform-tools & adb.exe root & adb.exe pull dev/block/bootdevice/by-name/boot_a ../boot_a_%s" % my_device_model_img)
				os.system("cd platform-tools & adb.exe root & adb.exe pull dev/block/bootdevice/by-name/boot_b ../boot_b_%s" % my_device_model_img)


		case "12":
			file = input("\n[1] Same Directory \n[2] Paste location \n")
			if file == "1":
				file = input("Enter the full file name : \n")
				os.system("cd platform-tools & adb.exe push ../%s sdcard/Download/" % file)
				print("File %s copied succesfully to /Download" % file)
				time.sleep(2)

			else:
				file = input("Enter the full file location : \n")
				os.system("cd platform-tools & adb.exe push %s sdcard/Download/" % file)
				print("File %s copied succesfully to /Download" % file)
				time.sleep(2)

		case "13" :
			file = input("\n[1] Same Directory \n[2] Paste location \n[3] Paste URL\n")
			match file :
				case "1":
					file = input("Enter the file name (without .zip extension) : \n")
					os.system("cd platform-tools & adb.exe sideload ../%s.zip" % file)
					print("\nOTA update pushed succesfully")
					time.sleep(2)

				case "2" :
					file = input("Enter the full file path : \n")
					os.system("cd platform-tools & adb.exe sideload %s" % file)
					print("\nOTA update pushed succesfully")
					time.sleep(2)

				case "3" :
					file = input("Enter the file URL : \n")
					print("Downloading the zip file as %s" % ota_package)
					download = wget.download(file,ota_package)
					os.system("cd platform-tools & adb.exe sideload ../%s" % ota_package)
					print("\nOTA update pushed succesfully")
					time.sleep(2)

# ================== End of Main =======================


"""
PyDroid
Python program powered by Android Platform-Tools

"""
import os

#======================== Beginning of dependencies ==============
print("-----------------------------\nInstalling core components...\nPlease wait\n-----------------------------")
os.system("pip3 install wheel")
os.system("pip3 install wget")
# =================== End of dependencies ===========================================


# ======================= Beginning of Imports ===================
import lzma
import wget # Allows URL downloads
import time # Allows to sleep the code execution
import lzma # Allows .xz extraction for gsi files
import sys
import tarfile
from pathlib import Path
import zipfile
from datetime import datetime
import subprocess
import subprocess
from zipfile import ZipFile
from os.path import exists
from pathlib import Path
# ==================== End of imports ================================


# ============================ Beginning of Functions ====================

def date_str():
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

def check_adb_device():
	try:
		my_device_model = subprocess.check_output("cd platform-tools & adb shell getprop ro.product.model", shell=True, )
		my_device_model = my_device_model.decode("utf-8")
		my_device_model = str(my_device_model)
		my_device_model = my_device_model.replace(" ", "")

	except subprocess.CalledProcessError as e:
		my_device_model = str("No ADB device found")

	return my_device_model

def check_fastboot_device():
	try:
		my_device_model = subprocess.check_output("cd platform-tools & fastboot devices", shell=True, )
		my_device_model = my_device_model.decode("utf-8")
		my_device_model = str(my_device_model)
		my_device_model = my_device_model.replace(" ", "")

	except subprocess.CalledProcessError as e:
		my_device_model = str("No ADB device found")

	return my_device_model

def install_tools(adb_linux, linux) :
	linux = wget.download(adb_linux,linux) #Download the platform-tools-latest-linux.zip from Google server
	with ZipFile('platform-tools-latest-linux.zip') as zipObj:
		zipObj.extractall() #Extracts the downloaded file into a subdir called /platform-tools
	os.system("rm platform-tools-latest-linux.zip ")


def android_tools_exists(adb_linux, linux) :
	exists = False
	if os.path.exists("platform-tools") :
		exists = True

	else :
		install_tools(adb_linux, linux)

	return exists

def check_for_updates(version) :
	message = False

	# Read the version string from an external text document
	os.system("rm -f version.txt")
	os.system("wget https://raw.githubusercontent.com/daviiid99/PyDroid/Linux/src/version.txt")
	version_str = Path('version.txt').read_text()
	version_str = version_str.replace('\n', '')
	os.system("rm -f version.txt")

	# Check if the latest version is installed
	if version_str != version :
		message = True

	return message

def latest_version() :
	# Read the version string from an external text document
	os.system("rm -f version.txt")
	os.system("wget https://raw.githubusercontent.com/daviiid99/PyDroid/Linux/src/version.txt")
	version_str = Path('version.txt').read_text()
	version_str = version_str.replace('\n', '')
	os.system("rm -f version.txt")

	return version_str

def latest_changelog() :
	# Read the version string from an external text document
	os.system("rm -f changelog.txt")
	os.system("wget https://raw.githubusercontent.com/daviiid99/PyDroid/Linux/src/changelog.txt")
	changelog_str = Path('changelog.txt').read_text()
	os.system("rm -f changelog.txt")

	return changelog_str


# ======================== End of Functions ================================

# =================== Beginning of variables=============
# Static URLs
adb_linux ="https://dl.google.com/android/repository/platform-tools-latest-linux.zip"
pydroidtools = "https://github.com/daviiid99/PyDroid/raw/Linux/Main.py"

# Packages names
usb = "Google_USB.zip"
linux = "platform-tools-latest-linux.zip"
gsi_image_xz = "system.img.xz"
gsi_image = "system.img"
ota_package = "android_ota.zip"

# Other variables
DATE_FORMAT = '%y%m%d'
user = 0 # For keyboard input 
version = "1.0-8"
header ="""
 ----------------------------------------------
|     ____        ____            _     _      |
|    |  _ \ _   _|  _ \ _ __ ___ (_) __| |     |
|    | |_) | | | | | | | '__/ _ \| |/ _` |     |
|    |  __/| |_| | |_| | | | (_) | | (_| |     |
|    |_|    \__, |____/|_|  \___/|_|\__,_|     |
|           |___/                              |
|                                              |
|----------------------------------------------|
"""

# ==================== End of variables ===================

# ================= Beginning of Main ======================
android_tools_exists(adb_linux, linux)
while user != "":
	my_adb_model = check_adb_device()
	my_fastboot_model = check_fastboot_device()
	user = "P"
	match user :

		case "P" | "p" :
			if my_adb_model == "No ADB device found" and my_fastboot_model == "No ADB device found" :
				my_device_model = my_adb_model
				user = input("""%s|Device : %s | <L> To Refresh |\n|----------------------------------------------|\n|Choose one of the following options:          |\n|----------------------------------------------|\n|[1] Check for PyDroid updates                 |\n|[2] Reinstall Platform-Tools                  |\n|[3] Check for ADB Devices                     |\n|[4] Check for Fastboot Devices                |\n|[5] Get Android Device Logcat                 |\n|[6] Flash a Generic System Image              |\n|[7] Unlock Android Bootloader                 |\n|[8] Remove Android App (Bloatware)            |\n|[9] Install Android App                       |\n|[10] Dump Thermal config file                 |\n|----------------------------------------------|\n| <ENTER> Exit                <N> Next Page -> |\n|----------------------------------------------|    \n| Version %s                     ©daviiid99 |\n ----------------------------------------------    \n""" % (header, my_device_model, version))
			
			elif my_adb_model != "No ADB device found" and my_adb_model !="" : 
					my_device_model = my_adb_model
					user = input("""%s|Current Device : %s|<R> Recovery <F> Fastboot <T> Reboot <K> Kill |\n|----------------------------------------------|\n|Choose one of the following options:          |\n|----------------------------------------------|\n|[1] Check for PyDroid updates                 |\n|[2] Reinstall Platform-Tools                  |\n|[3] Check for ADB Devices                     |\n|[4] Check for Fastboot Devices                |\n|[5] Get Android Device Logcat                 |\n|[6] Flash a Generic System Image              |\n|[7] Unlock Android Bootloader                 |\n|[8] Remove Android App (Bloatware)            |\n|[9] Install Android App                       |\n|[10] Dump Thermal config file                 |\n|----------------------------------------------|\n| <ENTER> Exit                <N> Next Page -> |\n|----------------------------------------------|    \n| Version %s                     ©daviiid99 |\n ----------------------------------------------    \n""" % (header, my_device_model, version))	
					

			elif my_fastboot_model != "No ADB device found" and my_fastboot_model !="" :
					my_device_model = my_fastboot_model
					user = input("""%s|Current Device : %s|<S> Recovery <U> Fastboot <V> Reboot <W> Kill |\n|----------------------------------------------|\n|Choose one of the following options:          |\n|----------------------------------------------|\n|[1] Check for PyDroid updates                 |\n|[2] Reinstall Platform-Tools                  |\n|[3] Check for ADB Devices                     |\n|[4] Check for Fastboot Devices                |\n|[5] Get Android Device Logcat                 |\n|[6] Flash a Generic System Image              |\n|[7] Unlock Android Bootloader                 |\n|[8] Remove Android App (Bloatware)            |\n|[9] Install Android App                       |\n|[10] Dump Thermal config file                 |\n|----------------------------------------------|\n| <ENTER> Exit                <N> Next Page -> |\n|----------------------------------------------|    \n| Version %s                     ©daviiid99 |\n ----------------------------------------------    \n""" % (header, my_device_model, version))	
				
			else :
				my_device_model = my_adb_model
				user = input("""%s|Device : %s | <L> To Refresh |\n|----------------------------------------------|\n|Choose one of the following options:          |\n|----------------------------------------------|\n|[1] Check for PyDroid updates                 |\n|[2] Reinstall Platform-Tools                  |\n|[3] Check for ADB Devices                     |\n|[4] Check for Fastboot Devices                |\n|[5] Get Android Device Logcat                 |\n|[6] Flash a Generic System Image              |\n|[7] Unlock Android Bootloader                 |\n|[8] Remove Android App (Bloatware)            |\n|[9] Install Android App                       |\n|[10] Dump Thermal config file                 |\n|----------------------------------------------|\n| <ENTER> Exit                <N> Next Page -> |\n|----------------------------------------------|    \n| Version %s                     ©daviiid99 |\n ----------------------------------------------    \n""" % (header, my_device_model, version))

			match user :
				case "1":
					print("\nChecking for PyDroid Updates ...\n")
					time.sleep(2)

					if check_for_updates(version) == True :
						user = input("\n%s|New Available version : %s    	       |\n ---------------------------------------------- \n Changelog : 				        \n%s 	        \n ----------------------------------------------- \n\nUpgrade to latest version ? (Y|N)\n " % (header, latest_version(), latest_changelog()) )
						match user :
							case "Y" | "y" :

								print("\nDownloading latest version ...")
								print("\nErasing previous version of PyDroid...")
								os.system("rm Main.py ")
								print("\nDownloading latest PyDroid, please wait...")
								release = wget.download(pydroidtools, "Main.py")
								print("\nExiting from previous PyDroid version and launching new version...")
								user = ""
								os.system("python3 Main.py")

							case "N" | "n" :

								print("\nOperation cancelled by the user")
								time.sleep(2)


					else :
						print("\nCurrent installed version : %s \nLatest Available Version : %s " % (version, latest_version()) )
						time.sleep(5)



				case "2":
					if android_tools_exists(adb_linux, linux) == True :
						print("\nAndroid Platform-Tools are already installed on your device\nHave a good day!")
						ask = input("\nReinstall ? (Y|N)\n")


						if ask.upper() == "Y" :
							os.system("rm -rf platform-tools")
							print("\nDownloading %s from Google server, please wait..." % linux)
							android_tools_exists(adb_linux, linux)

						else:
							print("\nOperation cancelled by the user")
							time.sleep(2)

					else : 
						print("\nDownloading %s from Google server, please wait..." % linux)

				case "3":
					print("\n---------------- ADB Devices Found ---------------\nIf your device is not listed, check your USB cable")
					os.system("cd platform-tools & adb devices")
					time.sleep(5)

				case "4":
					print("\n---------------- FASTBOOT Devices Found ---------------\nIf your device is not listed, check your USB cable")
					os.system("cd platform-tools & fastboot devices")
					time.sleep(5)

				case "5":
					logcat = "logcat" + "-" + my_device_model + ".txt"
					logcat = logcat.replace("\n.txt", ".txt")
					print("\nPlug your device to your PC USB port and wait\nA logcat file will be generated into your /PyDroidTools folder")
					os.system("cd platform-tools & adb logcat -d -b main -b system -b events -v time > %s" % logcat)

				case "6":
					resource = input("\nChoose an option to get the GSI file: \n[1] Local\n[2] URL\n")

					if resource == "1":
						print("\nPut your gsi file into your /PyDroidTools Folder and press enter..")
						empty = input("")
						gsi = input("\nEnter the filename of your GSI (without the .img extension) : \n")
						gsi = gsi + ".img"

					elif resource == "2":
						ask = input("\nChoose the extension of your GSI file : \n[1] .IMG \n[2] .XZ\n")

						if ask == "1" :
							url = input("\nEnter your GSI URL (Recommended GitHub:\n")
							gsi = wget.download(url,gsi_image) # Download the GSI
							gsi = gsi_image

						elif ask == "2" :
							url = input("\nEnter your GSI URL (Recommended GitHub:\n")
							gsi = wget.download(url,gsi_image_xz) # Download the GSI
							print("\nExtracting the %s file, please wait..." % gsi_image_xz)
							with lzma.open(gsi_image_xz) as gsi, open(gsi_image, 'wb') as extract:
								gsi = gsi.read()
								extract.write(gsi)
								gsi = gsi_image

					else :
						print("\nOperation cancelled by the user")
						time.sleep(2)

					user = input("\nSelect the slot to flash the Generic System Image : \n[1] Slot system_a\n[2] Slot system_b\n[3] Slots system_a & system_b")

					if user == "1" :
						os.system("cd platform-tools & fastboot devices")
						print("\nFlashing the Generic System Image...")
						os.system("cd platform-tools & fastboot flash system_a %s" % gsi)
						print("\nErasing temp files...")
						os.system("rm system.img")
						os.system("rm system.img.xz")

					elif user == "2" :
						os.system("cd platform-tools & fastboot devices")
						print("\nFlashing the Generic System Image...")
						os.system("cd platform-tools & fastboot flash system_b %s" % gsi)
						print("\nErasing temp files...")
						os.system("rm system.img")
						os.system("rm system.img.xz")

					elif user == "3" :
						os.system("cd platform-tools & fastboot devices")
						print("\nFlashing the Generic System Image...")
						os.system("cd platform-tools & fastboot flash system_a %s" % gsi)
						os.system("cd platform-tools & fastboot flash system_b %s" % gsi)
						print("\nErasing temp files...")
						os.system("rm system.img")
						os.system("rm system.img.xz")


					else :
						print("\nOperation cancelled by the user")
						time.sleep(2)

	

				case "7":
					print("\nWARNING!!\nBootloader Unlock will ONLY work with Google Pixel and Android One Devices\nIf you're using an unlockable device, enable\nSettings > System > Developer Options > OEM unlock > Enable\nAnd plug-in your Android device")
					os.system("cd platform-tools & fastboot flashing unlock")
					time.sleep(10)

				case "8":
					print("\nTo remove a preinstalled Android App, go to the settings of your app and search the package name\nExample 'com.android.vending'\nOr list all apps packages")
					ask = input("\n[1] List all apps packages\n[2] Enter app package\n")

					if ask == "1" :
						os.system("cd platform-tools & adb shell pm list packages")
						app = input("Enter App package name:\n")
						os.system("cd platform-tools & adb uninstall --user 0 %s " % app)

					elif ask == "2" :
						app = input("Enter App package name:\n")
						os.system("cd platform-tools & adb uninstall --user 0 %s " % app)

					else :
						print("\nOperation cancelled by the user")
						time.sleep(2)

				case "9":
					print("Place the .APK files into your /PyDroidTools dir and wait ...")
					time.sleep(3)
					user = input("\nEnter app name (without the .apk extension): \n")
					os.system("cd platform-tools & adb install -r %s.apk " % user)

					ask = input("Remove the installed file?:\n (Y/N)")
					if ask.upper() == "Y":
						os.system("rm %s.apk" % user)


				case "10":
					os.system("cd platform-tools & adb shell thermal-engine -o > ../thermal-engine.conf")
					print("\nDumped Device Thermal configuration to /PyDroidTools")
					time.sleep(3)

				case "R" | "r" :
					os.system("cd platform-tools & adb reboot recovery")

				case "F" | "f" :
					os.system("cd platform-tools & adb reboot bootloader")

				case "T" | "t" :
					os.system("cd platform-tools & adb reboot system")

				case "K" | "k" :
					os.system("cd platform-tools & adb shell reboot -p")

				case "S" | "s" :
					os.system("cd platform-tools & fastboot reboot recovery")

				case "U" | "u" :
					os.system("cd platform-tools & fastboot reboot bootloader")

				case "V" | "v" :
					os.system("cd platform-tools & fastboot reboot")

				case "W" | "w" :
					os.system("cd platform-tools & fastboot reboot -p")

				case "L" | "l" :
					my_device_model


				case "N" | "n" :

					if my_device_model == "No ADB device found" :
						user = input("""%s|Device : %s | <L> To Refresh |\n|----------------------------------------------|\n|Choose one of the following options:          |\n|----------------------------------------------|\n|[11] Android Device Backup                    |\n|[12] Backup current Android boot.img          |\n|[13] Send file over ADB                       |\n|[14] Sideload OTA file                        |\n|[15] Modify Screen DPI                        |\n|----------------------------------------------|\n| <- <P> Previous Page            <ENTER> Exit |\n|----------------------------------------------|    \n| Version %s                     ©daviiid99 |\n ----------------------------------------------    \n""" % (header, my_device_model, version))

					else: 
						user = input("""%s|Current Device : %s|<R> Recovery <F> Fastboot <T> Reboot <K> Kill |\n|----------------------------------------------|\n|Choose one of the following options:          |\n|----------------------------------------------|\n|[11] Android Device Backup                    |\n|[12] Backup current Android boot.img          |\n|[13] Send file over ADB                       |\n|[14] Sideload OTA file                        |\n|[15] Modify Screen DPI                        |\n|----------------------------------------------|\n| <- <P> Previous Page            <ENTER> Exit |\n|----------------------------------------------|    \n| Version %s                     ©daviiid99 |\n ----------------------------------------------    \n""" % (header, my_device_model, version))

					match user :
						case "11":
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
								os.system("cd platform-tools & adb pull sdcard/%s backup " % dirs )

							print("\nDone downloading the files from your devices... \nCreating a zip file...")

							zipdir = zip_dir("backup")

							print("\nErasing temp files...")
							os.system("rm -rf backup")

							print("\nBackup completed succesfully!")
							time.sleep(2)

						case "12":
							my_device_model_img = check_adb_device() + ".img"
							my_device_model_img = my_device_model_img.replace("\n.img", ".img")
							ask = input("Choose device partitions type: \n[1] A-only partition (2011-2017 devices\n[2] A|B Partitions (2017-2022 devices)\n[3] Check for all partitions (unknown partitions)\n")
							match ask:
								case "1" :
									os.system("cd platform-tools & adb root & adb pull dev/block/bootdevice/by-name/boot boot_%s" % my_device_model_img)

								case "2" :
									os.system("cd platform-tools & adb root & adb pull dev/block/bootdevice/by-name/boot_a boot_a_%s" % my_device_model_img)
									os.system("cd platform-tools & adb root & adb pull dev/block/bootdevice/by-name/boot_b boot_b_%s" % my_device_model_img)

								case "3" :
									os.system("cd platform-tools & adb root & adb pull dev/block/bootdevice/by-name/boot boot_%s" % my_device_model_img)
									os.system("cd platform-tools & adb root & adb pull dev/block/bootdevice/by-name/boot_a boot_a_%s" % my_device_model_img)
									os.system("cd platform-tools & adb root & adb pull dev/block/bootdevice/by-name/boot_b boot_b_%s" % my_device_model_img)


						case "13":
							file = input("\n[1] Same Directory \n[2] Paste location \n")
							if file == "1":
								file = input("Enter the full file name : \n")
								os.system("cd platform-tools & adb push ../%s sdcard/Download/" % file)
								print("File %s copied succesfully to /Download" % file)
								time.sleep(2)

							elif file == "2":
								file = input("Enter the full file location : \n")
								os.system("cd platform-tools & adb push %s sdcard/Download/" % file)
								print("File %s copied succesfully to /Download" % file)
								time.sleep(2)

							else :
								print("\nOperation cancelled by the user")
								time.sleep(2)

						case "14" :
							file = input("\n[1] Same Directory \n[2] Paste location \n[3] Paste URL\n")
							match file :
								case "1":
									file = input("Enter the file name (without .zip extension) : \n")
									os.system("cd platform-tools & adb sideload ../%s.zip" % file)
									print("\nOTA update pushed succesfully")
									time.sleep(2)

								case "2" :
									file = input("Enter the full file path : \n")
									os.system("cd platform-tools & adb sideload %s" % file)
									print("\nOTA update pushed succesfully")
									time.sleep(2)

								case "3" :
									file = input("Enter the file URL : \n")
									print("Downloading the zip file as %s" % ota_package)
									download = wget.download(file,ota_package)
									os.system("cd platform-tools & adb sideload ../%s" % ota_package)
									print("\nOTA update pushed succesfully")
									time.sleep(2)

						case "15" :
							option = input("\nAndroid Device Screen DPI Control\n[1] Check current DPI\n[2] Modify Screen DPI\n")

							if option == "1":
								os.system("cd platform-tools & adb shell wm density")
								time.sleep(5)

							elif option == "2" :
								dpi = int(input("\nEnter a new Display Density: \n"))
								os.system("cd platform-tools & adb shell wm density %d" % dpi)
								time.sleep(3)

							else :
								print("\nOperation cancelled by the user")
								time.sleep(2)
									
		
# ================== End of Main =======================


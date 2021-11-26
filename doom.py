#EZFTP - Build {1.1} - For Raspberry Pi Portable Usage | Developed By: ss12
try:
	import ftplib
	import os 
	from pyfiglet import figlet_format 
	from datetime import datetime
	from colorama import Fore
	import time 
except ImportError as err:
	print("EZFTP | Has Detected An Error With The Following Error Code: | %s |")
	raise Exception(
		'Please Fix The Following | %s |'
	)

def get_datetime_format(date_time):
  # convert to datetime object
  date_time = datetime.strptime(date_time, "%Y%m%d%H%M%S")
  # convert to human readable date time string
  return date_time.strftime("%Y/%m/%d %H:%M:%S")

def get_size_format(n, suffix="B"):
  # Converts Bytes To Scaled Format (e.g KB, MB, etc.)
  for unit in ["", "K", "M", "G", "T", "P"]:
    if n < 1024:
    	return f"{n:.2f}{unit}{suffix}"
    n /= 1024

#Used For A Light Weight Brute Force Attack
def lw_brf():
	get_quick = input(Fore.RED + "Enter FTP Host: ")
	print(Fore.RED + 'Trying Default FTP Creds..')
	try:
		ftp = ftplib.FTP(get_quick,'admin','password')
		ftp.encoding = 'utf-8'
		print(ftp.getwelcome())
	except Exception as err:
		print(Fore.RED + 'Brute Force Attack Failed...')


#Used For Browsing Files In Ftp Server If Creds Are Already Obtained..
def file_browse():
	get = input(Fore.WHITE + 'Enter FTP Host: ')
	user = input(Fore.WHITE + 'Enter FTP User: ')
	pass_ = input(Fore.WHITE + "Enter FTP Pass: ")
	ftp = ftplib.FTP(get,user,pass_)
	ftp.encoding = 'utf-8'
	print(ftp.getwelcome())
	ftp.cwd('pub/maps')
	print('*'*50,'LIST','*'*50)
	ftp.dir()
	time.sleep(2)
	print(Fore.WHITE + 'NLST Processing..')
	print("*"*50, "NLST", "*"*50)
	print("{:20} {}".format("File Name", "File Size"))
	for file_name in ftp.nlst():
		file_size = 'N/A'
		try:
			ftp.cwd(file_name)
		except Exception as e:
			ftp.voidcmd("TYPE I")
			file_size = get_size_format(ftp.size(file_name))
		print(f"{file_name:20} {file_size}")
	time.sleep(1)
	print(Fore.RED + 'MLSD Processing... 3rd Stage..')
	print("*"*50, "MLSD", "*"*50)
	# using the MLSD command
	print("{:30} {:19} {:6} {:5} {:4} {:4} {:4} {}".format("File Name", "Last Modified", "Size",
                                                    "Perm","Type", "GRP", "MODE", "OWNER"))
	for file_data in ftp.mlsd():
		file_name, meta = file_data
		file_type = meta.get('type')
		if file_type == 'file':
			ftp.voidcmd('TYPE I')
			file_size = ftp.size(file_name)
			file_size = get_size_format(file_size)
		else:
			file_size = 'N/A'
		last_modified = get_datetime_format(meta.get('modify'))
		permission = meta.get('perm')
		unique_id = meta.get('unique')
		unix_group = meta.get('unix.group')
		unix_mode = meta.get('unix.mode')
		unix_owner = meta.get('unix.owner')
		print(f"{file_name:30} {last_modified} {file_size:7} {permission:5} {file_type:4} {unix_group:4} {unix_mode:4} {unix_owner}")
		print(Fore.RED + '30 Seconds Remaining View Time..')
		time.sleep(30)
		ftp.quit()
		print(Fore.RED + "Connection Closed...")

def get_host():
	time.sleep(1)
	inp = input(Fore.WHITE + 'Select A For If Creds Are Obtained, Select B For Light Brute Force Attempt')
	if inp == 'A':
		file_browse()
	if inp == 'B':
		lw_brf()

#Use this as banner and initial instructions
def banner():
	print(Fore.BLUE + figlet_format('EZFTP',font='slant'))
	time.sleep(1)
	print(Fore.WHITE + "Used For FTP Access And File Directory Access")

if __name__ == '__main__':
	banner()
	get_host()

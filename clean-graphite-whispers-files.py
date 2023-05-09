#!/usr/bin/python3

import os
import time
import datetime
import logging
import argparse
import sys

def check_path_existence(path):
	if not os.path.exists(path):
		print("\n-----------------------------------------------------------------------------------------------------------------------------------------")
		print(f"Path {path} doesnt exist! Check the path!")
		print("\n-----------------------------------------------------------------------------------------------------------------------------------------")
		sys.exit(2)

def main():
	parser = argparse.ArgumentParser(description='Retrieve old obsolete whisper files and delete them!')
	parser.add_argument('-d', '--days', required=True, help='Older then, number of days, default is 365 days')
	parser.add_argument('-i', '--dry-run', action='store_true', help='Show me only what it could be deleted, without delete action!')
	parser.add_argument('-p', '--path', required=True, default='/opt/graphite/storage/whisper', help='Path/location of whisper files, dafault: /opt/graphite/storage/whisper')
	parser.add_argument('-l', '--log', action='store_true', help='Enable logging, dafault: /var/log/graphite_cleanup_yyyy_mm_dd.log')
	parser.add_argument('-s', '--show', action='store_true', help='Show me output of each deleted file!')
	parser.set_defaults(dry_run=False)
	parser.set_defaults(log=False)
	parser.set_defaults(show=False)
	
	try: 
		args = parser.parse_args()

		if args.dry_run:
			dry_run = True
		else:
			dry_run = False

		if args.days:
			selected_days=int(args.days)
		else:
			selected_days = 365
		
		if args.path:
			root_directory = args.path
		else:
			root_directory = "/opt/graphite/storage/whisper"
		
		# Record the start time
		start_time = time.time()
		
		#Check if the path is existen, if not it will break the execution
		check_path_existence(root_directory)

		if args.log:
			log_filename = f"/var/log/graphite_cleanup_{time.strftime('%Y_%m_%d')}.log"
			logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
			logging.info("Starting...")


		# Get the current time in seconds since the epoch
		current_time = time.time()

		# Calculate the number of seconds
		selected_days = selected_days * 24 * 60 * 60
		counter = 0
		total_size = 0
		total_del_size = 0
		file_size = 0
		file_del_size = 0

		#CHECKING AND DELETING OLD WHISPER FILES
		# Loop through each subdirectory and file in the root directory
		for dirpath, dirnames, filenames in os.walk(root_directory):
			for filename in filenames:
				if filename.endswith('.wsp'):
					file_path = os.path.join(dirpath, filename)
					
					# Get the modification time of the file in seconds since the epoch
					file_time = os.path.getmtime(os.path.join(dirpath, filename))
					
					# Format the modification time as a human-readable string
					formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_time))
					
					# Calculate the age of the file in seconds
					file_age = current_time - file_time
					file_size = os.path.getsize(file_path)
					total_size += file_size 
					if file_age > selected_days:
						file_del_size = os.path.getsize(file_path)
						counter = counter + 1
						total_del_size += file_del_size
						
						if not args.dry_run:
							os.remove(os.path.join(dirpath, filename))

						if args.log and args.dry_run:
							logging.info(f"{file_path} (no_update_days: {file_age/86400:.1f} days last_update: {formatted_time})")

						if args.show and args.dry_run:
							print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {file_path} (no_update_days: {file_age/86400:.1f} days, last_update: {formatted_time})")

						if not args.dry_run:
							if args.show:
								print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Deleted {file_path}! (no_update_days: {file_age/86400:.1f} days, last_update: {formatted_time})")
							logging.info(f"[Deleted {file_path}! (no_update_days: {file_age/86400:.1f} days, last_update: {formatted_time})")
		
		# Record end time
		end_time = time.time()
		duration_sec = end_time - start_time
		duration_timedelta = datetime.timedelta(seconds=duration_sec)
		
		# Format the duration as hh:mm:ss
		duration_formatted = str(duration_timedelta)

		#if args.show:
			#print("\n-----------------------------------------------------------------------------------------------------------------------------------------")
		
		if args.dry_run:
			print(f"Total old stale whisper files {counter}, Total size of old stale whisper files: {total_del_size/(1024*1024):.2f} MB, Total size of all whisper files: {total_size/(1024*1024*1024):.6f} GB, Ratio: {float(float(total_del_size)/float(total_size))*100:.2f}% to be deleted, Script duration: {duration_formatted}")
		else:
			print(f"Total deleted whisper files {counter}, Total deleted size: {total_del_size/(1024*1024):.2f} MB, Total size of all whisper files: {total_size/(1024*1024*1024):.6f} GB, Ratio: {float(float(total_del_size)/float(total_size))*100:.2f}% deleted, Script duration: {duration_formatted}")
		
		if args.log:
			if args.dry_run:
				logging.info(f"Report: Total old stale whisper files {counter}, Total size of old stale whisper files: {total_del_size/(1024*1024):.2f} MB, Total size of all whisper files: {total_size/(1024*1024*1024):.6f} GB, Ratio: {float(float(total_del_size)/float(total_size))*100:.2f}% to be deleted, Script duration: {duration_formatted}")
			else:
				logging.info(f"Report: Total Deleted whisper files {counter}, Total deleted size: {total_del_size/(1024*1024):.2f} MB, Total size of all whisper files: {total_size/(1024*1024*1024):.6f} GB, Ratio: {float(float(total_del_size)/float(total_size))*100:.2f}% deleted, Script duration: {duration_formatted}")
	
	except Exception as e:
		print("\n-----------------------------------------------------------------------------------------------------------------------------------------")
		print(f"An error occurred while executing the script: {e}\nPlease check given arguments and permissions!")
		print("\n-----------------------------------------------------------------------------------------------------------------------------------------")

if __name__ == '__main__':
	main()
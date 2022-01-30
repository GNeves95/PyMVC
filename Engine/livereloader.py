import os
import glob
import time
import msvcrt

'''
import msvcrt
print 'Press s or n to continue:\n'
input_char = msvcrt.getch()
'''

running = True

trackedFiles = {}

def changesCheck():
	try:
		while running:
			files = glob.glob("*/*")
			removed_files =[]
			for f in trackedFiles:
				if f not in files:
					removed_files += [f]
			#print(removed_files)
			for f in removed_files:
				del trackedFiles[f]
				print(f"{f} is no longer tracked")
			for file in files:
				if os.path.isfile(file):
					if file in trackedFiles.keys():
						#check if date chagned
						newTime = os.path.getmtime(file)
						if newTime != trackedFiles[file]:
							trackedFiles[file] = newTime
							print(f"{file} was changed from {trackedFiles[file]} at {newTime}")
					else:
						trackedFiles[file] = os.path.getmtime(file)
						print(f"{file} was newly created at {trackedFiles[file]}")
			time.sleep(0.1)
			#TODO: On change, inform every connected socket that they need to refresh
		print("Stopped checking for changes")
	except KeyboardInterrupt:
		print("stopped")
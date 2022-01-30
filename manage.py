import threading
from Engine import livereloader, GUI
import time

x = None

from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
FR_PRIVATE  = 0x10
FR_NOT_ENUM = 0x20

'''def loadfont(fontpath, private=True, enumerable=False):
    if isinstance(fontpath, str):
        pathbuf = create_string_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExA
    elif isinstance(fontpath, unicode):
        pathbuf = create_unicode_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExW
    else:
        raise TypeError('fontpath must be of type str or unicode')

    flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
    numFontsAdded = AddFontResourceEx(byref(pathbuf), flags, 0)
    return bool(numFontsAdded)'''


root = None

def main():
	global x
	if x is None:
		try:
			#Start thread to check changes to project and trigger livereload
			x = threading.Thread(target=livereloader.changesCheck)
			x.start()
			#Create GUI interface
			root = GUI.Window()
			root.root.mainloop()
			while livereloader.running:
				time.sleep(0.1)
			x.join()
			#print("Escaped in management")
		except KeyboardInterrupt:
			print("Exiting")
			livereloader.running = False
			time.sleep(1) #This probably isn't needed, but I'm keeping it alive for a second to ensure that everything shuts down properly
			x.join()

def second_main():
	try:
		main()
	except KeyboardInterrupt:
		print("Are you sure you wish to exit? [y]/n ")
		if opSys is OpSys.Windows:
			input_char = msvcrt.getch()
			if input_char == b'y' or input_char == b'\r':
				livereloader.running = False
				x.join()
				print("exiting")
			else:
				print("continuing")
				second_main()

if __name__ == "__main__":
	second_main()
import win32api
import win32gui
import win32con
import time
import cv2
from PIL import ImageGrab

WINDOW_TITLE = "Chrome"

# Get the coordinate of the window (up left)
def getGameWindowPosition(WINDOW_TITLE):
	# FindWindow(lpClassName=None, lpWindowName=None)  
	window = win32gui.FindWindow(None,WINDOW_TITLE)
	while not window:
		print('Failed to navigate the windows, wait 5s...')
		time.sleep(5)
		window = win32gui.FindWindow(None,WINDOW_TITLE)

	win32gui.SetForegroundWindow(window) # Put the window to the top
	pos = win32gui.GetWindowRect(window)
	print("Got window" + str(pos))
	return (pos[0],pos[1])

def getScreenImage():
    scim = ImageGrab.grab()
    scim.save('./screen.png')
    return cv2.imread("./screen.png") 


if __name__ == '__main__':
	pass
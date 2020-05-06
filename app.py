import numpy as np
from PIL import ImageGrab
import cv2
import time
import pyautogui
import glob
import webbrowser
import mss

DINO_FILE='utilities/img/dino.png'
GAME_URL='https://elgoog.im/t-rex/'

# convert image color from Blue green red to gray
def process_img(image):
	original_image = image
	# convert to gray
	processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	return processed_img

# Detect face dino
def detect_dino():
	last_time = time.time()
	dino = cv2.imread(DINO_FILE,0)
	w_dino, h_dino = dino.shape[::-1]
	bottom_right = (0,0)
	while True:
		sct = mss.mss()
		mon = {"top": 300, "left": 500, "width": 500, "height": 170}
		screen =  np.asarray(sct.grab(mon))
		new_screen = process_img(screen)
		res_dino = cv2.matchTemplate(new_screen, dino, cv2.TM_CCOEFF_NORMED)
		dino_min_val, dino_max_val, dino_min_loc, dino_max_loc = cv2.minMaxLoc(res_dino)
		bottom_right = (dino_max_loc[0] + w_dino, dino_max_loc[1] + h_dino)
		cv2.rectangle(new_screen, dino_max_loc, bottom_right, 255, 2)
		cv2.imshow('window', new_screen)

		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break
	return bottom_right

def main():
	webbrowser.open(GAME_URL)
	bottom_right = detect_dino()
	offset = 0
	timeleft = time.time()
	sct = mss.mss()
	mon = {"top":300+ bottom_right[1]/2, "left": 500+bottom_right[0]/2, "width": 100, "height": 20}
	screen1 =  np.asarray(sct.grab(mon))
	while True:
		# OFFSET
		# if time.time() - timeleft >= 10 and offset < 200:
		# 	timeleft = time.time()
		# 	offset = 30
		# 	print("enter")
		# 	mon = {"top":300+ bottom_right[1]/2, "left": 500+bottom_right[0]/2, "width": 100+offset, "height": 20}
		# 	screen1 =  np.asarray(sct.grab(mon))
		sct = mss.mss()
		mon = {"top":300+ bottom_right[1]/2, "left": 500+bottom_right[0]/2, "width": 100+offset, "height": 20}
		screen =  np.asarray(sct.grab(mon))

		last_time = time.time()
		new_screen = process_img(screen)
		cv2.imshow('window', new_screen)

		if not np.array_equal(screen, screen1):
			pyautogui.press('space')

		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break
if "__main__" == __name__:
	main()

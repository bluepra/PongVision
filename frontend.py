import pygame as py
import cv2 as cv

WIDTH, HEIGHT = 900, 500

WIN = py.display.set_mode((WIDTH, HEIGHT))

cap = cv.VideoCapture(0)
cap.set(3, WIDTH)  # Width
cap.set(4, HEIGHT)  # Height

# main loop in game
def main():

    run = True
    while run:
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False

    py.QUIT()


main()
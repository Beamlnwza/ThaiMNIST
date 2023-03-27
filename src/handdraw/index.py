import cv2
import numpy as np
import os
import random

store_unit = os.path.join(os.getcwd(), "data", "raw")

# Define the size of the image
dimision = random.randint(50, 100)
img_size = (dimision, dimision)

# Define the list of alphabets to be drawn
alphabet_range = 44
--alphabet_range
alphabet = list(range(0, alphabet_range))
alphabets = [str(x) for x in alphabet]
# alphabets = ['1']

# Random brush size
brush_size = 2


# Function to handle mouse events
def draw_circle(event, x, y, flags, param):
    global prev_x, prev_y
    if event == cv2.EVENT_LBUTTONDOWN:
        prev_x, prev_y = x, y
    elif event == cv2.EVENT_MOUSEMOVE and flags & cv2.EVENT_FLAG_LBUTTON:
        cv2.line(img, (prev_x, prev_y), (x, y), (0, 0, 0), brush_size)
        prev_x, prev_y = x, y


# Provide size of box that cover in THAIAlphabets.jpg
rec_size = 42


# Start points and end points of box
def startpoints(nums):
    x = nums % 8 * rec_size
    y = rec_size * (nums // 8)

    return (x, y)


def endpoints(nums):
    return ((nums % 8) + 1) * rec_size, rec_size * ((nums // 8) + 1)


# Loop through the list of alphabets
if __name__ == "__main__":
    for alphabet in alphabets:
        path = os.path.join(store_unit, alphabet)
        # Initialize the image with white color
        img = 255 * np.ones(img_size + (3,), dtype=np.uint8)

        # Program to make find lastest and set numbers to that number
        num_path = os.path.join(store_unit, alphabet)
        if not os.path.exists(num_path):
            lastest_number = "0"
        else:
            lastest_number = str(len(os.listdir(num_path)))

        # Create a window for drawing
        window_text = (
            alphabet
            + " - "
            + lastest_number
            + " - "
            + str(img_size)
            + " - brush : "
            + str(brush_size)
        )

        cv2.namedWindow(alphabet, cv2.WINDOW_GUI_EXPANDED)
        cv2.resizeWindow(alphabet, 800, 800)
        cv2.setWindowTitle(alphabet, window_text)

        # Bind the function to the window
        cv2.setMouseCallback(alphabet, draw_circle)

        thai = os.path.join(os.getcwd(), "src", "handdraw", "THAlphabets.jpg")
        img_alpha = cv2.imread(thai)

        cv2.rectangle(
            img_alpha,
            startpoints(int(alphabet)),
            endpoints(int(alphabet)),
            (0, 0, 255),
            3,
        )

        # Loop until user presses 'q'
        while True:
            cv2.imshow("Thai", img_alpha)
            cv2.imshow(alphabet, img)
            cv2.moveWindow(alphabet, 450, 75)

            if cv2.waitKey(20) & 0xFF == ord("r"):
                img = 255 * np.ones(img_size + (3,), dtype=np.uint8)

            if cv2.waitKey(20) & 0xFF == ord("q"):
                break

        # Check if the directory for the alphabet exists, and create it if it doesn't
        if not os.path.exists(path):
            os.makedirs(path)

        # Resize the image to 28x28
        img = cv2.resize(img, (28, 28))

        # Save the image to the directory if it is not blank
        # print(os.path.join(path, alphabet + ".jpg"))
        if np.mean(img) != 255:
            cv2.imwrite(os.path.join(num_path, lastest_number + ".jpg"), img)

        # Destroy the window
        cv2.destroyAllWindows()

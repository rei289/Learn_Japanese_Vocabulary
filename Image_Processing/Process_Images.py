"""
This file deals with processing the images into data which can be added to the csv file
"""
from PIL import Image
from datetime import datetime
import pytesseract
import os

class ImageProcess:
    """
    This class extracts data from the images
    """
    def __init__(self):
        """
        Initialize the class
        """
        pass

    def extractData(self) -> str:
        """
        This function extracts the data from images
        returns the name for data file
        """
        # first create a folder containing data
        # get time
        now = datetime.now()
        day = now.strftime("%m_%d")
        current_time = now.strftime("%H_%M_%S")

        # generate data folder for save result
        if not os.path.exists("Data"):
            os.mkdir("Data")

        global picFolder
        picFolder = "Data/{}_{}".format(day, current_time)

        if not os.path.exists(picFolder):
            os.mkdir(picFolder)

        # find the file name for all images needed for extracting data
        img = os.listdir("Image_Processing/Images/")

        # extract data for each image
        for i in range(len(img)):
            # find the image folder
            image_path = f"Image_Processing/Images/{img[i]}"

            # Opening the image & storing it in an image object
            img = Image.open(image_path)

            # Passing the image object to image_to_string() function
            # This function will extract the text from the image
            text = pytesseract.image_to_string(img, lang='jpn')

            # Displaying the extracted text
            print(text[:-1])

        return f"{day}_{current_time}"

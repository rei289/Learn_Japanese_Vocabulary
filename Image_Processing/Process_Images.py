"""
This file deals with processing the images into data which can be added to the csv file
"""
from PIL import Image
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

    def extractData(self) -> None:
        """
        This function extracts the data from images
        """
        # find the file name for all images needed for extracting data
        img = os.listdir("Image_Processing/Images/")

        # extract data for each image
        for i in range(len(img)):
            # find the image folder
            image_path = f"Image_PRocessing/Images/{img[i]}"

            # Opening the image & storing it in an image object
            img = Image.open(image_path)

            # Passing the image object to image_to_string() function
            # This function will extract the text from the image
            text = pytesseract.image_to_string(img, lang='jpn')

            # Displaying the extracted text
            print(text[:-1])

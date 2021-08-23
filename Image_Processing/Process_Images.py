"""
This file deals with processing the images into data which can be added to the csv file
"""
from PIL import Image
from datetime import datetime
from Image_Processing.Write_Log import openLog, closeLog, writeLog, showMessage
from typing import Tuple, List, Union
import pytesseract
import os

def extractData() -> str:
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
    image = os.listdir("Image_Processing/Images/")

    # extract data for each image
    for i in range(len(image)):
        # find the image folder
        image_path = f"Image_Processing/Images/{image[i]}"

        # Opening the image & storing it in an image object
        img = Image.open(image_path)

        # Passing the image object to image_to_string() function
        # This function will extract the text from the image
        text = pytesseract.image_to_string(img, lang='jpn')

        # Displaying the extracted text
        data = text[:-1]

        # organize the data into a dictionary
        # find the word in image
        word = findWord(data)
        # find meaning in image
        # meaning = findMeaning(data)

        # determine if word is kanji or kotoba
        if len(word) == 1:
            dict = {"漢字": word}
        else:
            dict = {"言葉": word}

        # showMessage(data)
        showMessage(word)

    return f"{day}_{current_time}"

def find(string:str, char:str) -> List[int]:
    """
    This function finds all targeted characters in a string and returns a list of indexes
    """
    return [i for i, ltr in enumerate(string) if ltr == char]

def findWord(data: str) -> str:
    """
    This function finds the word in the data
    """
    # find the 【 and 】string
    indStart = find(data,'【')
    indEnd = find(data,'】')

    # slice that string
    word = data[int(indStart[0]+1):indEnd[0]]
    return word

def findMeaning(data: str) -> str:
    """
    This function finds the meaning in the data
    """
    # two cases
    # if 》string exists, then meaning is string after this string
    if data.find('》') != -1:
        indStart = data.find('》')
        indEnd = data.find('「')
    # if 》string does not exist, then meaning is string after 】
    else:
        indStart = data.find('】')
        indEnd = data.find('】')

    # slice that string
    word = data[int(indStart+1):indEnd]

    # lastly, remove new lines
    word = word.replace('\n', '')
    return word

# class ImageProcess:
#     """
#     This class extracts data from the images
#     """
#     def __init__(self):
#         """
#         Initialize the class
#         """
#         pass
#
#     def extractData(self) -> str:
#         """
#         This function extracts the data from images
#         returns the name for data file
#         """
#         # first create a folder containing data
#         # get time
#         now = datetime.now()
#         day = now.strftime("%m_%d")
#         current_time = now.strftime("%H_%M_%S")
#
#         # generate data folder for save result
#         if not os.path.exists("Data"):
#             os.mkdir("Data")
#
#         global picFolder
#         picFolder = "Data/{}_{}".format(day, current_time)
#
#         if not os.path.exists(picFolder):
#             os.mkdir(picFolder)
#
#         # find the file name for all images needed for extracting data
#         img = os.listdir("Image_Processing/Images/")
#
#         # extract data for each image
#         for i in range(len(img)):
#             # find the image folder
#             image_path = f"Image_Processing/Images/{img[i]}"
#
#             # Opening the image & storing it in an image object
#             img = Image.open(image_path)
#
#             # Passing the image object to image_to_string() function
#             # This function will extract the text from the image
#             text = pytesseract.image_to_string(img, lang='jpn')
#
#             # Displaying the extracted text
#             data = text[:-1]
#
#             # organize the data into a dictionary
#             # find the kanji in image
#
#             kan = self.findWord(data)
#             # dict = {"漢字"}
#             showMessage(data)
#             showMessage(kan)
#
#         return f"{day}_{current_time}"
#
#     def findWord(self, data: str) -> str:
#         """
#         This function finds the word in the data
#         """
#         # find the 【 string
#         indStart = data.find('【')
#         indEnd = data.find('】')
#
#         # slice that string
#         word = data[indStart:indEnd]
#         return word

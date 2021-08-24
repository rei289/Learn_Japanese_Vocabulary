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

    if '.DS_Store' in image:
        image.remove('.DS_Store')

    showMessage(image)

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
        pronunciation = findPronunciation(data, word)

        # determine if word is kanji or kotoba
        if len(word) == 3:
            dict = {"漢字": word, "読み方": pronunciation}
        else:
            dict = {"言葉": word, "読み方": pronunciation}

        # showMessage(data)
        # showMessage(word)
        showMessage(pronunciation)


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
    # find the 【 and 】string　or 〖 and 〗string
    # either one will work
    # if 【 or 】string doesn't exist in the image, try the 〖 and 〗string
    if data.find('【') == -1 or data.find('】') == -1:
        indStart = find(data, '〖 ')
        indEnd = find(data, '〗')
    else:
        indStart = find(data,'【')
        indEnd = find(data,'】')

    # if both 【 and 】string　and〖 and 〗string doesn't exist, means image not properly take
    if len(indStart) == 0 or len(indEnd) == 0:
        raise RuntimeError("Image not properly taken")

    # # if the length of indStart and indEnd is more than 1, that most likely means it is a kanji
    # # we will compare the strings
    # if len(indStart) == len(indEnd) and len(indStart) > 1:
    #     words = [data[indStart[i]+1:indEnd[i]]for i in range(len(indStart))]

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
    meaning = data[int(indStart+1):indEnd]

    # lastly, remove new lines
    meaning = meaning.replace('\n', '')
    return meaning

def findPronunciation(data: str, word: str) -> str:
    """
    This function finds the meaning in the data
    """
    # 2 cases
    # if kotoba, then pronunciation will start with a ?
    # if kanji, then multiple pronunciation starting from 〗
    # for kotoba
    # showMessage(len(word))

    if len(word) != 3:
        string = '?'

    else:
        # locate 〗
        start = find(data, '】')
        # get the first index
        start = min(start)

        # now check to see if string after 〗is (
        if data[start+1] == "(":
            string = ")"
        else:
            string = "】"


    # find the indices for start and end
    indStart = find(data, string)
    indEnd = find(data, '\n')
    # we can assume the first index is the correct index for indStart
    indStart = indStart[0]
    # now find the closest index that is larger than indStart
    possibleIndEnd = [ind for ind in indEnd if ind > indStart]
    absolute_difference_function = lambda list_value: abs(list_value - indStart)
    indEnd = min(possibleIndEnd, key=absolute_difference_function)

    # get pronunciation
    pronunciation = data[indStart+1:indEnd]

    # if kanji, we need to separate into 2 sections
    if len(word) == 3:
        # for onyomi
        regex = {"from": ord(u"\u30a0"), "to": ord(u"\u30ff")}
        kata = [regex["from"] <= ord(pronunciation[i]) <= regex["to"] for i in range(len(pronunciation))]
        # find all the places that are listed as TRUE
        indOn = find(kata, True)
        # now find min and max of the indices
        indStart = min(indOn)
        indEnd = max(indOn)



    return pronunciation

def findEnglish(data: str, word: str) -> str:
    """
    This function finds the english translation in the data
    """


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

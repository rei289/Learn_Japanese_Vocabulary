"""
This file deals with processing the images into data which can be added to the csv file
"""
from PIL import Image
from datetime import datetime
from Image_Processing.Write_Log import openLog, closeLog, writeLog, showMessage
from typing import Tuple, List, Union, Dict
import pytesseract
import os
import pandas as pd
import csv

def writeFile(shorten=True):
    """
    This function writes the extracted data from images into a file
    """
    # first create a folder containing data
    # get time
    now = datetime.now()
    day = now.strftime("%m_%d")
    current_time = now.strftime("%H_%M_%S")

    # generate data folder for save result
    if not os.path.exists("Image_Processing/Data"):
        os.mkdir("Image_Processing/Data")

    # global picFolder
    # picFolder = "Image_Processing/Data/{}_{}".format(day, current_time)
    #
    # if not os.path.exists(picFolder):
    #     os.mkdir(picFolder)

    # create a csv file if already doesn't exist
    if not os.path.exists("Image_Processing/Data/Data.csv"):
        openLog(f'Image_Processing/Data/Data.csv')

        # csv header
        fieldnames = ["漢字", "言葉", "読み方 (音|訓)", "英語", "意味", "例文"]

        with open('Image_Processing/Data/Data.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

    # openLog(f'Image_Processing/Data/{day}_{current_time}/Data.csv')

    # find the file name for all images needed for extracting data
    image = os.listdir("Image_Processing/Images/")

    # remove file called DS_Store
    if '.DS_Store' in image:
        image.remove('.DS_Store')

    # initialize df
    df = pd.read_csv("Image_Processing/Data/Data.csv")
    # extract data for each image
    for i in range(len(image)):
        # initialize list
        list_data = []

        # find the image folder
        image_path = f"Image_Processing/Images/{image[i]}"

        # extract data
        data = extractData(image_path, shorten).items()

        # append it to list
        data = [string[1] for string in data]

        # if kanji, then second should be blank, else the first should be blank
        if len(data[0]) == 1:
            data.insert(1, '')
        else:
            data.insert(0, '')

        # showMessage(data)

        df2 = pd.DataFrame([data], columns=["漢字", "言葉", "読み方 (音|訓)", "英語", "意味", "例文"], index=[i+0.5])
        df = df.append(df2, ignore_index=False)
        df = df.sort_index().reset_index(drop=True)

        df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)

        df.to_csv("Image_Processing/Data/Data.csv")

        # now move the image from images to used_images




        # df2 = pd.DataFrame(ls, columns=["漢字", "言葉", "読み方 (音|訓)", "英語", "意味", "例文"], index=[nindx])

        # # write data into file
        # writeLog(data)

        # write data into list
        list_data.append(data)

    # # csv header
    # fieldnames = ["", "漢字", "言葉", "読み方 (音|訓)", "英語", "意味", "例文"]
    #
    # with open(f'Image_Processing/Data/{day}_{current_time}/Data.csv', 'w', newline='') as f:
    #     writer = csv.DictWriter(f, fieldnames=fieldnames)
    #     writer.writeheader()
    #     writer.writerows(list_data)



def extractData(image_path: str, shorten: bool) -> Dict[str, str]:
    """
    This function extracts the data from images
    returns the name for data file and dictionary containing all the information necessary
    """
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
    meaning = findMeaning(data, shorten)
    # find pronunciation in image
    pronunciation = findPronunciation(data, word)
    # find english translation in image
    english = findEnglish(data)
    # find example in image
    example = findExample(data, word)

    # determine if word is kanji or kotoba, then append it to dictionary
    if len(word) == 1:
        dict = {"漢字": word,
                "読み方 (音|訓)": pronunciation,
                "英語": english,
                "意味": meaning,
                "例文": example}
    else:
        dict = {"言葉": word,
                "読み方 (音|訓)": pronunciation,
                "英語": english,
                "意味": meaning,
                "例文": example}

    # finally, return the information
    return dict

def find(string:str, char:str) -> List[int]:
    """
    This function finds all targeted characters in a string and returns a list of indexes
    """
    return [i for i, ltr in enumerate(string) if ltr == char]

def lines(string:str) -> List[int]:
    """
    This function finds start and end index for each line 
    """
    # find all index with new lines
    return find(string, '\n')

def symbol_line_location(string:str, sym: str, move=0, addLast=False) -> List[Tuple[int, ...]]:
    """
    This function finds all lines where the symbol exists
    """
    # find the line after 】
    symbol = find(string, sym)

    # initialize line
    line = [0]
    # find index of lines
    lin = lines(string)

    for i in lin:
        line.append(i)

    # subtract all numbers by 1
    line = [int(num - 1) for num in line]

    # find which line symbol is in
    # to do this, we will create a nested list, which will contain a tuple with starting and ending index
    lines_index = [(line[i] + 1, line[i + 1]) for i in range(len(line) - 1)]

    # only keep the indices that is below the symbol
    symbol_lines_index = [lines_index[i+move] for i in range(len(lines_index)) for j in range(len(symbol))
                          if lines_index[i][0] <= symbol[j] and lines_index[i][1] >= symbol[j]]
    if addLast:
        symbol_lines_index.append(lines_index[-1])
    return symbol_lines_index

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

    # slice that string
    word = data[int(indStart[0]+1):indEnd[0]]

    # lastly, get rid of spaces
    word = word.replace(" ", "")
    return word

def findMeaning(data: str, shorten: bool) -> str:
    """
    This function finds the meaning in the data
    """
    # # remove all spaces
    # data.replace(' ', '')

    # two cases
    # if 》string exists, then meaning is string after this string
    if data.find('》') != -1:
        # find the line after 》
        sym = '》'
        symbol_lines_index = symbol_line_location(data, sym, move=0, addLast=True)
        symbol = find(data, '》')

        # now find all places with period
        period = find(data, '。')

        # initialize meaning
        meaning = ''
        # add to the meaning
        for i in range(len(symbol)):
            indStart = symbol[i]
            indEnd = max([period[j] for j in range(len(period)) if (period[j] >= symbol_lines_index[i][1]
                                                                    and period[j] < symbol_lines_index[i + 1][0]) or
                          period[j] < symbol_lines_index[i][1]])

            single_meaning = data[int(indStart + 1):indEnd + 1]
            meaning += single_meaning

    # if 》string does not exist, then meaning is string after 】
    else:
        # find the line after 】
        sym = '】'
        symbol_lines_index = symbol_line_location(data, sym, move=1, addLast=True)

        symbol = find(data, '】')

        # now find all places with period
        period = find(data, '。')

        # initialize meaning
        meaning = ''
        # add to the meaning
        for i in range(len(symbol)):
            indStart = symbol_lines_index[i][0]
            indEnd = max([period[j] for j in range(len(period)) if (period[j] >= symbol_lines_index[i][1]
                          and period[j] < symbol_lines_index[i+1][0]) or period[j] < symbol_lines_index[i][1]])


            single_meaning = data[int(indStart + 1):indEnd+1]
            meaning += single_meaning

    # showMessage(symbol)
    # showMessage(line)
    # showMessage(lines_index)
    # showMessage(symbol_lines_index)
    # showMessage(period)

    # remove new lines
    meaning = meaning.replace('\n', '')

    # lastly, get rid of spaces
    meaning = meaning.replace(" ", "")

    # if we want to shorten, we will only take the first sentence
    if shorten:
        # find period
        period = find(meaning, '。')
        # take the first period
        meaning = meaning[0:period[0]]
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

    if len(word) != 1:
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

    # lastly, get rid of spaces
    pronunciation = pronunciation.replace(" ", "")

    # if kanji, we need to separate into 2 sections
    if len(word) == 1:
        # for onyomi
        # find all strings that are katakana
        regex = {"from": ord(u"\u30a0"), "to": ord(u"\u30ff")}
        kata = [regex["from"] <= ord(pronunciation[i]) <= regex["to"] for i in range(len(pronunciation))]
        # find all the places that are listed as TRUE
        indOn = find(kata, True)
        # now find min and max of the indices
        indStart = min(indOn)
        indEnd = max(indOn)
        onyomi = pronunciation[indStart:indEnd+1]
        # lastly, replace any ・ with ,
        onyomi.replace('・', '、')

        # for kunyomi
        # find all strings that are hiragana
        regex = {'from': ord(u'\u3040'), 'to': ord(u'\u309f')}
        hira = [regex["from"] <= ord(pronunciation[i]) <= regex["to"] for i in range(len(pronunciation))]
        # find all the places that are listed as TRUE
        indHi = find(hira, True)
        # now find min and max of the indices
        indStart = min(indHi)
        indEnd = max(indHi)
        kunyomi = pronunciation[indStart:indEnd+1]
        # lastly, replace any ・ with ,
        kunyomi.replace('・', '、')

        # lastly combine the 2 strings
        pronunciation = f"[音] {onyomi}\n[訓] {kunyomi}"


    return pronunciation

def findEnglish(data: str) -> str:
    """
    This function finds the english translation in the data
    """
    # remove all string leading up to the word Translate
    data = data[data.find('Translate'):len(data)]
    # initalize list
    english_list = []

    # find all english in the string
    number_list = [int(num) for num in data if num.isnumeric()]

    # remove 4
    number_list.remove(4)

    # find smallest and largest numbers
    small = min(number_list)
    large = max(number_list)

    # first find the string with number
    for i in range(small,large+1):
        # find the line after i
        sym = f"{i}"
        symbol_lines_index = symbol_line_location(data, sym, move=0, addLast=False)

        # find index for that specific number
        eng = find(data, f"{i}")

        # for each location, determine if the 2 higher index is an alphabet or not
        for j in range(len(eng)):
            # if it is, then take that line
            if data[eng[j]+3].isalpha():
                indStart = eng[j]+3
                indEnd = symbol_lines_index[j][1]

                english = data[indStart:indEnd+1]
                english_list.append(english)

    # lastly combine the words, separating each translation with /
    english = " / ".join(english_list)

    return english

def findExample(data: str, word: str) -> str:
    """
    This function finds the examples in the data
    """
    # find strings with 「 and 」
    start = find(data, '「')
    end = find(data, '」')

    # initialize a list that contains each example
    example_list = []
    for i in range(len(start)):
        example = data[int(start[i]+1):end[i]]
        # remove spacing
        example = example.replace(' ', '')
        # remove new lines
        example = example.replace('\n', '')

        if '一' in example or word in example:
            example_list.append(example)


    # finally, return the first element in list
    if len(example_list) > 0:
        return example_list[0]
    else:
        return ''



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

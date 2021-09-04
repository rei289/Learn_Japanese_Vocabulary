"""
This file deals with the running of both image processing and application programs
We can make separate programs in the future to separate image processing and application when transferring to phone
"""
# from Image_Processing.Process_Images import ImageProcess
from Image_Processing.Process_Images import writeFile
from Application.Japanese_Vocab import MyMainApp
def runProgram():
    """
    This function runs the whole program
    """
    # if we are going to use image processing, adding data from image processing, runApp, set them to true or false respectively
    application = False
    imageProcessing = True
    addProcessedData = False

    if application:
        runApp()

    if imageProcessing:
        runImageProcessing()

    if addProcessedData:
        runAddData()

def runApp():
    """
    This function runs the app
    """
    # run app
    MyMainApp().run()

def runImageProcessing():
    """
    This function runs the image processing
    """
    # initialize instance
    extract = writeFile()

def runAddData():
    """
    This function adds all the data from image processing into the csv file
    """
    pass

if __name__ == '__main__':
    runProgram()
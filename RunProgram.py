from Image_Processing.Process_Images import ImageProcess
from Application.Japanese_Vocab import MyMainApp
def runProgram():
    """
    This function runs the whole program
    """
    # if we are going to use image processing or runApp, set them to true or false respectively
    application = True
    imageProcessing = False

    if application:
        runApp()

    if imageProcessing:
        runImageProcessing()

def runApp():
    """
    This function runs the app
    """
    # create instance
    # app = MyMainApp
    MyMainApp().run()

def runImageProcessing():
    """
    This function runs the image processing
    """
    # initialize instance
    image = ImageProcess
    ImageProcess.extractData(image)

if __name__ == '__main__':
    runProgram()
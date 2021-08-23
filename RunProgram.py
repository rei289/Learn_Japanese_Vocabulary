from Image_Processing.Process_Images import ImageProcess
def runProgram():
    """
    This function runs the whole program
    """
    # if we are going to use image processing or runApp, set them to true or false respectively
    runApp = False
    imageProcessing = True

    if runApp:
        runApp()

    if imageProcessing:
        runImageProcessing()

def runApp():
    """
    This function runs the app
    """
    pass

def runImageProcessing():
    """
    This function runs the image processing
    """
    image = ImageProcess
    extract = ImageProcess.extractData(image)

if __name__ == '__main__':
    runProgram()
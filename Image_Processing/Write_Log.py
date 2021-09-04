from datetime import datetime
from typing import Dict, IO, List
import time
import csv

def openLog(log_name) -> None:
    """
    This function open a log file
    """
    global log
    log = open(log_name, "w")


def closeLog() -> None:
    """
    This function close the log file
    """
    showMessage("Start to close log")
    startTime = time.time()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    info = "Time: {}, {}\n".format(current_time, "Write log at last, start to write it")
    log.write(info)

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    info = "Time: {}, {}\n".format(current_time, "Write log at last done")
    log.write(info)

    endTime = time.time()
    totalTime = endTime - startTime

    showMessage(f"Total time it took to write log is {totalTime} seconds")

    log.close()


def writeLog(message) -> None:
    """
    This function write the message into log
    """
    # now = datetime.now()
    # current_time = now.strftime("%H:%M:%S")
    #
    # info = "Time: {}, {}\n".format(current_time, message)

    # # replace , with new line
    # message = str(message).replace(',', ', \n')
    # info = f"{message} \n \n"

    info = f"{message} \n"



    log.write(info)
        
def showMessage(message: str) -> None:
    """
    This function take in a message and print it to the screen and record into the log file
    """
    # print to screen
    print(message)
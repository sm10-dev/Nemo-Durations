import tkinter as tk
import re
import ffmpeg
import sys

def convertSectoDay(n): 
    '''
    utility function to convert seconds to day(s):hour(s):minute(s):second(s)
    '''

    #get no of days
    day = n // (24 * 3600) 
    
    #get no of hours
    n = n % (24 * 3600) 
    hour = n // 3600
    
    #get no of minutes
    n %= 3600
    minutes = n // 60
    
    #get no of seconds
    n %= 60
    seconds = n 
    
    #build and return output string  
    fString = str(int(day)) + " day(s) " + str(int(hour)) + " hour(s) " +  str(int(minutes)) + " minute(s) " + str(int(seconds)) + " second(s) "
    return fString

def get_duration(filePaths):
    '''
    Utility function to return total duration of all files as string
    '''
    durationStr = ''
    durations = []
    totalDuration = 0

    for filePath in filePaths:
        filePath = filePath.replace("{", "")
        filePath = filePath.replace("}", "")
        filePath = filePath.strip()
        
        try:
            info=ffmpeg.probe(filePath)
            durations.append(info['format']['duration'])
        except:
            durationStr += "Failed to get duration for: " + filePath + '\n'
        

    for duration in durations:
        totalDuration += float(duration)

    durationStr += convertSectoDay(totalDuration)

    return durationStr

def displayDuration(duration):
    '''
    utility function to display input string as a label in tkinter window
    '''

    #top level window
    root = tk.Tk()
    root.title("Audio/Video Files Total Duration")
    root.geometry('400x100')

    #show output
    durationLabel = tk.Label(root, text=duration)
    durationLabel.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    #display tkinter widget
    root.mainloop() 

if __name__ == '__main__':
    '''
    main execution function. First fetches the total duration as a string
    and then calls get_duration to display it in tkinter window
    '''
    filePathList = []
    n = len(sys.argv)
    for i in range(1, n):
        filePathList.append(sys.argv[i])

    outputStr = get_duration(filePathList)
    displayDuration(outputStr)
#Modules
import os
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from tkinter.ttk import *
import tkinter.ttk as ttk
from pygame import mixer
from subprocess import Popen, PIPE
from moviepy.editor import AudioFileClip
from moviepy.editor import VideoFileClip

#Global variables
ScreenStatus = False
MusicStatus = False
FilePath = None
FilePathOld=None
PlayingStatus = False
VolumeStatus = False
FileStatus = False
Duration = "Duration - 00:00:00"
self=None
infos=[]

# Initializing the mixer fucntion
mixer.init()

# Function definitions



def ScreenMode(self):
    global ScreenStatus


    l = []
    l.append(str(self))
    w = [words for segments in l for words in segments.split()]


    if (ScreenStatus == False and w[3]=='keysym=F11'):
        ScreenStatus = True
        BaseWindow.attributes('-fullscreen', ScreenStatus)


    if (ScreenStatus == True and w[3]=='keysym=Escape'):
        ScreenStatus = False
        BaseWindow.attributes('-fullscreen', ScreenStatus)

def LengthOfMedia(FilePath):
    global  Duration
    #global FilePath
    lDuration=AudioFileClip(FilePath)
    sDuration=lDuration.duration
    print(sDuration)

def PlayMusic():

    global MusicStatus
    global FilePath
    global PlayingStatus
    if MusicStatus == False:

        if PlayingStatus == False:

            try:

                # Loading music file from disk
                mixer.music.load(FilePath)

                # Playing the loaded music file using play function
                mixer.music.play()
                StatusBar["text"] = "Playing " + os.path.basename(FilePath)
                PlayingStatus = True

            except:
                # Printing error message if no music file is loaded or found
                tkinter.messagebox.showerror(
                    "Can't play",
                    "Not file is loaded to play\nPlease load music file before playing ",
                )
    else:
        mixer.music.unpause()
        StatusBar["text"] = "Resumed"
        MusicStatus = False
        PlayingStatus = True


# Function against the pause button widget
def PauseMusic():

    # Accessing global variables
    global MusicStatus
    global FilePath

    # if(MusicStatus == False):
    if FilePath is None:
        StatusBar["text"] = "Can't be paused"

    elif PlayingStatus == False:
        StatusBar["text"] = "Music isn't played yet"
    else:
        mixer.music.pause()
        StatusBar["text"] = "Paused"
        MusicStatus = True


# Function against the rewind button widget
def RewindMusic():

    # Accessing global variables
    global FilePath

    if FilePath is None:
        StatusBar["text"] = "Can't rewind"
    else:
        StatusBar["text"] = "Rewind successfully"
        mixer.music.rewind()


# Function against the stop button widget
def StopMusic():

    global FilePath
    global PlayingStatus

    if FilePath is None:
        StatusBar["text"] = "Can't Stop"
    else:
        mixer.music.stop()
        StatusBar["text"] = "Stopped " + os.path.basename(FilePath)
        PlayingStatus = False



# tkinter automatically pass a variable called val as a string
def SetVolume(val):

    # Dividing val by 100 because pygame mixer takes value from 0 to 1 only
    val = eval(val)
    VolumeValue = (val) / 100
    mixer.music.set_volume(VolumeValue)
    global VolumeStatus
    if val == 0:
        VolumeButton.configure(image=MuteButtonPicture)
        VolumeStatus = True
    if val > 75:
        VolumeButton.configure(image=UnmuteButtonPicture)
    if val >= 1 and val <= 75:
        VolumeButton.configure(image=MiddelVolumeLevelPicture)



def MuteVolume():
    global VolumeStatus
    if VolumeStatus == False:

        VolumeButton.configure(image=MuteButtonPicture)
        VolumeLevel.set(0)
        mixer.music.set_volume(0)
        VolumeStatus = True
    else:
        VolumeButton.configure(image=UnmuteButtonPicture)
        VolumeLevel.set(100)
        mixer.music.set_volume(1)
        VolumeStatus = False



def FielOpenDialog(self):

    global FilePath
    global FilePathOld
    global Duration
    global FileStatus
    print(self)
    FilePath = filedialog.askopenfilename()

    if len(FilePath)>0:
        FileStatus = True
        FilePathOld = FilePath
    LengthOfMedia(FilePath)

def About():
    tkinter.messagebox.showinfo("About", "Kumawat_infinity")



def Exit(self):
    #pass

    BaseWindow.destroy()

def GetDetails():
    global FilePath
    global FileStatus
    cmd = "hachoir-metadata"
    global infos

    if FileStatus == True:
        try:
            import hachoir

            MediaInfo = Popen([cmd, FilePath], stdout=PIPE, stderr=PIPE, universal_newlines=True)
            for info in MediaInfo.communicate():
                infos.append(info)

            tkinter.messagebox.showinfo("File details", str(infos[0]))

        except:
            tkinter.messagebox.showerror('Error', 'Please install hachoir python library')
    else:
        tkinter.messagebox.showerror("Unable to find details", "Please open atleast single music file")

def ThemeChange():
    pass
    s=ttk.Style()
    s.theme_names('clam')

# Creating the main window and this will created
# with in miliseconds and disappear quickly
BaseWindow = Tk()
# BaseWindow.attributes('-topmost',True)

BaseWindow.bind("<F11>", ScreenMode)
BaseWindow.bind("<Escape>", ScreenMode)
BaseWindow.bind("<Control-Key-o>", FielOpenDialog)
BaseWindow.bind("<Control-Key-O>", FielOpenDialog)
BaseWindow.bind('<F10>',Exit)


#MenuBar definition
MenuBar=Menu(BaseWindow)
#Fixing MenuBar
BaseWindow.config(menu=MenuBar)

#Adding Attributes to the MenuBar
#File Section
FileSection=Menu(MenuBar,tearoff=0)
MenuBar.add_cascade(label='File',menu=FileSection)

#Help Section
HelpSection=Menu(MenuBar,tearoff=0)
MenuBar.add_cascade(label='Help',menu=HelpSection)

#Drop down list for  File Section
FileSection.add_command(label='Open File',command=lambda : FielOpenDialog(self))
FileSection.add_command(label='Get Detailed Info',command=GetDetails)
FileSection.add_command(label='Exit',command=lambda : Exit(self))

#Drop down list for Help Section
HelpSection.add_command(label='About Us',command=About)

BaseWindow.resizable(0,0)

# Fixing default window size
BaseWindow.geometry("800x500")


# Adding title to the BaseWindow
BaseWindow.title("Infinity Music Player")

# Adding icon to the BaseWindow using iconbitmap function
# where r for raw string as a path of the icon file
BaseWindow.iconbitmap(r"MainWindowIcon.ico")

# Adding widgets inside the BaseWindow by using Label function
sometext = Label(BaseWindow, text="Kumawat_infinity")
# Packing sometext widget to the BaseWindow
sometext.pack()

# Creating picture object to store picture for the widget button
PlayButtonPicture = PhotoImage(file="Play.png")
PauseButtonPicture = PhotoImage(file="Pause.png")
RewindButtonPicture = PhotoImage(file="Rewind.png")
StopButtonPicture = PhotoImage(file="Stop.png")
MuteButtonPicture = PhotoImage(file="Mute.png")
UnmuteButtonPicture = PhotoImage(file="Unmute.png")
MiddelVolumeLevelPicture = PhotoImage(file="MiddleVolumeLevel.png")


# Adding status bar for music file, using relief to give sunken look to the statusbar
# By using anchor we fixing the position of the status bar in west by W
StatusBar = Label(
    BaseWindow,
    text="Cureent Status Okay\t\t\t\t\t\t" + Duration,
    relief=SUNKEN,
    anchor=W,
)

StatusBar.pack(side=BOTTOM, fill=X)


ControlFream = Frame(BaseWindow)
ControlFream.pack(side=BOTTOM)


PlayButton = Button(ControlFream, image=PlayButtonPicture, command=PlayMusic)

PlayButton.grid(row=0, column=0)

PauseButton = Button(ControlFream, image=PauseButtonPicture, command=PauseMusic)
PauseButton.grid(row=0, column=1)

RewindButton = Button(ControlFream, image=RewindButtonPicture, command=RewindMusic)
RewindButton.grid(row=0, column=2)

StopButton = Button(ControlFream, image=StopButtonPicture, command=StopMusic)
StopButton.grid(row=0, column=3)


VolumeButton = Button(ControlFream, image=UnmuteButtonPicture, command=MuteVolume)
VolumeButton.grid(row=0, column=5)

VolumeLevel = Scale(ControlFream, from_=0, to=100, orient=HORIZONTAL, command=SetVolume)

# Setting default volume level of scale to 100
VolumeLevel.set(100)
# Setting volume to high in backend side
mixer.music.set_volume(1)
VolumeLevel.grid(row=0, column=4)


BaseWindow.mainloop()

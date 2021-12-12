import tkinter
from pygame import mixer
import tkinter.messagebox
import tkinter.filedialog
import os
from mutagen.mp3 import MP3  # for checking the metadata of music file

# creating a window
window = tkinter.Tk()

# creating menubar
menubar = tkinter.Menu(window)
window.config(menu=menubar)


def browse_files():
    global filename
    filename = tkinter.filedialog.askopenfilename()  # file location will store in the filename
    # print(filename)


# creating submenu

subMenu1 = tkinter.Menu(menubar, tearoff=0)  # above we have given argument as window and here as menubar for submenu
menubar.add_cascade(label="FILE", menu=subMenu1)
subMenu1.add_command(label="Open", command=browse_files)
subMenu1.add_command(label="Exit", command=window.destroy)


def about_us():
    tkinter.messagebox.showinfo("ABOUT APPLICATION",
                                message="This is fully functional music player application, developed in python using tkinter and pyplay library")


subMenu2 = tkinter.Menu(menubar, tearoff=0)
menubar.add_cascade(label="HELP", menu=subMenu2)
subMenu2.add_command(label="About", command=about_us)

# mixer.init()       # to initialize mixer
mixer.init(33100, -16, 2, 512)  # frequency,size,channel,chunksize are the parameters

window.geometry("300x200")  # for size of window

window.title("Music")  # for title of window

# r stand for raw string , generally used for entering location
# title icon
window.iconbitmap(r"Images\music.ico")

# label is a widget act as container
# for text
text = tkinter.Label(window, text="Browse and Play")
text.pack(pady=10)

timeLabel = tkinter.Label(window, text="Total Length - --:--")
timeLabel.pack(pady=10)


# to change the top text into the song name

def show_details():
    text['text'] = "Playing " + os.path.basename(filename)

    file_data = os.path.splitext(filename)  # to split the extention and location of file and store into tuple

    # to calculate the length

    if file_data[1] == ".mp3":
        x = MP3(filename).info.length
        # print(x)
    else:
        x = mixer.Sound(filename).get_length()  # ---> only works on .wav or ogg file

    # dividing by 60, quotient inside mins and reminder inside secs
    mins, secs = divmod(x, 60)
    mins = round(mins)  # it will be in decimal so rounding it off
    secs = round(secs)

    timeformat = '{:02d}:{:02d}'.format(mins,
                                        secs)  # {:02d} means 2 digit integer if it is single digit place 0 at starting

    timeLabel['text'] = "Total Length - " + timeformat


def play_fun():
    global paused
    if paused is True:  # to check whether the paused is initialized or not
        mixer.music.unpause()
        statusBar['text'] = "Playing " + os.path.basename(filename)
        paused = False
    else:
        try:
            mixer.music.load(filename)
            mixer.music.play()
            statusBar['text'] = "Playing " + os.path.basename(filename)
            show_details()
        except:
            tkinter.messagebox.showerror("file not found", "Please Select a track first.")
            print("ERROR")


paused = False


def pause_fun():
    global paused
    paused = True
    mixer.music.pause()
    statusBar['text'] = "Paused"


def stop_fun():
    mixer.music.stop()
    statusBar['text'] = "Stopped"


def volume_fun(val):
    value = int(val) / 100  # because mixer's set_value only takes volume from 0 to 1
    mixer.music.set_volume(value)


middle_frame = tkinter.Frame(window)
middle_frame.pack(padx=15, pady=10)  # pack and grid are layout manager

# for play
play = tkinter.PhotoImage(file="Images\play_button (1).png")
play_btn = tkinter.Button(middle_frame, image=play, command=play_fun)  # calling function play when btn pressed
play_btn.pack(side=tkinter.LEFT, padx=7)

# for pause
pause = tkinter.PhotoImage(file="Images\play_button (2).png")
pause_btn = tkinter.Button(middle_frame, image=pause, command=pause_fun)
pause_btn.pack(side=tkinter.LEFT, padx=7)

# for stop
stop = tkinter.PhotoImage(file="Images\stop.png")
stop_btn = tkinter.Button(middle_frame, image=stop, command=stop_fun)
stop_btn.pack(side=tkinter.LEFT, padx=7)

# to switch bw the vol pic
vol_btn = False


def mute_vol():
    global vol_btn
    if vol_btn is False:
        vol_icon.configure(image=novol_pic)
        mixer.music.set_volume(0)
        scale.set(0)
        vol_btn = True
    else:
        vol_icon.configure(image=vol_pic)
        mixer.music.set_volume(1)
        scale.set(60)
        vol_btn = False


# frame for scale and vol pic
volume_frame = tkinter.Frame(window)
volume_frame.pack()

# volume icon
vol_pic = tkinter.PhotoImage(file="Images\\volume.png")
novol_pic = tkinter.PhotoImage(file="Images\\no_sound.png")
vol_icon = tkinter.Button(volume_frame, image=vol_pic, command=mute_vol)
vol_icon.grid(row=0, column=0, padx=5)

# to control volume of music
scale = tkinter.Scale(volume_frame, from_=0, to=100, orient=tkinter.HORIZONTAL, command=volume_fun)
scale.set(60)  # by default scale starts from 0 ,so we set it to 60
mixer.music.set_volume(0.60)  # same thing with volume, like scale
scale.grid(row=0, column=4)

statusBar = tkinter.Label(window, text="Welcome...", relief=tkinter.SUNKEN, anchor=tkinter.W)
statusBar.pack(side=tkinter.BOTTOM, fill=tkinter.X)

# window will be seen for very less time so we use mainloop
window.mainloop()

# open file manager to ask for download location || done
import customtkinter as ctk
from pytube import YouTube
import os
import time
# resolutions_selected=0
#    https://youtu.be/Zrd9B2KtUdI?si=FVysjdHKINly20Wz
#       https://youtu.be/0hEmxOEeVO0
#       https://youtu.be/NLKwRW2y-sg?si=KhqBTvt4TYzvTvGX

download_path=0
prev_done=0
prev_time=time.time()

# selecting file location
def select_path():
    root=ctk.CTk()
    root.withdraw()  # Hide the main window
    folder_path = ctk.filedialog.askdirectory(title="Select Folder")
    if folder_path:
        print(f"Selected path: {folder_path}")
        global download_path
        download_path=folder_path
    else:
        print("No path selected ")

def download_video():
    status_label.configure(text="  Analyzing the link  ",text_color="black",fg_color="white") # resetting status
    status_label.update()
    # time.sleep(1)
    global resolutions_selected,prev_time,download_path,total_size
    
    if not download_path:
        select_path()
    prev_time=time.time()
    url=entry_url.get()
    print("download : ",url,"\tres : ",resolutions_variable.get())

    title_label.pack(padx=10,pady=7)
    # downloading_speed_label.pack(padx=4,pady=1)

    try:
        # getting the video
        yt_object=YouTube(url,on_progress_callback=uppdate_progress)
        if resolutions_selected=="mp3":
            print("Audio : ",resolutions_selected)
            stream_object=yt_object.streams.filter(only_audio=True).first()
            os.path.join(download_path,f"{yt_object.title}.mp3")
        else:
            stream_object=yt_object.streams.filter(res=resolutions_selected).first()
            os.path.join(download_path,f"{yt_object.title}.mp4")


        # resetting progress
        title_label.configure(text=f"{yt_object.title}  \n\nSize :  {int(stream_object.filesize/(1024*1024) *100)/100} MB  ",text_color="black")
        time.sleep(0.6)
        progress_bar.set(0)
        print("downloading : ",yt_object.title,"\tres : ",resolutions_variable.get() ," SIZE : ",int(stream_object.filesize/(1024*1024) *100)/100)
        # print(yt_object.title)

        # downloading in a specific path
        
        output_file=stream_object.download(output_path=download_path)

        # change extension for mp3 & save the file 
        if resolutions_selected=="mp3":
            base, ext = os.path.splitext(output_file) 
            new_file = base + '.mp3'
            os.rename(output_file, new_file) 
        # time.sleep(1)
        status_label.configure(text="  Downloaded Successfully  ",text_color="white",fg_color="green")
        print("downloaded ")
        progress_label.configure(text=str(int(100))+"%")
        progress_label.update()
        progress_bar.set(1)

    # showing progress
        progress_label.pack(padx=10,pady=5)
        progress_bar.pack(padx=10,pady=5)
    except Exception as e:
        print("Error downloading : ",e)
        # status_label.configure(text=f" Error : {str(e)} ",text_color="black",fg_color="yellow") # exact
        status_label.configure(text=f" Invalid link or resolution ",text_color="black",fg_color="yellow") # 
        # progress_bar.set(0)
    status_label.pack(padx=10,pady=5)

def uppdate_progress(stream,chunk,remaining_bytes):
    
    total_size=stream.filesize
    bytes_downloaded=total_size-remaining_bytes
    percentage_downloaded=bytes_downloaded/total_size*100
    print(percentage_downloaded)
    progress_label.configure(text=str(int(percentage_downloaded))+"%")
    progress_label.update()
    # progress_bar.set(0.6)
    progress_bar.set(float(percentage_downloaded/100)) # [0,1]

    #Downloading speed
    speed,time_left=downloading_speed(bytes_downloaded,total_size)
    status_label.configure(text=f"  Downloading Speed : {speed} MB/s  Estimated time : {time_left} ",text_color="black",fg_color="white")
    status_label.update()

def downloading_speed(done,total_size):
    global prev_done,prev_time
    current_time=time.time()
    speed=(done-prev_done)/(current_time-prev_time) # KB/s
    prev_done,prev_time=done,current_time

    sec=int((total_size-done)/speed)  # seconds
    time_left=f"{sec} sec "

    if sec>=60:
        min=int(sec/60) # min
        sec=sec%60 
        time_left=f"{min} min {sec} sec "
        if min>=60:
            hour=int(min/60) # hour
            min=min%60
            time_left=f"{hour} hour {min} min "
            if hour>=24:
                day=hour/24 # day
                hour=hour%24
                time_left=f"{day} day {hour} hour "



    speed=int(speed/10000)/100 # mbps

    return speed,time_left

def resolution_video(choice):
    global resolutions_selected

    resolutions_selected=choice
    print("resolution : ",choice)
    # print("resolution 2 : ",resolutions_selected)
    # print("resolution 3 : ",resolutions_variable.get())

# create a root window
root=ctk.CTk()
ctk.set_appearance_mode("system")  # default
ctk.set_default_color_theme("blue")

# icon
icon_path = './icons/movie.ico'
root.iconbitmap(default=icon_path)

# title of the window
root.title("Youtube Downloader")

# set min max size of window
root.geometry("720x480")
root.minsize(720,480)
root.maxsize(root.winfo_screenwidth(),root.winfo_screenheight())

# create content frame
content_frame=ctk.CTkFrame(root)
content_frame.pack(fill=ctk.BOTH,expand=True,padx=10,pady=10)

# create a label and the entry widget for the video url
url_label=ctk.CTkLabel(content_frame,text="Enter the youtube link here : ")
entry_url=ctk.CTkEntry(content_frame,width=400,height=40)
url_label.pack(padx=10,pady=10)
entry_url.pack(padx=10,pady=5)

# Create download button
download_button=ctk.CTkButton(content_frame,text="Download",command=download_video)
download_button.pack(padx=10,pady=5)

# create resolution combo box
resolutions=["1080p","720p","480p","360p","240p","mp3"]
resolutions_selected=resolutions[1]
resolutions_variable=ctk.StringVar(value=resolutions_selected)
resolution_combobox=ctk.CTkComboBox(content_frame,values=resolutions,command=resolution_video,variable=resolutions_variable)
resolutions_variable.set(resolutions_selected)
resolution_combobox.pack(padx=10,pady=5)


# show title of the video
title_label=ctk.CTkLabel(content_frame,text=None)

# show downloading speed
downloading_speed_label=ctk.CTkLabel(content_frame,text=None)

# create progress bar & label to display download %
progress_label=ctk.CTkLabel(content_frame,text="0 %")
# progress_label.pack(padx=10,pady=5)

progress_bar=ctk.CTkProgressBar(content_frame,width=400)
# progress_bar.set(0)
# progress_bar.pack(padx=10,pady=5)

# Status label
status_label=ctk.CTkLabel(content_frame,text="Downloaded")
# status_label.pack(padx=10,pady=5)

# start the app

def on_close():
    root.destroy()  # Close the Tkinter window
    exit()          # Exit the script


# Your GUI code here

# Register the on_close function to be called when the window is closed
root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()



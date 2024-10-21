import customtkinter as ctk
from PIL import Image, ImageDraw
from tkinter import filedialog
import os
import shutil

from Tools.Google_API import get_user_info
from Tools.get_playlist import get_playlist_urls, get_user_playlists
from Tools.download_data import get_thumbnail, get_mp3

playlist_to_show = ["Select a playlist"]

def make_circle(image_path, size=(50, 50)):
    if not os.path.exists(image_path):
        image_path = "assets/default_profile.jpg"  # Use a default image if path is invalid
    
    # Open the image and resize it
    img = Image.open(image_path).resize(size, Image.Resampling.LANCZOS)

    # Create a circular mask
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)

    # Apply the mask to the image
    img.putalpha(mask)

    return img

def login(profile_pic_label):
    info = get_user_info()
    global user
    user = {
        "name": info["nickname"],
        "email": info['email'],
        "profile_pic_path": info["profile_pic_path"],
        "out_path": "Please choose a folder",
        "playlist": None,
    }

    # Create and update the profile picture
    profile_image = make_circle(user["profile_pic_path"])

    # Create a new CTkImage
    profile_pic = ctk.CTkImage(dark_image=profile_image, size=(35, 35))
    
    # Update the label's image
    profile_pic_label.configure(image=profile_pic)
    profile_pic_label.image = profile_pic  # Keep a reference to avoid garbage collection
    profile_pic_label.pack(side="left", padx=(10, 0))  # Pack the label
    get_playlists()

def logout(profile_pic_label):
    global user
    user = {
        "name": "",
        "email": "",
        "profile_pic_path": "",
        "out_path": "Please choose a folder",
        "playlist": None,
    }
    profile_pic_label.pack_forget()
    os.remove("Tools/Google/token.pickle")
    print("TRY")

def handle_login_logout(profile_pic_label, username_label, email_label, playlist_chooser):
    if user["name"] == "":
        # Login actions
        login(profile_pic_label)
        username_label.configure(text=user["name"])
        email_label.configure(text=user["email"])
        print(playlist_to_show)
        # playlist_chooser.forget()
        playlist_chooser.configure(values=playlist_to_show)
    else:
        # Logout actions
        logout(profile_pic_label)
        username_label.configure(text="")
        email_label.configure(text="")
        # playlist_chooser.forget()
        playlist_chooser.configure(values=["Select a playlist"])
        # login_bnt.configure(text="Login")
        for widget in video_panel.winfo_children():
            widget.destroy()

def get_playlists():
    global playlists_for_dropdown, playlist, playlist_to_show
    playlists = get_user_playlists()
    print(playlists)

    playlist_to_show = ["Select a playlist"]
    playlists_for_dropdown = {}
    for playlist in playlists:
        playlists_for_dropdown[playlist["title"]] = playlist["id"]
        playlist_to_show.append(playlist["title"])
    print(playlists_for_dropdown)

    print(playlist_to_show)

def add_tab(vid):
    # Load the image from the specified path
    title = vid["title"]

    if title == "[Video Unavailable]":
        vid["thumbnail"] = "assets/video_unavailable.png"

    tn_path = vid["thumbnail"]


    # Create a new frame for the new panel
    new_frame = ctk.CTkFrame(
        master=video_panel,
        width=400,
        height=100,
        corner_radius=50,
        fg_color="#444444",
    )
    new_frame.pack(pady=5, fill="x", expand=False)  # Fill the width of the scrollable frame

    
    # Create a label to hold the CTkImage and pack it
    tn_label = ctk.CTkLabel(
        master=new_frame,  # Make sure scrollable_frame is defined in your context
        text="",
        image=ctk.CTkImage(
            dark_image=Image.open(tn_path),  # Use the PIL image directly
            size=(144, 81)),
        corner_radius=50,
    )
    tn_label.pack(side="left", padx=25, pady=10)  # Pack the label into the scrollable frame

    max_letters = 35
    out = ""
    for letter in title:
        if max_letters == 0:
            out += "..."
            break
        out += letter
        max_letters -= 1


    # Add a label with the random name
    title_label = ctk.CTkLabel(
        master=new_frame,
        text=out,
        text_color="white",
        justify="right",
        width=50,
        height=20,
        font=("Arial", 20),
        # anchor="e"
    )
    title_label.place(x = -100, y = -10, relx=0.5, rely=0.5)  # Center the label in the frame

def add_tabs(playlist_id):
    # print(playlist_id)
    videos = get_playlist_urls(playlist_id)

    for vid in videos:
        get_thumbnail(vid)
        print(vid)
        add_tab(vid)
    # print(videos)





global user
user = {
    "name": "",
    "email": "",
    "profile_pic_path": "",
    "out_path": "Please choose a folder",
    "playlist": None,
}

def choose_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:  # Check if a valid folder is chosen
        user["out_path"] = folder_path
        print("Updated folder path:", user["out_path"])

def on_select(selected):
    # user["playlist"] = selected
    # print("Selected:", selected)
    #TODO: add videos to video panel
    # print(playlists_for_dropdown[selected])
    for widget in video_panel.winfo_children():
        widget.destroy()
    add_tabs(playlists_for_dropdown[selected])
    global playlist
    playlist = playlists_for_dropdown[selected]

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    root = ctk.CTk()

    root.geometry("1000x600")
    root.title("Youtube Music Downloader")
    root.resizable(True, False)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=3)
    
    global video_panel
    video_panel = ctk.CTkScrollableFrame(root, width=605, corner_radius=25)
    video_panel.pack(padx=(10, 30), fill="y", pady=15, expand=False, side="right")

    settings_panel = ctk.CTkFrame(root, width=356, corner_radius=25)
    settings_panel.pack(padx=(30, 10), fill="y", pady=35, expand=True, side="right")
    settings_panel.pack_propagate(False)

    user_info_bar = ctk.CTkFrame(settings_panel, height=50, corner_radius=25)
    user_info_bar.pack(padx=15, pady=(25, 0), fill="x", expand=False, side="top")
    user_info_bar.pack_propagate(False)

    # Initialize profile picture label
    profile_pic_label = ctk.CTkLabel(user_info_bar, text="", image="")
    profile_pic_label.pack(side="left", padx=(10, 5)) 
    profile_pic_label.pack_propagate(False)
    
    right_user_info_frame = ctk.CTkFrame(user_info_bar, height=50, width=175, fg_color="transparent")
    right_user_info_frame.pack(side="right", fill="y", expand=False, padx=(0, 20))
    right_user_info_frame.pack_propagate(False)

    # Create email label
    username_label = ctk.CTkLabel(right_user_info_frame, text=user["name"], text_color="#FFFFFF", anchor="center")
    username_label.pack(side="top", padx=(10, 0), pady=0, anchor="w")
   
    # Create username label
    email_label = ctk.CTkLabel(right_user_info_frame, text=user["email"], text_color="#FFFFFF", anchor="center")
    email_label.pack(side="bottom", padx=(10, 0), pady=0, anchor="w")

    login_bnt_frame = ctk.CTkFrame(settings_panel, height=50, fg_color="transparent")
    login_bnt_frame.pack(pady=(15, 0), fill="x", expand=False, side="top")


    playlist_chooser_frame = ctk.CTkFrame(settings_panel, height=50, fg_color="transparent")
    playlist_chooser_frame.pack(pady=(5, 0), fill="x", expand=False, side="top")

    top_playlist_chooser_frame = ctk.CTkFrame(playlist_chooser_frame, height=50, fg_color="transparent")
    top_playlist_chooser_frame.pack(pady=(0, 5), fill="x", expand=False, side="top")

    playlist_chooser_label = ctk.CTkLabel(top_playlist_chooser_frame, text="Choose Playlist:", text_color="white", anchor="w", font=("Arial", 20))
    playlist_chooser_label.pack(side="left", padx=15)

    bottom_playlist_chooser_frame = ctk.CTkFrame(playlist_chooser_frame, height=50, fg_color="transparent")
    bottom_playlist_chooser_frame.pack(fill="x", expand=False, side="top")

    playlist_chooser = ctk.CTkComboBox(bottom_playlist_chooser_frame, values=playlist_to_show, command=on_select)
    playlist_chooser.pack(pady=(5, 0), padx=15, expand=False)

    login_bnt = ctk.CTkButton(
        login_bnt_frame, 
        text="Login" if user["name"] == "" else "Logout", 
        width=30, 
        command= lambda: (handle_login_logout(profile_pic_label, username_label, email_label, playlist_chooser), login_bnt, login_bnt.configure(text="Login") if user["name"] == "" else login_bnt.configure(text="Logout"))
    )
    login_bnt.pack(padx=20, expand=False, side="right")
    
    path_chooser_frame = ctk.CTkFrame(settings_panel, height=50, fg_color="transparent")
    path_chooser_frame.pack(pady=(25, 0), padx=15, fill="x", expand=False, side="top")

    top_choose_path_frame = ctk.CTkFrame(path_chooser_frame, height=50, fg_color="transparent")
    top_choose_path_frame.pack(pady=(0, 5), fill="x", expand=False, side="top")

    choose_path_label = ctk.CTkLabel(top_choose_path_frame, text="Path:", text_color="white", anchor="w", font=("Arial", 20))
    choose_path_label.pack(side="left", padx=0)

    mid_choose_path_frame = ctk.CTkFrame(path_chooser_frame, height=50)
    mid_choose_path_frame.pack(pady=(0, 5), padx=5, fill="x", expand=False)

    path_section_frame = ctk.CTkFrame(mid_choose_path_frame, height=50)
    path_section_frame.pack(pady=(0, 5), fill="x", expand=False, side="top")

    choosen_path_label = ctk.CTkLabel(path_section_frame, width=230, text=user["out_path"], text_color="white", anchor="w", font=("Arial", 20))
    choosen_path_label.pack(padx=10)

    bottom_choose_path_frame = ctk.CTkFrame(path_chooser_frame, height=50, fg_color="transparent")
    bottom_choose_path_frame.pack(pady=(0, 5), fill="x", expand=False, side="top")

    path_chooser_bnt = ctk.CTkButton(
        bottom_choose_path_frame, 
        text="Choose Path", 
        command=lambda: (
            choose_folder(), 
            choosen_path_label.configure(text=user["out_path"]), 
            choosen_path_label.configure(font=("Arial", 14))
        )
    )
    path_chooser_bnt.pack(pady=5, padx=5, expand=True, side="top")

    # Pack the profile_pic_label in the user_info_bar
    profile_pic_label.pack(side="left", padx=(10, 0))

    test_bnt = ctk.CTkButton(settings_panel, text="Test", command=lambda: (get_mp3(playlist, user["out_path"])))
    test_bnt.pack(pady=20, side="bottom")


    root.mainloop()

if __name__ == "__main__":
    main()
    #delete out folder
    if os.path.exists("out"):
        shutil.rmtree("out")
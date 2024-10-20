import customtkinter as ctk
from PIL import Image, ImageDraw
from tkinter import filedialog
import os

from Tools.Google_API import get_user_info
from Tools.get_playlist import get_playlist_urls, get_user_playlists

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

def get_playlists():
    global playlists_for_dropdown, playlist, playlist_to_show
    playlists = get_user_playlists()
    print(playlists)

    playlists_for_dropdown = {}
    for playlist in playlists:
        playlists_for_dropdown[playlist["title"]] = playlist["id"]
        playlist_to_show.append(playlist["title"])
    print(playlists_for_dropdown)

    print(playlist_to_show)





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
    user["playlist"] = selected
    print("Selected:", selected)
    #TODO: add videos to video panel

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    root = ctk.CTk()

    root.geometry("1000x600")
    root.title("Youtube Music Downloader")
    root.resizable(True, False)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=3)
    
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
    profile_pic_label.pack(side="left", padx=(10, 0)) 
    
    # Create email label
    username_label = ctk.CTkLabel(user_info_bar, text=user["name"], text_color="#FFFFFF", anchor="center")
    username_label.pack(side="top", padx=(10, 0), pady=0, anchor="w")
   
    # Create username label
    email_label = ctk.CTkLabel(user_info_bar, text=user["email"], text_color="#FFFFFF", anchor="center")
    email_label.pack(side="bottom", padx=(10, 0), pady=0, anchor="w")

    login_bnt_frame = ctk.CTkFrame(settings_panel, height=50, fg_color="transparent")
    login_bnt_frame.pack(pady=(15, 0), fill="x", expand=False, side="top")

    login_bnt = ctk.CTkButton(
        login_bnt_frame, 
        text="Login", 
        width=30, 
        command=lambda: (
            login(profile_pic_label), 
            username_label.configure(text=user["name"]), 
            email_label.configure(text=user["email"]),
            print(playlist_to_show),
            playlist_chooser.configure(values=playlist_to_show)
        )
    )
    login_bnt.pack(padx=20, expand=False, side="right")

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

    root.mainloop()

if __name__ == "__main__":
    main()
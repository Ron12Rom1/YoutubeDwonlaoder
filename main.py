from Tools.download_data import *
from Tools.Google_API import get_user_info
from Tools.get_playlist import get_playlist_urls, get_user_playlists
from build.gui import open_window


# user_info = get_user_info()
# print(user_info)

# user_playlists = get_user_playlists()
# for playlist in user_playlists:
#     print(f"{playlist['title']} - {playlist['id']}")

# selected_playlist = input("Enter the playlist ID: ") #"PLAklA4JvzQ-oSCX9Vwrius5lJQitcg9Wc"

# # TODO : handel video unavable
# list = get_playlist_urls(selected_playlist)
# print("\n", list)


# for debuging purposes
list = [
        {"url": "https://www.youtube.com/watch?v=nOdnoM9tvFY"},
        {"url": "https://youtu.be/9bZkp7q19f0"},
        ]


if __name__ == "__main__":
    
    # pass
    #TODO : handel video unable to download
    for vid in list:
        get_mp3(vid)
        get_thumbnail(vid)
    
    open_window(list)
    
    
    print(list)
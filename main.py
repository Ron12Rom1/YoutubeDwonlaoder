from Tools.download_data import *
from Tools.Google_API import get_user_info


user_info = get_user_info()
print(user_info) 

list = [

        {"url": "https://www.youtube.com/watch?v=nOdnoM9tvFY",
        "thumbnail": "https://www.youtube.com/watch?v=nOdnoM9tvFY",
        "name": None},

        {"url": "https://youtu.be/9bZkp7q19f0",
        "thumbnail": "https://youtu.be/9bZkp7q19f0",
        "name": None},
        
        ]


if __name__ == "__main__":
    # pass
    for vid in list:
        get_mp3(vid)
        get_thumbnail(vid)
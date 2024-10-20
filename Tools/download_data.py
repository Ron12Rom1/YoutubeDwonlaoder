import requests, os
from pytubefix import YouTube
from pytubefix.cli import on_progress


if os.path.exists("out"):
    pass
else:
    os.mkdir("out")

def get_mp3(vid):

    if os.path.exists("out"):
        pass
    else:
        os.mkdir("out")

    url = vid['url']

    yt = YouTube(url, on_progress_callback = on_progress)
    print(yt.title)
    vid['name'] = yt.title
    
    # thumbnail.download()
    ys = yt.streams.get_audio_only()
    ys.download(mp3=True, output_path="out")


def shape_tumbnail(file_name):

    from PIL import Image

    # Load the image
    image = Image.open("out/" + file_name)

    # Get the dimensions of the image (width, height)
    width, height = image.size

    # Define how much to crop from the top and bottom
    top_crop = 60  # Pixels to crop from the top
    bottom_crop = top_crop  # Pixels to crop from the bottom

    # Define the cropping box (left, upper, right, lower)
    crop_box = (0, top_crop, width, height - bottom_crop)

    # Crop the image
    cropped_image = image.crop(crop_box)

    # Save the cropped image
    cropped_image.save("out/" + file_name)

    print(f"Thumbnail shape successfully as {file_name}")

def get_thumbnail(vid):
    
    url = vid['url']

    try:
        # Create a YouTube object
        yt = YouTube(url, on_progress_callback = on_progress)
        
        # Get the thumbnail URL
        thumbnail_url = yt.thumbnail_url
        
        # Get the video title to use as the filename
        title = vid['name']
    
        # Clean the title to avoid file system issues
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '_')).rstrip()

        # Define the file name for the thumbnail
        file_name = f"{safe_title}_thumbnail.jpg"
        
        # Download the thumbnail
        response = requests.get(thumbnail_url)
        
        if response.status_code == 200:
            with open(f"out/{file_name}", 'wb') as file:
                file.write(response.content)
            print(f"Thumbnail downloaded successfully as {file_name}")
            vid["thumbnail"] = f"out/{file_name}"
            shape_tumbnail(file_name)
        else:
            print("Failed to download thumbnail")
    
    except Exception as e:
        print(f"An error occurred: {e}")

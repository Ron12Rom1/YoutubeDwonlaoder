import customtkinter as ctk
from PIL import Image

vid = {
    "name": "[SETUP]Count on you",
    "url": "https://www.youtube.com/watch?v=nOdnoM9tvFY",
    "thumbnail": "out/Nightcore  SPED UP  COUNT ON YOU NV_thumbnail.jpg"
}

def add_tab(vid):

    # Load the image from the specified path
    tn_path = vid["thumbnail"]

    title = vid["name"]

    # Create a new frame for the new panel
    new_frame = ctk.CTkFrame(
        master=scrollable_frame,
        width=400,
        height=100,
        corner_radius=15,
        fg_color="#AD49E1",
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
    tn_label.pack(side="left", padx=10, pady=10)  # Pack the label into the scrollable frame

    max_letters = 20
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
    title_label.place(x = -50, y = -11, relx=0.5, rely=0.5)  # Center the label in the frame



# Initialize the main window
window = ctk.CTk()
window.geometry("800x500")
window.configure(bg="#2E073F")  # Dark purple background

# Left Sector (smaller box with rounded edges)
left_frame = ctk.CTkFrame(
    window,
    width=200,  # Adjust width
    height=400,  # Adjust height
    corner_radius=30,  # Rounded corners
    fg_color="#7A00A9"  # Purple color
)
left_frame.place(x=50, y=50)  # Position of the left frame

# Add a gray rounded box inside the left sector
gray_inner_frame = ctk.CTkFrame(
    left_frame,
    width=150,  # Width smaller than left_frame
    height=50,  # Adjust height
    corner_radius=25,  # Rounded corners
    fg_color="#555555"  # Dark gray color
)
gray_inner_frame.place(x=25, y=25)  # Adjust position inside the left frame

# Define what happens when the button is clicked
def on_button_click():
    print("🔗 Button clicked!")

# Add a larger link button inside the left sector
icon_button = ctk.CTkButton(
    left_frame,
    text="🔗",  # Link icon
    text_color="black",  # Black color for the icon
    font=("Arial", 30),  # Increase font size to make the icon larger
    width=20,  # Adjust button width
    height=20,  # Adjust button height
    fg_color="transparent",  # Transparent background
    hover_color="#6A1796",  # Color when hovering
    command=on_button_click  # Command to run on click
)
icon_button.place(x=125, y=80)  # Adjust position for the button

# Right Sector (larger box with rounded edges)
scrollable_frame = ctk.CTkScrollableFrame(
    window,
    width=450,  # Keeping the original width
    height=400,  # Keeping the original height
    corner_radius=30,
    fg_color="#7A00A9"
)
scrollable_frame.place(x=275, y=25)  # Position of the scrollable frame

# Disable window resizing
window.resizable(False, False)
add_tab(vid)

# Run the window
window.mainloop()

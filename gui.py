### GUI for the folder organizer ###

from tkinter import Canvas, Button, PhotoImage, filedialog, Tk
from pathlib import Path

from main import organize_folder

# get the path of the directory where this file is located
PROJECT_DIR = Path(__file__).parent

# get the assets directory path
ASSETS_PATH = PROJECT_DIR / ".\\assets"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("405x127")
window.title("Folder Organizer")
window.iconphoto(False, PhotoImage(file=relative_to_assets("icon.png")))
window.resizable(False, False)

# create canvas
canvas = Canvas(
    window,
    bg="#35323b",
    height=127,
    width=405,
    bd=0,
    highlightthickness=0,
    relief="ridge",
)


def browse():
    global folder_path
    folder_path = filedialog.askdirectory(mustexist=True, title="Select a folder")
    if folder_path != "":
        canvas.delete("folder_path")

    canvas.create_text(
        138.0,
        30.0,
        anchor="nw",
        text=folder_path,
        fill="#b3a9a9",
        font=("RobotoRoman Light", 18 * -1),
        tags=("folder_path"),
    )


canvas.place(x=0, y=0)
button_image_1 = PhotoImage(file=relative_to_assets("button_browse.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=browse,
    relief="flat",
)
button_1.place(x=24.0, y=25.0, width=102.0, height=30.0)
canvas.create_text(
    138.0,
    30.0,
    anchor="nw",
    text="No file selected",
    fill="#b3a9a9",
    font=("RobotoRoman Light", 18 * -1),
    tags=("folder_path"),
)

button_image_2 = PhotoImage(file=relative_to_assets("button_organize.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: organize_folder(folder_path),
    relief="flat",
)
button_2.place(x=12.0, y=77.0, width=376.0, height=35.0)

window.mainloop()

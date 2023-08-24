# This code is a mess.
# This is me learning Python as I go.
# This is not how I write code for my day job.
import os
import tkinter as tk
import socket
import json
import time
import pygame

# os.chdir('./deletephone/')

from datetime import timedelta
from select import select
from tkinter import ttk
from view import *
from PIL import ImageTk, Image
from sys import platform


UDP_IP = "127.0.0.1"
UDP_PORT = 9090

DIVIDER_HEIGHT = 3

print(platform)
UP_KEY_CODE = 8255233 if platform == "darwin" else 40 if platform == 'win32' else 111
DOWN_KEY_CODE = 8320768 if platform == "darwin" else 38 if platform == 'win32' else 116
LEFT_KEY_CODE = 8124162 if platform == "darwin" else 37 if platform == 'win32' else 113
RIGHT_KEY_CODE = 8189699 if platform == "darwin" else 39 if platform == 'win32' else 114
ESC_KEY_CODE = 1 if platform == "darwin" else 27 if platform == 'win32' else 2
PREV_KEY_CODE = 2818092 if platform == "darwin" else 0
NEXT_KEY_CODE = 3080238 if platform == "darwin" else 0
PLAY_KEY_CODE = 3211296 if platform == "darwin" else 0

SCREEN_TIMEOUT_SECONDS = 60

wheel_position = -1
last_button = -1

last_interaction = time.time()
screen_on = True

# initialize audio mixer
pygame.mixer.init()


def screen_sleep():
    global screen_on
    screen_on = False
    os.system('xset -display :0 dpms force off')


def screen_wake():
    global screen_on
    screen_on = True
    os.system('xset -display :0 dpms force on')


def flattenAlpha(img):
    global SCALE
    [img_w, img_h] = img.size
    img = img.resize((int(img_w * SCALE), int(img_h * SCALE)), Image.LANCZOS)
    alpha = img.split()[-1]  # Pull off the alpha layer
    ab = alpha.tobytes()  # Original 8-bit alpha

    checked = []  # Create a new array to store the cleaned up alpha layer bytes

    # Walk through all pixels and set them either to 0 for transparent or 255 for opaque fancy pants
    transparent = 50  # change to suit your tolerance for what is and is not transparent

    p = 0
    for pixel in range(0, len(ab)):
        if ab[pixel] < transparent:
            checked.append(0)  # Transparent
        else:
            checked.append(255)  # Opaque
        p += 1

    mask = Image.frombytes('L', img.size, bytes(checked))

    img.putalpha(mask)

    return img


class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        global LARGEFONT, MED_FONT, SCALE
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        if (platform == 'darwin'):
            self.geometry("320x240")
            SCALE = 0.3
        else:
            self.attributes('-fullscreen', True)
            SCALE = 0.3
            # SCALE = self.winfo_screenheight() / 930

        LARGEFONT = ("ChicagoFLF", int(72 * SCALE))
        MED_FONT = ("Consolas", int(52 * SCALE))
        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in [StartPage]:
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.green_arrow_image = ImageTk.PhotoImage(flattenAlpha(Image.open('./assets/pod_arrow_grn.png')))
        self.black_arrow_image = ImageTk.PhotoImage(flattenAlpha(Image.open('./assets/pod_arrow_blk.png')))
        self.empty_arrow_image = ImageTk.PhotoImage(flattenAlpha(Image.open('./assets/pod_arrow_empty.png')))
        self.play_image = ImageTk.PhotoImage(flattenAlpha(Image.open('./assets/pod_play.png')))
        self.pause_image = ImageTk.PhotoImage(flattenAlpha(Image.open('./assets/pod_pause.png')))
        self.space_image = ImageTk.PhotoImage(flattenAlpha(Image.open('./assets/pod_space.png')))
        self.wifi_image = ImageTk.PhotoImage(flattenAlpha(Image.open('./assets/pod_wifi.png')))
        self.configure(bg=SPOT_BLACK)
        self.grid_columnconfigure(0, weight=1)
        contentFrame = tk.Canvas(self, bg=SPOT_BLACK, highlightthickness=0, relief='ridge')
        contentFrame.grid(row=2, column=0, sticky="nswe")
        self.grid_rowconfigure(2, weight=1)
        listFrame = tk.Canvas(contentFrame)
        listFrame.configure(bg=SPOT_BLACK, bd=0, highlightthickness=0)
        listFrame.grid(row=0, column=0, sticky="nsew")
        contentFrame.grid_rowconfigure(0, weight=1)
        contentFrame.grid_columnconfigure(0, weight=1)

        # scrollbar
        self.scrollFrame = tk.Canvas(contentFrame)
        self.scrollFrame.configure(bg=SPOT_BLACK, width=int(50 * SCALE), bd=0, highlightthickness=4,
                                   highlightbackground=SPOT_GREEN)
        self.scrollBar = tk.Canvas(self.scrollFrame, bg=SPOT_GREEN, highlightthickness=0, width=int(20 * SCALE))
        self.scrollBar.place(in_=self.scrollFrame, relx=.5, y=int(10 * SCALE), anchor="n", relwidth=.6, relheight=.9)
        self.scrollFrame.grid(row=0, column=1, sticky="ns", padx=(0, 30), pady=(0, 10))

        self.listItems = []
        self.arrows = []
        for x in range(25):
            item = tk.Label(listFrame, text=" " + str(x), justify=tk.LEFT, anchor="w", font=MED_FONT,
                            background=SPOT_BLACK, foreground=SPOT_GREEN, padx=(30 * SCALE))
            imgLabel = tk.Label(listFrame, image=self.green_arrow_image, background=SPOT_BLACK)
            imgLabel.image = self.green_arrow_image
            imgLabel.grid(row=x, column=1, sticky="nsw", padx=(0, 30))
            item.grid(row=x, column=0, sticky="ew", padx=(10, 0))
            self.listItems.append(item)
            self.arrows.append(imgLabel)
        listFrame.grid_columnconfigure(0, weight=1)
        # listFrame.grid_columnconfigure(1, weight=1)

    def show_scroll(self, index, total_count):
        scroll_bar_y_rel_size = max(0.9 - (total_count - MENU_PAGE_SIZE) * 0.06, 0.03)
        scroll_bar_y_raw_size = scroll_bar_y_rel_size * self.scrollFrame.winfo_height()
        percentage = index / (total_count - 1)
        offset = ((1 - percentage) * (scroll_bar_y_raw_size + int(20 * SCALE))) - (
                scroll_bar_y_raw_size + int(10 * SCALE))
        self.scrollBar.place(in_=self.scrollFrame, relx=.5, rely=percentage, y=offset, anchor="n", relwidth=.66,
                             relheight=scroll_bar_y_rel_size)
        self.scrollFrame.grid(row=0, column=1, sticky="ns", padx=(0, 30), pady=(0, 10))

    def hide_scroll(self):
        self.scrollFrame.grid_forget()

    def set_list_item(self, index, text, line_type=LINE_NORMAL, show_arrow=False):
        print(text, line_type)
        bgColor = SPOT_GREEN if line_type == LINE_HIGHLIGHT else SPOT_BLACK
        txtColor = SPOT_BLACK if line_type == LINE_HIGHLIGHT else \
            (SPOT_GREEN if line_type == LINE_NORMAL else SPOT_WHITE)
        truncd_text = text if len(text) < 30 else text[0:27] + "..."
        self.listItems[index].configure(background=bgColor, foreground=txtColor, text=truncd_text)
        self.listItems[index].bind("<Button-1>", lambda e: (onClick(index)))
        arrow = self.arrows[index]
        arrow.grid(row=index, column=1, sticky="nsw", padx=(0, 30))
        arrowImg = self.empty_arrow_image if not show_arrow else \
            (self.black_arrow_image if line_type == LINE_HIGHLIGHT else self.green_arrow_image)
        arrow.configure(background=bgColor, image=arrowImg)
        arrow.image = arrowImg


def render_menu(app, menu_render):
    app.show_frame(StartPage)
    page = app.frames[StartPage]
    if (menu_render.total_count > MENU_PAGE_SIZE):
        page.show_scroll(menu_render.page_start, menu_render.total_count)
    else:
        page.hide_scroll()
    for (i, line) in enumerate(menu_render.lines):
        page.set_list_item(i, text=line.title, line_type=line.line_type, show_arrow=line.show_arrow)
    # page.set_header(menu_render.header, menu_render.now_playing, menu_render.has_internet)


def render(app, render):
    if (render.type == MENU_RENDER_TYPE):
        render_menu(app, render)
    # elif (render.type == NOW_PLAYING_RENDER):
    #     render_now_playing(app, render)
    # elif (render.type == SEARCH_RENDER):
    #     render_search(app, render)


def onUpPressed():
    global page, app
    page.nav_up()
    render(app, page.render())


def onDownPressed():
    global page, app
    page.nav_down()
    render(app, page.render())


def onClick(index):
    global page, app
    page.nav_set(index)
    render(app, page.render())
    page.render().unsubscribe()

    onSelectPressed()


def onSelectPressed(index=None):
    global page, app
    print(page)

    if (not page.has_sub_page):
        page = page.nav_select()
        return
    page.render().unsubscribe()
    page = page.nav_select()
    render(app, page.render())


def onBackPressed():
    global page, app
    previous_page = page.nav_back()
    if (previous_page):
        page.render().unsubscribe()
        page = previous_page
        render(app, page.render())


def onKeyPress(event):
    c = event.keycode
    if (c == UP_KEY_CODE):
        onUpPressed()
    elif (c == DOWN_KEY_CODE):
        onDownPressed()
    elif (c == RIGHT_KEY_CODE):
        onSelectPressed()
    elif (c == LEFT_KEY_CODE):
        onBackPressed()
    elif (c == ESC_KEY_CODE):
        close_win()
    # elif (c == NEXT_KEY_CODE):
    #     onNextPressed()
    # elif (c == PREV_KEY_CODE):
    #     onPrevPressed()
    # elif (c == PLAY_KEY_CODE):
    #     onPlayPressed()
    else:
        print("unrecognized key: ", c)


# Define a function to close the window
def close_win():
    app.destroy()


# Driver Code
page = RootPage(None)
app = tkinterApp()

render_menu(app, page.render())
#
# sock = socket.socket(socket.AF_INET, # Internet
#                      socket.SOCK_DGRAM) # UDP
# sock.bind((UDP_IP, UDP_PORT))
# sock.setblocking(0)
# socket_list = [sock]
# loop_count = 0
app.bind('<KeyPress>', onKeyPress)
app.mainloop()

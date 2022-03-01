import json
import os
import tkinter as tk

from data.data import select_image_user
from source.app.Sys import set_color, select_image, set_appwindow, center

from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

class ParametreWindow(tk.Tk):
    def __init__(self, user):
        tk.Tk.__init__(self)

        self.user = user
        self.geometry("238x290")
        self.config(bg=set_color("entrycolor"))
        self.wm_overrideredirect(True)
        self.iconbitmap(select_image('icon.ico'))
        self.title_bar()
        self.title("GestMoney | Paramètre")

        self.widgets()
        center(self)
        # Permet de voir l'icon dans notre barre des taches
        self.after(10, lambda: set_appwindow(self))

    def select_files(self):
        filetypes = (
            ('Type', '*.png'),
            ('Type', '*.jpg')
        )

        filenames = fd.askopenfilenames(
            title='Open files',
            initialdir='/',
            filetypes=filetypes)

        with open(r'..\..\data\users.json', 'r+') as file:
            data = json.load(file)

            data[self.user]["image"] = filenames

        with open(r'..\..\data\users.json', 'w') as file:
            json.dump(data, file, indent=4)

    def widgets(self):
        profile_img = tk.PhotoImage(master=self, file=select_image_user(self.user)).subsample(14)

        profile = tk.Label(self, image=profile_img, background=set_color('entrycolor'), bd=0)
        profile.photo = profile_img
        profile.pack(ipady=10)

        open_button = tk.Button(self, text="Modifier la photo", background=set_color("entrycolor"), foreground=set_color("darkgreen"), bd=0, activebackground=set_color("entrycolor"), activeforeground=set_color("darkgreen"), cursor='hand2', command=self.select_files)
        open_button.place(x=72, y=115)

    def title_bar(self):
        title_bar = tk.Canvas(self, width=238, height=48, bg=set_color('darkgreen'), highlightthickness=0)
        title_bar.create_text(120, 25, text="GestMoney", font=('Roboto', 15, 'bold'), fill="white")
        title_bar.pack()

        imgs = tk.PhotoImage(master=self, file=select_image("parametre.png")).subsample(12)
        icon = tk.Label(self, image=imgs, background=set_color("darkgreen"), bd=0,
                        foreground=set_color("entrycolor"))
        icon.photo = imgs
        icon.place(x=5, y=2)

        quit_button = tk.Button(self, text="X", background=set_color("darkgreen"), cursor='hand2',
                                relief='groove', foreground=set_color("lightgreen"),
                                activebackground=set_color("darkgreen"), activeforeground=set_color("lightgreen"),
                                font=('Roboto', 15, 'bold'), command=self.destroy)
        quit_button.place(x=190, y=4, width=40, height=40)

        profile_img = tk.PhotoImage(master=self, file=select_image("profile-base.png")).subsample(14)
        profile_btn = tk.Button(self, image=profile_img, background=set_color('darkgreen'), cursor='hand2',
                                activebackground=set_color('darkgreen'), bd=0)
        profile_btn.photo = profile_img
        profile_btn.place(x=955, y=10)

        self.apply_drag([title_bar, icon])

    def update(self):
        self.mainloop()

    def mouse_down(self, event):
        self.x, self.y = event.x, event.y

    def mouse_up(self, event):
        self.x, self.y = None, None

    def mouse_drag(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x0 = self.winfo_x() + deltax
        y0 = self.winfo_y() + deltay
        self.geometry("+%s+%s" % (x0, y0))

    def apply_drag(self, elements):
        for element in elements:
            element.bind('<ButtonPress-1>', self.mouse_down)
            element.bind('<B1-Motion>', self.mouse_drag)
            element.bind('<ButtonRelease-1>', self.mouse_up)


if __name__ == '__main__':
    ParametreWindow().mainloop()

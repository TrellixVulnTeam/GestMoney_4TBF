import json
import os
from ctypes import windll


def select_image(name):
    scriptpath = os.path.abspath(__file__)
    scriptdir = os.path.dirname(scriptpath)
    return os.path.join(scriptdir, f"ressource\\img\\{name}")


def set_color(theme, color):
    themes = {
        'basic': {
            'lightblue': '#001242',
            'green': '#77AB7D',
            'entrycolor': '#000022',
            'white': 'white',
            'pink': '#DC2A58',
            'buttonactive': '#001242',
            'insert': 'white',
            'entrytext': 'white'
                  }
    }

    return themes[theme][color]


def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


def set_appwindow(mainWindow):  # Pour afficher l'icon dans la barre des taches

    GWL_EXSTYLE = -20
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080
    # Magic
    hwnd = windll.user32.GetParent(mainWindow.winfo_id())
    stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    stylew = stylew & ~WS_EX_TOOLWINDOW
    stylew = stylew | WS_EX_APPWINDOW
    windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)

    mainWindow.wm_withdraw()
    mainWindow.after(10, mainWindow.wm_deiconify)

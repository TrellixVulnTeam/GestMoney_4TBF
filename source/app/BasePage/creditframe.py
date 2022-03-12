import tkinter as tk

from data.data import add_credit
from source.app.Sys import set_color
from source.app.BasePage.baseframe import create_buttons, date_valid


class CreditFrame(tk.Frame):

    def __init__(self, window):
        self.window = window
        super().__init__(window, width=853, height=584, bg=self.set_color('bg'))

        self.canvas = tk.Canvas(self, height=853, width=853, background=self.set_color('bg'), highlightthickness=0)
        self.error_canvas = tk.Canvas()

        self.canvas.create_text(426.5, 50, text="Créditer le compte", font=('Roboto', 30, 'bold'),
                                fill=self.set_color('text'))

        self.create_inputs()
        self.canvas.pack()

    def create_inputs(self):
        self.canvas.create_text(50, 150, text='Montant', font=('Roboto', 18), fill=self.set_color('text'), anchor='w')
        self.canvas.create_text(50, 270, text='Origine de la somme', font=('Roboto', 18),
                                fill=self.set_color('text'), anchor='w')
        self.canvas.create_text(470, 150, text='Date', font=('Roboto', 18), fill=self.set_color('text'), anchor='w')

        self.canvas.create_text(470, 270, text='Moyen de paiement', font=('Roboto', 18),
                                fill=self.set_color('text'), anchor='w')

        self.amount = tk.Entry(self.canvas, bg=self.set_color('entrycolor'), font=('Roboto', 15), fg='white',
                               bd=0, insertbackground=self.set_color('entrytext'))
        self.amount.place(x=50, y=170, width=330, height=46)

        self.origin = tk.Entry(self.canvas, bg=self.set_color('entrycolor'), font=('Roboto', 15), fg='white',
                               bd=0, insertbackground=self.set_color('entrytext'))
        self.origin.place(x=50, y=290, width=330, height=46)

        self.date = tk.Entry(self.canvas, bg=self.set_color('entrycolor'), font=('Roboto', 15), fg='white',
                             bd=0, insertbackground=self.set_color('entrytext'))
        self.date.place(x=470, y=170, width=330, height=46)

        cheque_var = tk.IntVar()
        virement_var = tk.IntVar()
        especes_var = tk.IntVar()
        self.check_vars = [virement_var, especes_var, cheque_var]

        vir_checkbutton = tk.Checkbutton(self, text='Virement', background=self.set_color('bg'),
                                         foreground=self.set_color('text'), font=('Roboto', 16, 'bold'),
                                         highlightthickness=0, bd=0, activebackground=self.set_color('bg'),
                                         activeforeground=self.set_color('text'), variable=virement_var,
                                         command=lambda: self.uncheck_buttons(0))
        vir_checkbutton.place(x=460, y=300)
        self.origin = tk.Entry(self.canvas, bg=self.set_color('entrycolor'), font=('Roboto', 15), fg='white',
                               bd=0, insertbackground=self.set_color('entrytext'))
        self.origin.place(x=50, y=290, width=330, height=46)

        espece_checkbutton = tk.Checkbutton(self, text='Espèce', background=self.set_color('bg'), bd=0,
                                            foreground=self.set_color('text'), font=('Roboto', 16, 'bold'),
                                            activebackground=self.set_color('bg'), highlightthickness=0,
                                            activeforeground=self.set_color('text'), variable=especes_var,
                                            command=lambda: self.uncheck_buttons(1))
        espece_checkbutton.place(x=585, y=300)

        cheque_checkbutton = tk.Checkbutton(self, text='Chèque', background=self.set_color('bg'), bd=0,
                                            foreground=self.set_color('text'), font=('Roboto', 16, 'bold'),
                                            activebackground=self.set_color('bg'), highlightthickness=0,
                                            activeforeground=self.set_color('text'), variable=cheque_var,
                                            command=lambda: self.uncheck_buttons(2))
        cheque_checkbutton.place(x=700, y=300)

        self.check_buttons = [vir_checkbutton, espece_checkbutton, cheque_checkbutton]

        create_buttons(self, self.valid_credit)

    def valid_credit(self):
        origin = self.origin.get()
        amount = self.amount.get()
        date = self.date.get()

        transaction = {
            'origin': origin,
            'amount': amount,
            'date': date
        }

        if '' in transaction.values():
            self.show_error('Veuillez remplir toutes les cases')

        elif not amount.isdigit():
            self.show_error('Veuillez entrer un montant valide')

        elif not date_valid(date):
            self.show_error('Veuillez entrer une date au format dd/mm/yy')

        elif 1 not in [var.get() for var in self.check_vars]:
            self.show_error('Veuillez choisir un mode de paiement')

        else:
            transaction['amount'] = int(transaction['amount'])
            methods_names = ['virement', 'especes', 'cheque']

            for var in self.check_vars:
                if var.get() == 1:
                    transaction['method'] = methods_names[self.check_vars.index(var)]

            add_credit(self.window.user_id, transaction)

            self.window.switch_frame('BasePage')

    def show_error(self, text):
        self.error_canvas.destroy()
        self.error_canvas = tk.Canvas(self, height=50, width=self.window.winfo_width(),
                                      background=self.set_color("lightgreen"), highlightthickness=0)
        self.error_canvas.create_text(self.winfo_width() / 2, 25, text=text, font=('Roboto', 14), fill='red')

        self.error_canvas.place(x=0, y=80)

    def uncheck_buttons(self, exception):
        for button in self.check_buttons:
            if button != self.check_buttons[exception]:
                button.deselect()

    def set_color(self, color):
        return set_color(self.window.color_theme, color)
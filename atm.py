import tkinter as tk
import tkinter.messagebox as tmsg
import mysql.connector as connector

account_number = 0

root_password='123456789' # This is the password of the user of the database (may be different for different users)

class ATM(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.shared_data = {
            'Balance': tk.IntVar(), 'Current_user': tk.StringVar()}

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, MenuPage, WithdrawPage, DepositPage, BalancePage, ChangePinPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3d3d5c')
        self.controller = controller

        self.controller.title('State Bank of India')
        self.controller.state('zoomed')

        heading_label = tk.Label(self, text='State Bank of India', font=(
            'orbitron', 45, 'bold'), foreground='#ffffff', background='#3d3d5c')
        heading_label.pack(pady=25)

        space_label = tk.Label(self, height=4, bg='#3d3d5c')
        space_label.pack()

        account_label = tk.Label(
            self, text='Enter A/C Number', font=('helvetica', 15), bg='#3d3d5c', fg='white')
        account_label.pack(pady=10)
        my_account = tk.StringVar()

        account_entry_box = tk.Entry(self, textvariable=my_account, font=(
            'helvetica', 15), width=22, justify='center')
        account_entry_box.focus_set()
        account_entry_box.pack(ipady=10)

        password_label = tk.Label(
            self, text='Enter 4-digit PIN', font=('helvetica', 15), bg='#3d3d5c', fg='white')
        password_label.pack(pady=10)

        my_password = tk.StringVar()
        password_entry_box = tk.Entry(self, textvariable=my_password, font=(
            'helvetica', 15), width=22, justify='center')
        password_entry_box.pack(ipady=10)

        def handle_focus_in(_):
            password_entry_box.configure(fg='black', show='*')
        password_entry_box.bind('<FocusIn>', handle_focus_in)

        def check_credentials():
            global account_number
            mydb = connector.connect(
                host='localhost', user='root', password=root_password, database='atm')
            mycursor = mydb.cursor()
            mycursor.execute("select * from users where card_no=%s and pin=%s",
                             (my_account.get(), my_password.get()))
            row = mycursor.fetchone()
            if row == None:
                incorrect_credential_label['text'] = '*Incorrect Account Number or Password'
            else:
                account_number = my_account.get()
                curr = mydb.cursor()
                curr.execute("select card_name from users where card_no={}".format(my_account.get()))
                n = curr.fetchone()
                controller.shared_data['Current_user'].set(n[0])
                incorrect_credential_label['text'] = ''
                my_password.set('')
                my_account.set('')
                controller.show_frame('MenuPage')

        enter_button = tk.Button(self, text='Sign In', font=(
            'helvetica', 15), command=check_credentials, relief='raised', borderwidth=3, width=25, height=2)
        enter_button.pack(pady=30)

        incorrect_credential_label = tk.Label(self, text='', font=(
            'helvetica', 15), fg='red', bg='#3d3d5c', anchor='n')
        incorrect_credential_label.pack(fill='both', expand=True)


class MenuPage(tk.Frame):

    def __init__(self, parent, controller):
        global account_number

        tk.Frame.__init__(self, parent, bg='#3d3d5c')
        self.controller = controller

        heading_label = tk.Label(self, text='State Bank of India', font=(
            'helvetica', 45, 'bold'), foreground='#ffffff', background='#3d3d5c')
        heading_label.pack(pady=25)

        main_menu_label = tk.Label(self, text='Main Menu', font=(
            'helvetica', 16), fg='white', bg='#3d3d5c')
        main_menu_label.pack()

        name_frame = tk.Frame(self, bg='#3d3d5c')
        name_frame.pack(pady=20)

        hi_label = tk.Label(name_frame, text="Hi, ", font=('helvetica', 15, 'bold'), fg='white', bg='#3d3d5c')
        hi_label.grid(row=0, column=1)

        name_label = tk.Label(name_frame, textvariable=controller.shared_data['Current_user'], font=(
            'helvetica', 18, 'bold'), fg='white', bg='#3d3d5c')
        name_label.grid(row=0, column=2)

        selection_label = tk.Label(self, text='Select Any Option', font=(
            'helvetica', 16, 'bold'), fg='white', bg='#3d3d5c')
        selection_label.pack(fill='x', pady=30)

        button_frame = tk.Frame(self, bg='#33334d')
        button_frame.pack()

        def withdraw():
            controller.show_frame('WithdrawPage')

        withdraw_button = tk.Button(button_frame, text='Withdraw', font=(
            'helvetica', 20), command=withdraw, relief='raised', borderwidth=3, width=30, height=3)
        withdraw_button.grid(row=0, column=2, pady=5)

        def deposit():
            controller.show_frame('DepositPage')

        deposit_button = tk.Button(button_frame, text='Deposit', font=(
            'helvetica', 20), command=deposit, relief='raised', borderwidth=3, width=30, height=3)
        deposit_button.grid(row=0, column=3, pady=5)

        def balance():
            global account_number
            mydb = connector.connect(
                host='localhost', user='root', password=root_password, database='atm')
            mycursor = mydb.cursor()
            mycursor.execute(
                "select balance from users where card_no={}".format(account_number))
            row = mycursor.fetchone()
            controller.shared_data['Balance'].set(row[0])
            controller.show_frame('BalancePage')

        balance_button = tk.Button(button_frame, text='Balance', font=(
            'helvetica', 20), command=balance, relief='raised', borderwidth=3, width=30, height=3)
        balance_button.grid(row=1, column=2, pady=5)

        def change_pin():
            controller.show_frame('ChangePinPage')

        change_pin_button = tk.Button(button_frame, text='Change Pin', font=(
            'helvetica', 20), command=change_pin, relief='raised', borderwidth=3, width=30, height=3)
        change_pin_button.grid(row=1, column=3, pady=5)

        def exit():
            controller.show_frame('StartPage')

        exit_button = tk.Button(button_frame, text='Exit', font=(
            'helvetica', 20), command=exit, relief='raised', borderwidth=3, width=30, height=3)
        exit_button.grid(row=2, column=2, pady=5)


class WithdrawPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3d3d5c')
        self.controller = controller

        heading_label = tk.Label(self, text='State Bank of India', font=(
            'helvetica', 45, 'bold'), foreground='#ffffff', background='#3d3d5c')
        heading_label.pack(pady=25)

        enter_amount_label = tk.Label(self, text='Enter the amount you want to withdraw and Press "Enter"', font=(
            'helvetica', 16), fg='white', bg='#3d3d5c')
        enter_amount_label.pack()

        cash = tk.StringVar()

        other_amount_entry = tk.Entry(self, textvariable=cash, font=(
            'helvetica', 16), width=30, justify='center')
        other_amount_entry.pack(pady=5, ipady=20, side='top')

        def other_amount(_):
            global account_number
            mydb = connector.connect(
                host='localhost', user='root', password=root_password, database='atm')
            a = tmsg.askquestion(
                'Confirm', f'Do you want to withdraw ${cash.get()}?')
            if (a == 'yes'):
                curr = mydb.cursor()
                curr.execute(
                    "select balance from users where card_no={}".format(account_number))
                row = curr.fetchone()
                if (int(cash.get()) <= int(int(row[0]))):
                    amt_rem = int(row[0])-int(cash.get())
                    controller.shared_data['Balance'].set(amt_rem)
                    mycursor = mydb.cursor()
                    mycursor.execute("update users set balance={} where card_no={}".format(
                        amt_rem, account_number))
                    mydb.commit()
                    tmsg.showinfo('Withdrawal Successfull',
                                  f'You have successfully withdrawn ${cash.get()}.')
                    cash.set('')
                    controller.show_frame('MenuPage')
                else:
                    tmsg.showerror('Insufficient Balance',
                                   "You don't have enough money to withdraw.")

        other_amount_entry.bind('<Return>', other_amount)

        choose_amount_label = tk.Label(self, text='or, Choose the amount you want to withdraw', font=(
            'helvetica', 16), fg='white', bg='#3d3d5c')
        choose_amount_label.pack()

        button_frame = tk.Frame(self, bg='#33334d')
        button_frame.pack(pady=7)

        def withdraw(amount):
            global account_number
            mydb = connector.connect(
                host='localhost', user='root', password=root_password, database='atm')
            a = tmsg.askquestion(
                'Confirm', f'Do you want to withdraw ${amount}?')
            if (a == 'yes'):
                curr = mydb.cursor()
                curr.execute(
                    "select balance from users where card_no={}".format(account_number))
                row = curr.fetchone()
                if (amount <= int(int(row[0]))):
                    amt_rem = int(row[0])-int(amount)
                    controller.shared_data['Balance'].set(amt_rem)
                    mycursor = mydb.cursor()
                    mycursor.execute("update users set balance={} where card_no={}".format(
                        amt_rem, account_number))
                    mydb.commit()
                    tmsg.showinfo('Withdrawal Successfull',
                                  f'You have successfully withdrawn ${amount}.')
                    cash.set('')
                    controller.show_frame('MenuPage')
                else:
                    tmsg.showerror('Insufficient Balance',
                                   "You don't have enough money to withdraw.")

        twenty_button = tk.Button(button_frame, text='$20', font=(
            'helvetica', 16), command=lambda: withdraw(20), relief='raised', borderwidth=3, width=20, height=3)
        twenty_button.grid(row=0, column=0, pady=5)

        forty_button = tk.Button(button_frame, text='$40', font=('helvetica', 16), command=lambda: withdraw(
            40), relief='raised', borderwidth=3, width=20, height=3)
        forty_button.grid(row=0, column=1, pady=5)

        sixty_button = tk.Button(button_frame, text='$60', font=('helvetica', 16), command=lambda: withdraw(
            60), relief='raised', borderwidth=3, width=20, height=3)
        sixty_button.grid(row=0, column=2, pady=5)

        eighty_button = tk.Button(button_frame, text='$80', font=(
            'helvetica', 16), command=lambda: withdraw(80), relief='raised', borderwidth=3, width=20, height=3)
        eighty_button.grid(row=0, column=3, pady=5)

        one_hundred_button = tk.Button(button_frame, text='$100', font=(
            'helvetica', 16), command=lambda: withdraw(100), relief='raised', borderwidth=3, width=20, height=3)
        one_hundred_button.grid(row=1, column=0, pady=5)

        two_hundred_button = tk.Button(button_frame, text='$200', font=(
            'helvetica', 16), command=lambda: withdraw(200), relief='raised', borderwidth=3, width=20, height=3)
        two_hundred_button.grid(row=1, column=1, pady=5)

        three_hundred_button = tk.Button(button_frame, text='$300', font=(
            'helvetica', 16), command=lambda: withdraw(300), relief='raised', borderwidth=3, width=20, height=3)
        three_hundred_button.grid(row=1, column=2, pady=5)

        five_hundred_button = tk.Button(button_frame, text='$500', font=(
            'helvetica', 16), command=lambda: withdraw(500), relief='raised', borderwidth=3, width=20, height=3)
        five_hundred_button.grid(row=1, column=3, pady=5)

        def menu():
            controller.show_frame('MenuPage')

        menu_button = tk.Button(self, text='Go to Main Menu', font=('helvetica', 15), command=menu,  relief='raised', borderwidth=3, width=30, height=5)
        menu_button.pack(pady=5)


class DepositPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3d3d5c')
        self.controller = controller

        heading_label = tk.Label(self,
                                 text='State Bank of India',
                                 font=('helvetica', 45, 'bold'),
                                 foreground='#ffffff',
                                 background='#3d3d5c')
        heading_label.pack(pady=25)

        space_label = tk.Label(self, height=4, bg='#3d3d5c')
        space_label.pack()

        enter_amount_label = tk.Label(self,
                                      text='Enter the amount to be deposited',
                                      font=('helvetica', 15),
                                      bg='#3d3d5c',
                                      fg='white')
        enter_amount_label.pack(pady=10)

        cash = tk.StringVar()
        deposit_entry = tk.Entry(self,
                                 textvariable=cash,
                                 font=('helvetica', 15),
                                 width=22,
                                 justify='center')
        deposit_entry.pack(ipady=10)

        def deposit_cash():
            global account_number
            mydb = connector.connect(
                host='localhost', user='root', password=root_password, database='atm')
            curr = mydb.cursor()
            curr.execute(
                "select balance from users where card_no={}".format(account_number))
            row = curr.fetchone()
            amt_rem = int(row[0])+int(cash.get())
            controller.shared_data['Balance'].set(amt_rem)
            mycursor = mydb.cursor()
            mycursor.execute("update users set balance={} where card_no={}".format(
                amt_rem, account_number))
            mydb.commit()
            tmsg.showinfo(
                "Successfull", f"${cash.get()} is successfully deposited into your account.")
            cash.set('')
            controller.show_frame('MenuPage')

        enter_button = tk.Button(self,
                                 text='Deposit',
                                 font=('helvetica', 15),
                                 command=deposit_cash,
                                 relief='raised',
                                 borderwidth=3,
                                 width=30,
                                 height=2)
        enter_button.pack(pady=30)

        def menu():
            controller.show_frame('MenuPage')

        menu_button = tk.Button(self,
                                text='Go to Main Menu',
                                font=('helvetica', 15),
                                command=menu,
                                relief='raised',
                                borderwidth=3,
                                width=30,
                                height=2)
        menu_button.pack(pady=30)


class BalancePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3d3d5c')
        self.controller = controller

        heading_label = tk.Label(self, text='State Bank of India',  font=(
            'helvetica', 45, 'bold'), foreground='#ffffff', background='#3d3d5c')
        heading_label.pack(pady=25)

        balance = tk.Frame(self)
        balance.pack(pady=30)
        current_label = tk.Label(balance,
                                 text="Current Balance : $",
                                 font=('helvetica', 30),
                                 fg='white',
                                 bg='#3d3d5c')
        current_label.grid(row=0, column=0)
        balance_label = tk.Label(balance,
                                 textvariable=controller.shared_data['Balance'],
                                 font=('helvetica', 30),
                                 fg='white',
                                 bg='#3d3d5c',
                                 anchor='w')
        balance_label.grid(row=0, column=1)

        button_frame = tk.Frame(self, bg='#3d3d5c')
        button_frame.pack()

        def menu():
            controller.show_frame('MenuPage')

        menu_button = tk.Button(button_frame,
                                command=menu,
                                text='Go to Main Menu',
                                font=('helvetica', 15),
                                relief='raised',
                                borderwidth=3,
                                width=30,
                                height=3)
        menu_button.grid(row=0, column=0, pady=5)

        def exit():
            controller.show_frame('StartPage')

        exit_button = tk.Button(button_frame,
                                text='Exit',
                                font=('helvetica', 15),
                                command=exit,
                                relief='raised',
                                borderwidth=3,
                                width=30,
                                height=3)
        exit_button.grid(row=1, column=0, pady=5)


class ChangePinPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3d3d5c')
        self.controller = controller

        heading_label = tk.Label(self,
                                 text='State Bank of India',
                                 font=('helvetica', 45, 'bold'),
                                 foreground='#ffffff',
                                 background='#3d3d5c')
        heading_label.pack(pady=25)

        space_label = tk.Label(self, height=4, bg='#3d3d5c')
        space_label.pack()

        enter_pin_label = tk.Label(self,
                                   text='Enter new PIN',
                                   font=('helvetica', 15),
                                   bg='#3d3d5c',
                                   fg='white')
        enter_pin_label.pack(pady=10)

        pin = tk.StringVar()
        confirm_pin = tk.StringVar()
        pin_entry = tk.Entry(self,
                             textvariable=pin,
                             font=('helvetica', 15),
                             width=22,
                             justify='center')
        pin_entry.pack(ipady=10)

        enter_pin_label = tk.Label(self,
                                   text='Confirm PIN',
                                   font=('helvetica', 15),
                                   bg='#3d3d5c',
                                   fg='white')
        enter_pin_label.pack(pady=10)

        confirm_pin_entry = tk.Entry(self,
                                     textvariable=confirm_pin,
                                     font=('helvetica', 15),
                                     width=22,
                                     justify='center')
        confirm_pin_entry.pack(ipady=10)

        def handle_focus_in(_):
            pin_entry.configure(fg='black', show='*')
            confirm_pin_entry.configure(fg='black', show='*')

        pin_entry.bind('<FocusIn>', handle_focus_in)
        confirm_pin_entry.bind('<FocusIn>', handle_focus_in)

        def change_pin():
            global pin_code
            if (pin.get() == confirm_pin.get()):
                global account_number
                mydb = connector.connect(
                    host='localhost', user='root', password=root_password, database='atm')
                mycursor = mydb.cursor()
                mycursor.execute("update users set pin={} where card_no={}".format(
                    pin.get(), account_number))
                mydb.commit()
                pin.set('')
                confirm_pin.set('')
                tmsg.showinfo("Successfull", "PIN is successfully changed!")
                controller.show_frame('StartPage')
            else:
                tmsg.showerror("Failed!", "Passwords don't match.")

        enter_button = tk.Button(self,
                                 text='Change PIN',
                                 font=('helvetica', 15),
                                 command=change_pin,
                                 relief='raised',
                                 borderwidth=3,
                                 width=30,
                                 height=2)
        enter_button.pack(pady=30)

        def menu():
            controller.show_frame('MenuPage')

        menu_button = tk.Button(self,
                                text='Go to Main Menu',
                                font=('helvetica', 15),
                                command=menu,
                                relief='raised',
                                borderwidth=3,
                                width=30,
                                height=2)
        menu_button.pack(pady=30)


if __name__ == "__main__":
    app = ATM()
    app.mainloop()

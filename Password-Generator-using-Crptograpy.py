from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import json
import pyperclip
from cryptography.fernet import Fernet

GREENISH_YELLOW = "#F85C70"
GREENISH_WHITE = "#0D98BA"
LIGHT_SKY = "#C0E5E4"
LIGHT_GREEN = "#92E3A9"
COURIER_FONT = "Courier"

file = open('key.key', 'rb')  # Open the file as wb to read bytes
key = file.read()  # The key will be type bytes
file.close()

f = Fernet(key)

def decrypt(k):
    k = k.encode('utf-8')
    decrypted = f.decrypt(k)  # Decrypt the bytes. The returning object is of type bytes
    a = decrypted.decode()
    return a

def password_vault():
    # ------------ PASSWORD GENERATOR ----------------------- #

    def password_generator():
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u',
                   'v',
                   'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                   'Q',
                   'R',
                   'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

        password_letters = [choice(letters) for _ in range(randint(8, 10))]
        password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
        password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

        # add all password in a list
        password_list = password_letters + password_symbols + password_numbers

        # shuffle those generated password in the list
        shuffle(password_list)

        # join password
        password = "".join(password_list)

        # show generated password in the password label field
        password_entry.insert(0, password)

        # copy password on the clipboard automatically
        pyperclip.copy(password)

    # ------------ SAVED PASSWORD --------------------------- #

    def save():
        website = website_entry.get()
        # website = website.encode()
        # website = f.encrypt(website)
        # website = website.decode()

        email = email_entry.get()
        email = email.encode()
        email = f.encrypt(email)
        email = email.decode()

        password = password_entry.get()
        password = password.encode()
        password = f.encrypt(password)
        password = password.decode()

        print(website,"\n",email,"\n",password)
        # create new dictionary for store in json file
        new_data = {
            website: {
                "email": email,
                "password": password,
            }
        }
        print(new_data,"88888888888888888")
        # checking empty fields
        if len(website) == 0 or len(password) == 0:
            messagebox.showinfo(title="Opps", message=" Please fill up the empty fields.")
        else:
            try:
                # open the data file
                with open("data.json", "r") as data_file:

                    # reading old data
                    data = json.load(data_file)

            # if file not found
            except FileNotFoundError:
                # if file not found then create a new file
                with open("data.json", "w") as data_file:
                    # saving updated data with indent 4
                    json.dump(new_data, data_file, indent=4)
                    messagebox.showinfo(title="Success", message="Credentials Saved")
            # if file found
            else:
                # then update the old file
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    # saving updated data with indent 4
                    json.dump(data, data_file, indent=4)
                    messagebox.showinfo(title="Success", message="Credentials Saved")
            finally:
                # finally save the file
                website_entry.delete(0, END)
                email_entry.delete(0, END)
                password_entry.delete(0, END)

    # -------------- FIND PASSWORD ----------------------- #
    def find_password():
        website = website_entry.get()
        try:
            with open("data.json") as data_file:
                # open the data file
                # print(data_file,"*************")
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showinfo(title="Error", message="No Data File Found.")
        else:
            if website in data:
                email = data[website]["email"]
                email = f.decrypt(email)
                email = email.decode()
                password = data[website]["password"]
                password = f.decrypt(password)
                password = password.decode()
                messagebox.showinfo(title=website, message=f"Email: {email} \nPassword: {password}")
            else:
                messagebox.showinfo(title="Error", message=f"No details for {website} exists.")

    # ------------ UI SETUP --------------------------------- #

    # creating window object
    window = Tk()

    # window title
    window.title("Password Generator")

    # add custom favicon
    window.iconbitmap(r'favicon.ico')

    # add padding and background color
    window.config(padx=60, pady=60, bg=GREENISH_WHITE)

    # canvas size
    canvas = Canvas(height=350, width=350, bg=GREENISH_WHITE, highlightthickness=0)

    # assign the image location to a variable
    logo_image = PhotoImage(file="download.png")

    # add image in the canvas in the center by "/" half of the dimension
    canvas.create_image(180, 150, image=logo_image)

    # assign the grid for the canvas
    canvas.grid(row=0, column=1)

    # TODO: Labels

    # website labels
    website_label = Label(text="Website:", bg=GREENISH_WHITE, font=COURIER_FONT)

    # website label on grid
    website_label.grid(row=1, column=0)

    # email labels
    email_label = Label(text="Email:", bg=GREENISH_WHITE, font=COURIER_FONT)

    # email label on grid
    email_label.grid(row=2, column=0)

    # password labels
    password_label = Label(text="Password:", bg=GREENISH_WHITE, font=COURIER_FONT)

    # password label on grid
    password_label.grid(row=3, column=0)

    # TODO: Labels entry

    # website entry
    website_entry = Entry(width=42, font=COURIER_FONT)

    # website entry placement
    website_entry.grid(row=1, column=1)

    # focus the website entry
    website_entry.focus()

    # email entry
    email_entry = Entry(width=55, font=COURIER_FONT)

    # email entry placement on grid
    email_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

    # pre populated value
    email_entry.insert(0, "")

    # password entry
    password_entry = Entry(width=42, font=COURIER_FONT)

    # password entry placement on grid
    password_entry.grid(row=3, column=1)

    # TODO: Buttons

    # search button

    search_button = Button(text="Search", width=10, font=COURIER_FONT, bg=LIGHT_GREEN, command=find_password)

    # search button placement on grid
    search_button.grid(row=1, column=2)

    # generate password button
    generate_password_button = Button(text="Generate", width=10, font=COURIER_FONT, bg=LIGHT_SKY,
                                      command=password_generator)
    # generate button placement on grid
    generate_password_button.grid(row=3, column=2)

    # add password on file button
    save_button = Button(text="Save", width=55, bg=GREENISH_YELLOW, font=COURIER_FONT, command=save)

    # save button placement on the grid
    save_button.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

    # window run
    window.mainloop()


def login():

    # creating window object
    window = Tk()

    def Close():
        window.destroy()

    # window title
    window.title("Password Generator Login")

    # add custom favicon
    window.iconbitmap(r'logo.ico')

    # add padding and background color
    window.config(padx=60, pady=60, bg=GREENISH_WHITE)

    # canvas size
    canvas = Canvas(height=350, width=350, bg=GREENISH_WHITE, highlightthickness=0)

    # assign the image location to a variable
    logo_image = PhotoImage(file="download.png")

    # add image in the canvas in the center by "/" half of the dimension
    canvas.create_image(180, 150, image=logo_image)

    # assign the grid for the canvas
    canvas.grid(row=0, column=1)

    # TODO: Labels

    # website labels
    username_label = Label(text="User Name:", bg=GREENISH_WHITE, font=COURIER_FONT)

    # website label on grid
    username_label.grid(row=1, column=0)

    # email labels
    email_label = Label(text="Password:", bg=GREENISH_WHITE, font=COURIER_FONT)

    # email label on grid
    email_label.grid(row=2, column=0)

    # TODO: Labels entry

    # website entry
    username_entry = Entry(width=42, font=COURIER_FONT)

    # website entry placement
    username_entry.grid(row=1, column=1)

    # focus the website entry
    username_entry.focus()

    # email entry
    password_entry = Entry(width=42, font=COURIER_FONT)

    # email entry placement on grid
    password_entry.grid(row=2, column=1, columnspan=1, padx=10, pady=20)

    def save():
        q = username_entry.get()
        w = password_entry.get()
        try:
            with open("main_data.json") as data_file:
                # open the data file
                data = json.load(data_file)
            c = f.decrypt(data["username"])
            c = c.decode()
            d = f.decrypt(data["password"])
            d = d.decode()
            if q == c and w == d:
                # print("saved")
                messagebox.showinfo(title="Success", message="Successfully logged in")
                Close()
                password_vault()
            else:
                # print(q, w)
                messagebox.showinfo(title="Error", message="Invalid username or password.")
                Close()
                login()
        except FileNotFoundError:
            messagebox.showinfo(title="Error!!", message="Unexpected Error Occured")
            Close()

    def credentials():

        def Close():
            window.destroy()

        Close()

        # creating window object
        window2 = Tk()

        # window title
        window2.title("Password Generator Password Setting")

        # add custom favicon
        window2.iconbitmap(r'logo.ico')

        # add padding and background color
        window2.config(padx=60, pady=60, bg=GREENISH_WHITE)

        # canvas size
        canvas = Canvas(height=350, width=350, bg=GREENISH_WHITE, highlightthickness=0)

        # assign the image location to a variable
        logo_image = PhotoImage(file="download.png")

        # add image in the canvas in the center by "/" half of the dimension
        canvas.create_image(180, 150, image=logo_image)

        # assign the grid for the canvas
        canvas.grid(row=0, column=1)

        def Close2():
            window2.destroy()

        # TODO: Labels

        # website labels
        username_label = Label(text="New User Name:", bg=GREENISH_WHITE, font=COURIER_FONT)

        # website label on grid
        username_label.grid(row=1, column=0)

        # email labels
        email_label = Label(text="New Password:", bg=GREENISH_WHITE, font=COURIER_FONT)

        # email label on grid
        email_label.grid(row=2, column=0)

        # TODO: Labels entry

        # website entry
        username_entry = Entry(width=42, font=COURIER_FONT)

        # website entry placement
        username_entry.grid(row=1, column=1)

        # focus the website entry
        username_entry.focus()

        # email entry
        password_entry = Entry(width=42, font=COURIER_FONT)

        # email entry placement on grid
        password_entry.grid(row=2, column=1, columnspan=1, padx=10, pady=20)

        def save_password():
            new_data = {}
            a = username_entry.get()

            a = a.encode()
            a = f.encrypt(a)
            a = a.decode()

            b = password_entry.get()

            b = b.encode()
            b = f.encrypt(b)
            b = b.decode()

            new_data["username"] = a
            new_data["password"] = b


            with open("main_data.json", "w") as data_file:
                # saving updated data with indent 4
                json.dump(new_data, data_file, indent=4)

            messagebox.showinfo(title="Success", message="Credentials Changed")
            Close2()
            login()

        # TODO: Buttons
        # add password on file button
        save_button = Button(text="Save", width=10, bg=GREENISH_YELLOW, font=COURIER_FONT, command=save_password)
        # save button placement on the grid
        save_button.grid(row=4, column=1, columnspan=1, padx=10, pady=10)
        # window run
        window2.mainloop()

    # TODO: Buttons
    # add password on file button
    save_button = Button(text="Log in", width=10, bg = '#009E60', font=COURIER_FONT, command=save)
    # save button placement on the grid
    save_button.grid(row=4, column=1, columnspan=1, padx=10, pady=10)

    # add password on file button
    forget_button = Button(text="Forget Password", width=20, bg = GREENISH_YELLOW, font=COURIER_FONT, command=credentials)
    # save button placement on the grid
    forget_button.grid(row=5, column=1, columnspan=1, padx=10, pady=10)

    # window run
    window.mainloop()


login()
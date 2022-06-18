from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():

    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
   
    new_data={website: {
        "email": email,
        "password":password,
    }}

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")

    else:
        messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email} "f"\nPassword: {password} \nIs it ok to save?")
        try:
            with open("data.json","r") as data_file: 
                data=json.load(data_file) 
        except FileNotFoundError: 
            with open("data.json","w") as data_file: 
                json.dump(new_data,data_file,indent=4) 
        else:
            data.update(new_data)
            with open("data.json","w") as data_file:
                json.dump(data,data_file,indent=4) 
        finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END) 
# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data=json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error",message="No data file found")
    else:
        if website in data:
            email=data[website]["email"]
            password=data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
            password_entry.insert(0, password)
            pyperclip.copy(password)
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="white")

canvas = Canvas(height=250, width=250, bg="white",highlightthickness=0)
logo_img = PhotoImage(file="transparent_image.png")
canvas.create_image(150, 130, image=logo_img)
canvas.grid(row=0, column=1)

#Labels
website_label = Label(text="Website:", bg="white")
website_label.grid(sticky="w",row=1, column=0)
email_label = Label(text="Email/Username:", bg="white")
email_label.grid(sticky="w",row=2, column=0)
password_label = Label(text="Password:", bg="white")
password_label.grid(sticky="w",row=3, column=0)

#Entries
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1,sticky="news") # , columnspan=2
website_entry.focus()
email_entry = Entry(width=65)
email_entry.grid(row=2, column=1, columnspan=2,sticky="news")
email_entry.insert(0, "@gmail.com")
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1,sticky="news")

# Buttons
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2,sticky="news")
add_button = Button(text="Add", width=65, command=save)
add_button.grid(row=4, column=1, columnspan=2)
search_button=Button(text="Search",width=20,command=find_password)
search_button.grid(row=1,column=2,sticky="news")


window.mainloop()

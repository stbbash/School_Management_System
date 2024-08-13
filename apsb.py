import os
import socket
import sqlite3
from tkinter import messagebox, PhotoImage
import requests
from PIL import Image, ImageTk
from customtkinter import *
import database as db
from my_images import *

db.connect_database()
checked = db.table_exists("users")
class RootWindow(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x350")
        self.resizable(0, 0)
        self.title("Register Page")
        # Set the background color
        self.configure(fg_color="#191718")
        set_appearance_mode("dark")

        try:
            # Set the window icon
            self.iconbitmap(favicon_image)
        except Exception as e:
            print(f"{e}: Cant load image")

        try:
            # Load the .gif image using PhotoImage
            #self.image_reg = CTkImage(light_image=Image.open("favicon.gif"), size=(80, 80))
            self.image_reg = CTkImage(light_image=Image.open(gif_image),
                                              dark_image=Image.open(gif_image),
                                              size=(80, 80))
            # Create a CTkLabel and set the image
            self.image_top_reg = CTkLabel(self, image=self.image_reg, text="")
            self.image_top_reg.place(x=250, y=27)
        except Exception as e:
            print(f"{e}: Cant load image")

        self.heading_label_reg = CTkLabel(self, text="WELCOME TO THE ANAMBRA STATE PRIVATE DATA CAPTURE",
                                          bg_color="#191718",
                                          font=("Goudy Old Style", 15, "bold"), text_color="#FDC211")
        self.heading_label_reg.place(x=80, y=0)

        self.instruction_label_reg = CTkLabel(self, text="NB: Make sure you have internet access",
                                              bg_color="#191718",
                                              font=("arial", 10, "bold"), text_color="#BD1D18")
        self.instruction_label_reg.place(x=100, y=120)

        self.username_entry_reg = CTkEntry(self, placeholder_text="Enter your username", width=400, bg_color="#191718",
                                           text_color="#F3F4F6")
        self.username_entry_reg.place(x=100, y=150)

        self.password_label_reg = CTkLabel(self, text="CREATE A UNIQUE PASSWORD",
                                              bg_color="#191718",
                                              font=("arial", 13, "bold"), text_color="#FDC211")
        self.password_label_reg.place(x=100, y=190)

        self.password_entry1 = CTkEntry(self, placeholder_text="Enter your password", width=400,
                                        bg_color="#191718", text_color="#F3F4F6")
        self.password_entry1.place(x=100, y=220)

        self.password_entry2 = CTkEntry(self, placeholder_text="Enter your password again", width=400,
                                       bg_color="#191718", text_color="#F3F4F6")
        self.password_entry2.place(x=100, y=270)

        self.register_button = CTkButton(self, text="Register", bg_color="#191718", cursor="hand2",
                                         command=self.register, fg_color="#10A1E1")
        self.register_button.place(x=230, y=310)

        # Create a label for the status
        self.status_reg = CTkLabel(self, text="Checking...", width=20, bg_color="#191718",
                                   font=("Goudy Old Style", 15, "bold"))
        self.status_reg.place(x=25, y=325)

        self.connection_state_reg = "Checking..."
        # Create a canvas for the status circle
        self.status_canvas_reg = CTkCanvas(self, width=20, height=20, bg="#191718", highlightthickness=0)
        self.status_canvas_reg.place(x=5, y=500)

    def verify_user(self):
        try:
            # Send a GET request to the specified URL with a timeout
            response = requests.get('https://stbbash.pythonanywhere.com/app/api/users/', timeout=10)
            response.raise_for_status()  # Check for HTTP errors
            result = response.json()
            for people in result:
                if self.username_entry_reg.get() == people["username"] and people["is_active"]:
                    user_id = people["id"]
                    # with open("output.csv", "w", newline='') as output:
                    #     fieldnames = ["id", "username"]
                    #     writer = csv.DictWriter(output, fieldnames=fieldnames)
                    #     writer.writeheader()
                    #     writer.writerow({"id": people["id"], "username": people["username"]})
                    db.create_user(self.username_entry_reg.get(), self.password_entry1.get(), user_id)
                    return True
        except Exception as json_err:
            return False

    def register(self):
        if self.verify_user():
            messagebox.showinfo(f"Success",
                                f"Registration is successful, you can login now \nUsername: {self.username_entry_reg.get()} \nPassword: {self.password_entry1.get()}")
            self.switch_to_login_window()
        elif self.username_entry_reg.get() == "" or self.password_entry1.get() == "" or self.password_entry2.get() == "":
            messagebox.showerror("Error", "All fields are required")
        elif self.password_entry1.get() != self.password_entry2.get():
            messagebox.showerror("Error", "Passwords do not match")
        elif self.connection_state_reg == "Offline":
            messagebox.showwarning("No Internet Access", "Please connect to the Internet to continue")
        else:
            messagebox.showerror("Error", "Username not Found")

    def switch_to_login_window(self):
        self.destroy()  # Hide the main window
        from login import MainWindow
        login_window = MainWindow()
        login_window.mainloop()

    def draw_online_status_reg(self):
        self.status_canvas_reg.delete("all")
        self.status_canvas_reg.create_oval(5, 5, 15, 15, fill="#00ff00")

    # Draw a red circle for offline status
    def draw_offline_status_reg(self):
        self.status_canvas_reg.delete("all")
        self.status_canvas_reg.create_oval(5, 5, 15, 15, fill="#ff0000")

    def is_connected_reg(self):
        try:
            socket.create_connection(("www.google.com", 80), timeout=1)  # Set a timeout of 1 second
            self.connection_state_reg = "Online"
            self.draw_online_status_reg()
        except OSError:
            self.connection_state_reg = "Offline"
            self.draw_offline_status_reg()
        self.status_reg.configure(text=self.connection_state_reg)
        self.after(1000, self.is_connected_reg)


if __name__ == "__main__":
    if checked:
        from login import MainWindow
        login_window = MainWindow()
        login_window.mainloop()
    else:
        root_window = RootWindow()
        root_window.is_connected_reg()
        root_window.mainloop()

import csv
import database as db
from tkinter import messagebox, PhotoImage
from PIL import Image, ImageTk
from customtkinter import *
from my_images import *



class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("930x478")
        self.resizable(0, 0)
        self.title("Login Page")
        set_appearance_mode("dark")

        try:
            # Set the window icon
            self.iconbitmap(favicon_image)
        except Exception as e:
            print(f"{e}: Cant load image")
        # # Create a button to switch to the second window
        # switch_button = CTkButton(self, text="Switch to Second Window", command=self.switch_to_second_window)
        # switch_button.pack(pady=20)

        try:
            self.image1 = CTkImage(Image.open(background_image), size=(930, 478))
            self.image_top = CTkLabel(self, image=self.image1, text="")
            self.image_top.place(x=0, y=0)
        except Exception as e:
            print(f"{e}: Cant load image")

        self.heading_label = CTkLabel(self, text="Private Schools Management System", bg_color="#F3F4F6",
                                      font=("arial", 20, "bold"), text_color="#191718")
        self.heading_label.place(x=280, y=120)

        self.username_entry = CTkEntry(self, placeholder_text="Enter your username", width=220, bg_color="#191718",
                                       text_color="#F3F4F6")
        self.username_entry.place(x=340, y=300)

        self.password_entry = CTkEntry(self, placeholder_text="Enter your username", width=220, show="*",
                                       bg_color="#191718", text_color="#F3F4F6")
        self.password_entry.place(x=340, y=350)

        self.login_button = CTkButton(self, text="Login", bg_color="#F3F4F6", cursor="hand2", command=self.login)
        self.login_button.place(x=380, y=400)

    def switch_to_school_window(self):
        self.destroy()  # Hide the main window
        from school import SchoolWindow
        school_window = SchoolWindow()
        school_window.is_connected()
        school_window.mainloop()

    def login(self):
        # try:
        #     with open("output.csv", "r", newline='') as file:
        #         csv_reader = csv.DictReader(file)
        #         for row in csv_reader:
        #             if row['username']:
        #                 username = row['username']
        # except FileNotFoundError:
        #     quit()
        result = db.check_user(self.username_entry.get(), self.password_entry.get())
        if result:
            if self.username_entry.get() == result[0][0] and self.password_entry.get() == result[0][1]:
                messagebox.showinfo("Success", "Login is successful")
                self.switch_to_school_window()
        elif self.username_entry.get() == "" or self.password_entry.get() == "":
            messagebox.showerror("Error", "All fields are required")
        else:
            messagebox.showerror("Error", "Invalid username or password")

if __name__ == "__main__":
    login_window = MainWindow()
    login_window.mainloop()

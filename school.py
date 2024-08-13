import socket
import sqlite3
from io import BytesIO
from tkinter import Menu, PhotoImage, messagebox, ttk
from PIL import Image, ImageTk
from customtkinter import *
import database as db
from my_images import *





class SchoolWindow(CTk):
    def __init__(self):
        super().__init__()
        self.title("School List")
        self.geometry("930x478")
        # self.resizable(0, 0)
        set_appearance_mode("dark")

        try:
            # Set the window icon
            self.iconbitmap(favicon_image)
        except Exception as e:
            print(f"{e}: Cant load image")

        self.menu_bar = Menu(self)

        # Create the File menu
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New")
        self.file_menu.add_command(label="Open")
        self.file_menu.add_command(label="Save")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Create the View menu
        self.view_menu = Menu(self.menu_bar, tearoff=0)
        self.view_menu.add_command(label="View Students", command=self.view_students)
        self.view_menu.add_command(label="View Teachers", command=self.view_teachers)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)

        # Create the Admin menu
        self.admin_menu = Menu(self.menu_bar, tearoff=0)
        self.admin_menu.add_command(label="upload")
        self.admin_menu.add_command(label="Delete all", command=self.delete_all)
        self.menu_bar.add_cascade(label="Admin", menu=self.admin_menu)

        # Create the Help menu
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About")
        self.help_menu.add_command(label="Contact")
        self.help_menu.add_command(label="logout")
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        # Add the menu bar to the app
        self.config(menu=self.menu_bar)

        # Create the main frame
        self.main_frame = CTkFrame(self, fg_color="#191718")
        self.main_frame.pack(fill="both", expand=True)

        # Configure the grid to make the frames expand
        self.main_frame.grid_columnconfigure(0, weight=1, uniform="foo")
        self.main_frame.grid_columnconfigure(1, weight=1, uniform="foo")
        self.main_frame.grid_rowconfigure(1, weight=1)

        # Create school label
        self.school_label = CTkLabel(self.main_frame, text="School list", bg_color="#191718",
                                     font=("Goudy Old Style", 20, "bold"), text_color="#F3F4F6")
        self.school_label.grid(row=0, column=0, columnspan=2)

        """ ----------------LEFT SIDE ----------------"""
        self.left_frame = CTkFrame(self.main_frame, fg_color="#191718")
        self.left_frame.grid(row=1, column=0, sticky="nsew")

        # Configure the grid for the left frame
        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_columnconfigure(1, weight=0)

        # Create canvas and scrollbar
        self.canvas = CTkCanvas(self.left_frame, bg="#191718")
        self.scrollbar = CTkScrollbar(self.left_frame, orientation="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="nsew")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Configure canvas to use scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create frame within canvas for widgets
        self.scrollable_frame = CTkFrame(self.canvas, fg_color="#191718")
        # Make sure scrollable frame expands to fill the canvas
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_rowconfigure(0, weight=1)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="center", tags="scrollable_frame")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig("scrollable_frame", width=e.width)
        )
        self.canvas.configure(bg="#191718")

        # Define choices
        self.CONTENT_CHOICES = [("Logo", "Logo"), ("Passport", "Passport")]
        self.LGA_CHOICES = [('Anambra East', 'Anambra East'), ('Anambra West', 'Anambra West'),
                            ('Ayamelum', 'Ayamelum'), ('Ogbaru', 'Ogbaru'),
                            ('Onitsha North', 'Onitsha North'), ('Onitsha South', 'Onitsha South'),
                            ('Oyi', 'Oyi'), ('Awka North', 'Awka North'),
                            ('Awka South', 'Awka South'), ('Anaocha', 'Anaocha'),
                            ('Dunukofia', 'Dunukofia'), ('Idemili North', 'Idemili North'),
                            ('Idemili South', 'Idemili South'), ('Njikoka', 'Njikoka'),
                            ('Aguata', 'Aguata'), ('Ekwusigo', 'Ekwusigo'),
                            ('Ihiala', 'Ihiala'), ('Nnewi North', 'Nnewi North'),
                            ('Nnewi South', 'Nnewi South'), ('Orumba North', 'Orumba North'),
                            ('Orumba South', 'Orumba South')]
        self.SETTLEMENT_CHOICES = [('Rural', 'Rural'), ('Urban', 'Urban')]
        self.EDUCATION_CHOICES = [('Primary', 'Primary'), ('Secondary', 'Secondary')]
        self.CATEGORY_CHOICES = [('Public', 'Public'), ('Private', 'Private')]
        self.GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Mixed', 'Mixed')]
        self.OPTION_CHOICES = [("Yes", "Yes"), ("No", "No")]
        self.SECURITY_CHOICES = [("PTA Employee", "PTA Employee"), ("Government", "Government")]
        self.STATUS_CHOICES = [("Active", "Active"), ("Inactive", "Inactive")]

        # Create Picture
        self.picture_label = CTkLabel(self.scrollable_frame, text="Picture", font=("arial", 16, "bold"))
        self.picture_label.grid(row=0, column=0, padx=20, pady=5)
        self.browse_button = CTkButton(self.scrollable_frame, text="Browse", width=180, command=self.browse_picture)
        self.browse_button.grid(row=0, column=1, padx=20, pady=5)

        # Create Content Type
        self.content_type_label = CTkLabel(self.scrollable_frame, text="Content Type", font=("arial", 16, "bold"))
        self.content_type_label.grid(row=1, column=0, padx=20, pady=5)
        self.content_type_combo = CTkComboBox(self.scrollable_frame,
                                              values=[choice[0] for choice in self.CONTENT_CHOICES],
                                              font=("arial", 12, "bold"), width=180, state="readonly")
        self.content_type_combo.grid(row=1, column=1, padx=20, pady=5)

        # Create Name
        self.name_label = CTkLabel(self.scrollable_frame, text="Name", font=("arial", 16, "bold"))
        self.name_label.grid(row=2, column=0, padx=20, pady=5)
        self.name_entry = CTkEntry(self.scrollable_frame, font=("arial", 12, "bold"), width=180)
        self.name_entry.grid(row=2, column=1, padx=20, pady=5)

        # Create Contact Address
        self.contact_address_label = CTkLabel(self.scrollable_frame, text="Contact Address", font=("arial", 16, "bold"))
        self.contact_address_label.grid(row=3, column=0, padx=20, pady=5)
        self.contact_address_entry = CTkEntry(self.scrollable_frame, font=("arial", 12, "bold"), width=180)
        self.contact_address_entry.grid(row=3, column=1, padx=20, pady=5)

        # Create Town
        self.town_label = CTkLabel(self.scrollable_frame, text="Town", font=("arial", 16, "bold"))
        self.town_label.grid(row=4, column=0, padx=20, pady=5)
        self.town_entry = CTkEntry(self.scrollable_frame, font=("arial", 12, "bold"), width=180)
        self.town_entry.grid(row=4, column=1, padx=20, pady=5)

        # Create Ward
        self.ward_label = CTkLabel(self.scrollable_frame, text="Ward", font=("arial", 16, "bold"))
        self.ward_label.grid(row=5, column=0, padx=20, pady=5)
        self.ward_entry = CTkEntry(self.scrollable_frame, font=("arial", 12, "bold"), width=180)
        self.ward_entry.grid(row=5, column=1, padx=20, pady=5)

        # Create LGA
        self.lga_label = CTkLabel(self.scrollable_frame, text="LGA", font=("arial", 16, "bold"))
        self.lga_label.grid(row=6, column=0, padx=20, pady=5)
        self.lga_combo = CTkComboBox(self.scrollable_frame, values=[choice[0] for choice in self.LGA_CHOICES],
                                     font=("arial", 12, "bold"), width=180, state="readonly")
        self.lga_combo.grid(row=6, column=1, padx=20, pady=5)

        # Create Email
        self.email_label = CTkLabel(self.scrollable_frame, text="Email", font=("arial", 16, "bold"))
        self.email_label.grid(row=7, column=0, padx=20, pady=5)
        self.email_entry = CTkEntry(self.scrollable_frame, font=("arial", 12, "bold"), width=180)
        self.email_entry.grid(row=7, column=1, padx=20, pady=5)

        # Create Phone
        self.phone_label = CTkLabel(self.scrollable_frame, text="Phone", font=("arial", 16, "bold"))
        self.phone_label.grid(row=8, column=0, padx=20, pady=5)
        self.phone_entry = CTkEntry(self.scrollable_frame, font=("arial", 12, "bold"), width=180)
        self.phone_entry.grid(row=8, column=1, padx=20, pady=5)

        # Create Year Established
        self.year_established_label = CTkLabel(self.scrollable_frame, text="Year Established",
                                               font=("arial", 16, "bold"))
        self.year_established_label.grid(row=9, column=0, padx=20, pady=5)
        self.year_established_entry = CTkEntry(self.scrollable_frame, font=("arial", 12, "bold"), width=180)
        self.year_established_entry.grid(row=9, column=1, padx=20, pady=5)

        # Create Settlement
        self.settlement_label = CTkLabel(self.scrollable_frame, text="Settlement", font=("arial", 16, "bold"))
        self.settlement_label.grid(row=10, column=0, padx=20, pady=5)
        self.settlement_combo = CTkComboBox(self.scrollable_frame,
                                            values=[choice[0] for choice in self.SETTLEMENT_CHOICES],
                                            font=("arial", 12, "bold"), width=180, state="readonly")
        self.settlement_combo.grid(row=10, column=1, padx=20, pady=5)

        # Create Education
        self.education_label = CTkLabel(self.scrollable_frame, text="Education", font=("arial", 16, "bold"))
        self.education_label.grid(row=11, column=0, padx=20, pady=5)
        self.education_combo = CTkComboBox(self.scrollable_frame,
                                           values=[choice[0] for choice in self.EDUCATION_CHOICES],
                                           font=("arial", 12, "bold"), width=180, state="readonly")
        self.education_combo.grid(row=11, column=1, padx=20, pady=5)

        # Create Category
        self.category_label = CTkLabel(self.scrollable_frame, text="Category", font=("arial", 16, "bold"))
        self.category_label.grid(row=12, column=0, padx=20, pady=5)
        self.category_combo = CTkComboBox(self.scrollable_frame, values=[choice[0] for choice in self.CATEGORY_CHOICES],
                                          font=("arial", 12, "bold"), width=180, state="readonly")
        self.category_combo.grid(row=12, column=1, padx=20, pady=5)

        # Create Gender
        self.gender_label = CTkLabel(self.scrollable_frame, text="Gender", font=("arial", 16, "bold"))
        self.gender_label.grid(row=13, column=0, padx=20, pady=5)
        self.gender_combo = CTkComboBox(self.scrollable_frame, values=[choice[0] for choice in self.GENDER_CHOICES],
                                        font=("arial", 12, "bold"), width=180, state="readonly")
        self.gender_combo.grid(row=13, column=1, padx=20, pady=5)

        # Create Operate Shift System
        self.operate_shift_system_label = CTkLabel(self.scrollable_frame, text="Operate Shift System",
                                                   font=("arial", 16, "bold"))
        self.operate_shift_system_label.grid(row=14, column=0, padx=20, pady=5)
        self.operate_shift_system_combo = CTkComboBox(self.scrollable_frame,
                                                      values=[choice[0] for choice in self.OPTION_CHOICES],
                                                      font=("arial", 12, "bold"), width=180, state="readonly")
        self.operate_shift_system_combo.grid(row=14, column=1, padx=20, pady=5)

        # Create Share Facility
        self.share_facility_label = CTkLabel(self.scrollable_frame, text="Share Facility", font=("arial", 16, "bold"))
        self.share_facility_label.grid(row=15, column=0, padx=20, pady=5)
        self.share_facility_combo = CTkComboBox(self.scrollable_frame,
                                                values=[choice[0] for choice in self.OPTION_CHOICES],
                                                font=("arial", 12, "bold"), width=180, state="readonly")
        self.share_facility_combo.grid(row=15, column=1, padx=20, pady=5)

        # Create Have Boarding Facility
        self.have_boarding_facility_label = CTkLabel(self.scrollable_frame, text="Have Boarding Facility",
                                                     font=("arial", 16, "bold"))
        self.have_boarding_facility_label.grid(row=16, column=0, padx=20, pady=5)
        self.have_boarding_facility_combo = CTkComboBox(self.scrollable_frame,
                                                        values=[choice[0] for choice in self.OPTION_CHOICES],
                                                        font=("arial", 12, "bold"), width=180, state="readonly")
        self.have_boarding_facility_combo.grid(row=16, column=1, padx=20, pady=5)

        # Create Have Perimeter Fencing
        self.have_perimeter_fencing_label = CTkLabel(self.scrollable_frame, text="Have Perimeter Fencing",
                                                     font=("arial", 16, "bold"))
        self.have_perimeter_fencing_label.grid(row=17, column=0, padx=20, pady=5)
        self.have_perimeter_fencing_combo = CTkComboBox(self.scrollable_frame,
                                                        values=[choice[0] for choice in self.OPTION_CHOICES],
                                                        font=("arial", 12, "bold"), width=180, state="readonly")
        self.have_perimeter_fencing_combo.grid(row=17, column=1, padx=20, pady=5)

        # Create Have Security Person
        self.have_security_person_label = CTkLabel(self.scrollable_frame, text="Have Security Person",
                                                   font=("arial", 16, "bold"))
        self.have_security_person_label.grid(row=18, column=0, padx=20, pady=5)
        self.have_security_person_combo = CTkComboBox(self.scrollable_frame,
                                                      values=[choice[0] for choice in self.OPTION_CHOICES],
                                                      font=("arial", 12, "bold"), width=180, state="readonly")
        self.have_security_person_combo.grid(row=18, column=1, padx=20, pady=5)

        # Create Type of Security
        self.type_of_security_label = CTkLabel(self.scrollable_frame, text="Type of Security",
                                               font=("arial", 16, "bold"))
        self.type_of_security_label.grid(row=19, column=0, padx=20, pady=5)
        self.type_of_security_combo = CTkComboBox(self.scrollable_frame,
                                                  values=[choice[0] for choice in self.SECURITY_CHOICES],
                                                  font=("arial", 12, "bold"), width=180, state="readonly")
        self.type_of_security_combo.grid(row=19, column=1, padx=20, pady=5)

        # Create Number of Security
        self.no_of_security_label = CTkLabel(self.scrollable_frame, text="Number of Security",
                                             font=("arial", 16, "bold"))
        self.no_of_security_label.grid(row=20, column=0, padx=20, pady=5)
        self.no_of_security_entry = CTkEntry(self.scrollable_frame, font=("arial", 12, "bold"), width=180)
        self.no_of_security_entry.grid(row=20, column=1, padx=20, pady=5)

        # Create Prepare School Improvement Plan
        self.prepare_school_improvement_plan_label = CTkLabel(self.scrollable_frame,
                                                              text="Prepare School Improvement Plan",
                                                              font=("arial", 16, "bold"))
        self.prepare_school_improvement_plan_label.grid(row=21, column=0, padx=20, pady=5)
        self.prepare_school_improvement_plan_combo = CTkComboBox(self.scrollable_frame,
                                                                 values=[choice[0] for choice in self.OPTION_CHOICES],
                                                                 font=("arial", 12, "bold"), width=180,
                                                                 state="readonly")
        self.prepare_school_improvement_plan_combo.grid(row=21, column=1, padx=20, pady=5)

        # Create Have PTA
        self.have_pta_label = CTkLabel(self.scrollable_frame, text="Have PTA", font=("arial", 16, "bold"))
        self.have_pta_label.grid(row=22, column=0, padx=20, pady=5)
        self.have_pta_combo = CTkComboBox(self.scrollable_frame, values=[choice[0] for choice in self.OPTION_CHOICES],
                                          font=("arial", 12, "bold"), width=180, state="readonly")
        self.have_pta_combo.grid(row=22, column=1, padx=20, pady=5)

        # Create Have Playground
        self.have_playground_label = CTkLabel(self.scrollable_frame, text="Have Playground", font=("arial", 16, "bold"))
        self.have_playground_label.grid(row=23, column=0, padx=20, pady=5)
        self.have_playground_combo = CTkComboBox(self.scrollable_frame,
                                                 values=[choice[0] for choice in self.OPTION_CHOICES],
                                                 font=("arial", 12, "bold"), width=180, state="readonly")
        self.have_playground_combo.grid(row=23, column=1, padx=20, pady=5)

        # Create Have Sport Facility
        self.have_sport_facility_label = CTkLabel(self.scrollable_frame, text="Have Sport Facility",
                                                  font=("arial", 16, "bold"))
        self.have_sport_facility_label.grid(row=24, column=0, padx=20, pady=5)
        self.have_sport_facility_combo = CTkComboBox(self.scrollable_frame,
                                                     values=[choice[0] for choice in self.OPTION_CHOICES],
                                                     font=("arial", 12, "bold"), width=180, state="readonly")
        self.have_sport_facility_combo.grid(row=24, column=1, padx=20, pady=5)

        # Create Status
        self.status_school_label = CTkLabel(self.scrollable_frame, text="Status", font=("arial", 16, "bold"))
        self.status_school_label.grid(row=25, column=0, padx=20, pady=5)
        self.status = CTkComboBox(self.scrollable_frame, values=[choice[0] for choice in self.STATUS_CHOICES],
                                  font=("arial", 12, "bold"), width=180, state="readonly")
        self.status.grid(row=25, column=1, padx=20, pady=5)

        """ ----------------RIGHT SIDE ----------------"""

        # Create right frame
        self.right_frame = CTkFrame(self.main_frame, fg_color="#191718")
        self.right_frame.grid(row=1, column=1, sticky="nsew")

        # Configure grid for right frame
        self.right_frame.grid_rowconfigure(0, weight=0)  # search row
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(1, weight=1)  # treeview row
        self.right_frame.grid_columnconfigure(1, weight=1)  # treeview column

        # Define search options
        self.search_options = [
            'name', 'contact_address', 'town', 'ward', 'lga', 'email', 'phone',
            'year_established', 'settlement', 'education', 'category', 'gender',
            'operate_shift_system', 'share_facility', 'have_boarding_facility',
            'have_perimeter_fencing', 'have_security_person', 'type_of_security',
            'no_of_security', 'prepare_school_improvement_plan', 'have_pta',
            'have_playground', 'have_sport_facility', 'status'
        ]

        # Create search box
        self.search_box = CTkComboBox(self.right_frame, values=self.search_options, state="readonly")
        self.search_box.grid(row=0, column=0, padx=5, pady=5)
        self.search_box.set("Search By")

        # Create search entry
        self.search_entry = CTkEntry(self.right_frame)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)

        # Create search button
        self.search_button = CTkButton(self.right_frame, text="Search", command=self.search_school)
        self.search_button.grid(row=0, column=2, padx=5, pady=5)

        # Create show all button
        self.search_refresh_button = CTkButton(self.right_frame, text="Refresh", command=self.search_refresh)
        self.search_refresh_button.grid(row=0, column=3, padx=5, pady=5)

        # Create treeview and scrollbars
        self.tree = ttk.Treeview(self.right_frame, height=13)
        self.tree.grid(row=1, column=0, sticky="nsew", columnspan=4)

        # Create vertical scrollbar
        self.v_scrollbar = CTkScrollbar(self.right_frame, orientation="vertical", command=self.tree.yview)
        self.v_scrollbar.grid(row=1, column=4, sticky="ns")

        # Create horizontal scrollbar
        self.h_scrollbar = CTkScrollbar(self.right_frame, orientation="horizontal", command=self.tree.xview)
        self.h_scrollbar.grid(row=2, column=0, sticky="ew", columnspan=4)

        # Configure treeview to use scrollbars
        self.tree.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)

        self.tree["columns"] = (
            'id',
            'picture',
            'content_type',
            'name',
            'contact_address',
            'town',
            'ward',
            'lga',
            'email',
            'phone',
            'year_established',
            'settlement',
            'education',
            'category',
            'gender',
            'operate_shift_system',
            'share_facility',
            'have_boarding_facility',
            'have_perimeter_fencing',
            'have_security_person',
            'type_of_security',
            'no_of_security',
            'prepare_school_improvement_plan',
            'have_pta',
            'have_playground',
            'have_sport_facility',
            'status'
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("picture", text="Picture")
        self.tree.heading("content_type", text="Content Type")
        self.tree.heading("name", text="Name")
        self.tree.heading("contact_address", text="Contact Address")
        self.tree.heading("town", text="Town")
        self.tree.heading("ward", text="Ward")
        self.tree.heading("lga", text="LGA")
        self.tree.heading("email", text="Email")
        self.tree.heading("phone", text="Phone")
        self.tree.heading("year_established", text="Year Established")
        self.tree.heading("settlement", text="Settlement")
        self.tree.heading("education", text="Education")
        self.tree.heading("category", text="Category")
        self.tree.heading("gender", text="Gender")
        self.tree.heading("operate_shift_system", text="Operate Shift System")
        self.tree.heading("share_facility", text="Share Facility")
        self.tree.heading("have_boarding_facility", text="Have Boarding Facility")
        self.tree.heading("have_perimeter_fencing", text="Have Perimeter Fencing")
        self.tree.heading("have_security_person", text="Have Security Personnel")
        self.tree.heading("type_of_security", text="Type of Security")
        self.tree.heading("no_of_security", text="Number of Security Personnel")
        self.tree.heading("prepare_school_improvement_plan", text="Prepare School Improvement Plan")
        self.tree.heading("have_pta", text="Have PTA")
        self.tree.heading("have_playground", text="Have Playground")
        self.tree.heading("have_sport_facility", text="Have Sport Facility")
        self.tree.heading("status", text="Status")

        self.tree.config(show="headings")

        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=("arial", 15, "bold"))
        self.style.configure("Treeview", font=("Arial", 15, "bold"), rowheight=30, background="#191718",
                             foreground="white")

        # Create a frame for the status bar
        self.status_bar_frame = CTkFrame(self, fg_color="#f0f0f0", corner_radius=0)
        self.status_bar_frame.pack(fill="x", side="bottom")

        # Create a label for the status
        self.status_label = CTkLabel(self.status_bar_frame, text="Status: ", width=20,
                                     font=("Goudy Old Style", 20, "bold"),
                                     text_color="#191718")
        self.status_label.pack(side="left", padx=10, pady=10)
        self.internet_status = CTkLabel(self.status_bar_frame, text="Checking ", width=20,
                                        font=("Goudy Old Style", 20, "bold"),
                                        text_color="#191718")
        self.internet_status.pack(side="left", padx=10, pady=10)

        # Create a canvas for the status circle
        self.status_canvas = CTkCanvas(self.status_bar_frame, width=20, height=20, bg="#f0f0f0", highlightthickness=0)
        self.status_canvas.pack(side="left", padx=10, pady=10)

        # Create a logout button
        self.logout_button = CTkButton(self.status_bar_frame, text="Logout", command=self.logout, fg_color="#ff0000",
                                       cursor="hand2", hover_color="#1C3441")
        self.logout_button.pack(side="right", padx=10, pady=10)

        self.delete_school_button = CTkButton(self.status_bar_frame, text="Delete School", command=self.delete_school,
                                              fg_color="#179AD8",
                                              cursor="hand2", hover_color="#1C3441")
        self.delete_school_button.pack(side="right", padx=10, pady=10)

        self.update_school_button = CTkButton(self.status_bar_frame, text="Update School", command=self.update_schoool,
                                              fg_color="#179AD8",
                                              cursor="hand2", hover_color="#1C3441")
        self.update_school_button.pack(side="right", padx=10, pady=10)

        self.add_school_button = CTkButton(self.status_bar_frame, text="Add School", command=self.add_school,
                                           fg_color="#179AD8",
                                           cursor="hand2", hover_color="#1C3441")
        self.add_school_button.pack(side="right", padx=10, pady=10)

        self.show_all_school_button = CTkButton(self.status_bar_frame, text="refresh",
                                                command=lambda: self.clear_school_form(True),
                                                fg_color="#179AD8",
                                                cursor="hand2", hover_color="#1C3441")
        self.show_all_school_button.pack(side="right", padx=10, pady=10)

        self.connection_state = "Checking..."

        self.list_school()
        self.bind("<ButtonRelease>", self.selected_school)
        self.image_blob = None

    def search_refresh(self):
        self.list_school()
        self.search_box.set("Search By")
        self.search_entry.delete(0, END)

    def search_school(self):
        if self.search_entry.get() == "":
            messagebox.showerror("Error", "No field to search")
        elif self.search_box.get() == "Search By":
            messagebox.showerror("Error", "Please select a search option")
        else:
            search_result = db.search(self.search_box.get().strip(), self.search_entry.get().strip())
            self.tree.delete(*self.tree.get_children())
            if search_result:
                for school in search_result:
                    if school:
                        self.tree.insert("", "end", values=school)
                    else:
                        messagebox.showinfo("Info", "No matching school found")
    def browse_picture(self):
        # Open a file dialog to select an image file
        file_path = filedialog.askopenfilename(title="Open Image File", filetypes=[("Image files", "*.jpg;*.png")])
        if not file_path:
            messagebox.showwarning("No File Selected", "Please select an image file.")
        else:
            try:
                # Check the file size (1MB = 1,000,000 bytes)
                max_file_size = 500_000  # 1MB
                file_size = os.path.getsize(file_path)
                if file_size > max_file_size:
                    messagebox.showwarning("File Too Large",
                                           "The selected image is too large. Please select an image smaller than 0.5MB.")
                    return
                # Read the uploaded image
                image = Image.open(file_path)
                # Resize the image to 30% of its original size
                width, height = image.size
                new_size = (int(width * 0.3), int(height * 0.3))
                image = image.resize(new_size, Image.LANCZOS)
                # Compress and save the image to a BytesIO object
                compressed_image_io = BytesIO()
                if file_path.lower().endswith(("jpeg", "jpg")):
                    image.save(compressed_image_io, format='JPEG', quality=50)
                elif file_path.lower().endswith("png"):
                    image.save(compressed_image_io, format='PNG', optimize=True)
                else:
                    raise ValueError("Unsupported image format.")
                # Get the BLOB data
                compressed_image_io.seek(0)
                self.image_blob = compressed_image_io.getvalue()
                # Close the BytesIO object
                compressed_image_io.close()
                return self.image_blob
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while processing the image: {e}")

    def add_school(self):
        data = (
            self.name_entry.get().strip(),
            self.image_blob,
            self.content_type_combo.get().strip(),
            self.contact_address_entry.get().strip(),
            self.town_entry.get().strip(),
            self.ward_entry.get().strip(),
            self.email_entry.get().strip(),
            self.phone_entry.get().strip(),
            self.year_established_entry.get().strip(),
            self.no_of_security_entry.get().strip(),
            self.lga_combo.get().strip(),
            self.settlement_combo.get().strip(),
            self.education_combo.get().strip(),
            self.category_combo.get().strip(),
            self.gender_combo.get().strip(),
            self.operate_shift_system_combo.get().strip(),
            self.share_facility_combo.get().strip(),
            self.have_boarding_facility_combo.get().strip(),
            self.have_perimeter_fencing_combo.get().strip(),
            self.have_security_person_combo.get().strip(),
            self.type_of_security_combo.get().strip(),
            self.prepare_school_improvement_plan_combo.get().strip(),
            self.have_pta_combo.get().strip(),
            self.have_playground_combo.get().strip(),
            self.have_sport_facility_combo.get().strip(),
            self.status.get().strip()
        )
        for field in data:
            if field == "":
                messagebox.showerror("Error", "All fields are required")
                return False
        db.insert(data)
        self.list_school()
        self.clear_school_form()
        return True

    def update_schoool(self):
        data = (
            self.name_entry.get().strip(),
            self.image_blob,
            self.content_type_combo.get().strip(),
            self.contact_address_entry.get().strip(),
            self.town_entry.get().strip(),
            self.ward_entry.get().strip(),
            self.email_entry.get().strip(),
            self.phone_entry.get().strip(),
            self.year_established_entry.get().strip(),
            self.no_of_security_entry.get().strip(),
            self.lga_combo.get().strip(),
            self.settlement_combo.get().strip(),
            self.education_combo.get().strip(),
            self.category_combo.get().strip(),
            self.gender_combo.get().strip(),
            self.operate_shift_system_combo.get().strip(),
            self.share_facility_combo.get().strip(),
            self.have_boarding_facility_combo.get().strip(),
            self.have_perimeter_fencing_combo.get().strip(),
            self.have_security_person_combo.get().strip(),
            self.type_of_security_combo.get().strip(),
            self.prepare_school_improvement_plan_combo.get().strip(),
            self.have_pta_combo.get().strip(),
            self.have_playground_combo.get().strip(),
            self.have_sport_facility_combo.get().strip(),
            self.status.get().strip()
        )
        self.selected_item = self.tree.selection()
        if self.selected_item:
            self.row = self.tree.item(self.selected_item)["values"]
            school_id = self.row[0]
            db.update(data, school_id)
            self.list_school()
            self.clear_school_form()
        else:
            messagebox.showerror("Error", "Please select data to update")

    def list_school(self):
        schools = db.fetch_school()
        self.tree.delete(*self.tree.get_children())
        for school in schools:
            self.tree.insert("", "end", values=school)

    def selected_school(self, event):
        self.selected_item = self.tree.selection()
        if self.selected_item:
            self.clear_school_form()
            # Get the row data for the selected item
            self.row = self.tree.item(self.selected_item)["values"]

            # Insert values into the entry fields
            self.name_entry.insert(0, self.row[3])
            self.contact_address_entry.insert(0, self.row[4])
            self.town_entry.insert(0, self.row[5])
            self.ward_entry.insert(0, self.row[6])
            self.email_entry.insert(0, self.row[8])
            self.phone_entry.insert(0, self.row[9])
            self.year_established_entry.insert(0, self.row[10])
            self.no_of_security_entry.insert(0, self.row[21])

            # Set values for the combo boxes
            self.content_type_combo.set(self.row[2])
            self.lga_combo.set(self.row[9])
            self.settlement_combo.set(self.row[11])
            self.education_combo.set(self.row[12])
            self.category_combo.set(self.row[13])
            self.gender_combo.set(self.row[14])
            self.operate_shift_system_combo.set(self.row[15])
            self.share_facility_combo.set(self.row[16])
            self.have_boarding_facility_combo.set(self.row[17])
            self.have_perimeter_fencing_combo.set(self.row[18])
            self.have_security_person_combo.set(self.row[19])
            self.type_of_security_combo.set(self.row[20])
            self.prepare_school_improvement_plan_combo.set(self.row[22])
            self.have_pta_combo.set(self.row[23])
            self.have_playground_combo.set(self.row[24])
            self.have_sport_facility_combo.set(self.row[25])
            self.status.set(self.row[26])

    def clear_school_form(self, value=False):
        if value:
            self.tree.selection_remove(self.tree.focus())
        # Clear all entry fields
        self.name_entry.delete(0, END)
        self.contact_address_entry.delete(0, END)
        self.town_entry.delete(0, END)
        self.ward_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.phone_entry.delete(0, END)
        self.year_established_entry.delete(0, END)
        self.no_of_security_entry.delete(0, END)

        # Reset all combo boxes
        self.content_type_combo.set('')
        self.lga_combo.set('')
        self.settlement_combo.set('')
        self.education_combo.set('')
        self.category_combo.set('')
        self.gender_combo.set('')
        self.operate_shift_system_combo.set('')
        self.share_facility_combo.set('')
        self.have_boarding_facility_combo.set('')
        self.have_perimeter_fencing_combo.set('')
        self.have_security_person_combo.set('')
        self.type_of_security_combo.set('')
        self.prepare_school_improvement_plan_combo.set('')
        self.have_pta_combo.set('')
        self.have_playground_combo.set('')
        self.have_sport_facility_combo.set('')
        self.status.set('')
        # # Reset the picture field
        # self.picture_label.config(text="Picture")  # Reset the label text
        # self.browse_button.config(text="Browse")  # Optionally reset the button text or state
        # # If needed, you can also reset any stored image path or variable
        # self.image_path = None  # Assuming you have a variable to store the image path

    def delete_school(self):
        self.selected_item = self.tree.selection()
        if self.selected_item:
            self.row = self.tree.item(self.selected_item)["values"]
            school_id = self.row[0]
            db.delete(school_id)
            self.list_school()
            self.clear_school_form()
        else:
            messagebox.showerror("Error", "Please select data to delete")

    def delete_all(self):
        messagebox.showwarning("Warning", "You are about to delete every record in this database")
        result = messagebox.askyesno("Confirm", "Are you sure you want to delete every school?")
        if result:
            db.delete_all_records()

    def view_students(self):
        print("list of students")

    def view_teachers(self):
        print("list of teachers")

    def logout(self):
        messagebox.showwarning("Warning", "Are you sure you want to log out?")
        self.destroy()  # Hide the main window
        from login import MainWindow
        login_window = MainWindow()
        login_window.mainloop()

    # Draw a green circle for online status
    def draw_online_status(self):
        self.status_canvas.delete("all")
        self.status_canvas.create_oval(5, 5, 15, 15, fill="#00ff00")

    # Draw a red circle for offline status
    def draw_offline_status(self):
        self.status_canvas.delete("all")
        self.status_canvas.create_oval(5, 5, 15, 15, fill="#ff0000")

    def is_connected(self):
        try:
            socket.create_connection(("www.google.com", 80), timeout=1)  # Set a timeout of 1 second
            self.connection_state = "Online"
            self.draw_online_status()
        except OSError:
            self.connection_state = "Offline"
            self.draw_offline_status()
        self.internet_status.configure(text=self.connection_state)
        self.after(1000, self.is_connected)  # Check again in 1 second


if __name__ == "__main__":
    school_window = SchoolWindow()
    school_window.is_connected()
    school_window.mainloop()

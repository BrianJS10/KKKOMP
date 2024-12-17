import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import hashlib
import json

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1000x600")
        
        # Define colors
        self.colors = {
            'primary': '#8B0000',      # Dark Red
            'secondary': '#B22222',    # Light Red
            'background': '#f8f9fa',   # Light Gray
            'white': '#ffffff',
            'text': '#2d3436',         # Dark Gray
            'border': '#e0e0e0'        # Light Border
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['background'])
        
        # Create main container
        self.setup_main_container()
        
        # Try to load remembered credentials
        try:
            with open('remembered_login.txt', 'r') as f:
                saved_username = f.readline().strip()
                saved_password = f.readline().strip()
                if saved_username and saved_password:
                    self.username_entry.insert(0, saved_username)
                    self.password_entry.insert(0, saved_password)
                    self.remember_var.set(True)
        except:
            pass
        
        # Add credentials file path
        self.credentials_file = 'user_credentials.json'
        # Initialize or load credentials
        self.initialize_credentials()
        
    def setup_main_container(self):
        # Step 1: Create main frame with padding
        self.main_frame = tk.Frame(self.root, bg=self.colors['background'])
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=50, pady=30)
        
        # Step 2: Create left panel (Welcome section)
        self.setup_left_panel()
        
        # Step 3: Create right panel (Login form)
        self.setup_right_panel()
        
    def setup_left_panel(self):
        # Step 4: Create and style left panel
        self.left_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        self.left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=(0, 25))
        
        # Welcome text container
        welcome_frame = tk.Frame(self.left_frame, bg=self.colors['background'])
        welcome_frame.pack(expand=True, fill=tk.BOTH, pady=(50, 0))
        
        # Welcome messages
        tk.Label(welcome_frame, 
                text="Welcome to", 
                font=('Arial', 24),
                bg=self.colors['background'],
                fg=self.colors['text']).pack()
                
        tk.Label(welcome_frame,
                text="ProfBook",
                font=('Arial', 32, 'bold'),
                bg=self.colors['background'],
                fg=self.colors['primary']).pack(pady=(10, 0))
                
        tk.Label(welcome_frame,
                text="One way to connect with Professors",
                font=('Arial', 12),
                bg=self.colors['background'],
                fg=self.colors['text']).pack(pady=(20, 0))
        
    def setup_right_panel(self):
        # Step 5: Create and style right panel
        self.right_frame = tk.Frame(self.main_frame, 
                                  bg=self.colors['white'],
                                  highlightthickness=1,
                                  highlightbackground=self.colors['border'])
        self.right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=(25, 0))
        
        # Login form container
        login_container = tk.Frame(self.right_frame, bg=self.colors['white'])
        login_container.pack(expand=True, fill=tk.BOTH, padx=40, pady=50)
        
        # Login header
        tk.Label(login_container,
                text="Login to Your Account",
                font=('Arial', 20, 'bold'),
                bg=self.colors['white'],
                fg=self.colors['primary']).pack(pady=(0, 30))
        
        # Username field
        self.username_entry = self.create_input_field(login_container, "Username")
        
        # Password field with show/hide button
        self.create_password_field(login_container)
        
        # Login button
        self.create_login_button(login_container)
        
        # Separator
        self.create_separator(login_container)
        
        # Register button
        self.create_register_button(login_container)
        
    def create_input_field(self, parent, label_text):
        tk.Label(parent,
                text=label_text,
                font=('Arial', 12),
                bg=self.colors['white'],
                fg=self.colors['text']).pack(anchor='w')
                
        entry = tk.Entry(parent,
                        font=('Arial', 12),
                        bg=self.colors['background'],
                        relief=tk.FLAT,
                        highlightthickness=1,
                        highlightbackground=self.colors['border'])
        entry.pack(fill=tk.X, pady=(5, 20), ipady=8)
        return entry
        
    def create_password_field(self, parent):
        # Password label frame
        password_label_frame = tk.Frame(parent, bg=self.colors['white'])
        password_label_frame.pack(fill=tk.X)
        
        tk.Label(password_label_frame,
                text="Password",
                font=('Arial', 12),
                bg=self.colors['white'],
                fg=self.colors['text']).pack(side=tk.LEFT)
                
        # Show/Hide password button
        self.show_password_btn = tk.Button(password_label_frame,
                                         text="Show",
                                         font=('Arial', 10),
                                         bg=self.colors['white'],
                                         fg=self.colors['primary'],
                                         bd=0,
                                         cursor='hand2',
                                         activebackground=self.colors['white'],
                                         activeforeground=self.colors['secondary'],
                                         command=self.toggle_password)
        self.show_password_btn.pack(side=tk.RIGHT)
        
        # Password entry
        self.password_entry = tk.Entry(parent,
                                     font=('Arial', 12),
                                     bg=self.colors['background'],
                                     show='*',
                                     relief=tk.FLAT,
                                     highlightthickness=1,
                                     highlightbackground=self.colors['border'])
        self.password_entry.pack(fill=tk.X, pady=(5, 15), ipady=8)
        
        # Create remember password frame
        remember_frame = tk.Frame(parent, bg=self.colors['white'])
        remember_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Add remember password checkbox
        self.remember_var = tk.BooleanVar()
        remember_checkbox = tk.Checkbutton(remember_frame,
                                         text="Remember Password",
                                         variable=self.remember_var,
                                         bg=self.colors['white'],
                                         fg=self.colors['text'],
                                         activebackground=self.colors['white'],
                                         activeforeground=self.colors['primary'],
                                         selectcolor=self.colors['white'])
        remember_checkbox.pack(side=tk.LEFT)
        
        # Add Forgot Password link
        forgot_password_btn = tk.Button(remember_frame,
                                      text="Forgot Password?",
                                      font=('Arial', 10),
                                      bg=self.colors['white'],
                                      fg=self.colors['primary'],
                                      bd=0,
                                      cursor='hand2',
                                      activebackground=self.colors['white'],
                                      activeforeground=self.colors['secondary'],
                                      command=self.show_forgot_password)
        forgot_password_btn.pack(side=tk.RIGHT)
        
    def create_login_button(self, parent):
        self.login_btn = tk.Button(parent,
                                 text="LOGIN",
                                 font=('Arial', 12, 'bold'),
                                 bg=self.colors['primary'],
                                 fg=self.colors['white'],
                                 activebackground=self.colors['secondary'],
                                 activeforeground=self.colors['white'],
                                 cursor='hand2',
                                 relief=tk.FLAT,
                                 command=self.login)
        self.login_btn.pack(fill=tk.X, ipady=10)
        
        # Add hover effect
        self.login_btn.bind('<Enter>', lambda e: self.login_btn.config(bg=self.colors['secondary']))
        self.login_btn.bind('<Leave>', lambda e: self.login_btn.config(bg=self.colors['primary']))
        
    def create_separator(self, parent):
        separator_frame = tk.Frame(parent, bg=self.colors['white'])
        separator_frame.pack(fill=tk.X, pady=30)
        
        tk.Frame(separator_frame, bg=self.colors['border'], height=1).pack(
            side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        tk.Label(separator_frame, text="OR", bg=self.colors['white'],
                fg=self.colors['text']).pack(side=tk.LEFT)
        tk.Frame(separator_frame, bg=self.colors['border'], height=1).pack(
            side=tk.LEFT, expand=True, fill=tk.X, padx=(10, 0))
        
    def create_register_button(self, parent):
        self.register_btn = tk.Button(parent,
                                    text="REGISTER",
                                    font=('Arial', 12),
                                    bg=self.colors['white'],
                                    fg=self.colors['primary'],
                                    activebackground=self.colors['background'],
                                    activeforeground=self.colors['primary'],
                                    cursor='hand2',
                                    relief=tk.FLAT,
                                    command=self.show_register)
        self.register_btn.pack(fill=tk.X, ipady=10)
        
        # Add hover effect
        self.register_btn.bind('<Enter>', lambda e: self.register_btn.config(bg=self.colors['background']))
        self.register_btn.bind('<Leave>', lambda e: self.register_btn.config(bg=self.colors['white']))
        
    def toggle_password(self):
        if self.password_entry.cget('show') == '*':
            self.password_entry.config(show='')
            self.show_password_btn.config(text='Hide')
        else:
            self.password_entry.config(show='*')
            self.show_password_btn.config(text='Show')
            
    def initialize_credentials(self):
        """Initialize or load user credentials"""
        if not os.path.exists(self.credentials_file):
            # Default credentials with hashed passwords
            default_credentials = {
                "admin": self.hash_password("admin123"),
                "user": self.hash_password("user123"),
                "student": self.hash_password("student123")
            }
            # Save to file
            with open(self.credentials_file, 'w') as f:
                json.dump(default_credentials, f)

    def hash_password(self, password):
        """Create a simple hash of the password"""
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self):
        """Handle user login with improved security"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        try:
            # Load current credentials
            with open(self.credentials_file, 'r') as f:
                valid_credentials = json.load(f)
                
            # Check if username exists and password matches
            if username in valid_credentials:
                hashed_password = self.hash_password(password)
                if hashed_password == valid_credentials[username]:
                    # Handle remember me
                    if self.remember_var.get():
                        with open('remembered_login.txt', 'w') as f:
                            f.write(f"{username}\n{password}")
                    else:
                        # Remove remembered credentials if exists
                        if os.path.exists('remembered_login.txt'):
                            os.remove('remembered_login.txt')
                    
                    messagebox.showinfo("Success", f"Welcome back, {username}!")
                    self.main_frame.destroy()
                    
                    # Direct to appropriate window based on user type
                    if username == "admin":
                        AdminPanel(self.root)
                    else:
                        ProfessorDirectory(self.root, username)
                else:
                    messagebox.showerror("Error", "Invalid password")
            else:
                messagebox.showerror("Error", "Username not found")
                
        except Exception as e:
            messagebox.showerror("Error", "An error occurred during login. Please try again.")
            print(f"Login error: {str(e)}")  # For debugging
            
    def show_register(self):
        # Hide main frame
        self.main_frame.destroy()
        
        # Create registration frame
        self.register_frame = tk.Frame(self.root, bg=self.colors['background'])
        self.register_frame.pack(expand=True, fill=tk.BOTH, padx=50, pady=30)
        
        # Title
        tk.Label(self.register_frame,
                text="Create New Account",
                font=('Arial', 24, 'bold'),
                bg=self.colors['background'],
                fg=self.colors['primary']).pack(pady=(0, 30))
        
        # Username field
        self.reg_username_entry = self.create_input_field(self.register_frame, "Username")
        
        # Password fields
        self.reg_password_entry = self.create_input_field(self.register_frame, "Password")
        self.reg_password_entry.config(show='*')
        
        self.reg_confirm_entry = self.create_input_field(self.register_frame, "Confirm Password")
        self.reg_confirm_entry.config(show='*')
        
        # Register button
        register_btn = tk.Button(self.register_frame,
                               text="REGISTER",
                               font=('Arial', 12, 'bold'),
                               bg=self.colors['primary'],
                               fg=self.colors['white'],
                               activebackground=self.colors['secondary'],
                               activeforeground=self.colors['white'],
                               cursor='hand2',
                               relief=tk.FLAT,
                               command=self.register)
        register_btn.pack(fill=tk.X, ipady=10, pady=(20, 10))
        
        # Back to login button
        back_btn = tk.Button(self.register_frame,
                            text="BACK TO LOGIN",
                            font=('Arial', 12),
                            bg=self.colors['white'],
                            fg=self.colors['primary'],
                            activebackground=self.colors['background'],
                            activeforeground=self.colors['primary'],
                            cursor='hand2',
                            relief=tk.FLAT,
                            command=self.show_login)
        back_btn.pack(fill=tk.X, ipady=10)
        
        # Add hover effects
        for btn, from_color, to_color in [(register_btn, self.colors['primary'], self.colors['secondary']),
                                         (back_btn, self.colors['white'], self.colors['background'])]:
            btn.bind('<Enter>', lambda e, b=btn, c=to_color: b.config(bg=c))
            btn.bind('<Leave>', lambda e, b=btn, c=from_color: b.config(bg=c))
            
    def show_login(self):
        # Remove registration frame
        self.register_frame.destroy()
        # Recreate login interface
        self.setup_main_container()
        
    def register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        confirm = self.reg_confirm_entry.get()
        
        if not all([username, password, confirm]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
            
        # Hash password
        hashed_password = self.hash_password(password)
        
        # Save new user to credentials file
        try:
            with open(self.credentials_file, 'r') as f:
                credentials = json.load(f)
            credentials[username] = hashed_password
            with open(self.credentials_file, 'w') as f:
                json.dump(credentials, f)
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.show_login()
        except Exception as e:
            messagebox.showerror("Error", "An error occurred during registration. Please try again.")
            print(f"Registration error: {str(e)}")  # For debugging

    def show_forgot_password(self):
        # Create password reset window
        reset_window = tk.Toplevel(self.root)
        reset_window.title("Reset Password")
        reset_window.geometry("400x300")
        reset_window.configure(bg=self.colors['background'])
        
        # Center the window
        reset_window.transient(self.root)
        reset_window.grab_set()
        
        # Create main frame
        main_frame = tk.Frame(reset_window, bg=self.colors['white'],
                            highlightthickness=1,
                            highlightbackground=self.colors['border'])
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Title
        tk.Label(main_frame,
                text="Reset Password",
                font=('Arial', 16, 'bold'),
                bg=self.colors['white'],
                fg=self.colors['primary']).pack(pady=20)
        
        # Email entry
        tk.Label(main_frame,
                text="Enter your email address:",
                font=('Arial', 12),
                bg=self.colors['white'],
                fg=self.colors['text']).pack(anchor='w', padx=20)
        
        email_entry = tk.Entry(main_frame,
                             font=('Arial', 12),
                             bg=self.colors['background'],
                             relief=tk.FLAT,
                             highlightthickness=1,
                             highlightbackground=self.colors['border'])
        email_entry.pack(fill=tk.X, padx=20, pady=(5, 20), ipady=8)
        
        def submit_reset():
            email = email_entry.get().strip()
            if not email:
                messagebox.showerror("Error", "Please enter your email address")
                return
            
            # Here you would typically:
            # 1. Verify if email exists in your database
            # 2. Generate a reset token
            # 3. Send reset email to user
            # For now, we'll just show a success message
            messagebox.showinfo("Success", 
                              "If an account exists with this email, "
                              "you will receive password reset instructions shortly.")
            reset_window.destroy()
        
        # Submit button
        submit_btn = tk.Button(main_frame,
                             text="Send Reset Link",
                             font=('Arial', 12, 'bold'),
                             bg=self.colors['primary'],
                             fg=self.colors['white'],
                             activebackground=self.colors['secondary'],
                             activeforeground=self.colors['white'],
                             cursor='hand2',
                             relief=tk.FLAT,
                             command=submit_reset)
        submit_btn.pack(fill=tk.X, padx=20, pady=20, ipady=8)
        
        # Add hover effect
        submit_btn.bind('<Enter>', lambda e: submit_btn.config(bg=self.colors['secondary']))
        submit_btn.bind('<Leave>', lambda e: submit_btn.config(bg=self.colors['primary']))

class Professor:
    def __init__(self, Name, Department, Contact, Email, Picture=None):
        self.Name = Name
        self.Department = Department
        self.Contact = Contact
        self.Email = Email
        self.Schedule = []  # List of schedules
        self.Picture = Picture if Picture else "N/A"

    

class ProfessorDirectory:
    def __init__(self, root, username):
        self.root = root
        self.root.title("List of professors")
        self.root.geometry("1000x700")
        
        # Load default N/A image
        na_image = Image.new('RGB', (100, 100), color='lightgray')
        self.default_photo = ImageTk.PhotoImage(na_image)
        
        # Define colors (same as login interface)
        self.colors = {
            'primary': '#8B0000',      # Dark Red
            'secondary': '#B22222',    # Light Red
            'background': '#f8f9fa',   # Light Gray
            'white': '#ffffff',
            'text': '#2d3436',         # Dark Gray
            'border': '#e0e0e0'        # Light Border
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['background'])
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure custom styles
        self.style.configure('Custom.TFrame',
                           background=self.colors['background'])
        
        self.style.configure('Custom.TLabel',
                           background=self.colors['background'],
                           foreground=self.colors['text'])
        
        self.style.configure('Custom.TButton',
                           background=self.colors['primary'],
                           foreground=self.colors['white'],
                           borderwidth=0,
                           font=('Arial', 10))
        
        self.style.map('Custom.TButton',
                      background=[('active', self.colors['secondary'])])
        
        # Create main frame
        self.main_frame = ttk.Frame(root, style='Custom.TFrame', padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create header frame
        self.create_header()
        
        # Create search frame
        self.create_search_bar()
        
        # Create professors list
        self.create_professors_list()
        
        # Create logout button
        self.create_logout_button()
        
        # Initialize professors data
        self.professors = [
            Professor("Mr. Brian Sarmiento", "IT Department", "+1-555-0123", "brianjmesonez@gmail.com"),
            Professor("Dr. Charles Tabares", "BSCPE Department", "+1-555-0124", "sarah.johnson@university.edu"),
            Professor("Dr. Wensley Naarte", "HM Department", "+1-555-0125", "michael.brown@university.edu")
        ]
        
        # Add sample schedules for professors
        self.professors[0].Schedule = [
            {"subject": "Programming 1", "day": "Monday", "time": "9:00 AM - 10:30 AM"},
            {"subject": "Web Development", "day": "Wednesday", "time": "1:00 PM - 2:30 PM"}
        ]
        
        self.professors[1].Schedule = [
            {"subject": "Data Structures", "day": "Tuesday", "time": "10:00 AM - 11:30 AM"},
            {"subject": "Algorithms", "day": "Thursday", "time": "2:00 PM - 3:30 PM"}
        ]
        
        self.professors[2].Schedule = [
            {"subject": "Database Systems", "day": "Friday", "time": "11:00 AM - 12:30 PM"},
            {"subject": "Software Engineering", "day": "Monday", "time": "3:00 PM - 4:30 PM"}
        ]
        
        # Display initial list
        self.display_professors()
        
    def create_header(self):
        header_frame = ttk.Frame(self.main_frame, style='Custom.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title = ttk.Label(header_frame,
                         text="List of Professors",
                         style='Custom.TLabel',
                         font=('Arial', 24, 'bold'))
        title.pack(side=tk.LEFT)
        
    def create_search_bar(self):
        search_frame = ttk.Frame(self.main_frame, style='Custom.TFrame')
        search_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame,
                              textvariable=self.search_var,
                              font=('Arial', 12),
                              bg=self.colors['white'],
                              fg=self.colors['text'],
                              relief=tk.FLAT,
                              highlightthickness=1,
                              highlightbackground=self.colors['border'])
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
        
        search_button = tk.Button(search_frame,
                                text="Search",
                                font=('Arial', 12),
                                bg=self.colors['primary'],
                                fg=self.colors['white'],
                                activebackground=self.colors['secondary'],
                                activeforeground=self.colors['white'],
                                cursor='hand2',
                                relief=tk.FLAT,
                                command=self.search_professors)
        search_button.pack(side=tk.RIGHT, padx=(10, 0), ipadx=20, ipady=8)
        
    def create_professors_list(self):
        # Create container frame
        container = tk.Frame(self.main_frame, bg=self.colors['white'],
                           highlightthickness=1,
                           highlightbackground=self.colors['border'])
        container.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas
        canvas = tk.Canvas(container, bg=self.colors['white'])
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        
        # Create scrollable frame
        self.list_frame = tk.Frame(canvas, bg=self.colors['white'])
        
        # Configure canvas
        self.list_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Create window inside canvas
        canvas.create_window((0, 0), window=self.list_frame, anchor="nw", width=canvas.winfo_reqwidth())
        
        # Configure canvas scroll
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack everything
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
    def create_logout_button(self):
        self.logout_button = tk.Button(self.main_frame,
                                     text="LOGOUT",
                                     font=('Arial', 12),
                                     bg=self.colors['primary'],
                                     fg=self.colors['white'],
                                     activebackground=self.colors['secondary'],
                                     activeforeground=self.colors['white'],
                                     cursor='hand2',
                                     relief=tk.FLAT,
                                     command=self.logout)
        self.logout_button.pack(pady=(20, 0), ipadx=30, ipady=8)
        
    def display_professors(self, professors=None):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
            
        if professors is None:
            professors = self.professors
            
        for professor in professors:
            # Create clickable frame
            professor_frame = tk.Frame(self.list_frame, bg=self.colors['white'], cursor='hand2')
            professor_frame.pack(fill=tk.X, pady=10)
            
            # Bind click event to the entire frame
            professor_frame.bind('<Button-1>', lambda e, p=professor: self._show_profile(p))
            
            # Add hover effect to entire frame
            def on_enter(e, frame=professor_frame):
                frame.configure(bg='#f5f5f5')
                for widget in frame.winfo_children():
                    widget.configure(bg='#f5f5f5')
                
            def on_leave(e, frame=professor_frame):
                frame.configure(bg=self.colors['white'])
                for widget in frame.winfo_children():
                    widget.configure(bg=self.colors['white'])
            
            professor_frame.bind('<Enter>', on_enter)
            professor_frame.bind('<Leave>', on_leave)
            
            # Picture frame
            picture_frame = tk.Frame(professor_frame, bg=self.colors['white'])
            picture_frame.pack(side=tk.LEFT, padx=20)
            
            # Display picture or N/A logo
            if professor.Picture == "N/A":
                photo_label = tk.Label(picture_frame, image=self.default_photo, bg=self.colors['white'])
            else:
                try:
                    img = Image.open(professor.Picture)
                    img = img.resize((100, 100), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    photo_label = tk.Label(picture_frame, image=photo, bg=self.colors['white'])
                    photo_label.image = photo  # Keep a reference
                except:
                    photo_label = tk.Label(picture_frame, image=self.default_photo, bg=self.colors['white'])
            
            photo_label.pack()
            
            # Info frame
            info_frame = tk.Frame(professor_frame, bg=self.colors['white'])
            info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=15)
            
            # Create clickable name label
            name_label = tk.Label(info_frame,
                     text=professor.Name,
                     font=('Arial', 14, 'bold'),
                     bg=self.colors['white'],
                     fg=self.colors['text'],
                     cursor='hand2')  # Change cursor to hand when hovering
            name_label.pack(anchor='w')
            
            # Bind click event to name label
            name_label.bind('<Button-1>', lambda e, p=professor: self._show_profile(p))
            
            # Add hover effect to name
            def on_name_enter(e):
                e.widget.configure(fg=self.colors['secondary'])
                
            def on_name_leave(e):
                e.widget.configure(fg=self.colors['text'])
                
            name_label.bind('<Enter>', on_name_enter)
            name_label.bind('<Leave>', on_name_leave)
            
            tk.Label(info_frame,
                     text=professor.Department,
                     font=('Arial', 12),
                     bg=self.colors['white'],
                     fg=self.colors['text']).pack(anchor='w')
        
    def _mask_contact(self, contact):
        # Return actual contact number
        return contact

    def _mask_email(self, email):
        # Return actual email
        return email
        
    def _show_profile(self, professor):
        # Create profile window
        profile_window = tk.Toplevel(self.root)
        profile_window.title(f"Professor Profile - {professor.Name}")
        profile_window.geometry("1000x700")  # Made window larger
        profile_window.configure(bg=self.colors['background'])
        
        # Create main content frame
        content_frame = tk.Frame(profile_window, bg=self.colors['white'],
                               highlightthickness=1,
                               highlightbackground=self.colors['border'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Top section - Basic Info with Picture
        top_frame = tk.Frame(content_frame, bg=self.colors['white'])
        top_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Picture on the left
        picture_frame = tk.Frame(top_frame, bg=self.colors['white'])
        picture_frame.pack(side=tk.LEFT, padx=(0, 30))
        
        if professor.Picture == "N/A":
            na_image_large = Image.new('RGB', (150, 150), color='lightgray')
            photo_large = ImageTk.PhotoImage(na_image_large)
            photo_label = tk.Label(picture_frame, image=photo_large, bg=self.colors['white'])
            photo_label.image = photo_large
        else:
            try:
                img = Image.open(professor.Picture)
                img = img.resize((150, 150), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                photo_label = tk.Label(picture_frame, image=photo, bg=self.colors['white'])
                photo_label.image = photo
            except:
                na_image_large = Image.new('RGB', (150, 150), color='lightgray')
                photo_large = ImageTk.PhotoImage(na_image_large)
                photo_label = tk.Label(picture_frame, image=photo_large, bg=self.colors['white'])
                photo_label.image = photo_large
        photo_label.pack()
        
        # Information on the right
        info_frame = tk.Frame(top_frame, bg=self.colors['white'])
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Name and Department
        tk.Label(info_frame,
                text=professor.Name,
                font=('Arial', 24, 'bold'),
                bg=self.colors['white'],
                fg=self.colors['text']).pack(anchor='w')
        
        tk.Label(info_frame,
                text=professor.Department,
                font=('Arial', 16),
                bg=self.colors['white'],
                fg=self.colors['text']).pack(anchor='w', pady=(5, 20))
        
        # Contact and Email
        contact_frame = tk.Frame(info_frame, bg=self.colors['white'])
        contact_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(contact_frame,
                text="Contact: ",
                font=('Arial', 12, 'bold'),
                bg=self.colors['white'],
                fg=self.colors['text']).pack(side=tk.LEFT)
        
        tk.Label(contact_frame,
                text=self._mask_contact(professor.Contact),
                font=('Arial', 12),
                bg=self.colors['white'],
                fg=self.colors['text']).pack(side=tk.LEFT)
        
        email_frame = tk.Frame(info_frame, bg=self.colors['white'])
        email_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(email_frame,
                text="Email: ",
                font=('Arial', 12, 'bold'),
                bg=self.colors['white'],
                fg=self.colors['text']).pack(side=tk.LEFT)
        
        tk.Label(email_frame,
                text=self._mask_email(professor.Email),
                font=('Arial', 12),
                bg=self.colors['white'],
                fg=self.colors['text']).pack(side=tk.LEFT)
        
        # Separator
        ttk.Separator(content_frame, orient='horizontal').pack(fill=tk.X, padx=20, pady=20)
        
        # Schedule section with border
        schedule_frame = tk.Frame(content_frame, bg=self.colors['white'], bd=1, relief=tk.SOLID)
        schedule_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20,0))
        
        # Schedule header
        tk.Label(schedule_frame,
                text="Class Schedule",
                font=('Arial', 18, 'bold'),
                bg=self.colors['white'],
                fg=self.colors['text']).pack(anchor='w', pady=(10, 20), padx=10)
        
        # Create Treeview for schedule
        columns = ("Subject", "Day", "Time")
        tree = ttk.Treeview(schedule_frame, columns=columns, show='headings', height=10)
        
        # Configure column widths and headings
        widths = [400, 200, 200]
        for col, width in zip(columns, widths):
            tree.column(col, width=width, minwidth=width)
            tree.heading(col, text=col)
        
        # Style configuration for headers
        style = ttk.Style()
        style.configure("Treeview.Heading",
                       background=self.colors['primary'],
                       foreground=self.colors['white'],
                       font=('Arial', 12, 'bold'))
        
        # Add vertical scrollbar
        scrollbar = ttk.Scrollbar(schedule_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=(0, 10))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 10))
        
        # Insert schedule data
        if professor.Schedule:
            for schedule in professor.Schedule:
                tree.insert('', tk.END, values=(
                    schedule['subject'],
                    schedule['day'],
                    schedule['time']
                ))
        else:
            tree.insert('', tk.END, values=('No schedules available', '', ''))
        
        # Close button at bottom
        close_btn = tk.Button(profile_window,
                            text="Close",
                            font=('Arial', 12),
                            bg=self.colors['primary'],
                            fg=self.colors['white'],
                            activebackground=self.colors['secondary'],
                            activeforeground=self.colors['white'],
                            cursor='hand2',
                            relief=tk.FLAT,
                            command=profile_window.destroy)
        close_btn.pack(pady=20, ipadx=30, ipady=8)
        
        # Add hover effect to close button
        close_btn.bind('<Enter>', lambda e: close_btn.config(bg=self.colors['secondary']))
        close_btn.bind('<Leave>', lambda e: close_btn.config(bg=self.colors['primary']))
        
    def search_professors(self):
        query = self.search_var.get().lower()
        results = [professor for professor in self.professors if query in professor.Name.lower() or query in professor.Department.lower() or query in professor.Contact.lower() or query in professor.Email.lower()]
        self.display_professors(results)
        
    def logout(self):
        self.main_frame.destroy()
        LoginWindow(self.root)

class WelcomeWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to ProfBook")
        self.root.geometry("800x500")
        
        # Define colors (same as other windows)
        self.colors = {
            'primary': '#8B0000',      # Dark Red
            'secondary': '#B22222',    # Light Red
            'background': '#f8f9fa',   # Light Gray
            'white': '#ffffff',
            'text': '#2d3436',         # Dark Gray
            'border': '#e0e0e0'        # Light Border
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['background'])
        
        # Create main container with fixed size
        self.main_frame = tk.Frame(self.root, bg=self.colors['background'], width=800, height=500)
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        self.main_frame.pack_propagate(False)  # Prevent frame from shrinking
        
        # Content frame for centered alignment
        self.content_frame = tk.Frame(self.main_frame, bg=self.colors['background'], width=600)
        self.content_frame.pack(expand=True, pady=(50, 0))
        
        # Create all widgets with initial transparency
        self.widgets = []
        
        # Welcome message
        welcome_label = tk.Label(self.content_frame,
                text="Welcome to ProfBook",
                font=('Arial', 32, 'bold'),
                bg=self.colors['background'],
                fg=self.colors['background'],  # Start with background color (invisible)
                wraplength=600)
        welcome_label.pack(pady=(0, 20))
        self.widgets.append((welcome_label, self.colors['primary']))
        
        # Subtitle
        subtitle_label = tk.Label(self.content_frame,
                text="Student Management System",
                font=('Arial', 18),
                bg=self.colors['background'],
                fg=self.colors['background'],
                wraplength=600)
        subtitle_label.pack(pady=(0, 40))
        self.widgets.append((subtitle_label, self.colors['text']))
        
        # Description
        description = """ProfBook is your comprehensive solution for managing 
student-professor interactions and schedules.

Get started by clicking the button below."""
        desc_label = tk.Label(self.content_frame,
                text=description,
                font=('Arial', 12),
                bg=self.colors['background'],
                fg=self.colors['background'],
                justify=tk.CENTER,
                wraplength=600)
        desc_label.pack(pady=(0, 40))
        self.widgets.append((desc_label, self.colors['text']))
        
        # Get Started button
        self.start_btn = tk.Button(self.content_frame,
                            text="Get Started",
                            font=('Arial', 14, 'bold'),
                            bg=self.colors['primary'],
                            fg=self.colors['white'],
                            activebackground=self.colors['secondary'],
                            activeforeground=self.colors['white'],
                            cursor='hand2',
                            relief=tk.FLAT,
                            command=self.show_login)
        self.start_btn.pack(ipadx=30, ipady=10)
        self.start_btn.configure(bg=self.colors['background'])  # Start invisible
        
        # Add hover effect
        self.start_btn.bind('<Enter>', self.on_hover_enter)
        self.start_btn.bind('<Leave>', self.on_hover_leave)
        
        # Center the window
        self.center_window()
        
        # Start fade-in animation
        self.fade_in(0)
        
        # Start button pulse animation
        self.pulse_button()
    
    def fade_in(self, index, alpha=0):
        if index < len(self.widgets):
            widget, final_color = self.widgets[index]
            if alpha <= 1.0:
                # Interpolate color
                current_color = self.interpolate_color(self.colors['background'], final_color, alpha)
                widget.configure(fg=current_color)
                self.root.after(20, lambda: self.fade_in(index, alpha + 0.1))
            else:
                # Move to next widget
                self.root.after(100, lambda: self.fade_in(index + 1, 0))
        else:
            # All widgets faded in, fade in the button
            self.fade_in_button()
    
    def fade_in_button(self, alpha=0):
        if alpha <= 1.0:
            # Interpolate button background color
            current_color = self.interpolate_color(self.colors['background'], self.colors['primary'], alpha)
            self.start_btn.configure(bg=current_color)
            self.root.after(20, lambda: self.fade_in_button(alpha + 0.1))
    
    def pulse_button(self):
        def animate_pulse(scale=1.0, increasing=True):
            if increasing and scale < 1.1:
                scale += 0.01
            elif not increasing and scale > 1.0:
                scale -= 0.01
            else:
                increasing = not increasing
            
            # Apply scale transformation
            new_font = ('Arial', int(14 * scale), 'bold')
            self.start_btn.configure(font=new_font)
            
            # Continue animation
            self.root.after(50, lambda: animate_pulse(scale, increasing))
        
        # Start pulse animation after a delay
        self.root.after(1000, lambda: animate_pulse())
    
    def interpolate_color(self, start_color, end_color, alpha):
        # Convert hex to RGB
        start_rgb = tuple(int(start_color[i:i+2], 16) for i in (1, 3, 5))
        end_rgb = tuple(int(end_color[i:i+2], 16) for i in (1, 3, 5))
        
        # Interpolate
        current_rgb = tuple(
            int(start_rgb[i] + (end_rgb[i] - start_rgb[i]) * alpha)
            for i in range(3)
        )
        
        # Convert back to hex
        return f'#{current_rgb[0]:02x}{current_rgb[1]:02x}{current_rgb[2]:02x}'
    
    def on_hover_enter(self, event):
        self.start_btn.config(bg=self.colors['secondary'])
    
    def on_hover_leave(self, event):
        self.start_btn.config(bg=self.colors['primary'])
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def show_login(self):
        self.root.withdraw()  # Hide welcome window
        login_window = tk.Toplevel()
        login_app = LoginWindow(login_window)
        login_window.protocol("WM_DELETE_WINDOW", lambda: self.on_login_close(login_window))
    
    def on_login_close(self, login_window):
        login_window.destroy()
        self.root.destroy()

class AdminPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Panel")
        self.root.geometry("1000x700")
        
        # Define colors (same as other windows)
        self.colors = {
            'primary': '#8B0000',      # Dark Red
            'secondary': '#B22222',    # Light Red
            'background': '#f8f9fa',   # Light Gray
            'white': '#ffffff',
            'text': '#2d3436',         # Dark Gray
            'border': '#e0e0e0'        # Light Border
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['background'])
        
        # Create main container
        self.setup_main_container()
        
    def setup_main_container(self):
        # Main frame
        self.main_frame = tk.Frame(self.root, bg=self.colors['background'])
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        tk.Label(header_frame,
                text="Admin Panel",
                font=('Arial', 24, 'bold'),
                bg=self.colors['background'],
                fg=self.colors['primary']).pack(side=tk.LEFT)
        
        # Logout button
        logout_btn = tk.Button(header_frame,
                             text="Logout",
                             font=('Arial', 12),
                             bg=self.colors['primary'],
                             fg=self.colors['white'],
                             command=self.logout,
                             cursor='hand2')
        logout_btn.pack(side=tk.RIGHT)
        
        # Create tabs
        self.create_tabs()
        
    def create_tabs(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(expand=True, fill=tk.BOTH)
        
        # User Management Tab
        self.user_tab = tk.Frame(self.notebook, bg=self.colors['white'])
        self.notebook.add(self.user_tab, text="User Management")
        self.setup_user_management()
        
        # Professor Management Tab
        self.professor_tab = tk.Frame(self.notebook, bg=self.colors['white'])
        self.notebook.add(self.professor_tab, text="Professor Management")
        self.setup_professor_management()
        
        # System Settings Tab
        self.settings_tab = tk.Frame(self.notebook, bg=self.colors['white'])
        self.notebook.add(self.settings_tab, text="System Settings")
        self.setup_system_settings()
        
    def setup_user_management(self):
        # User list frame
        list_frame = tk.Frame(self.user_tab, bg=self.colors['white'])
        list_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Controls
        controls_frame = tk.Frame(list_frame, bg=self.colors['white'])
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Button(controls_frame,
                 text="Add User",
                 command=self.add_user,
                 bg=self.colors['primary'],
                 fg=self.colors['white']).pack(side=tk.LEFT, padx=5)
                 
        tk.Button(controls_frame,
                 text="Delete User",
                 command=self.delete_user,
                 bg=self.colors['primary'],
                 fg=self.colors['white']).pack(side=tk.LEFT, padx=5)
        
        # User list
        self.user_tree = ttk.Treeview(list_frame, columns=("Username", "Role", "Last Login"), show="headings")
        self.user_tree.heading("Username", text="Username")
        self.user_tree.heading("Role", text="Role")
        self.user_tree.heading("Last Login", text="Last Login")
        self.user_tree.pack(expand=True, fill=tk.BOTH)
        
        # Load users
        self.load_users()
        
    def setup_professor_management(self):
        # Professor list frame
        list_frame = tk.Frame(self.professor_tab, bg=self.colors['white'])
        list_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Controls
        controls_frame = tk.Frame(list_frame, bg=self.colors['white'])
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Button(controls_frame,
                 text="Add Professor",
                 command=self.add_professor,
                 bg=self.colors['primary'],
                 fg=self.colors['white']).pack(side=tk.LEFT, padx=5)
                 
        tk.Button(controls_frame,
                 text="Edit Professor",
                 command=self.edit_professor,
                 bg=self.colors['primary'],
                 fg=self.colors['white']).pack(side=tk.LEFT, padx=5)
                 
        tk.Button(controls_frame,
                 text="Delete Professor",
                 command=self.delete_professor,
                 bg=self.colors['primary'],
                 fg=self.colors['white']).pack(side=tk.LEFT, padx=5)
        
        # Professor list
        self.prof_tree = ttk.Treeview(list_frame, 
                                    columns=("Name", "Department", "Contact", "Email"),
                                    show="headings")
        self.prof_tree.heading("Name", text="Name")
        self.prof_tree.heading("Department", text="Department")
        self.prof_tree.heading("Contact", text="Contact")
        self.prof_tree.heading("Email", text="Email")
        self.prof_tree.pack(expand=True, fill=tk.BOTH)
        
        # Load professors
        self.load_professors()
        
    def setup_system_settings(self):
        settings_frame = tk.Frame(self.settings_tab, bg=self.colors['white'])
        settings_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # System settings options
        tk.Label(settings_frame,
                text="System Settings",
                font=('Arial', 16, 'bold'),
                bg=self.colors['white']).pack(anchor='w', pady=(0, 20))
        
        # Backup settings
        backup_frame = tk.LabelFrame(settings_frame, text="Backup Settings", bg=self.colors['white'])
        backup_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(backup_frame,
                 text="Backup Database",
                 command=self.backup_database,
                 bg=self.colors['primary'],
                 fg=self.colors['white']).pack(pady=10, padx=10)
        
        # Security settings
        security_frame = tk.LabelFrame(settings_frame, text="Security Settings", bg=self.colors['white'])
        security_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(security_frame,
                 text="Change Admin Password",
                 command=self.change_admin_password,
                 bg=self.colors['primary'],
                 fg=self.colors['white']).pack(pady=10, padx=10)
    
    def load_users(self):
        try:
            with open('user_credentials.json', 'r') as f:
                users = json.load(f)
                for username in users:
                    role = "Admin" if username == "admin" else "User"
                    self.user_tree.insert("", "end", values=(username, role, "N/A"))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load users: {str(e)}")
    
    def load_professors(self):
        # Load professors from your existing data
        for professor in self.get_professors():
            self.prof_tree.insert("", "end", values=(
                professor.Name,
                professor.Department,
                professor.Contact,
                professor.Email
            ))
    
    def get_professors(self):
        # This should return your list of professors
        # For now, returning sample data
        return [
            Professor("Mr. Brian Sarmiento", "IT Department", "+1-555-0123", "brianjmesonez@gmail.com"),
            Professor("Dr. Charles Tabares", "BSCPE Department", "+1-555-0124", "sarah.johnson@university.edu"),
            Professor("Dr. Wensley Naarte", "HM Department", "+1-555-0125", "michael.brown@university.edu")
        ]
    
    def add_user(self):
        # Create add user dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Add User")
        dialog.geometry("300x200")
        dialog.configure(bg=self.colors['white'])
        
        tk.Label(dialog, text="Username:", bg=self.colors['white']).pack(pady=5)
        username_entry = tk.Entry(dialog)
        username_entry.pack(pady=5)
        
        tk.Label(dialog, text="Password:", bg=self.colors['white']).pack(pady=5)
        password_entry = tk.Entry(dialog, show="*")
        password_entry.pack(pady=5)
        
        def save_user():
            username = username_entry.get().strip()
            password = password_entry.get()
            
            if not username or not password:
                messagebox.showerror("Error", "Please fill all fields")
                return
                
            try:
                with open('user_credentials.json', 'r') as f:
                    users = json.load(f)
                
                if username in users:
                    messagebox.showerror("Error", "Username already exists")
                    return
                
                users[username] = self.hash_password(password)
                
                with open('user_credentials.json', 'w') as f:
                    json.dump(users, f)
                
                self.user_tree.insert("", "end", values=(username, "User", "N/A"))
                dialog.destroy()
                messagebox.showinfo("Success", "User added successfully")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add user: {str(e)}")
        
        tk.Button(dialog,
                 text="Save",
                 command=save_user,
                 bg=self.colors['primary'],
                 fg=self.colors['white']).pack(pady=20)
    
    def delete_user(self):
        selected = self.user_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a user to delete")
            return
            
        username = self.user_tree.item(selected[0])['values'][0]
        
        if username == "admin":
            messagebox.showerror("Error", "Cannot delete admin account")
            return
            
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete user '{username}'?"):
            try:
                with open('user_credentials.json', 'r') as f:
                    users = json.load(f)
                
                del users[username]
                
                with open('user_credentials.json', 'w') as f:
                    json.dump(users, f)
                
                self.user_tree.delete(selected[0])
                messagebox.showinfo("Success", "User deleted successfully")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete user: {str(e)}")
    
    def add_professor(self):
        # Create add professor dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Professor")
        dialog.geometry("400x300")
        dialog.configure(bg=self.colors['white'])
        
        fields = ["Name", "Department", "Contact", "Email"]
        entries = {}
        
        for field in fields:
            tk.Label(dialog, text=f"{field}:", bg=self.colors['white']).pack(pady=5)
            entry = tk.Entry(dialog)
            entry.pack(pady=5)
            entries[field] = entry
        
        def save_professor():
            values = {field: entry.get().strip() for field, entry in entries.items()}
            
            if not all(values.values()):
                messagebox.showerror("Error", "Please fill all fields")
                return
            
            self.prof_tree.insert("", "end", values=tuple(values.values()))
            dialog.destroy()
            messagebox.showinfo("Success", "Professor added successfully")
        
        tk.Button(dialog,
                 text="Save",
                 command=save_professor,
                 bg=self.colors['primary'],
                 fg=self.colors['white']).pack(pady=20)
    
    def edit_professor(self):
        selected = self.prof_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a professor to edit")
            return
            
        current_values = self.prof_tree.item(selected[0])['values']
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Professor")
        dialog.geometry("400x300")
        dialog.configure(bg=self.colors['white'])
        
        fields = ["Name", "Department", "Contact", "Email"]
        entries = {}
        
        for i, field in enumerate(fields):
            tk.Label(dialog, text=f"{field}:", bg=self.colors['white']).pack(pady=5)
            entry = tk.Entry(dialog)
            entry.insert(0, current_values[i])
            entry.pack(pady=5)
            entries[field] = entry
        
        def save_changes():
            values = {field: entry.get().strip() for field, entry in entries.items()}
            
            if not all(values.values()):
                messagebox.showerror("Error", "Please fill all fields")
                return
            
            self.prof_tree.item(selected[0], values=tuple(values.values()))
            dialog.destroy()
            messagebox.showinfo("Success", "Professor updated successfully")
        
        tk.Button(dialog,
                 text="Save Changes",
                 command=save_changes,
                 bg=self.colors['primary'],
                 fg=self.colors['white']).pack(pady=20)
    
    def delete_professor(self):
        selected = self.prof_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a professor to delete")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this professor?"):
            self.prof_tree.delete(selected[0])
            messagebox.showinfo("Success", "Professor deleted successfully")
    
    def backup_database(self):
        # Implement database backup functionality
        messagebox.showinfo("Backup", "Database backup completed successfully")
    
    def change_admin_password(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Change Admin Password")
        dialog.geometry("300x250")
        dialog.configure(bg=self.colors['white'])
        
        tk.Label(dialog, text="Current Password:", bg=self.colors['white']).pack(pady=5)
        current_pass = tk.Entry(dialog, show="*")
        current_pass.pack(pady=5)
        
        tk.Label(dialog, text="New Password:", bg=self.colors['white']).pack(pady=5)
        new_pass = tk.Entry(dialog, show="*")
        new_pass.pack(pady=5)
        
        tk.Label(dialog, text="Confirm New Password:", bg=self.colors['white']).pack(pady=5)
        confirm_pass = tk.Entry(dialog, show="*")
        confirm_pass.pack(pady=5)
        
        def save_password():
            current = current_pass.get()
            new = new_pass.get()
            confirm = confirm_pass.get()
            
            if not all([current, new, confirm]):
                messagebox.showerror("Error", "Please fill all fields")
                return
                
            if new != confirm:
                messagebox.showerror("Error", "New passwords do not match")
                return
            
            try:
                with open('user_credentials.json', 'r') as f:
                    users = json.load(f)
                
                if self.hash_password(current) != users['admin']:
                    messagebox.showerror("Error", "Current password is incorrect")
                    return
                
                users['admin'] = self.hash_password(new)
                
                with open('user_credentials.json', 'w') as f:
                    json.dump(users, f)
                
                dialog.destroy()
                messagebox.showinfo("Success", "Admin password changed successfully")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to change password: {str(e)}")
        
        tk.Button(dialog,
                 text="Save Changes",
                 command=save_password,
                 bg=self.colors['primary'],
                 fg=self.colors['white']).pack(pady=20)
    
    def hash_password(self, password):
        """Create a simple hash of the password"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def logout(self):
        self.main_frame.destroy()
        LoginWindow(self.root)

def main():
    root = tk.Tk()
    app = WelcomeWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
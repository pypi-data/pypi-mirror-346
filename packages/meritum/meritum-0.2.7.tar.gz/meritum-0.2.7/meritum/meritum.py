import os
import json
import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from datetime import datetime, timedelta
import platform
import time
import sys

APP_VERSION = "0.2.7"

# Patch CustomTkinter to better handle animation cancellation
original_ctk_destroy = ctk.CTkBaseClass.destroy


def patched_destroy(self):
    """Patched destroy method to cancel animations before destroying"""
    try:
        # Try to cancel any after events associated with this widget
        widget_id = str(self.winfo_id()) if hasattr(self, "winfo_id") else ""
        if widget_id:
            try:
                # Try to find after events by their string representation
                for after_id in self.after_info():
                    try:
                        if widget_id in str(after_id):
                            self.after_cancel(after_id)
                    except:
                        pass
            except Exception:
                pass
    except Exception:
        pass
        
    # Call the original destroy method
    try:
        original_ctk_destroy(self)
    except Exception:
        # If original destroy fails, try to use the basic Tkinter destroy as fallback
        try:
            if hasattr(self, "_destroy_orig"):
                self._destroy_orig()
        except:
            pass

# Apply the patch
ctk.CTkBaseClass.destroy = patched_destroy

# Set appearance mode and default color theme
ctk.DrawEngine.preferred_drawing_method = "circle_shapes"
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Define color schemes using HEX codes
COLOR_SCHEME = {
    'background': '#1E1E1E',
    'canvas': '#2D2D2D',
    'text': '#FFFFFF',
    'buttons': '#404040',
    'button_text': '#FFFFFF',
    'highlight': '#1f6aa5',
    'active': '#28a745',
    'hover': '#2580c9',
    'inactive': '#6c757d',
    'content_bg': '#2D2D2D',
    'content_inside_bg': '#393E41',
    'task_normal': '#1f6aa5',  # Blue for normal tasks of unassigned tasks to any objective.
    'task_late': '#dc3545',    # Red for late tasks
    'task_completed': '#28a745',  # Green for completed tasks of unassigned tasks to any objective.
    'milestone': '#ffc107',     # Yellow for milestones
}

class ConfigManager:
    def __init__(self):
        self.config_file = os.path.join(os.path.expanduser("~"), ".meritum_config.json")
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from file or create default if it doesn't exist"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.get_default_config()
        else:
            return self.get_default_config()
    
    def get_default_config(self):
        """Return default configuration"""
        return {
            "app_mode": None,  # None, "teacher", or "student"
            "last_student_path": None,  # Path for student mode
            "teacher_data": {
                "student_paths": {}  # Dictionary of student names and paths
            }
        }
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def set_app_mode(self, mode):
        """Set application mode"""
        self.config["app_mode"] = mode
        self.save_config()
    
    def get_app_mode(self):
        """Get saved application mode"""
        return self.config.get("app_mode")
    
    def set_student_path(self, path):
        """Set path for student mode"""
        self.config["last_student_path"] = path
        self.save_config()
    
    def get_student_path(self):
        """Get saved student path"""
        return self.config.get("last_student_path")
    
    def set_student_name(self, name):
        """Set last used student name"""
        self.config["last_student_name"] = name
        self.save_config()
    
    def get_student_name(self):
        """Get last used student name"""
        return self.config.get("last_student_name")
    
    def update_teacher_data(self, students_dict):
        """Update teacher's students data"""
        self.config["teacher_data"]["student_paths"] = students_dict
        self.save_config()
    
    def get_teacher_data(self):
        """Get teacher's students data"""
        return self.config["teacher_data"]["student_paths"]

    def get_gantt_config(self):
        """Get saved Gantt chart configuration"""
        gantt_config = self.config.get("gantt_config", {})
        if not gantt_config:
            # Default values
            gantt_config = {
                "start_date": None,
                "end_date": None,
                "zoom_factor": 1.0,
                "view_mode": "Month"
            }
            self.config["gantt_config"] = gantt_config
            self.save_config()
        return gantt_config

    def set_gantt_config(self, start_date=None, end_date=None, zoom_factor=None, view_mode=None):
        """Save Gantt chart configuration"""
        if "gantt_config" not in self.config:
            self.config["gantt_config"] = {}

        # Only update provided values
        if start_date is not None:
            self.config["gantt_config"]["start_date"] = start_date
        if end_date is not None:
            self.config["gantt_config"]["end_date"] = end_date
        if zoom_factor is not None:
            self.config["gantt_config"]["zoom_factor"] = zoom_factor
        if view_mode is not None:
            self.config["gantt_config"]["view_mode"] = view_mode

        self.save_config()

class ModeSelectionDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.selected_mode = None
        self.selected_student = None
        self.student_data_path = None
        
        self.title("Select Mode")
        self.geometry("400x400")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()
        
        # Center the dialog
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 400) // 2
        y = (self.winfo_screenheight() - 400) // 2
        self.geometry(f"400x400+{x}+{y}")
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Show the initial selection screen
        self.show_mode_selection()
    
    def show_mode_selection(self):
        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Meritum",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=20)
        
        # Mode selection
        self.mode_label = ctk.CTkLabel(
            self.main_frame,
            text="Select Mode:",
            font=ctk.CTkFont(size=14)
        )
        self.mode_label.pack(pady=(10, 5))
        
        # Teacher mode button
        self.teacher_btn = ctk.CTkButton(
            self.main_frame,
            text="Teacher Mode",
            command=self.select_teacher_mode,
            width=200,
            height=40
        )
        self.teacher_btn.pack(pady=5)
        
        # Student mode button
        self.student_btn = ctk.CTkButton(
            self.main_frame,
            text="Student Mode",
            command=self.select_student_mode,
            width=200,
            height=40
        )
        self.student_btn.pack(pady=5)
        
        # Exit button
        self.exit_btn = ctk.CTkButton(
            self.main_frame,
            text="Exit",
            command=self.exit_app,
            width=200,
            height=30,
            fg_color=COLOR_SCHEME['inactive']
        )
        self.exit_btn.pack(pady=20)
    
    def select_teacher_mode(self):
        self.selected_mode = "teacher"
        self.destroy()
    
    def select_student_mode(self):
        self.selected_mode = "student"
        # Show student setup screen
        self.show_student_setup()
    
    def show_student_setup(self):
        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Student Setup",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=20)

        # Data folder path first
        self.path_label = ctk.CTkLabel(
            self.main_frame,
            text="Data Folder Path (shared with teacher):",
            font=ctk.CTkFont(size=14)
        )
        self.path_label.pack(anchor='w', pady=(10, 5))

        self.path_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.path_frame.pack(fill='x', pady=(0, 15))

        self.path_entry = ctk.CTkEntry(
            self.path_frame,
            width=280
        )
        self.path_entry.pack(side='left', fill='x', expand=True)

        # Set default path
        default_path = os.path.join(os.path.expanduser("~"), "Documents", "PhD_Progress")
        self.path_entry.insert(0, default_path)

        self.browse_btn = ctk.CTkButton(
            self.path_frame,
            text="Browse",
            command=self.browse_folder,
            width=70
        )
        self.browse_btn.pack(side='right', padx=(10, 0))

        # Check config button
        self.check_btn = ctk.CTkButton(
            self.main_frame,
            text="Check for Existing Profile",
            command=self.check_for_profile,
            width=200
        )
        self.check_btn.pack(pady=10)

        # Student name (initially hidden, will show if needed)
        self.student_info_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.student_info_frame.pack(fill='x', pady=(0, 10), padx=5)

        # Hide student info frame initially
        self.student_info_frame.pack_forget()

        # Buttons
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(fill='x', pady=(20, 0))

        self.back_btn = ctk.CTkButton(
            self.button_frame,
            text="Back",
            command=self.show_mode_selection,
            width=100,
            fg_color=COLOR_SCHEME['inactive']
        )
        self.back_btn.pack(side='left')

        self.continue_btn = ctk.CTkButton(
            self.button_frame,
            text="Continue",
            command=self.setup_student,
            width=100
        )
        self.continue_btn.pack(side='right')

        # Initially disable continue button until profile is selected or created
        self.continue_btn.configure(state="disabled")

    def check_for_profile(self):
        """Check if student profile exists in the specified folder"""
        data_path = self.path_entry.get().strip()

        if not data_path:
            messagebox.showerror("Error", "Please enter a data folder path")
            return

        # Create folder if it doesn't exist
        try:
            os.makedirs(data_path, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create folder: {str(e)}")
            return

        # Check for student config file
        student_config_path = os.path.join(data_path, "student_config.json")

        if os.path.exists(student_config_path):
            try:
                with open(student_config_path, 'r') as f:
                    student_config = json.load(f)

                if student_config:
                    # Student profiles exist, let user select one
                    student_names = list(student_config.keys())

                    # Display student selection dropdown
                    self.show_student_selector(student_names, student_config)
                    return
            except Exception as e:
                messagebox.showwarning("Warning", f"Error reading configuration file: {str(e)}")

        # No existing profiles, show form to create new one
        self.show_new_profile_form()

    def show_student_selector(self, student_names, student_config):
        """Show UI to select from existing student profiles"""
        # Clear any existing widgets in student_info_frame
        for widget in self.student_info_frame.winfo_children():
            widget.destroy()

        # Show the frame
        self.student_info_frame.pack(fill='x', pady=(0, 10), padx=5)

        # Add a label
        select_label = ctk.CTkLabel(
            self.student_info_frame,
            text="Select Your Profile:",
            font=ctk.CTkFont(size=14)
        )
        select_label.pack(anchor='w', pady=(10, 5))

        # Add dropdown for student selection
        self.student_var = tk.StringVar(value=student_names[0])
        self.student_dropdown = ctk.CTkOptionMenu(
            self.student_info_frame,
            values=student_names,
            variable=self.student_var,
            width=300
        )
        self.student_dropdown.pack(pady=5)

        # Enable continue button
        self.continue_btn.configure(state="normal")

        # Store config for later use
        self.existing_student_config = student_config

    def show_new_profile_form(self):
        """Show form to create a new student profile"""
        # Clear any existing widgets in student_info_frame
        for widget in self.student_info_frame.winfo_children():
            widget.destroy()

        # Show the frame
        self.student_info_frame.pack(fill='x', pady=(0, 10), padx=5)

        # Add a label
        new_profile_label = ctk.CTkLabel(
            self.student_info_frame,
            text="Create New Profile:",
            font=ctk.CTkFont(size=14)
        )
        new_profile_label.pack(anchor='w', pady=(10, 5))

        # Student name
        self.name_label = ctk.CTkLabel(
            self.student_info_frame,
            text="Your Name:",
            font=ctk.CTkFont(size=12)
        )
        self.name_label.pack(anchor='w', pady=(5, 0))

        self.name_entry = ctk.CTkEntry(
            self.student_info_frame,
            width=300
        )
        self.name_entry.pack(fill='x', pady=(0, 10))

        # Email address
        self.email_label = ctk.CTkLabel(
            self.student_info_frame,
            text="Email Address:",
            font=ctk.CTkFont(size=12)
        )
        self.email_label.pack(anchor='w', pady=(5, 0))

        self.email_entry = ctk.CTkEntry(
            self.student_info_frame,
            width=300
        )
        self.email_entry.pack(fill='x', pady=(0, 10))

        # Program/Department
        self.program_label = ctk.CTkLabel(
            self.student_info_frame,
            text="Program/Department:",
            font=ctk.CTkFont(size=12)
        )
        self.program_label.pack(anchor='w', pady=(5, 0))

        self.program_entry = ctk.CTkEntry(
            self.student_info_frame,
            width=300
        )
        self.program_entry.pack(fill='x', pady=(0, 10))

        # Birth date
        self.birth_date_label = ctk.CTkLabel(
            self.student_info_frame,
            text="Birth Date (YYYY-MM-DD):",
            font=ctk.CTkFont(size=12)
        )
        self.birth_date_label.pack(anchor='w', pady=(5, 0))

        self.birth_date_entry = ctk.CTkEntry(
            self.student_info_frame,
            width=300
        )
        self.birth_date_entry.pack(fill='x', pady=(0, 10))

        # Profession
        self.profession_label = ctk.CTkLabel(
            self.student_info_frame,
            text="Profession (if applicable):",
            font=ctk.CTkFont(size=12)
        )
        self.profession_label.pack(anchor='w', pady=(5, 0))

        self.profession_entry = ctk.CTkEntry(
            self.student_info_frame,
            width=300
        )
        self.profession_entry.pack(fill='x', pady=(0, 10))

        # Telephone
        self.telephone_label = ctk.CTkLabel(
            self.student_info_frame,
            text="Telephone Number:",
            font=ctk.CTkFont(size=12)
        )
        self.telephone_label.pack(anchor='w', pady=(5, 0))

        self.telephone_entry = ctk.CTkEntry(
            self.student_info_frame,
            width=300
        )
        self.telephone_entry.pack(fill='x', pady=(0, 10))

        # Enable continue button
        self.continue_btn.configure(state="normal")

        # Set flag to indicate this is a new profile
        self.creating_new_profile = True

    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)
    
    def setup_student(self):
        """Set up student data and continue"""
        data_path = self.path_entry.get().strip()

        if not data_path:
            messagebox.showerror("Error", "Please enter a data folder path")
            return

        # Check if we're selecting existing profile or creating new one
        if hasattr(self, 'creating_new_profile') and self.creating_new_profile:
            # Creating new profile
            student_name = self.name_entry.get().strip()
            email = self.email_entry.get().strip()
            program = self.program_entry.get().strip()
            # New fields
            birth_date = self.birth_date_entry.get().strip()
            profession = self.profession_entry.get().strip()
            telephone = self.telephone_entry.get().strip()

            if not student_name:
                messagebox.showerror("Error", "Please enter your name")
                return

            # Validate birth date if provided
            if birth_date:
                try:
                    datetime.strptime(birth_date, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Error", "Invalid birth date format. Use YYYY-MM-DD")
                    return

            # Create student config file
            student_config_path = os.path.join(data_path, "student_config.json")

            try:
                # Load existing config if file exists
                if os.path.exists(student_config_path):
                    with open(student_config_path, 'r') as f:
                        student_config = json.load(f)
                else:
                    student_config = {}

                # Add or update student profile
                student_config[student_name] = {
                    "data_path": data_path,
                    "email": email,
                    "program": program,
                    "birth_date": birth_date,  
                    "profession": profession,  
                    "telephone": telephone,   
                    "created_date": datetime.now().strftime("%Y-%m-%d")
                }

                # Save updated config
                with open(student_config_path, 'w') as f:
                    json.dump(student_config, f, indent=2)

                self.selected_student = student_name
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create configuration file: {str(e)}")
                return
        else:
            # Using existing profile
            if hasattr(self, 'student_var'):
                student_name = self.student_var.get()
                self.selected_student = student_name
            else:
                messagebox.showerror("Error", "Please select or create a student profile")
                return

        # Create default progress data file if it doesn't exist
        progress_data_path = os.path.join(data_path, "progress_data.json")
        try:
            if not os.path.exists(progress_data_path):
                default_data = {
                    "tasks": [],
                    "notes": []
                }
                with open(progress_data_path, 'w') as f:
                    json.dump(default_data, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create data file: {str(e)}")
            return

        # Set the student data path
        self.student_data_path = data_path

        # Close dialog
        self.destroy()
    
    def exit_app(self):
        self.parent.destroy()

class ProfileFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        
        # Student data
        self.student_data = {}
        
        # Setup UI
        self.setup_ui()
        
        # Load data if student is selected
        if self.app.current_student and self.app.current_student != "Add a student...":
            self.load_student_data()
            # Enable form fields when student is selected
            self.set_form_state("normal")
        else:
            # Disable form fields when no student is selected
            self.set_form_state("disabled")
            # Show message to select a student
            self.show_no_student_message()

    def show_no_student_message(self):
        """Show message when no student is selected"""
        # Clear any existing message
        if hasattr(self, 'message_label') and self.message_label.winfo_exists():
            self.message_label.destroy()
            
        # Create message label
        self.message_label = ctk.CTkLabel(
            self.content_frame,
            text="Please select a student or create a new profile first",
            font=ctk.CTkFont(size=16),
            text_color="#ff6b6b"
        )
        self.message_label.place(relx=0.5, rely=0.2, anchor="center")
        
    def set_form_state(self, state):
        """Enable or disable all form fields"""
        # This will be called after setup_ui
        if not hasattr(self, 'name_entry'):
            return

        # Set state for all entry fields
        for entry in [
            self.name_entry, self.email_entry, self.program_entry,
            self.start_entry, self.end_entry, self.supervisor_entry,
            self.research_entry, self.birth_date_entry, self.profession_entry,
            self.telephone_entry
        ]:
            entry.configure(state=state)

        # Also enable/disable the save button
        self.save_btn.configure(state=state)

    def setup_ui(self):
        # Create main content container
        self.content_frame = ctk.CTkFrame(self, fg_color=COLOR_SCHEME['content_bg'])
        self.content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Profile title
        self.title_label = ctk.CTkLabel(
            self.content_frame,
            text="Student Profile",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(anchor='w', padx=20, pady=20)
        
        # Create form for profile data
        self.form_frame = ctk.CTkFrame(self.content_frame)
        self.form_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Student name
        self.name_label = ctk.CTkLabel(
            self.form_frame,
            text="Name:",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=150,
            anchor="w"
        )
        self.name_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        self.name_entry = ctk.CTkEntry(
            self.form_frame,
            width=300
        )
        self.name_entry.grid(row=0, column=1, padx=20, pady=10, sticky="w")
        
        # Email
        self.email_label = ctk.CTkLabel(
            self.form_frame,
            text="Email Address:",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=150,
            anchor="w"
        )
        self.email_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        
        self.email_entry = ctk.CTkEntry(
            self.form_frame,
            width=300
        )
        self.email_entry.grid(row=1, column=1, padx=20, pady=10, sticky="w")
        
        # Program/Department
        self.program_label = ctk.CTkLabel(
            self.form_frame,
            text="Program/Department:",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=150,
            anchor="w"
        )
        self.program_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        
        self.program_entry = ctk.CTkEntry(
            self.form_frame,
            width=300
        )
        self.program_entry.grid(row=2, column=1, padx=20, pady=10, sticky="w")
        
        # Start date
        self.start_label = ctk.CTkLabel(
            self.form_frame,
            text="Start Date:",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=150,
            anchor="w"
        )
        self.start_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        
        self.start_entry = ctk.CTkEntry(
            self.form_frame,
            width=300,
            placeholder_text="YYYY-MM-DD"
        )
        self.start_entry.grid(row=3, column=1, padx=20, pady=10, sticky="w")
        
        # Expected end date
        self.end_label = ctk.CTkLabel(
            self.form_frame,
            text="Expected End Date:",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=150,
            anchor="w"
        )
        self.end_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        
        self.end_entry = ctk.CTkEntry(
            self.form_frame,
            width=300,
            placeholder_text="YYYY-MM-DD"
        )
        self.end_entry.grid(row=4, column=1, padx=20, pady=10, sticky="w")
        
        # Supervisor
        self.supervisor_label = ctk.CTkLabel(
            self.form_frame,
            text="Supervisor:",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=150,
            anchor="w"
        )
        self.supervisor_label.grid(row=5, column=0, padx=20, pady=10, sticky="w")
        
        self.supervisor_entry = ctk.CTkEntry(
            self.form_frame,
            width=300
        )
        self.supervisor_entry.grid(row=5, column=1, padx=20, pady=10, sticky="w")
        
        # Research area
        self.research_label = ctk.CTkLabel(
            self.form_frame,
            text="Research Area:",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=150,
            anchor="w"
        )
        self.research_label.grid(row=6, column=0, padx=20, pady=10, sticky="w")

        self.research_entry = ctk.CTkEntry(
            self.form_frame,
            width=300
        )
        self.research_entry.grid(row=6, column=1, padx=20, pady=10, sticky="w")

        # Birth date
        self.birth_date_label = ctk.CTkLabel(
            self.form_frame,
            text="Birth Date:",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=150,
            anchor="w"
        )
        self.birth_date_label.grid(row=7, column=0, padx=20, pady=10, sticky="w")

        self.birth_date_entry = ctk.CTkEntry(
            self.form_frame,
            width=300,
            placeholder_text="YYYY-MM-DD"
        )
        self.birth_date_entry.grid(row=7, column=1, padx=20, pady=10, sticky="w")

        # Profession
        self.profession_label = ctk.CTkLabel(
            self.form_frame,
            text="Profession:",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=150,
            anchor="w"
        )
        self.profession_label.grid(row=8, column=0, padx=20, pady=10, sticky="w")

        self.profession_entry = ctk.CTkEntry(
            self.form_frame,
            width=300
        )
        self.profession_entry.grid(row=8, column=1, padx=20, pady=10, sticky="w")

        # Telephone
        self.telephone_label = ctk.CTkLabel(
            self.form_frame,
            text="Telephone:",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=150,
            anchor="w"
        )
        self.telephone_label.grid(row=9, column=0, padx=20, pady=10, sticky="w")

        self.telephone_entry = ctk.CTkEntry(
            self.form_frame,
            width=300
        )
        self.telephone_entry.grid(row=9, column=1, padx=20, pady=10, sticky="w")
        
        # Button frame
        self.button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.button_frame.pack(fill='x', padx=20, pady=(10, 20))
        
        # Save button
        self.save_btn = ctk.CTkButton(
            self.button_frame,
            text="Save Profile",
            command=self.save_profile,
            width=150,
            height=35
        )
        self.save_btn.pack(side='right', padx=20)
    
    def load_student_data(self):
        """Load student profile data"""
        try:
            # Clear any existing message
            if hasattr(self, 'message_label') and self.message_label.winfo_exists():
                self.message_label.destroy()

            # Enable form fields
            self.set_form_state("normal")

            student_data = self.app.students.get(self.app.current_student, {})
            data_path = student_data.get("data_path", "")

            if not data_path:
                return

            # Load student config
            config_path = os.path.join(data_path, "student_config.json")
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config_data = json.load(f)

                if self.app.current_student in config_data:
                    self.student_data = config_data[self.app.current_student]

                    # Populate form fields
                    self.name_entry.delete(0, 'end')
                    self.name_entry.insert(0, self.app.current_student)

                    if "email" in self.student_data:
                        self.email_entry.delete(0, 'end')
                        self.email_entry.insert(0, self.student_data["email"])

                    if "program" in self.student_data:
                        self.program_entry.delete(0, 'end')
                        self.program_entry.insert(0, self.student_data["program"])

                    if "start_date" in self.student_data:
                        self.start_entry.delete(0, 'end')
                        self.start_entry.insert(0, self.student_data["start_date"])

                    if "end_date" in self.student_data:
                        self.end_entry.delete(0, 'end')
                        self.end_entry.insert(0, self.student_data["end_date"])

                    if "supervisor" in self.student_data:
                        self.supervisor_entry.delete(0, 'end')
                        self.supervisor_entry.insert(0, self.student_data["supervisor"])

                    if "research_area" in self.student_data:
                        self.research_entry.delete(0, 'end')
                        self.research_entry.insert(0, self.student_data["research_area"])

                    # Add the new fields
                    if "birth_date" in self.student_data:
                        self.birth_date_entry.delete(0, 'end')
                        self.birth_date_entry.insert(0, self.student_data["birth_date"])

                    if "profession" in self.student_data:
                        self.profession_entry.delete(0, 'end')
                        self.profession_entry.insert(0, self.student_data["profession"])

                    if "telephone" in self.student_data:
                        self.telephone_entry.delete(0, 'end')
                        self.telephone_entry.insert(0, self.student_data["telephone"])

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load profile data: {str(e)}")

    def save_profile(self):
        """Save student profile data"""
        # Check if a student is selected
        if not self.app.current_student or self.app.current_student == "Add a student...":
            messagebox.showerror("Error", "No student selected. Please select or create a student profile first.")
            return
        try:
            student_data = self.app.students.get(self.app.current_student, {})
            data_path = student_data.get("data_path", "")

            if not data_path:
                messagebox.showerror("Error", "No data path available for student")
                return

            # Get form values
            name = self.name_entry.get().strip()
            email = self.email_entry.get().strip()
            program = self.program_entry.get().strip()
            start_date = self.start_entry.get().strip()
            end_date = self.end_entry.get().strip()
            supervisor = self.supervisor_entry.get().strip()
            research_area = self.research_entry.get().strip()
            birth_date = self.birth_date_entry.get().strip()
            profession = self.profession_entry.get().strip()
            telephone = self.telephone_entry.get().strip()

            if not name:
                messagebox.showerror("Error", "Please enter a name")
                return

            # Validate dates if provided
            if start_date:
                try:
                    datetime.strptime(start_date, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Error", "Invalid start date format. Use YYYY-MM-DD")
                    return

            if end_date:
                try:
                    datetime.strptime(end_date, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Error", "Invalid end date format. Use YYYY-MM-DD")
                    return

            # Validate birth date if provided
            if birth_date:
                try:
                    datetime.strptime(birth_date, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Error", "Invalid birth date format. Use YYYY-MM-DD")
                    return

            # Load existing config
            config_path = os.path.join(data_path, "student_config.json")
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config_data = json.load(f)
            else:
                config_data = {}

            # Check if name changed
            old_name = self.app.current_student

            # Update profile data
            profile_data = {
                "data_path": data_path,
                "email": email,
                "program": program,
                "start_date": start_date,
                "end_date": end_date,
                "supervisor": supervisor,
                "research_area": research_area,
                "birth_date": birth_date,
                "profession": profession,
                "telephone": telephone,
                "last_modified": datetime.now().strftime("%Y-%m-%d")
            }

            # If created_date exists in old data, preserve it
            if old_name in config_data and "created_date" in config_data[old_name]:
                profile_data["created_date"] = config_data[old_name]["created_date"]
            else:
                profile_data["created_date"] = datetime.now().strftime("%Y-%m-%d")

            # Handle name change if needed
            if name != old_name:
                # Remove old entry
                if old_name in config_data:
                    del config_data[old_name]

                # Update app's current student name
                self.app.current_student = name
                self.app.student_var.set(name)

                # Update students dictionary
                if old_name in self.app.students:
                    self.app.students[name] = self.app.students[old_name]
                    del self.app.students[old_name]

            # Add updated profile
            config_data[name] = profile_data

            # Save updated config
            with open(config_path, 'w') as f:
                json.dump(config_data, f, indent=2)

            # Update app's students data
            self.app.students[name]["data_path"] = data_path

            # Refresh student dropdown if in teacher mode
            if self.app.app_mode == "teacher":
                self.app.update_student_dropdown()

            messagebox.showinfo("Success", "Profile saved successfully")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save profile: {str(e)}")

class StudentProgressApp(ctk.CTk):
    def __init__(self, app_mode=None, student_name=None, student_data_path=None, target_screen=0):
        # Initialize the main window
        super().__init__()

        # Initialize config manager
        self.config_manager = ConfigManager()
        
        # Initialize variables
        self.target_screen = target_screen
        self.current_frame = None
        self.students = {}
        self.current_student = None
        self.app_mode = app_mode  # Set directly from parameters
        self.student_name = student_name
        self.student_data_path = student_data_path

        # Variables to store Gantt chart date range
        self.gantt_start_date = None
        self.gantt_end_date = None
        self.gantt_zoom_factor = 1.0
        self.gantt_view_mode = "Month"

        if self.config_manager:
            gantt_config = self.config_manager.get_gantt_config()
            if gantt_config:
                self.gantt_start_date = gantt_config.get("start_date")
                self.gantt_end_date = gantt_config.get("end_date")
                self.gantt_zoom_factor = gantt_config.get("zoom_factor", 1.0)
                self.gantt_view_mode = gantt_config.get("view_mode", "Month")
        
        # If no mode provided, check saved config
        if not self.app_mode:
            self.app_mode = self.config_manager.get_app_mode()
            if self.app_mode == "student":
                self.student_name = self.config_manager.get_student_name()
                self.student_data_path = self.config_manager.get_student_path()
            
        # If still no mode, show selection dialog
        if not self.app_mode:
            self.select_mode()
            
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Configure main window
        self.title("Meritum")
        
        # Button color constants
        self.BUTTON_COLORS = {
            'active': "#1f6aa5",        # Dark blue for active button
            'inactive': "#404040",      # Gray for inactive button
            'hover_active': "#2580c9",  # Light blue for active hover
            'hover_inactive': "#4d4d4d" # Light gray for inactive hover
        }
        
        # Get screen dimensions and position window
        screen_width, screen_height, screen_x, screen_y = self.get_screen_dimensions(self.target_screen)
        window_width = 1250
        window_height = 800
        self.minsize(1250, 800)
        x = max(0, screen_x + (screen_width - window_width) // 2)
        y = max(0, screen_y + (screen_height - window_height) // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Load students config BEFORE creating the UI
        if self.app_mode == "teacher":
            self.load_students_config()
        elif self.app_mode == "student" and self.student_name and self.student_data_path:
            self.students = {
                self.student_name: {
                    "data_path": self.student_data_path
                }
            }
            self.current_student = self.student_name
        
        # Create main layout
        self.setup_layout()
        
        # Update the dropdown AFTER layout is created
        if self.app_mode == "teacher":
            self.update_student_dropdown()
        
        # If student mode, configure for the selected student
        if self.app_mode == "student" and self.student_name:
            self.refresh_current_view()

    def cancel_animations(self, widget):
        """Recursively cancel any animations for a widget and its children"""
        # Try to cancel any click animations
        widget_id = str(widget.winfo_id())
        for after_id in self.tk.call('after', 'info'):
            if widget_id in str(after_id):
                try:
                    self.after_cancel(after_id)
                except Exception:
                    pass
        
        # Recursively process children
        try:
            for child in widget.winfo_children():
                self.cancel_animations(child)
        except (AttributeError, tk.TclError):
            pass
    
    def on_closing(self):
        """Handle window closing properly"""
        # First, try to grab and disable all callback IDs
        try:
            # Disable known CustomTkinter callbacks
            for callback_name in ["check_dpi_scaling", "update"]:
                try:
                    self.after_cancel(callback_name)
                except Exception:
                    pass

            # Cancel ALL after events we can find
            all_after_ids = list(self.tk.call('after', 'info'))
            for after_id in all_after_ids:
                try:
                    self.after_cancel(after_id)
                except Exception:
                    pass
        except Exception as e:
            print(f"Error canceling callbacks: {e}")

        # Release grab if it exists
        try:
            self.grab_release()
        except:
            pass

        # Use a safer widget destruction approach - avoid recursion
        try:
            # Use a queue-based approach instead of recursion
            widgets_to_destroy = list(self.winfo_children())

            while widgets_to_destroy:
                widget = widgets_to_destroy.pop(0)

                # Add children to the queue
                if hasattr(widget, 'winfo_children'):
                    try:
                        children = widget.winfo_children()
                        widgets_to_destroy.extend(children)
                    except:
                        pass
                    
                # Try to destroy this widget
                try:
                    if hasattr(widget, 'winfo_exists') and widget.winfo_exists():
                        widget.destroy()
                except Exception as e:
                    # Just continue if a widget can't be destroyed
                    pass
        except Exception as e:
            print(f"Error during widget cleanup: {e}")

        # Finally quit and destroy
        try:
            self.quit()
            self.destroy()
        except Exception as e:
            print(f"Error during final destruction: {e}")

        # Force exit as a last resort
        sys.exit(0)

    def select_mode(self):
        # Create and show the mode selection dialog
        dialog = ModeSelectionDialog(self)
        self.wait_window(dialog)  # Wait for the dialog to close

        # Get the selected mode from the dialog
        if hasattr(dialog, "selected_mode"):
            self.app_mode = dialog.selected_mode
        else:
            return  # No mode selected

        # Additional student data if in student mode
        if self.app_mode == "student":
            if hasattr(dialog, "selected_student"):
                self.student_name = dialog.selected_student
            if hasattr(dialog, "student_data_path"):
                self.student_data_path = dialog.student_data_path

    def get_screen_dimensions(self, target_screen):
        """Get dimensions for a specific screen"""
        try:
            total_width = self.winfo_screenwidth()
            screen_width = total_width // 2
            
            if target_screen == 0:
                return (screen_width, self.winfo_screenheight(), 0, 0)
            elif target_screen == 1:
                return (screen_width, self.winfo_screenheight(), screen_width, 0)
            
        except Exception as e:
            print(f"Error getting screen dimensions: {str(e)}")
        
        return (self.winfo_screenwidth(), self.winfo_screenheight(), 0, 0)

    def setup_layout(self):
        # Create sidebar frame
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side='left', fill='y')
        self.sidebar.pack_propagate(False)

        # Add title and mode indicator to sidebar
        mode_text = "Teacher Mode" if self.app_mode == "teacher" else "Student Mode"
        self.title_label = ctk.CTkLabel(
            self.sidebar,
            text=f"Meritum\n({mode_text})",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLOR_SCHEME['text'],
            fg_color=COLOR_SCHEME['highlight'],
            corner_radius=5,
            width=150,
            height=40,
            anchor='center'
        )
        self.title_label.pack(pady=20)

        # Create student selection dropdown (only enabled in teacher mode)
        if self.app_mode == "teacher":
            self.student_label = ctk.CTkLabel(
                self.sidebar,
                text="Select Student:",
                font=ctk.CTkFont(size=12)
            )
            self.student_label.pack(pady=(10, 0))

            self.student_var = tk.StringVar()
            self.student_dropdown = ctk.CTkOptionMenu(
                self.sidebar,
                variable=self.student_var,
                values=["Add a student..."],
                command=self.change_student,
                width=150
            )
            self.student_dropdown.pack(pady=5)

            # Add student button
            self.add_student_btn = ctk.CTkButton(
                self.sidebar,
                text="Add Student",
                command=self.show_add_student_dialog,
                width=150
            )
            self.add_student_btn.pack(pady=5)
        else:
            # In student mode, just show the student name
            self.student_var = tk.StringVar(value=self.student_name)
            self.student_label = ctk.CTkLabel(
                self.sidebar,
                text=f"Student: {self.student_name}",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            self.student_label.pack(pady=(10, 20))

        # Create sidebar menu buttons
        # Add Profile button first
        self.profile_btn = ctk.CTkButton(
            self.sidebar,
            text="Profile",
            command=self.show_profile_frame,
            width=150,
            height=40,
            fg_color=self.BUTTON_COLORS['active'],
            hover_color=self.BUTTON_COLORS['hover_active']
        )
        self.profile_btn.pack(pady=10)

        # Add Goals button
        self.goals_btn = ctk.CTkButton(
            self.sidebar,
            text="Goals",
            command=self.show_goals_frame,
            width=150,
            height=40,
            fg_color=self.BUTTON_COLORS['inactive'],
            hover_color=self.BUTTON_COLORS['hover_inactive']
        )
        self.goals_btn.pack(pady=10)

        self.gantt_btn = ctk.CTkButton(
            self.sidebar,
            text="Gantt Chart",
            command=self.show_gantt_frame,
            width=150,
            height=40,
            fg_color=self.BUTTON_COLORS['inactive'],
            hover_color=self.BUTTON_COLORS['hover_inactive']
        )
        self.gantt_btn.pack(pady=10)

        self.tasks_btn = ctk.CTkButton(
            self.sidebar,
            text="Tasks",
            command=self.show_tasks_frame,
            width=150,
            height=40,
            fg_color=self.BUTTON_COLORS['inactive'],
            hover_color=self.BUTTON_COLORS['hover_inactive']
        )
        self.tasks_btn.pack(pady=10)

        self.notes_btn = ctk.CTkButton(
            self.sidebar,
            text="Notes",
            command=self.show_notes_frame,
            width=150,
            height=40,
            fg_color=self.BUTTON_COLORS['inactive'],
            hover_color=self.BUTTON_COLORS['hover_inactive']
        )
        self.notes_btn.pack(pady=10)

        # Show settings button in both teacher and student mode, but with different functionality
        self.settings_btn = ctk.CTkButton(
            self.sidebar,
            text="Settings",
            command=self.show_settings_frame,
            width=150,
            height=40,
            fg_color=self.BUTTON_COLORS['inactive'],
            hover_color=self.BUTTON_COLORS['hover_inactive']
        )
        self.settings_btn.pack(pady=10)

        # Create main content frame
        self.main_content = ctk.CTkFrame(self)
        self.main_content.pack(side='left', fill='both', expand=True)

        # Show profile frame by default
        self.show_profile_frame()

    def show_goals_frame(self):
        # Clear main content
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # Create goals frame
        self.current_frame = GoalsFrame(self.main_content, self)
        self.current_frame.pack(fill='both', expand=True)

        # Update button colors
        self.update_button_colors("goals")

        # If a student is selected, force refresh of goal statistics
        if self.current_student and self.current_student != "Add a student...":
            # Load data first
            self.current_frame.load_student_data()

            # If the refresh method exists, call it to update goal stats
            if hasattr(self.current_frame, 'refresh_goal_statistics'):
                self.current_frame.refresh_goal_statistics()

    def show_profile_frame(self):
        # Clear main content
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # Create new frame for profile
        self.current_frame = ProfileFrame(self.main_content, self)
        self.current_frame.pack(fill='both', expand=True)

        # Update button colors
        self.update_button_colors("profile")

    def update_button_colors(self, active_button):
        """Update button colors based on which view is active"""
        # Reset all buttons to inactive
        buttons = ['profile', 'goals', 'gantt', 'tasks', 'notes']
        button_widgets = {
            'profile': self.profile_btn,
            'goals': self.goals_btn,
            'gantt': self.gantt_btn,
            'tasks': self.tasks_btn,
            'notes': self.notes_btn,
        }

        # Only add settings button if it exists (teacher mode)
        if hasattr(self, 'settings_btn'):
            buttons.append('settings')
            button_widgets['settings'] = self.settings_btn

        for btn in buttons:
            button_widgets[btn].configure(
                fg_color=self.BUTTON_COLORS['active'] if btn == active_button 
                else self.BUTTON_COLORS['inactive'],
                hover_color=self.BUTTON_COLORS['hover_active'] if btn == active_button 
                else self.BUTTON_COLORS['hover_inactive']
            )

    def show_gantt_frame(self):
        # Clear main content
        for widget in self.main_content.winfo_children():
            widget.destroy()
            
        # Create new frame for gantt chart
        self.current_frame = GanttChartFrame(self.main_content, self)
        self.current_frame.pack(fill='both', expand=True)
        
        # Update button colors
        self.update_button_colors("gantt")

        # If was previously set a zoom factor, make sure it's applied
        if hasattr(self, 'gantt_zoom_factor'):
            self.current_frame.zoom_factor = self.gantt_zoom_factor
            self.current_frame.update_zoom_indicator()
        
        if hasattr(self, 'gantt_view_mode'):
            self.current_frame.view_var.set(self.gantt_view_mode)
        
        self.current_frame.update_chart()
    
    def show_tasks_frame(self):
        # Clear main content
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # Create tasks frame
        self.current_frame = TasksFrame(self.main_content, self)
        self.current_frame.pack(fill='both', expand=True)

        # Update button colors
        self.update_button_colors("tasks")

        if self.current_student and self.current_student != "Add a student...":
            self.current_frame.load_student_data()
    
    def show_notes_frame(self):
        # Clear main content
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # Create notes frame
        self.current_frame = NotesFrame(self.main_content, self)
        self.current_frame.pack(fill='both', expand=True)

        # Update button colors
        self.update_button_colors("notes")

        if self.current_student and self.current_student != "Add a student...":
            self.current_frame.load_student_data()
    
    def show_settings_frame(self):
        # Clear main content
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # Create settings frame based on mode
        if self.app_mode == "teacher":
            self.current_frame = SettingsFrame(self.main_content, self)
        else:
            self.current_frame = StudentSettingsFrame(self.main_content, self)

        self.current_frame.pack(fill='both', expand=True)

        # Update button colors
        self.update_button_colors("settings")
    
    def show_add_student_dialog(self):
        dialog = AddStudentDialog(self)
        self.wait_window(dialog)
        # Update dropdown after dialog is closed
        if hasattr(dialog, "student_added") and dialog.student_added:
            self.update_student_dropdown()
    
    def update_student_dropdown(self):
        # Update student dropdown with current students
        student_names = list(self.students.keys())

        # Debug output
        #print(f"Updating dropdown with students: {student_names}")

        if not student_names:
            student_names = ["Add a student..."]

        # Make sure student_dropdown exists
        if hasattr(self, 'student_dropdown') and self.student_dropdown is not None:
            try:
                self.student_dropdown.configure(values=student_names)

                # Set current selection if we have students
                if student_names and student_names[0] != "Add a student...":
                    self.student_var.set(student_names[0])
                    self.current_student = student_names[0]
                    self.refresh_current_view()
                else:
                    self.student_var.set("Add a student...")
            except Exception as e:
                print(f"Error updating dropdown: {str(e)}")
    
    def change_student(self, student_name):
        if student_name == "Add a student...":
            self.show_add_student_dialog()
            return
        
        self.current_student = student_name
        self.refresh_current_view()
    
    def refresh_current_view(self):
        """Refresh current view to show selected student's data"""
        if hasattr(self, 'current_frame'):
            if hasattr(self.current_frame, 'load_student_data'):
                self.current_frame.load_student_data()

                # For Gantt Chart, explicitly call update_chart after loading data
                if isinstance(self.current_frame, GanttChartFrame):
                    # Ensure zoom factor is preserved
                    self.current_frame.zoom_factor = self.gantt_zoom_factor
                    self.current_frame.update_zoom_indicator()

                    # Restore view mode if saved
                    if hasattr(self, 'gantt_view_mode'):
                        self.current_frame.view_var.set(self.gantt_view_mode)

                    self.current_frame.update_chart()
                # For Tasks Frame, apply the current filter to refresh the view
                elif isinstance(self.current_frame, TasksFrame):
                    self.current_frame.apply_filter(self.current_frame.filter_var.get())

            elif isinstance(self.current_frame, ProfileFrame):
                # For profile frame, also handle enabling/disabling fields
                if self.current_student and self.current_student != "Add a student...":
                    self.current_frame.load_student_data()
                    self.current_frame.set_form_state("normal")
                    # Clear any existing message
                    if hasattr(self.current_frame, 'message_label') and self.current_frame.message_label.winfo_exists():
                        self.current_frame.message_label.destroy()
                else:
                    self.current_frame.set_form_state("disabled")
                    self.current_frame.show_no_student_message()

    def propagate_goal_color_change(self, goal_id, new_color):
        """Update all task colors associated with a goal across all views"""
        # First update the database
        try:
            if not self.current_student or self.current_student == "Add a student...":
                return

            student_data = self.students.get(self.current_student, {})
            data_path = student_data.get("data_path", "")

            if not data_path:
                return

            data_file = os.path.join(data_path, "progress_data.json")
            if not os.path.exists(data_file):
                return

            with open(data_file, 'r') as f:
                data = json.load(f)

            tasks = data.get("tasks", [])
            modified = False

            # Update all tasks with this goal_id
            for i, task in enumerate(tasks):
                if task.get('goal_id', '') == goal_id:
                    tasks[i]['goal_color'] = new_color
                    modified = True

            if modified:
                data["tasks"] = tasks
                with open(data_file, 'w') as f:
                    json.dump(data, f, indent=2)

            # Now refresh all views that display tasks
            self.refresh_current_view()

        except Exception as e:
            print(f"Error propagating goal color change: {str(e)}")
    
    def load_students_config(self):
        # Load students configuration from config file
        config_path = Path("students_config.json")

        print(f"Loading student config from: {config_path.absolute()}")

        if self.app_mode == "student" and hasattr(self, 'student_data_path'):
            student_config_path = Path(os.path.join(self.student_data_path, "student_config.json"))
            if student_config_path.exists():
                config_path = student_config_path
                print(f"Using student-specific config: {config_path}")

        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    data = json.load(f)
                    print(f"Loaded student data: {data}")
                    self.students = data

                    if not self.students:
                        print("Warning: Student config exists but contains no students")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load student configuration: {str(e)}")
                print(f"Error loading student configuration: {str(e)}")
        else:
            print(f"No config file found at {config_path}, creating empty config")
            # Create empty config file
            self.save_students_config()
    
    def save_students_config(self):
        # Save students configuration to config file
        config_path = Path("students_config.json")
        try:
            with open(config_path, 'w') as f:
                json.dump(self.students, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save student configuration: {str(e)}")
            
        if hasattr(self, 'config_manager'):
            self.config_manager.update_teacher_data(self.students)

class StudentSettingsFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        # Create main container
        self.main_container = ctk.CTkFrame(self, fg_color=COLOR_SCHEME['content_bg'])
        self.main_container.pack(fill='both', expand=True, padx=20, pady=20)

        # Settings title
        self.title_label = ctk.CTkLabel(
            self.main_container,
            text="Settings",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(anchor='w', padx=20, pady=20)
        
        # Application Mode settings
        self.mode_frame = ctk.CTkFrame(self.main_container)
        self.mode_frame.pack(fill='x', padx=20, pady=10)

        self.mode_label = ctk.CTkLabel(
            self.mode_frame,
            text="Application Mode",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.mode_label.pack(anchor='w', padx=20, pady=10)

        # Mode selection options
        self.mode_options_frame = ctk.CTkFrame(self.mode_frame, fg_color="transparent")
        self.mode_options_frame.pack(fill='x', padx=20, pady=10)

        # Description text
        mode_desc = (
            "You can set the default mode for the next application startup.\n"
            "This allows you to switch between student and teacher modes."
        )
        self.mode_desc_label = ctk.CTkLabel(
            self.mode_options_frame,
            text=mode_desc,
            justify="left",
            wraplength=600
        )
        self.mode_desc_label.pack(anchor='w', pady=(0, 10))

        # Default startup mode
        self.startup_mode_frame = ctk.CTkFrame(self.mode_options_frame, fg_color="transparent")
        self.startup_mode_frame.pack(fill='x', pady=5)

        self.startup_label = ctk.CTkLabel(
            self.startup_mode_frame,
            text="Default startup mode:",
            width=150,
            anchor="w"
        )
        self.startup_label.pack(side='left', padx=5)

        self.startup_var = tk.StringVar(value="student")

        # Check if a config manager exists and get the current setting
        if hasattr(self.app, 'config_manager'):
            current_mode = self.app.config_manager.get_app_mode()
            if current_mode:
                self.startup_var.set(current_mode)

        self.student_radio = ctk.CTkRadioButton(
            self.startup_mode_frame,
            text="Student Mode",
            variable=self.startup_var,
            value="student",
            command=self.update_startup_mode
        )
        self.student_radio.pack(side='left', padx=(10, 20))

        self.teacher_radio = ctk.CTkRadioButton(
            self.startup_mode_frame,
            text="Teacher Mode",
            variable=self.startup_var,
            value="teacher",
            command=self.update_startup_mode
        )
        self.teacher_radio.pack(side='left', padx=5)

        # Data Path section
        self.path_frame = ctk.CTkFrame(self.main_container)
        self.path_frame.pack(fill='x', padx=20, pady=10)

        self.path_label = ctk.CTkLabel(
            self.path_frame,
            text="Data Path Management",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.path_label.pack(anchor='w', padx=20, pady=10)

        # Path options frame
        self.path_options_frame = ctk.CTkFrame(self.path_frame, fg_color="transparent")
        self.path_options_frame.pack(fill='x', padx=20, pady=10)

        # Current path display
        current_path = self.app.student_data_path
        
        self.current_path_label = ctk.CTkLabel(
            self.path_options_frame,
            text="Current Data Path:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.current_path_label.pack(anchor='w', pady=(0, 5))
        
        self.path_display = ctk.CTkLabel(
            self.path_options_frame,
            text=current_path,
            font=ctk.CTkFont(size=12),
            wraplength=600,
            justify="left"
        )
        self.path_display.pack(anchor='w', pady=(0, 10))

        # Path management button
        self.manage_path_btn = ctk.CTkButton(
            self.path_options_frame,
            text="Change Data Path",
            command=self.show_path_manager,
            width=150,
            height=35
        )
        self.manage_path_btn.pack(anchor='w', pady=5)
        
        # Description
        description = (
            "Changing the data path will move your student profile and all related "
            "tasks and notes to the new location. This is useful if you need to "
            "synchronize your data with your teacher using a different folder."
        )
        self.desc_label = ctk.CTkLabel(
            self.path_options_frame,
            text=description,
            wraplength=600,
            justify="left"
        )
        self.desc_label.pack(anchor='w', pady=(10, 0))

        # App information section
        self.about_frame = ctk.CTkFrame(self.main_container)
        self.about_frame.pack(fill='x', padx=20, pady=(20, 10))

        self.about_label = ctk.CTkLabel(
            self.about_frame,
            text="About",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.about_label.pack(anchor='w', padx=20, pady=10)

        self.app_info = ctk.CTkLabel(
            self.about_frame,
            text=f"Meritum v{APP_VERSION}\n"
                 "A tool for tracking student progress using Gantt charts and task management."
        )
        self.app_info.pack(anchor='w', padx=20, pady=5)
    
    def update_startup_mode(self):
        """Update the default startup mode in config"""
        if hasattr(self.app, 'config_manager'):
            mode = self.startup_var.get()
            self.app.config_manager.set_app_mode(mode)
            messagebox.showinfo(
                "Startup Mode Changed",
                f"The application will start in {mode.capitalize()} Mode the next time it is launched."
            )
    
    def show_path_manager(self):
        """Show dialog to manage student data path"""
        dialog = StudentPathManagerDialog(self)
        self.wait_window(dialog)
        # Reload path display if path changed
        if hasattr(dialog, "path_changed") and dialog.path_changed:
            self.path_display.configure(text=self.app.student_data_path)
            # If applicable, refresh other data that might depend on the path

class AddStudentDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.student_added = False
        self.using_existing_profile = False  # Flag to track if using existing profile
        self.selected_profile_name = None    # Store selected profile name
        
        self.title("Add Student")
        self.geometry("400x400")  # Increased height to accommodate profile selection
        self.resizable(False, False)
        
        # Center dialog on parent
        self.update_idletasks()
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        dialog_width = 400
        dialog_height = 400
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Initialize UI with student creation form
        self.init_create_student_ui()
    
    def init_create_student_ui(self):
        """Initialize the UI for creating a new student"""
        # Clear any existing widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Add Student",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.title_label.pack(pady=(0, 15))
        
        # Name field
        self.name_label = ctk.CTkLabel(self.main_frame, text="Student Name:")
        self.name_label.pack(anchor='w', pady=(0, 5))
        
        self.name_entry = ctk.CTkEntry(self.main_frame, width=360)
        self.name_entry.pack(fill='x', pady=(0, 10))
        
        # Data path field
        self.path_label = ctk.CTkLabel(self.main_frame, text="Data Folder Path:")
        self.path_label.pack(anchor='w', pady=(0, 5))
        
        self.path_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.path_frame.pack(fill='x', pady=(0, 10))
        
        self.path_entry = ctk.CTkEntry(self.path_frame, width=280)
        self.path_entry.pack(side='left', fill='x', expand=True)
        
        self.browse_btn = ctk.CTkButton(
            self.path_frame,
            text="Browse",
            command=self.browse_folder,
            width=70
        )
        self.browse_btn.pack(side='right', padx=(10, 0))
        
        # Set default path to script directory
        default_path = os.path.join(os.getcwd(), "student_data")
        self.path_entry.insert(0, default_path)
        
        # Check profiles button
        self.check_btn = ctk.CTkButton(
            self.main_frame,
            text="Check for Existing Profiles",
            command=self.check_for_profiles,
            width=200
        )
        self.check_btn.pack(pady=10)
        
        # Create a container for the profile selection (initially hidden)
        self.profile_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.profile_container.pack(fill='x', pady=10)
        self.profile_container.pack_forget()  # Hide initially
        
        # Buttons
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(fill='x', pady=(10, 0))
        
        self.cancel_btn = ctk.CTkButton(
            self.button_frame,
            text="Cancel",
            command=self.destroy,
            fg_color=COLOR_SCHEME['inactive'],
            width=100
        )
        self.cancel_btn.pack(side='right', padx=(10, 0))
        
        self.add_btn = ctk.CTkButton(
            self.button_frame,
            text="Add Student",
            command=self.add_student,
            width=100
        )
        self.add_btn.pack(side='right')
        
        # Reset flags
        self.using_existing_profile = False
        self.selected_profile_name = None
        
        # Set focus on name entry
        self.name_entry.focus_set()
    
    def check_for_profiles(self):
        """Check if profiles exist in the selected data path"""
        data_path = self.path_entry.get().strip()
        
        if not data_path:
            messagebox.showerror("Error", "Please enter a data folder path")
            return
        
        # Check if path exists
        if not os.path.exists(data_path):
            try:
                os.makedirs(data_path, exist_ok=True)
                messagebox.showinfo("Info", "Created new folder. No existing profiles found.")
                return
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create folder: {str(e)}")
                return
        
        # Check for student configuration file
        config_path = os.path.join(data_path, "student_config.json")
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    student_config = json.load(f)
                
                if student_config and len(student_config) > 0:
                    # Show student profiles found in this path
                    self.show_existing_profiles(student_config)
                    return
                else:
                    messagebox.showinfo("Info", "No student profiles found in this path.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read configuration file: {str(e)}")
        else:
            messagebox.showinfo("Info", "No student profiles found in this path.")
    
    def show_existing_profiles(self, student_config):
        """Show UI for selecting from existing profiles"""
        # Clear profile container
        for widget in self.profile_container.winfo_children():
            widget.destroy()
        
        # Show the container
        self.profile_container.pack(fill='x', pady=10)
        
        # Add a label
        self.profiles_label = ctk.CTkLabel(
            self.profile_container,
            text="Existing profiles found. Select one to add:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.profiles_label.pack(anchor='w', pady=(0, 10))
        
        # Get student names
        student_names = list(student_config.keys())
        
        # Create a scrollable frame if there are many students
        self.profiles_scroll = ctk.CTkScrollableFrame(
            self.profile_container,
            height=150
        )
        self.profiles_scroll.pack(fill='x', expand=True)
        
        # Add radio buttons for each profile
        self.profile_var = tk.StringVar(value="")
        
        for name in student_names:
            profile_data = student_config[name]
            
            # Format display text
            display_text = f"{name}"
            if "email" in profile_data and profile_data["email"]:
                display_text += f" - {profile_data['email']}"
            if "program" in profile_data and profile_data["program"]:
                display_text += f" ({profile_data['program']})"
            
            # Create the radio button
            radio = ctk.CTkRadioButton(
                self.profiles_scroll,
                text=display_text,
                variable=self.profile_var,
                value=name,
                command=self.on_profile_selected  # Add callback when profile is selected
            )
            radio.pack(anchor='w', pady=5)
        
        # Store the config for later use
        self.existing_profiles = student_config
    
    def on_profile_selected(self):
        """Called when a profile is selected from the list"""
        self.using_existing_profile = True
        self.selected_profile_name = self.profile_var.get()
        
        # Auto-fill the name field with the selected profile name
        if self.selected_profile_name:
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, self.selected_profile_name)
    
    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)
    
    def add_student(self):
        data_path = self.path_entry.get().strip()
        
        if not data_path:
            messagebox.showerror("Error", "Please enter a data folder path")
            return
        
        # Check if we're using an existing profile
        if self.using_existing_profile and self.selected_profile_name:
            # Using an existing profile selected from the list
            name = self.selected_profile_name
        else:
            # Creating a new profile, need to validate the name
            name = self.name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Please enter a student name")
                return
        
        # Check if the student already exists
        if name in self.parent.students:
            messagebox.showerror("Error", "A student with this name already exists")
            return
        
        # Create folder if it doesn't exist
        try:
            os.makedirs(data_path, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create folder: {str(e)}")
            return
        
        # Check if we're using an existing profile
        if self.using_existing_profile and self.selected_profile_name:
            self.parent.students[name] = {
                "data_path": data_path
            }
            self.parent.save_students_config()
            self.student_added = True
            self.destroy()
            return
        
        # If we get here, we're creating a new profile
        # Check if student_config.json already exists
        config_path = os.path.join(data_path, "student_config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    existing_config = json.load(f)
                
                # Check if the name already exists in the config
                if name in existing_config:
                    use_existing = messagebox.askyesno(
                        "Profile Exists",
                        f"A profile with name '{name}' already exists in this data folder. Use this existing profile?"
                    )
                    if use_existing:
                        self.parent.students[name] = {
                            "data_path": data_path
                        }
                        self.parent.save_students_config()
                        self.student_added = True
                        self.destroy()
                        return
                    else:
                        # Let them continue with creating a new entry
                        pass
                
                # Otherwise, we'll add a new entry to the existing config file
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read configuration file: {str(e)}")
                # Continue with creating a new profile
        
        # Create default data file if it doesn't exist
        data_file = os.path.join(data_path, "progress_data.json")
        if not os.path.exists(data_file):
            default_data = {
                "tasks": [],
                "notes": []
            }
            try:
                with open(data_file, 'w') as f:
                    json.dump(default_data, f, indent=2)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create data file: {str(e)}")
                return
        
        # Create/update student config file
        try:
            student_config = {}
            
            # Load existing config if available
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    student_config = json.load(f)
            
            # Add the new student profile
            student_config[name] = {
                "data_path": data_path,
                "created_date": datetime.now().strftime("%Y-%m-%d")
            }
            
            # Save updated config
            with open(config_path, 'w') as f:
                json.dump(student_config, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create student configuration: {str(e)}")
            return
        
        # Add student to app config
        self.parent.students[name] = {
            "data_path": data_path
        }
        
        # Save config
        self.parent.save_students_config()
        
        # Set flag to indicate student was added
        self.student_added = True
        
        # Close dialog
        self.destroy()

    def show_new_profile_form(self):
        """Show form to create a new student profile"""
        # Clear any existing widgets in student_info_frame
        for widget in self.student_info_frame.winfo_children():
            widget.destroy()
    
        # Show the frame
        self.student_info_frame.pack(fill='x', pady=(0, 10), padx=5)
    
        # Add a label
        new_profile_label = ctk.CTkLabel(
            self.student_info_frame,
            text="Create New Profile:",
            font=ctk.CTkFont(size=14)
        )
        new_profile_label.pack(anchor='w', pady=(10, 5))
    
        # Student name
        self.name_label = ctk.CTkLabel(
            self.student_info_frame,
            text="Your Name:",
            font=ctk.CTkFont(size=12)
        )
        self.name_label.pack(anchor='w', pady=(5, 0))
    
        self.name_entry = ctk.CTkEntry(
            self.student_info_frame,
            width=300
        )
        self.name_entry.pack(fill='x', pady=(0, 10))
    
        # Email address
        self.email_label = ctk.CTkLabel(
            self.student_info_frame,
            text="Email Address:",
            font=ctk.CTkFont(size=12)
        )
        self.email_label.pack(anchor='w', pady=(5, 0))
    
        self.email_entry = ctk.CTkEntry(
            self.student_info_frame,
            width=300
        )
        self.email_entry.pack(fill='x', pady=(0, 10))
    
        # Program/Department
        self.program_label = ctk.CTkLabel(
            self.student_info_frame,
            text="Program/Department:",
            font=ctk.CTkFont(size=12)
        )
        self.program_label.pack(anchor='w', pady=(5, 0))
    
        self.program_entry = ctk.CTkEntry(
            self.student_info_frame,
            width=300
        )
        self.program_entry.pack(fill='x', pady=(0, 10))
        
        # Birth date
        self.birth_date_label = ctk.CTkLabel(
            self.student_info_frame,
            text="Birth Date (YYYY-MM-DD):",
            font=ctk.CTkFont(size=12)
        )
        self.birth_date_label.pack(anchor='w', pady=(5, 0))
    
        self.birth_date_entry = ctk.CTkEntry(
            self.student_info_frame,
            width=300
        )
        self.birth_date_entry.pack(fill='x', pady=(0, 10))
        
        # Profession
        self.profession_label = ctk.CTkLabel(
            self.student_info_frame,
            text="Profession (if applicable):",
            font=ctk.CTkFont(size=12)
        )
        self.profession_label.pack(anchor='w', pady=(5, 0))
    
        self.profession_entry = ctk.CTkEntry(
            self.student_info_frame,
            width=300
        )
        self.profession_entry.pack(fill='x', pady=(0, 10))
        
        # Telephone
        self.telephone_label = ctk.CTkLabel(
            self.student_info_frame,
            text="Telephone Number:",
            font=ctk.CTkFont(size=12)
        )
        self.telephone_label.pack(anchor='w', pady=(5, 0))
    
        self.telephone_entry = ctk.CTkEntry(
            self.student_info_frame,
            width=300
        )
        self.telephone_entry.pack(fill='x', pady=(0, 10))
    
        # Enable continue button
        self.continue_btn.configure(state="normal")
    
        # Set flag to indicate this is a new profile
        self.creating_new_profile = True

class GoalsFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        
        # Goals data
        self.goals = []
        
        # Setup UI
        self.setup_ui()
        
        # Load data if student is selected
        if self.app.current_student and self.app.current_student != "Add a student...":
            self.load_student_data()
    
    def setup_ui(self):
        # Top control panel
        self.control_panel = ctk.CTkFrame(self)
        self.control_panel.pack(fill='x', padx=20, pady=10)

        # Add goal button
        self.add_goal_btn = ctk.CTkButton(
            self.control_panel,
            text="Add New Goal",
            command=self.add_goal,
            width=150
        )
        self.add_goal_btn.pack(side='left', padx=10)

        # Progress overview
        self.progress_frame = ctk.CTkFrame(self.control_panel, fg_color="transparent")
        self.progress_frame.pack(side='right', padx=10)
        
        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="Overall Progress: 0%",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.progress_label.pack(side='right')

        # Create main content area
        self.content_frame = ctk.CTkFrame(self, fg_color=COLOR_SCHEME['content_bg'])
        self.content_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Create scrollable goals list
        self.goal_list = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent"
        )
        self.goal_list.pack(fill='both', expand=True, padx=10, pady=10)
    
    def load_student_data(self):
        """Load student goals data from JSON file"""
        try:
            # Clear any existing content
            for widget in self.goal_list.winfo_children():
                widget.destroy()

            # Check if student is selected
            if not self.app.current_student or self.app.current_student == "Add a student...":
                # Show message to select a student
                label = ctk.CTkLabel(
                    self.goal_list,
                    text="Please select a student to view goals",
                    font=ctk.CTkFont(size=14)
                )
                label.pack(pady=20)
                return

            # Get student data
            student_data = self.app.students.get(self.app.current_student, {})
            data_path = student_data.get("data_path", "")

            if not data_path:
                # Show no data path message
                no_path_label = ctk.CTkLabel(
                    self.goal_list,
                    text="No data path set for this student",
                    font=ctk.CTkFont(size=14)
                )
                no_path_label.pack(pady=20)
                return

            data_file = os.path.join(data_path, "progress_data.json")
            if not os.path.exists(data_file):
                # Create default data file if it doesn't exist
                default_data = {
                    "tasks": [],
                    "notes": [],
                    "goals": []
                }
                with open(data_file, 'w') as f:
                    json.dump(default_data, f, indent=2)
                self.goals = []
            else:
                with open(data_file, 'r') as f:
                    data = json.load(f)
                    self.goals = data.get("goals", [])
                    
                    # If goals don't exist in data, initialize it
                    if "goals" not in data:
                        data["goals"] = []
                        with open(data_file, 'w') as f:
                            json.dump(data, f, indent=2)

            # Update goals list
            self.update_goals_list()
            # Update overall progress
            self.update_overall_progress()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load student data: {str(e)}")
    
    def save_student_data(self):
        """Save student goals data to JSON file"""
        try:
            student_data = self.app.students.get(self.app.current_student, {})
            data_path = student_data.get("data_path", "")
            
            if not data_path:
                return
            
            data_file = os.path.join(data_path, "progress_data.json")
            
            # Load existing data to preserve tasks and notes
            if os.path.exists(data_file):
                with open(data_file, 'r') as f:
                    data = json.load(f)
            else:
                data = {"tasks": [], "notes": []}
            
            # Update goals
            data["goals"] = self.goals
            
            # Save updated data
            with open(data_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save student data: {str(e)}")
    
    def update_goals_list(self):
        """Update the goals list display"""
        # Clear existing goals
        for widget in self.goal_list.winfo_children():
            widget.destroy()

        if not self.app.current_student or self.app.current_student == "Add a student...":
            # Show message to select a student
            label = ctk.CTkLabel(
                self.goal_list,
                text="Please select a student to view goals",
                font=ctk.CTkFont(size=14)
            )
            label.pack(pady=20)
            return

        if not self.goals:
            # Show message when no goals exist
            no_goals_label = ctk.CTkLabel(
                self.goal_list,
                text="No goals found. Add goals using the 'Add New Goal' button.",
                font=ctk.CTkFont(size=14)
            )
            no_goals_label.pack(pady=20)
            return

        # Display goals
        for goal in self.goals:
            self.create_goal_item(goal)
            
        # Update overall progress
        self.update_overall_progress()
    
    def create_goal_item(self, goal):
        """Create a goal item widget"""
        # Main goal frame with the goal's color as background
        goal_frame = ctk.CTkFrame(
            self.goal_list, 
            fg_color=goal.get('color', COLOR_SCHEME['task_normal'])
        )
        goal_frame.pack(fill='x', padx=5, pady=5)

        # Inner frame with normal background for content
        inner_frame = ctk.CTkFrame(goal_frame)
        inner_frame.pack(fill='x', padx=2, pady=2)

        # Goal content
        content_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
        content_frame.pack(fill='x', padx=10, pady=10, expand=True)

        # Title and progress in first row
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill='x', expand=True)

        # Title with color indicator
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side='left')

        # Color indicator
        color_indicator = ctk.CTkFrame(
            title_frame, 
            width=20, 
            height=20, 
            fg_color=goal.get('color', COLOR_SCHEME['task_normal'])
        )
        color_indicator.pack(side='left', padx=(0, 10))

        # Goal title
        title_label = ctk.CTkLabel(
            title_frame,
            text=goal.get('title', 'Untitled Goal'),
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(side='left')

        # Progress percentage
        progress = goal.get('progress', 0)
        progress_label = ctk.CTkLabel(
            header_frame,
            text=f"Progress: {progress}%",
            font=ctk.CTkFont(size=14)
        )
        progress_label.pack(side='right')

        # Progress bar
        progress_bar_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        progress_bar_frame.pack(fill='x', pady=5)
        
        progress_bar = ctk.CTkProgressBar(progress_bar_frame)
        progress_bar.pack(fill='x')
        progress_bar.set(progress / 100)

        # Task statistics
        stats_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        stats_frame.pack(fill='x', pady=5)
        
        # Calculate task stats
        task_count = goal.get('task_count', 0)
        completed_count = goal.get('completed_count', 0)
        
        stats_label = ctk.CTkLabel(
            stats_frame,
            text=f"Tasks: {completed_count} of {task_count} completed",
            font=ctk.CTkFont(size=12)
        )
        stats_label.pack(side='left')

        # Description section
        if goal.get('description'):
            desc_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            desc_frame.pack(fill='x', pady=5)
            
            desc_text = ctk.CTkTextbox(desc_frame, height=60)
            desc_text.pack(fill='x')
            desc_text.insert('1.0', goal.get('description', ''))
            desc_text.configure(state="disabled")

        # Action buttons
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.pack(fill='x', pady=(10, 0))

        # Edit button
        edit_btn = ctk.CTkButton(
            button_frame,
            text="Edit Goal",
            command=lambda g=goal: self.edit_goal(g),
            width=100,
            height=30
        )
        edit_btn.pack(side='left', padx=5)

        # Change color button
        color_btn = ctk.CTkButton(
            button_frame,
            text="Change Color",
            command=lambda g=goal: self.change_color(g),
            width=120,
            height=30
        )
        color_btn.pack(side='left', padx=5)

        # Delete button
        delete_btn = ctk.CTkButton(
            button_frame,
            text="Delete",
            command=lambda g=goal: self.delete_goal(g),
            width=80,
            height=30,
            fg_color="#dc3545",
            hover_color="#c82333"
        )
        delete_btn.pack(side='right', padx=5)
    
    def add_goal(self):
        """Open dialog to add a new goal"""
        if not self.app.current_student or self.app.current_student == "Add a student...":
            messagebox.showinfo("Info", "Please select a student first")
            return
        
        dialog = GoalDialog(self)
        self.wait_window(dialog)
        
        if dialog.goal_data:
            # Add new goal
            self.goals.append(dialog.goal_data)
            # Save data
            self.save_student_data()
            # Update goals list
            self.update_goals_list()
    
    def edit_goal(self, goal):
        """Edit an existing goal"""
        dialog = GoalDialog(self, goal)
        self.wait_window(dialog)
        
        if dialog.goal_data:
            # Update goal
            for i, g in enumerate(self.goals):
                if g.get('id', '') == goal.get('id', ''):
                    self.goals[i] = dialog.goal_data
                    break
            
            # Save data
            self.save_student_data()
            
            # Update goals list
            self.update_goals_list()

            # Update progress statistics for related tasks
            self.update_task_goal_data()
    
    def update_task_colors(self, goal_id, new_color):
        """Update colors of tasks associated with the goal"""
        try:
            # Get student data
            student_data = self.app.students.get(self.app.current_student, {})
            data_path = student_data.get("data_path", "")

            if not data_path:
                return

            data_file = os.path.join(data_path, "progress_data.json")
            if not os.path.exists(data_file):
                return

            # Load tasks
            with open(data_file, 'r') as f:
                data = json.load(f)

            tasks = data.get("tasks", [])
            modified = False

            # Update task colors
            for i, task in enumerate(tasks):
                if task.get('goal_id', '') == goal_id:
                    # Update task color
                    tasks[i]['goal_color'] = new_color
                    modified = True

            if modified:
                # Save updated tasks
                data["tasks"] = tasks
                with open(data_file, 'w') as f:
                    json.dump(data, f, indent=2)

                # If the current frame is a TasksFrame, refresh it
                if hasattr(self.app, 'current_frame'):
                    # Refresh the Gantt chart if it's the current view
                    if isinstance(self.app.current_frame, GanttChartFrame):
                        self.app.current_frame.load_student_data()
                        self.app.current_frame.update_chart()

                    # Refresh the Tasks list if it's the current view
                    elif isinstance(self.app.current_frame, TasksFrame):
                        self.app.current_frame.load_student_data()
                        self.app.current_frame.apply_filter(self.app.current_frame.filter_var.get())

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update task colors: {str(e)}")

    def change_color(self, goal):
        """Open color picker to change goal color"""
        dialog = ColorPickerDialog(self, goal)
        self.wait_window(dialog)

        if dialog.selected_color:
            # Update goal color
            for i, g in enumerate(self.goals):
                if g.get('id', '') == goal.get('id', ''):
                    self.goals[i]['color'] = dialog.selected_color
                    break
                
            # Save data
            self.save_student_data()

            # Update goals list
            self.update_goals_list()

            # Update tasks that use this goal
            self.update_task_colors(goal.get('id', ''), dialog.selected_color)

            # Force update of all frames that might display tasks
            self.refresh_all_task_views()

    def refresh_all_task_views(self):
        """Force refresh of all views that display tasks"""
        try:
            # First update all task references to the goal colors in the database
            student_data = self.app.students.get(self.app.current_student, {})
            data_path = student_data.get("data_path", "")

            if not data_path:
                return

            data_file = os.path.join(data_path, "progress_data.json")
            if not os.path.exists(data_file):
                return

            # Load data
            with open(data_file, 'r') as f:
                data = json.load(f)

            tasks = data.get("tasks", [])
            goals = data.get("goals", [])

            # Create a goal lookup dictionary for efficiency
            goal_colors = {}
            for goal in goals:
                goal_colors[goal.get('id', '')] = goal.get('color', '')

            # Update all tasks with their goal colors
            modified = False
            for i, task in enumerate(tasks):
                goal_id = task.get('goal_id', '')
                if goal_id and goal_id in goal_colors:
                    # Make sure the task has the correct goal color
                    if task.get('goal_color', '') != goal_colors[goal_id]:
                        tasks[i]['goal_color'] = goal_colors[goal_id]
                        modified = True

            # Save if modified
            if modified:
                data["tasks"] = tasks
                with open(data_file, 'w') as f:
                    json.dump(data, f, indent=2)

            # Now refresh all relevant views
            # If a GanttChartFrame exists anywhere, refresh it
            for attr_name in dir(self.app):
                attr = getattr(self.app, attr_name)
                if isinstance(attr, GanttChartFrame):
                    attr.load_student_data()
                    attr.update_chart()

            # If the current frame is a GanttChartFrame, refresh it
            if hasattr(self.app, 'current_frame'):
                if isinstance(self.app.current_frame, GanttChartFrame):
                    self.app.current_frame.load_student_data()
                    self.app.current_frame.update_chart()
                elif isinstance(self.app.current_frame, TasksFrame):
                    self.app.current_frame.load_student_data()
                    self.app.current_frame.apply_filter(self.app.current_frame.filter_var.get())

        except Exception as e:
            print(f"Error refreshing task views: {str(e)}")

    def update_task_goal_data(self):
        """Update task statistics in goals"""
        try:
            # Get student data
            student_data = self.app.students.get(self.app.current_student, {})
            data_path = student_data.get("data_path", "")
            
            if not data_path:
                return
            
            data_file = os.path.join(data_path, "progress_data.json")
            if not os.path.exists(data_file):
                return
            
            # Load tasks
            with open(data_file, 'r') as f:
                data = json.load(f)
            
            tasks = data.get("tasks", [])
            
            # Initialize task statistics for each goal
            for i, goal in enumerate(self.goals):
                self.goals[i]['task_count'] = 0
                self.goals[i]['completed_count'] = 0
                self.goals[i]['total_progress'] = 0
            
            # Calculate task statistics
            for task in tasks:
                goal_id = task.get('goal_id', '')
                if goal_id:
                    # Find the goal
                    for i, goal in enumerate(self.goals):
                        if goal.get('id', '') == goal_id:
                            # Update task count
                            self.goals[i]['task_count'] = self.goals[i].get('task_count', 0) + 1
                            
                            # Update completed count
                            if task.get('completed', False):
                                self.goals[i]['completed_count'] = self.goals[i].get('completed_count', 0) + 1
                            
                            # Add to total progress
                            self.goals[i]['total_progress'] = self.goals[i].get('total_progress', 0) + task.get('progress', 0)
                            break
            
            # Calculate average progress for each goal
            for i, goal in enumerate(self.goals):
                task_count = self.goals[i].get('task_count', 0)
                if task_count > 0:
                    avg_progress = self.goals[i].get('total_progress', 0) / task_count
                    self.goals[i]['progress'] = round(avg_progress)
                else:
                    self.goals[i]['progress'] = 0
            
            # Save updated goals
            data["goals"] = self.goals
            with open(data_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            # Update goals list
            self.update_goals_list()
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update goal statistics: {str(e)}")
    
    def update_overall_progress(self):
        """Update the overall progress indicator"""
        if not self.goals:
            self.progress_label.configure(text="Overall Progress: 0%")
            return
        
        # Calculate average progress across all goals
        total_progress = sum(goal.get('progress', 0) for goal in self.goals)
        average_progress = total_progress / len(self.goals)
        
        # Update progress label
        self.progress_label.configure(text=f"Overall Progress: {round(average_progress)}%")
    
    def delete_goal(self, goal):
        """Delete a goal after confirmation"""
        # Check how many tasks are using this goal
        task_count = self.count_tasks_with_goal(goal.get('id', ''))
        
        message = f"Are you sure you want to delete the goal '{goal.get('title', '')}'?"
        if task_count > 0:
            message += f"\n\nThis goal is used by {task_count} tasks. Deleting it will remove the goal association from these tasks."
        
        confirm = messagebox.askyesno("Confirm Delete", message)
        
        if confirm:
            # Remove goal from tasks
            self.remove_goal_from_tasks(goal.get('id', ''))
            
            # Remove goal from list
            self.goals = [g for g in self.goals if g.get('id', '') != goal.get('id', '')]
            
            # Save data
            self.save_student_data()
            
            # Update goals list
            self.update_goals_list()
    
    def count_tasks_with_goal(self, goal_id):
        """Count tasks associated with a goal"""
        try:
            # Get student data
            student_data = self.app.students.get(self.app.current_student, {})
            data_path = student_data.get("data_path", "")
            
            if not data_path:
                return 0
            
            data_file = os.path.join(data_path, "progress_data.json")
            if not os.path.exists(data_file):
                return 0
            
            # Load tasks
            with open(data_file, 'r') as f:
                data = json.load(f)
            
            tasks = data.get("tasks", [])
            
            # Count tasks with this goal
            count = sum(1 for task in tasks if task.get('goal_id', '') == goal_id)
            
            return count
        
        except Exception:
            return 0
    
    def remove_goal_from_tasks(self, goal_id):
        """Remove goal association from tasks"""
        try:
            # Get student data
            student_data = self.app.students.get(self.app.current_student, {})
            data_path = student_data.get("data_path", "")
            
            if not data_path:
                return
            
            data_file = os.path.join(data_path, "progress_data.json")
            if not os.path.exists(data_file):
                return
            
            # Load tasks
            with open(data_file, 'r') as f:
                data = json.load(f)
            
            tasks = data.get("tasks", [])
            modified = False
            
            # Remove goal from tasks
            for i, task in enumerate(tasks):
                if task.get('goal_id', '') == goal_id:
                    # Remove goal association
                    if 'goal_id' in tasks[i]:
                        del tasks[i]['goal_id']
                    if 'goal_color' in tasks[i]:
                        del tasks[i]['goal_color']
                    modified = True
            
            if modified:
                # Save updated tasks
                data["tasks"] = tasks
                with open(data_file, 'w') as f:
                    json.dump(data, f, indent=2)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update tasks: {str(e)}")

    def refresh_goal_statistics(self):
        """Force an automatic refresh of goal statistics from tasks"""
        try:
            # Get student data
            student_data = self.app.students.get(self.app.current_student, {})
            data_path = student_data.get("data_path", "")

            if not data_path:
                return

            data_file = os.path.join(data_path, "progress_data.json")
            if not os.path.exists(data_file):
                return

            # Load data
            with open(data_file, 'r') as f:
                data = json.load(f)

            tasks = data.get("tasks", [])
            goals = data.get("goals", [])

            # Reset statistics for all goals
            for i, goal in enumerate(goals):
                goals[i]['task_count'] = 0
                goals[i]['completed_count'] = 0
                goals[i]['total_progress'] = 0

            # Calculate task statistics for each goal
            for task in tasks:
                goal_id = task.get('goal_id', '')
                if goal_id:
                    # Find the goal with this ID
                    for i, goal in enumerate(goals):
                        if goal.get('id', '') == goal_id:
                            # Update task count
                            goals[i]['task_count'] = goals[i].get('task_count', 0) + 1

                            # Update completed count
                            if task.get('completed', False):
                                goals[i]['completed_count'] = goals[i].get('completed_count', 0) + 1

                            # Add to total progress
                            goals[i]['total_progress'] = goals[i].get('total_progress', 0) + task.get('progress', 0)
                            break
                        
            # Calculate average progress for each goal
            for i, goal in enumerate(goals):
                task_count = goals[i].get('task_count', 0)
                if task_count > 0:
                    avg_progress = goals[i].get('total_progress', 0) / task_count
                    goals[i]['progress'] = round(avg_progress)
                else:
                    goals[i]['progress'] = 0

            # Save updated goals
            data["goals"] = goals
            with open(data_file, 'w') as f:
                json.dump(data, f, indent=2)

            # Update our local goals data
            self.goals = goals

            # Update the UI
            self.update_goals_list()

        except Exception as e:
            print(f"Error refreshing goal statistics: {str(e)}")

class GoalDialog(ctk.CTkToplevel):
    def __init__(self, parent, existing_goal=None):
        super().__init__(parent)
        self.parent = parent
        self.goal_data = None
        self.existing_goal = existing_goal
        
        title_text = "Edit Goal" if existing_goal else "Add Goal"
        self.title(title_text)
        self.geometry("500x675")
        self.resizable(False, False)
        
        # Center dialog on parent
        self.update_idletasks()
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        dialog_width = 500
        dialog_height = 675
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        
        # Create form fields
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Goal title
        self.title_label = ctk.CTkLabel(self.main_frame, text="Goal Title:")
        self.title_label.pack(anchor='w', pady=(0, 5))
        
        self.title_entry = ctk.CTkEntry(self.main_frame, width=460)
        self.title_entry.pack(fill='x', pady=(0, 10))
        
        # Color selection
        self.color_label = ctk.CTkLabel(self.main_frame, text="Goal Color:")
        self.color_label.pack(anchor='w', pady=(0, 5))
        
        self.color_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.color_frame.pack(fill='x', pady=(0, 10))
        
        self.default_colors = [
            # Blues
            "#03045E", "#023E8A", "#0077B6", "#0096C7", "#1f6aa5", "#00B4D8", "#48CAE4", "#90E0EF", "#ADE8F4", "#CAF0F8",
            # Greens
            "#036666", "#14746F", "#248277", "#358F80", "#469D89", "#56AB91", "#67B99A", "#78C6A3", "#88D4AB", "#99E2B4",
            # Yellows/Oranges
            "#a67700", "#d39e00", "#EE9B00", "#F9B122", "#ffc107", "#ffdb72", "#fd7e14", "#ff9248", "#ffb074", "#ffe0cb",
            # Reds/Pinks
            "#7a0000", "#bd2130", "#dc3545", "#e83e8c", "#ff6ba9", "#FC93BF", "#ffafd0", "#FAC1D9", "#ffd0e6", "#FADBE9",
            # Purples/Violets
            "#341b6b", "#5a37a0", "#6f42c1", "#8e44ad", "#9D54BC", "#B37BA4", "#a98eda", "#c6b1f0", "#d4a6cc", "#f9ecfa",
            # Neutral/Earth tones
            "#3C2B24", "#5E503F", "#A47E3B", "#83764F", "#B6AD90", "#C7B7A3", "#D4C7B0", "#E6CCBE", "#E0E2DB", "#FAF3DD",
        ]
        
        self.color_var = tk.StringVar(value=self.default_colors[0])
        if existing_goal and 'color' in existing_goal:
            self.color_var.set(existing_goal['color'])
        
        # Create color option buttons
        self.color_buttons = []
        for i, color in enumerate(self.default_colors):
            color_btn = ctk.CTkButton(
                self.color_frame,
                text="",
                width=30,
                height=30,
                fg_color=color,
                hover_color=color,
                command=lambda c=color: self.select_color(c)
            )
            # Position 5 buttons per row
            row = i // 10
            col = i % 10
            color_btn.grid(row=row, column=col, padx=5, pady=5)
            self.color_buttons.append(color_btn)
        
        # Current color selection indicator
        self.color_indicator_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.color_indicator_frame.pack(fill='x', pady=(0, 10))
        
        self.selected_color_label = ctk.CTkLabel(self.color_indicator_frame, text="Selected Color:")
        self.selected_color_label.pack(side='left', padx=(0, 10))
        
        self.color_indicator = ctk.CTkFrame(
            self.color_indicator_frame,
            width=30,
            height=30,
            fg_color=self.color_var.get()
        )
        self.color_indicator.pack(side='left')
        
        # Description
        self.desc_label = ctk.CTkLabel(self.main_frame, text="Description:")
        self.desc_label.pack(anchor='w', pady=(0, 5))
        
        self.desc_text = ctk.CTkTextbox(self.main_frame, height=150)
        self.desc_text.pack(fill='x', pady=(0, 10))
        
        # Buttons
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(fill='x', pady=(10, 0))
        
        self.cancel_btn = ctk.CTkButton(
            self.button_frame,
            text="Cancel",
            command=self.destroy,
            fg_color=COLOR_SCHEME['inactive'],
            width=100
        )
        self.cancel_btn.pack(side='right', padx=(10, 0))
        
        self.save_btn = ctk.CTkButton(
            self.button_frame,
            text="Save Goal",
            command=self.save_goal,
            width=100
        )
        self.save_btn.pack(side='right')
        
        # Populate fields if editing an existing goal
        if existing_goal:
            self.populate_fields(existing_goal)
            
        # Set focus on title entry
        self.title_entry.focus_set()
    
    def select_color(self, color):
        """Update selected color"""
        self.color_var.set(color)
        self.color_indicator.configure(fg_color=color)
    
    def populate_fields(self, goal):
        """Populate form fields with goal data"""
        self.title_entry.insert(0, goal.get('title', ''))
        
        if 'color' in goal:
            self.select_color(goal['color'])
        
        if 'description' in goal:
            self.desc_text.insert('1.0', goal['description'])
    
    def save_goal(self):
        """Save goal data and close dialog"""
        # Validate fields
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Please enter a goal title")
            return
        
        color = self.color_var.get()
        description = self.desc_text.get('1.0', 'end-1c')
        
        # Create goal data
        self.goal_data = {
            'id': self.existing_goal.get('id', str(int(time.time()))) if self.existing_goal else str(int(time.time())),
            'title': title,
            'color': color,
            'description': description,
            'progress': self.existing_goal.get('progress', 0) if self.existing_goal else 0,
            'task_count': self.existing_goal.get('task_count', 0) if self.existing_goal else 0,
            'completed_count': self.existing_goal.get('completed_count', 0) if self.existing_goal else 0,
            'created_date': self.existing_goal.get('created_date', datetime.now().strftime("%Y-%m-%d")) if self.existing_goal else datetime.now().strftime("%Y-%m-%d"),
            'last_modified': datetime.now().strftime("%Y-%m-%d")
        }
        
        # Close dialog
        self.destroy()

class ColorPickerDialog(ctk.CTkToplevel):
    def __init__(self, parent, goal):
        super().__init__(parent)
        self.parent = parent
        self.goal = goal
        self.selected_color = None
        
        self.title(f"Choose Color for: {goal.get('title', 'Goal')}")
        self.geometry("550x500")
        self.resizable(False, False)
        
        # Center dialog on parent
        self.update_idletasks()
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        dialog_width = 550
        dialog_height = 500
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Select a color for this goal",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.title_label.pack(pady=(0, 20))
        
        # Color grid
        self.color_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.color_frame.pack(fill='x', pady=(0, 20))
                 
        self.colors = [
            # Blues
            "#03045E", "#023E8A", "#0077B6", "#0096C7", "#1f6aa5", "#00B4D8", "#48CAE4", "#90E0EF", "#ADE8F4", "#CAF0F8",
            # Greens
            "#036666", "#14746F", "#248277", "#358F80", "#469D89", "#56AB91", "#67B99A", "#78C6A3", "#88D4AB", "#99E2B4",
            # Yellows/Oranges
            "#a67700", "#d39e00", "#EE9B00", "#F9B122", "#ffc107", "#ffdb72", "#fd7e14", "#ff9248", "#ffb074", "#ffe0cb",
            # Reds/Pinks
            "#7a0000", "#bd2130", "#dc3545", "#e83e8c", "#ff6ba9", "#FC93BF", "#ffafd0", "#FAC1D9", "#ffd0e6", "#FADBE9",
            # Purples/Violets
            "#341b6b", "#5a37a0", "#6f42c1", "#8e44ad", "#9D54BC", "#B37BA4", "#a98eda", "#c6b1f0", "#d4a6cc", "#f9ecfa",
            # Neutral/Earth tones
            "#3C2B24", "#5E503F", "#A47E3B", "#83764F", "#B6AD90", "#C7B7A3", "#D4C7B0", "#E6CCBE", "#E0E2DB", "#FAF3DD",
        ]
        
        # Create color buttons in a grid
        self.color_buttons = []
        for i, color in enumerate(self.colors):
            # Position 10 buttons per row
            row = i // 10
            col = i % 10
            
            color_btn = ctk.CTkButton(
                self.color_frame,
                text="",
                width=40,
                height=40,
                fg_color=color,
                hover_color=color,
                command=lambda c=color: self.select_color(c)
            )
            color_btn.grid(row=row, column=col, padx=5, pady=5)
            self.color_buttons.append(color_btn)
        
        # Current selection
        self.current_color_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.current_color_frame.pack(fill='x', pady=(0, 20))
        
        self.current_color_label = ctk.CTkLabel(
            self.current_color_frame,
            text="Current color:"
        )
        self.current_color_label.pack(side='left', padx=(0, 10))
        
        current_color = goal.get('color', "#1f6aa5")
        self.color_indicator = ctk.CTkFrame(
            self.current_color_frame,
            width=40,
            height=40,
            fg_color=current_color
        )
        self.color_indicator.pack(side='left')
        
        # Buttons
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(fill='x', pady=(10, 0))
        
        self.cancel_btn = ctk.CTkButton(
            self.button_frame,
            text="Cancel",
            command=self.destroy,
            fg_color=COLOR_SCHEME['inactive'],
            width=100
        )
        self.cancel_btn.pack(side='right', padx=(10, 0))
        
        self.save_btn = ctk.CTkButton(
            self.button_frame,
            text="Apply Color",
            command=self.apply_color,
            width=100
        )
        self.save_btn.pack(side='right')
        
        # Set initial selected color to current goal color
        self.selected_color = current_color
    
    def select_color(self, color):
        """Update selected color"""
        self.selected_color = color
        self.color_indicator.configure(fg_color=color)
    
    def apply_color(self):
        """Apply selected color and close dialog"""
        # Close dialog
        self.destroy()

class GanttChartFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        
        # Task data
        self.tasks = []
        self.selected_task = None
        
        # Zoom factor
        # Set zoom factor from app if available, otherwise use default
        if hasattr(self.app, 'gantt_zoom_factor'):
            self.zoom_factor = self.app.gantt_zoom_factor
        else:
            self.zoom_factor = 1.0
            # Initialize the zoom factor in the app instance
            self.app.gantt_zoom_factor = self.zoom_factor
            
        self.min_zoom = 0.1
        self.max_zoom = 3.0
        
        # Setup UI
        self.setup_ui()

        # Set view mode from app if available
        if hasattr(self.app, 'gantt_view_mode'):
            self.view_var.set(self.app.gantt_view_mode)
        else:
            # Initialize it in the app instance (default is "Month" from setup_ui)
            self.app.gantt_view_mode = self.view_var.get()
        
        # Load data if student is selected
        if self.app.current_student and self.app.current_student != "Add a student...":
            self.load_student_data()

    def setup_ui(self):
        # Top control panel
        self.control_panel = ctk.CTkFrame(self)
        self.control_panel.pack(fill='x', padx=20, pady=10)

        # Date range controls
        self.date_frame = ctk.CTkFrame(self.control_panel, fg_color="transparent")
        self.date_frame.pack(side='left', padx=10)

        self.start_date_label = ctk.CTkLabel(self.date_frame, text="Start Date:")
        self.start_date_label.grid(row=0, column=0, padx=5, pady=5)

        self.start_date_entry = ctk.CTkEntry(self.date_frame, width=100)
        self.start_date_entry.grid(row=0, column=1, padx=5, pady=5)
        
        today = datetime.now()
        if hasattr(self.app, 'gantt_start_date') and self.app.gantt_start_date:
            self.start_date_entry.insert(0, self.app.gantt_start_date)
        else:
            # Default to a month ago if no saved date
            month_ago = today - timedelta(days=30)
            self.start_date_entry.insert(0, month_ago.strftime("%Y-%m-%d"))

        self.end_date_label = ctk.CTkLabel(self.date_frame, text="End Date:")
        self.end_date_label.grid(row=0, column=2, padx=5, pady=5)

        self.end_date_entry = ctk.CTkEntry(self.date_frame, width=100)
        self.end_date_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Check if we have stored end date in app instance
        if hasattr(self.app, 'gantt_end_date') and self.app.gantt_end_date:
            self.end_date_entry.insert(0, self.app.gantt_end_date)
        else:
            # Default to two months ahead if no saved date
            month_ahead = today + timedelta(days=60)
            self.end_date_entry.insert(0, month_ahead.strftime("%Y-%m-%d"))

        self.update_btn = ctk.CTkButton(
            self.date_frame,
            text="Update",
            command=self.update_chart,
            width=80
        )
        self.update_btn.grid(row=0, column=4, padx=10, pady=5)

        # Assignee filter
        self.assignee_frame = ctk.CTkFrame(self.control_panel, fg_color="transparent")
        self.assignee_frame.pack(side='left', padx=10)

        self.assignee_label = ctk.CTkLabel(self.assignee_frame, text="Assignee:")
        self.assignee_label.pack(side='left', padx=5)

        self.assignee_var = tk.StringVar(value="All")
        self.assignee_menu = ctk.CTkOptionMenu(
            self.assignee_frame,
            values=["All", "Student", "Teacher"],
            variable=self.assignee_var,
            command=self.on_assignee_change,
            width=100
        )
        self.assignee_menu.pack(side='left', padx=5)

        # Goal filter
        self.goal_frame = ctk.CTkFrame(self.control_panel, fg_color="transparent")
        self.goal_frame.pack(side='left', padx=10)

        self.goal_label = ctk.CTkLabel(self.goal_frame, text="Goal:")
        self.goal_label.pack(side='left', padx=5)

        self.goal_var = tk.StringVar(value="All")
        self.goal_menu = ctk.CTkOptionMenu(
            self.goal_frame,
            values=["All"],  # Will be populated when tasks are loaded
            variable=self.goal_var,
            command=self.on_goal_change,
            width=150
        )
        self.goal_menu.pack(side='left', padx=5)

        self.goals = []
        
        # Zoom controls
        self.zoom_frame = ctk.CTkFrame(self.control_panel, fg_color="transparent")
        self.zoom_frame.pack(side='left', padx=20)
        
        self.zoom_label = ctk.CTkLabel(self.zoom_frame, text="Zoom:")
        self.zoom_label.pack(side='left', padx=5)
        
        self.zoom_out_btn = ctk.CTkButton(
            self.zoom_frame,
            text="-",
            command=self.zoom_out,
            width=30,
            height=30
        )
        self.zoom_out_btn.pack(side='left', padx=2)
        
        self.zoom_reset_btn = ctk.CTkButton(
            self.zoom_frame,
            text="Reset",
            command=self.zoom_reset,
            width=60,
            height=30
        )
        self.zoom_reset_btn.pack(side='left', padx=2)

        zoom_percentage = int(self.zoom_factor * 100)
        self.zoom_indicator = ctk.CTkLabel(
            self.zoom_frame,
            text=f"{zoom_percentage}%",
            width=50
        )
        
        self.zoom_in_btn = ctk.CTkButton(
            self.zoom_frame,
            text="+",
            command=self.zoom_in,
            width=30,
            height=30
        )
        self.zoom_in_btn.pack(side='left', padx=2)
        
        # Zoom indicator
        self.zoom_indicator = ctk.CTkLabel(
            self.zoom_frame,
            text="100%",
            width=50
        )
        self.zoom_indicator.pack(side='left', padx=5)

        # View options
        self.view_frame = ctk.CTkFrame(self.control_panel, fg_color="transparent")
        self.view_frame.pack(side='right', padx=10)

        self.view_label = ctk.CTkLabel(self.view_frame, text="View:")
        self.view_label.pack(side='left', padx=5)

        self.view_var = tk.StringVar(value="Month")
        self.view_menu = ctk.CTkOptionMenu(
            self.view_frame,
            values=["Week", "Month", "Quarter", "Year"],
            variable=self.view_var,
            command=self.change_view,
            width=100
        )
        self.view_menu.pack(side='left', padx=5)
        
        # Gantt chart container
        self.chart_container = ctk.CTkFrame(self, fg_color=COLOR_SCHEME['content_bg'])
        self.chart_container.pack(fill='both', expand=True, padx=20, pady=(0, 10))
        
        # Create header (days or weeks)
        self.header_canvas = tk.Canvas(
            self.chart_container,
            bg=COLOR_SCHEME['content_bg'],
            highlightthickness=0,
            height=50
        )
        self.header_canvas.pack(fill='x')
        
        # Create Gantt chart with scrollbar
        self.chart_frame = ctk.CTkFrame(self.chart_container, fg_color="transparent")
        self.chart_frame.pack(fill='both', expand=True)
        
        self.vertical_scroll = ctk.CTkScrollbar(self.chart_frame, orientation="vertical")
        self.vertical_scroll.pack(side='right', fill='y')
        
        self.horizontal_scroll = ctk.CTkScrollbar(self.chart_frame, orientation="horizontal")
        self.horizontal_scroll.pack(side='bottom', fill='x')
        
        self.gantt_canvas = tk.Canvas(
            self.chart_frame,
            bg=COLOR_SCHEME['content_inside_bg'],
            highlightthickness=0,
            yscrollcommand=self.vertical_scroll.set,
            xscrollcommand=self.horizontal_scroll.set
        )
        self.gantt_canvas.pack(fill='both', expand=True)

        self.header_canvas.configure(xscrollcommand=self.horizontal_scroll.set)
        
        self.vertical_scroll.configure(command=self.gantt_canvas.yview)
        self.horizontal_scroll.configure(command=self.sync_scroll)
        
        # Bind canvas events
        self.gantt_canvas.bind("<Button-1>", self.on_canvas_click)
        self.gantt_canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Task details panel
        self.task_panel = ctk.CTkFrame(self)
        self.task_panel.pack(fill='x', padx=20, pady=(0, 20))
        
        # Task details
        self.details_frame = ctk.CTkFrame(self.task_panel, fg_color="transparent")
        self.details_frame.pack(fill='x', padx=10, pady=10)
        
        self.task_label = ctk.CTkLabel(
            self.details_frame,
            text="Select a task to view details",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.task_label.grid(row=0, column=0, columnspan=4, sticky='w', padx=5, pady=5)
        
        self.date_info = ctk.CTkLabel(
            self.details_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.date_info.grid(row=1, column=0, columnspan=4, sticky='w', padx=5, pady=2)
        
        self.assignee_label = ctk.CTkLabel(
            self.details_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.assignee_label.grid(row=2, column=0, sticky='w', padx=5, pady=2)
        
        self.status_label = ctk.CTkLabel(
            self.details_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=2, column=1, sticky='w', padx=5, pady=2)
        
        # Action buttons
        self.action_frame = ctk.CTkFrame(self.task_panel, fg_color="transparent")
        self.action_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        self.edit_btn = ctk.CTkButton(
            self.action_frame,
            text="Edit Task",
            command=self.edit_task,
            width=100,
            state="disabled"
        )
        self.edit_btn.pack(side='left', padx=5)
        
        self.complete_btn = ctk.CTkButton(
            self.action_frame,
            text="Mark Complete",
            command=self.mark_complete,
            width=120,
            state="disabled"
        )
        self.complete_btn.pack(side='left', padx=5)
        
        self.add_note_btn = ctk.CTkButton(
            self.action_frame,
            text="Add Note",
            command=self.add_note,
            width=100,
            state="disabled"
        )
        self.add_note_btn.pack(side='left', padx=5)

        self.not_complete_btn = ctk.CTkButton(
            self.action_frame,
            text="Mark Not Complete",
            command=self.mark_not_complete,
            width=140,
            state="disabled"
        )
        self.not_complete_btn.pack(side='left', padx=5)
        
        self.add_task_btn = ctk.CTkButton(
            self.action_frame,
            text="Add New Task",
            command=self.add_task,
            width=120
        )
        self.add_task_btn.pack(side='right', padx=5)
        
        # Initialize empty chart
        self.update_chart()
        
    def zoom_in(self):
        """Increase zoom level by 20%"""
        if self.zoom_factor < self.max_zoom:
            self.zoom_factor += 0.2
            self.zoom_factor = min(self.zoom_factor, self.max_zoom)  # Ensure we don't exceed max
            self.update_zoom_indicator()
            self.app.gantt_zoom_factor = self.zoom_factor
            if hasattr(self.app, 'config_manager'):
                self.app.config_manager.set_gantt_config(zoom_factor=self.app.gantt_zoom_factor)
            self.update_chart()
    
    def zoom_out(self):
        """Decrease zoom level by 20%"""
        if self.zoom_factor > self.min_zoom:
            self.zoom_factor -= 0.2
            self.zoom_factor = max(self.zoom_factor, self.min_zoom)  # Ensure we don't go below min
            self.update_zoom_indicator()
            self.app.gantt_zoom_factor = self.zoom_factor
            if hasattr(self.app, 'config_manager'):
                self.app.config_manager.set_gantt_config(zoom_factor=self.app.gantt_zoom_factor)
            self.update_chart()
    
    def zoom_reset(self):
        """Reset zoom to 100%"""
        self.zoom_factor = 1.0
        self.update_zoom_indicator()
        self.app.gantt_zoom_factor = self.zoom_factor
        if hasattr(self.app, 'config_manager'):
            self.app.config_manager.set_gantt_config(zoom_factor=self.app.gantt_zoom_factor)
        self.update_chart()
    
    def update_zoom_indicator(self):
        """Update the zoom level indicator"""
        zoom_percentage = int(self.zoom_factor * 100)
        self.zoom_indicator.configure(text=f"{zoom_percentage}%")
        self.app.gantt_zoom_factor = self.zoom_factor

    def update_chart(self):
        """Update Gantt chart display"""
        # Reset task rectangles tracking
        self.task_rectangles = []

        # Clear canvas
        self.gantt_canvas.delete("all")
        self.header_canvas.delete("all")

        if not self.app.current_student or self.app.current_student == "Add a student...":
            # Show message to select a student
            self.gantt_canvas.create_text(
                self.gantt_canvas.winfo_width() // 2,
                self.gantt_canvas.winfo_height() // 2,
                text="Please select a student to view their progress",
                fill=COLOR_SCHEME['text'],
                font=("Arial", 14)
            )
            return

        # Parse date range
        try:
            start_date = datetime.strptime(self.start_date_entry.get(), "%Y-%m-%d")
            end_date = datetime.strptime(self.end_date_entry.get(), "%Y-%m-%d")
            self.app.gantt_start_date = self.start_date_entry.get()
            self.app.gantt_end_date = self.end_date_entry.get()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
            return

        # Ensure start_date is before end_date
        if start_date >= end_date:
            messagebox.showerror("Error", "Start date must be before end date")
            return

        # Calculate chart dimensions
        days = (end_date - start_date).days + 1

        # Apply zoom factor to day width
        base_day_width = 30  # Base width in pixels per day
        day_width = base_day_width * self.zoom_factor
        
        # Set chart width based on zoomed day width
        chart_width = max(self.gantt_canvas.winfo_width(), days * day_width)

        # Filter tasks if needed
        filtered_tasks = self.tasks.copy()  # Make a copy to avoid modifying the original

        # Parse date range
        try:
            start_date = datetime.strptime(self.start_date_entry.get(), "%Y-%m-%d")
            end_date = datetime.strptime(self.end_date_entry.get(), "%Y-%m-%d")
            self.app.gantt_start_date = self.start_date_entry.get()
            self.app.gantt_end_date = self.end_date_entry.get()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
            return
        
        if hasattr(self.app, 'config_manager'):
            self.app.config_manager.set_gantt_config(
                start_date=self.app.gantt_start_date,
                end_date=self.app.gantt_end_date
            )

        # Apply assignee filter
        assignee_filter = self.assignee_var.get()
        if assignee_filter != "All":
            filtered_tasks = [t for t in filtered_tasks if t.get('assignee', '') == assignee_filter]

        # Apply goal filter if applicable
        goal_filter = self.goal_var.get()
        if goal_filter != "All":
            # Find all tasks associated with this goal
            goal_id = None
            for goal in self.goals:
                if goal.get('title', '') == goal_filter:
                    goal_id = goal.get('id', '')
                    break

            if goal_id:
                filtered_tasks = [t for t in filtered_tasks if t.get('goal_id', '') == goal_id]

        # Calculate chart height based on filtered tasks
        task_count = max(1, len(filtered_tasks))  # Ensure at least one row
        chart_height = max(self.gantt_canvas.winfo_height(), task_count * 40 + 50)

        # Configure scroll regions for both canvases
        self.gantt_canvas.configure(scrollregion=(0, 0, chart_width, chart_height))
        self.header_canvas.configure(scrollregion=(0, 0, chart_width, 50))

        # Draw time scale at the top (header) with day_width affected by zoom
        self.draw_time_scale(start_date, end_date, chart_width, chart_height, day_width)

        # Draw tasks (using filtered tasks and zoomed day width)
        self.draw_tasks(start_date, end_date, chart_width, filtered_tasks, day_width)

        # Link horizontal scrolling of both canvases
        self.horizontal_scroll.configure(command=self.sync_scroll)

    def draw_time_scale(self, start_date, end_date, chart_width, chart_height, day_width=30):
        """Draw time scale header with custom day width"""
        view_mode = self.view_var.get()
        days = (end_date - start_date).days + 1

        # Set header dimensions
        self.header_canvas.configure(width=chart_width)
        self.header_canvas.delete("all")  # Clear existing content

        # Configure intervals and formats based on view mode
        if view_mode == "Week":
            interval = 1  # Daily intervals
            day_format = "%d"  # Just the day number
            month_format = "%B %Y"  # Full month name with year
        elif view_mode == "Month":
            interval = 7  # Weekly intervals
            day_format = "%d"  # Day number
            month_format = "%B %Y"  # Full month name with year
        elif view_mode == "Quarter":
            interval = 14  # Bi-weekly intervals
            day_format = "%d"  # Day number
            month_format = "%B %Y"  # Full month name with year
        else:  # Year
            interval = 30  # Monthly intervals
            month_format = "%B %Y"  # Full month name with year

        # For all views, draw month headers first
        current_month = start_date.month
        current_year = start_date.year
        month_start_x = 0
        month_label = start_date.strftime(month_format)

        for i in range(days):
            date = start_date + timedelta(days=i)
            x = i * day_width

            # If month changes or last day, draw the month label
            if date.month != current_month or date.year != current_year or i == days - 1:
                # Calculate month width
                month_width = x - month_start_x
                if i == days - 1:  # Include the last day
                    month_width += day_width

                # Draw month label centered over its days
                self.header_canvas.create_text(
                    month_start_x + month_width/2,
                    15,
                    text=month_label,
                    fill=COLOR_SCHEME['text'],
                    font=("Arial", 10, "bold")
                )

                # Draw a subtle separator line
                self.header_canvas.create_line(
                    x, 0, x, 30,
                    fill="#555555", dash=(2, 2)
                )

                # Update for next month
                current_month = date.month
                current_year = date.year
                month_start_x = x
                month_label = date.strftime(month_format)

        # Draw day/week markings
        for i in range(0, days, interval):
            x = i * day_width
            current_date = start_date + timedelta(days=i)

            # Draw vertical line on chart
            self.gantt_canvas.create_line(x, 0, x, chart_height, fill="#555555", dash=(4, 4))

            # Draw date label in header based on view mode
            if view_mode == "Week":
                # Place day numbers below month names for Week view
                date_str = current_date.strftime(day_format)
                self.header_canvas.create_text(
                    x + day_width/2, 
                    35, 
                    text=date_str, 
                    fill=COLOR_SCHEME['text'],
                    font=("Arial", 9)
                )
            elif view_mode in ["Month", "Quarter"]:
                # For Month and Quarter views, show day with month abbreviation
                date_str = current_date.strftime("%d %b")
                self.header_canvas.create_text(
                    x + day_width/2, 
                    35, 
                    text=date_str, 
                    fill=COLOR_SCHEME['text'],
                    font=("Arial", 9)
                )
            else:  # Year view
                # For Year view, just show month abbreviations
                if current_date.day == 1 or i == 0:  # Only on first day of month
                    date_str = current_date.strftime("%b")
                    self.header_canvas.create_text(
                        x + day_width/2, 
                        35, 
                        text=date_str, 
                        fill=COLOR_SCHEME['text'],
                        font=("Arial", 9)
                    )

        # Draw today's date line if it falls within the range
        today = datetime.now().date()
        if start_date.date() <= today <= end_date.date():
            days_from_start = (today - start_date.date()).days
            today_x = days_from_start * day_width

            # Draw vertical line on chart for today
            self.gantt_canvas.create_line(
                today_x, 0, today_x, chart_height, 
                fill="#ff6b6b", width=2, dash=(2, 2)
            )

            # Draw today indicator in header
            self.header_canvas.create_line(
                today_x, 0, today_x, 50, 
                fill="#ff6b6b", width=2, dash=(2, 2)
            )

            # Add "Today" label
            self.header_canvas.create_text(
                today_x + 10, 45, 
                text="Today", 
                fill="#ff6b6b", 
                anchor='w',
                font=("Arial", 9, "bold")
            )
    
    def draw_tasks(self, start_date, end_date, chart_width, filtered_tasks=None, day_width=30):
        """Draw tasks on the Gantt chart with custom day width"""
        # Use filtered tasks if provided, otherwise use all tasks
        tasks_to_draw = filtered_tasks if filtered_tasks is not None else self.tasks

        if not tasks_to_draw:
            # Show message if no tasks
            self.gantt_canvas.create_text(
                chart_width // 2,
                50,
                text="No tasks found. Add tasks using the 'Add New Task' button.",
                fill=COLOR_SCHEME['text'],
                font=("Arial", 12)
            )
            return

        # Calculate dimensions
        days = (end_date - start_date).days + 1
        row_height = 40
        task_height = 30

        chart_height = max(self.gantt_canvas.winfo_height(), len(tasks_to_draw) * row_height + 50)

        # Track task rectangles for click events
        self.task_rectangles = []

        # Sort tasks by start date
        sorted_tasks = sorted(tasks_to_draw, key=lambda t: datetime.strptime(t['start_date'], "%Y-%m-%d"))

        # Draw each task
        for idx, task in enumerate(sorted_tasks):
            try:
                # Parse dates
                task_start = datetime.strptime(task['start_date'], "%Y-%m-%d")
                task_end = datetime.strptime(task['end_date'], "%Y-%m-%d")

                # Skip if task is completely outside view range
                if task_end < start_date or task_start > end_date:
                    continue
                
                # Adjust dates to fit within view
                if task_start < start_date:
                    task_start = start_date
                if task_end > end_date:
                    task_end = end_date

                # Calculate position
                days_from_start = (task_start - start_date).days
                task_days = (task_end - task_start).days + 1

                x1 = days_from_start * day_width
                y1 = idx * row_height + 10
                x2 = x1 + (task_days * day_width)
                y2 = y1 + task_height

                # Determine if milestone
                is_milestone = task.get('is_milestone', False)
                is_completed = task.get('completed', False)
                is_late = task_end < datetime.now() and not is_completed

                # Determine color based on status and goal
                if task.get('goal_color'):
                    base_color = task.get('goal_color')

                    # Adjust color based on status
                    if is_completed:
                        color = self.adjust_color_opacity(base_color, 1.2)  # Use full color for completed tasks
                    elif is_late:
                        color = COLOR_SCHEME['task_late']  # Red for overdue tasks regardless of goal
                    elif is_milestone:
                        color = COLOR_SCHEME['milestone']  # Yellow for milestones
                    else:
                        # For in-progress tasks, adjust the color based on progress
                        progress = task.get('progress', 0)
                        if progress < 25:
                            # Very light version of the color for low progress
                            color = self.adjust_color_opacity(base_color, 0.3)
                        elif progress < 50:
                            # Slightly stronger but still light
                            color = self.adjust_color_opacity(base_color, 0.5)
                        elif progress < 75:
                            # Medium strength
                            color = self.adjust_color_opacity(base_color, 0.7)
                        else:
                            # Almost full strength for high progress
                            color = self.adjust_color_opacity(base_color, 0.9)
                else:
                    # Fallback to default colors if no goal color is specified
                    if is_milestone:
                        if is_completed:
                            color = COLOR_SCHEME['task_completed']  # Green for completed milestones
                        elif is_late:
                            color = COLOR_SCHEME['task_late']  # Red for late milestones
                        else:
                            color = COLOR_SCHEME['milestone']  # Yellow for normal milestones
                    elif is_completed:
                        color = COLOR_SCHEME['task_completed']  # Green for completed tasks
                    elif is_late:
                        color = COLOR_SCHEME['task_late']  # Red for overdue tasks
                    else:
                        color = COLOR_SCHEME['task_normal']  # Blue for normal tasks

                # Draw task shape
                if is_milestone:
                    # Draw diamond for milestone
                    mid_x = (x1 + x2) / 2
                    mid_y = (y1 + y2) / 2
                    points = [mid_x, y1, x2, mid_y, mid_x, y2, x1, mid_y]
                    rect_id = self.gantt_canvas.create_polygon(points, fill=color, outline=color, tags=("task",))
                else:
                    # Draw rectangle for normal task
                    rect_id = self.gantt_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color, tags=("task",))

                    # Draw completion percentage if provided and not complete
                    if 'progress' in task and not is_completed:
                        progress = task.get('progress', 0)
                        progress_width = (task_days * day_width) * (progress / 100)

                        if progress_width > 2:  # Only draw if there's enough space
                            # Use a darker version of the task color for progress bar
                            progress_color = "#81c784"  # Default green progress

                            if task.get('goal_color'):
                                base_color = task.get('goal_color')
                                progress_color = self.adjust_color_opacity(base_color, 1.2)  # Slightly darker

                            self.gantt_canvas.create_rectangle(
                                x1, y1, x1 + progress_width, y2,
                                fill=progress_color, outline=progress_color, tags=("progress",)
                            )

                # Store rectangle id and task data for click events
                self.task_rectangles.append((rect_id, task))

                # Draw task name
                text_x = x1 + 5
                if is_milestone:
                    text_x = mid_x + 20  # Adjust text position for milestone

                self.gantt_canvas.create_text(
                    text_x, 
                    y1 + (task_height // 2),
                    text=task['title'],
                    fill=COLOR_SCHEME['text'],
                    anchor='w',
                    tags=("task_text",)
                )

            except Exception as e:
                print(f"Error drawing task {task['title']}: {str(e)}")
                
    def on_goal_change(self, value):
            """Handle goal filter change in the GanttChartFrame

            This method is called when the user selects a different goal from the
            goal filter dropdown. It triggers the chart to update with the new
            goal filter applied.

            Args:
                value (str): The selected goal title
            """
            # Reset task rectangles to force complete refresh
            self.task_rectangles = []

            # Clear canvas
            self.gantt_canvas.delete("all")
            self.header_canvas.delete("all")

            # Update the chart with the new filter applied
            self.update_chart()

    def on_assignee_change(self, value):
        """Wrapper function to handle assignee filter change"""
        # The value parameter receives the selected dropdown option
        # but we don't need to use it directly since we're using the variable
        self.update_chart()

    def mark_not_complete(self):
        """Mark the selected task as not complete"""
        if not self.selected_task:
            return

        # Get the current user (teacher or student)
        current_user = "Teacher" if self.app.app_mode == "teacher" else "Student"

        # Update task completion status
        for i, task in enumerate(self.tasks):
            if task.get('id', '') == self.selected_task.get('id', ''):
                # Store current progress before changing
                old_progress = self.tasks[i]['progress']

                # Update task data
                self.tasks[i]['completed'] = False
                self.tasks[i]['last_modified'] = datetime.now().strftime("%Y-%m-%d")
                self.tasks[i]['last_modified_by'] = current_user

                # Add to progress history
                if 'progress_history' not in self.tasks[i]:
                    self.tasks[i]['progress_history'] = []

                # Only add entry if this changes progress from 100%
                if old_progress == 100:
                    # Keep same progress value but mark as not completed
                    self.tasks[i]['progress_history'].append({
                        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'progress': old_progress,
                        'previous_progress': old_progress,
                        'modified_by': current_user,
                        'action': 'Marked not complete'
                    })

                self.selected_task = self.tasks[i]
                break

            # Save data
            self.save_student_data()
            # Update goal statistics
            self.update_goal_statistics()
            # Update chart and details
            self.update_chart()
            self.update_task_details()

    def load_student_data(self):
        """Load student data from JSON file"""
        try:
            student_data = self.app.students.get(self.app.current_student, {})
            data_path = student_data.get("data_path", "")

            if not data_path:
                return

            data_file = os.path.join(data_path, "progress_data.json")
            if not os.path.exists(data_file):
                # Create default data file if it doesn't exist
                default_data = {
                    "tasks": [],
                    "notes": [],
                    "goals": []
                }
                with open(data_file, 'w') as f:
                    json.dump(default_data, f, indent=2)
                self.tasks = []
                self.goals = []
            else:
                with open(data_file, 'r') as f:
                    data = json.load(f)
                    self.tasks = data.get("tasks", [])
                    self.goals = data.get("goals", [])

                    # Initialize goals array if it doesn't exist in data
                    if "goals" not in data:
                        data["goals"] = []
                        with open(data_file, 'w') as f:
                            json.dump(data, f, indent=2)

                    # Ensure all tasks have the correct goal color
                    self.synchronize_task_colors()

            # Update goal filter dropdown options
            goal_options = ["All"]
            for goal in self.goals:
                if 'title' in goal and goal['title']:
                    goal_options.append(goal['title'])

            self.goal_var.set("All")  # Reset to "All" when loading new data
            self.goal_menu.configure(values=goal_options)

            # Reset task rectangles to force complete refresh
            self.task_rectangles = []

            # Update chart with loaded data
            self.update_chart()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load student data: {str(e)}")

    def synchronize_task_colors(self):
        """Ensure all tasks have the correct goal color based on their goal_id"""
        modified = False

        # Create a goal lookup for efficiency
        goal_colors = {}
        for goal in self.goals:
            goal_colors[goal.get('id', '')] = goal.get('color', '')

        # Update tasks with correct goal colors
        for i, task in enumerate(self.tasks):
            goal_id = task.get('goal_id', '')
            if goal_id and goal_id in goal_colors:
                # If goal color doesn't match or is missing, update it
                if task.get('goal_color', '') != goal_colors[goal_id]:
                    self.tasks[i]['goal_color'] = goal_colors[goal_id]
                    modified = True

        # If changes were made, save the updated tasks
        if modified:
            try:
                student_data = self.app.students.get(self.app.current_student, {})
                data_path = student_data.get("data_path", "")

                if data_path:
                    data_file = os.path.join(data_path, "progress_data.json")
                    if os.path.exists(data_file):
                        with open(data_file, 'r') as f:
                            data = json.load(f)

                        data["tasks"] = self.tasks

                        with open(data_file, 'w') as f:
                            json.dump(data, f, indent=2)
            except Exception as e:
                print(f"Error saving synchronized task colors: {str(e)}")

    def save_student_data(self):
        """Save student data to JSON file"""
        try:
            student_data = self.app.students.get(self.app.current_student, {})
            data_path = student_data.get("data_path", "")
            
            if not data_path:
                return
            
            data_file = os.path.join(data_path, "progress_data.json")
            
            # Load existing data to preserve notes
            if os.path.exists(data_file):
                with open(data_file, 'r') as f:
                    data = json.load(f)
            else:
                data = {"notes": []}
            
            # Update tasks
            data["tasks"] = self.tasks
            
            # Save updated data
            with open(data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save student data: {str(e)}")
    
    def sync_scroll(self, *args):
        """Synchronize scrolling between header and chart canvas"""
        # Update both canvases with the same horizontal scroll position
        self.gantt_canvas.xview(*args)
        self.header_canvas.xview(*args)

    def adjust_color_opacity(self, hex_color, opacity_factor):
            """Adjust color opacity by lightening or darkening it

            Args:
                hex_color (str): Hex color code (e.g. '#1f6aa5')
                opacity_factor (float): Factor to adjust opacity
                    - Values < 1: Lighten the color (blend with white)
                    - Values = 1: Keep the color as is
                    - Values > 1: Darken the color (blend with black)

            Returns:
                str: Adjusted hex color code
            """
            # Convert hex to RGB
            hex_color = hex_color.lstrip('#')

            # Handle potential issues with hex color format
            if len(hex_color) == 3:  # Convert 3-digit hex to 6-digit
                hex_color = ''.join([c+c for c in hex_color])

            try:
                r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            except ValueError:
                # Return original color if conversion fails
                return '#' + hex_color

            if opacity_factor < 1:
                # The min_opacity variable helps to prevent colors from becoming too light
                min_opacity = 0.5  
                effective_opacity = min_opacity + (opacity_factor * (1 - min_opacity))

                # Lighter color (blend with white) but maintain minimum darkness
                r = int(r + (255 - r) * (1 - effective_opacity))
                g = int(g + (255 - g) * (1 - effective_opacity))
                b = int(b + (255 - b) * (1 - effective_opacity))
            elif opacity_factor > 1:
                # Darker color (blend with black)
                factor = min(opacity_factor - 1, 1.0)  # Normalize to 0-1 range
                r = int(r * (1 - factor))
                g = int(g * (1 - factor))
                b = int(b * (1 - factor))

            # Ensure values are within valid range
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))

            # Convert back to hex
            return f'#{r:02x}{g:02x}{b:02x}'

    def on_canvas_click(self, event):
        """Handle click on canvas to select tasks"""
        # Reset selected task
        self.selected_task = None

        # Get the canvas scroll position
        canvas_x = self.gantt_canvas.canvasx(event.x)
        canvas_y = self.gantt_canvas.canvasy(event.y)

        # Find clicked task
        for rect_id, task in self.task_rectangles:
            if self.gantt_canvas.find_withtag(rect_id) and self.gantt_canvas.type(rect_id) == "rectangle":
                coords = self.gantt_canvas.coords(rect_id)
                if len(coords) >= 4:
                    x1, y1, x2, y2 = coords
                    if x1 <= canvas_x <= x2 and y1 <= canvas_y <= y2:
                        self.selected_task = task
                        break
            elif self.gantt_canvas.find_withtag(rect_id) and self.gantt_canvas.type(rect_id) == "polygon":
                # For milestone (polygon), check if click is near the center
                coords = self.gantt_canvas.coords(rect_id)
                if len(coords) >= 8:
                    # Calculate center of the diamond
                    center_x = (coords[0] + coords[4]) / 2
                    center_y = (coords[1] + coords[5]) / 2
                    # Check if click is within 15 pixels of center
                    if abs(canvas_x - center_x) <= 15 and abs(canvas_y - center_y) <= 15:
                        self.selected_task = task
                        break
                    
        # Update task details panel
        self.update_task_details()
    
    def update_task_details(self):
        """Update task details panel with selected task"""
        if self.selected_task:
            # Update task details
            self.task_label.configure(text=self.selected_task['title'])

            # Format dates
            start_date = datetime.strptime(self.selected_task['start_date'], "%Y-%m-%d").strftime("%d %b %Y")
            end_date = datetime.strptime(self.selected_task['end_date'], "%Y-%m-%d").strftime("%d %b %Y")

            # Calculate duration
            start = datetime.strptime(self.selected_task['start_date'], "%Y-%m-%d")
            end = datetime.strptime(self.selected_task['end_date'], "%Y-%m-%d")
            duration = (end - start).days + 1

            date_text = f"Start: {start_date} | End: {end_date} | Duration: {duration} days"
            if 'progress' in self.selected_task:
                date_text += f" | Progress: {self.selected_task['progress']}%"

            # Add completion date and who completed it if the task is completed
            if self.selected_task.get('completed', False) and self.selected_task.get('completion_date'):
                completion_date = datetime.strptime(self.selected_task['completion_date'], "%Y-%m-%d").strftime("%d %b %Y")
                completed_by = self.selected_task.get('completed_by', 'Unknown')
                date_text += f" | Completed: {completion_date} by {completed_by}"

            self.date_info.configure(text=date_text)

            # Assignee and status
            assignee = self.selected_task.get('assignee', 'Not assigned')
            self.assignee_label.configure(text=f"Assigned to: {assignee}")

            status = "Completed" if self.selected_task.get('completed', False) else "In Progress"
            if end < datetime.now() and not self.selected_task.get('completed', False):
                status = "Overdue"
            if self.selected_task.get('is_milestone', False):
                status = "Milestone"

            self.status_label.configure(text=f"Status: {status}")

            # Check if task is completed
            is_completed = self.selected_task.get('completed', False)

            # Enable/disable buttons based on completion status
            if is_completed:
                # If completed, disable Edit Task and Add Note buttons
                self.edit_btn.configure(state="disabled")
                self.add_note_btn.configure(state="disabled")
                self.complete_btn.configure(state="disabled", text="Completed")
                self.not_complete_btn.configure(state="normal")
            else:
                # If not completed, enable all buttons
                self.edit_btn.configure(state="normal")
                self.add_note_btn.configure(state="normal")
                self.complete_btn.configure(state="normal", text="Mark Complete")
                self.not_complete_btn.configure(state="disabled")

        else:
            # Reset task details
            self.task_label.configure(text="Select a task to view details")
            self.date_info.configure(text="")
            self.assignee_label.configure(text="")
            self.status_label.configure(text="")

            # Disable buttons
            self.edit_btn.configure(state="disabled")
            self.complete_btn.configure(state="disabled")
            self.not_complete_btn.configure(state="disabled")
            self.add_note_btn.configure(state="disabled")
    
    def on_canvas_configure(self, event):
        """Handle canvas resize"""
        # Redraw chart when canvas is resized
        self.update_chart()
    
    def change_view(self, view_mode):
        """Change the view mode and update chart"""
        self.app.gantt_view_mode = view_mode
        if hasattr(self.app, 'config_manager'):
            self.app.config_manager.set_gantt_config(view_mode=view_mode)
        self.update_chart()
    
    def add_task(self):
            """Open dialog to add a new task"""
            if not self.app.current_student or self.app.current_student == "Add a student...":
                messagebox.showinfo("Info", "Please select a student first")
                return

            dialog = TaskDialog(self, "Add Task")
            self.wait_window(dialog)

            if dialog.task_data:
                # Add new task
                self.tasks.append(dialog.task_data)
                # Save data
                self.save_student_data()
                # Update goal statistics
                self.update_goal_statistics()

                # Reset task rectangles list to force complete refresh
                self.task_rectangles = []

                # Clear canvas and update chart
                self.gantt_canvas.delete("all")
                self.header_canvas.delete("all")

                # Force a complete refresh of the chart
                self.update_chart()
    
    def edit_task(self):
        """Edit the selected task"""
        if not self.selected_task:
            return

        # In student mode, only allow editing tasks assigned to student
        if self.app.app_mode == "student" and self.selected_task.get('assignee', '') != "Student":
            messagebox.showinfo("Permission Denied", 
                             "You can only edit tasks assigned to you.")
            return
        
        dialog = TaskDialog(self, "Edit Task", self.selected_task)
        self.wait_window(dialog)
        
        if dialog.task_data:
            # Update task data
            for i, task in enumerate(self.tasks):
                if task.get('id', '') == self.selected_task.get('id', ''):
                    self.tasks[i] = dialog.task_data
                    break
            
            # Reset selected task
            self.selected_task = dialog.task_data
            
            # Save data
            self.save_student_data()
            # Update goal statistics
            self.update_goal_statistics()
            # Update chart and details
            self.update_chart()
            self.update_task_details()
    
    def mark_complete(self):
        """Mark the selected task as complete"""
        if not self.selected_task:
            return

        # Get the current user (teacher or student)
        current_user = "Teacher" if self.app.app_mode == "teacher" else "Student"

        # Update task completion status
        for i, task in enumerate(self.tasks):
            if task.get('id', '') == self.selected_task.get('id', ''):
                self.tasks[i]['completed'] = True
                self.tasks[i]['progress'] = 100
                self.tasks[i]['completion_date'] = datetime.now().strftime("%Y-%m-%d")
                self.tasks[i]['completed_by'] = current_user
                self.tasks[i]['last_modified'] = datetime.now().strftime("%Y-%m-%d")
                self.tasks[i]['last_modified_by'] = current_user

                # Add progress history entry
                if 'progress_history' not in self.tasks[i]:
                    self.tasks[i]['progress_history'] = []

                # Only add to history if progress changed
                old_progress = self.selected_task.get('progress', 0)
                if old_progress != 100:
                    self.tasks[i]['progress_history'].append({
                        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'progress': 100,
                        'previous_progress': old_progress,
                        'modified_by': current_user
                    })

                self.selected_task = self.tasks[i]
                break
            
        # Save data
        self.save_student_data()
        # Update goal statistics
        self.update_goal_statistics()
        # Update chart and details
        self.update_chart()
        self.update_task_details()
    
    def add_note(self):
        """Add a note to the selected task"""
        if not self.selected_task:
            return
        
        dialog = NoteDialog(self, self.selected_task)
        self.wait_window(dialog)
        
        if dialog.note_data:
            # Get student data file path
            student_data = self.app.students.get(self.app.current_student, {})
            data_path = student_data.get("data_path", "")
            
            if not data_path:
                return
            
            data_file = os.path.join(data_path, "progress_data.json")
            
            try:
                # Load existing data
                with open(data_file, 'r') as f:
                    data = json.load(f)
                
                # Add note to notes list
                if "notes" not in data:
                    data["notes"] = []
                
                data["notes"].append(dialog.note_data)
                
                # Save updated data
                with open(data_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                messagebox.showinfo("Success", "Note added successfully")
            
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save note: {str(e)}")

    def update_goal_statistics(self):
            """Update task statistics for all goals based on associated tasks"""
            try:
                # Get student data
                student_data = self.app.students.get(self.app.current_student, {})
                data_path = student_data.get("data_path", "")

                if not data_path:
                    return

                data_file = os.path.join(data_path, "progress_data.json")
                if not os.path.exists(data_file):
                    return

                # Load tasks and goals
                with open(data_file, 'r') as f:
                    data = json.load(f)

                tasks = data.get("tasks", [])
                goals = data.get("goals", [])

                # Reset statistics for all goals
                for i, goal in enumerate(goals):
                    goals[i]['task_count'] = 0
                    goals[i]['completed_count'] = 0
                    goals[i]['total_progress'] = 0

                # Calculate task statistics for each goal
                for task in tasks:
                    goal_id = task.get('goal_id', '')
                    if goal_id:
                        # Find the goal with this ID
                        for i, goal in enumerate(goals):
                            if goal.get('id', '') == goal_id:
                                # Update task count
                                goals[i]['task_count'] = goals[i].get('task_count', 0) + 1

                                # Update completed count
                                if task.get('completed', False):
                                    goals[i]['completed_count'] = goals[i].get('completed_count', 0) + 1

                                # Add to total progress
                                goals[i]['total_progress'] = goals[i].get('total_progress', 0) + task.get('progress', 0)
                                break
                            
                # Calculate average progress for each goal
                for i, goal in enumerate(goals):
                    task_count = goals[i].get('task_count', 0)
                    if task_count > 0:
                        avg_progress = goals[i].get('total_progress', 0) / task_count
                        goals[i]['progress'] = round(avg_progress)
                    else:
                        goals[i]['progress'] = 0

                # Save updated goals
                data["goals"] = goals
                with open(data_file, 'w') as f:
                    json.dump(data, f, indent=2)

                # Update our local goals data
                self.goals = goals

                # Update goal filter dropdown options
                goal_options = ["All"]
                for goal in self.goals:
                    if 'title' in goal and goal['title']:
                        goal_options.append(goal['title'])

                # Preserve current selection if possible
                current_selection = self.goal_var.get()
                self.goal_menu.configure(values=goal_options)
                if current_selection in goal_options:
                    self.goal_var.set(current_selection)
                else:
                    self.goal_var.set("All")

            except Exception as e:
                print(f"Error updating goal statistics: {str(e)}")

class TaskDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, existing_task=None):
        super().__init__(parent)
        self.parent = parent
        self.task_data = None
        self.existing_task = existing_task
        
        self.title(title)
        self.geometry("500x600")
        self.resizable(False, False)
        
        # Center dialog on parent
        self.update_idletasks()
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        dialog_width = 500
        dialog_height = 600
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        
        # Create form fields
        self.main_frame = ctk.CTkScrollableFrame(self)
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Task title
        self.title_label = ctk.CTkLabel(self.main_frame, text="Task Title:")
        self.title_label.pack(anchor='w', pady=(0, 5))
        
        self.title_entry = ctk.CTkEntry(self.main_frame, width=460)
        self.title_entry.pack(fill='x', pady=(0, 10))
        
        # Date range
        self.date_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.date_frame.pack(fill='x', pady=(0, 10))
        
        # Start date
        self.start_label = ctk.CTkLabel(self.date_frame, text="Start Date (YYYY-MM-DD):")
        self.start_label.grid(row=0, column=0, padx=(0, 10), pady=5, sticky='w')
        
        self.start_entry = ctk.CTkEntry(self.date_frame, width=200)
        self.start_entry.grid(row=0, column=1, pady=5, sticky='w')
        
        # End date
        self.end_label = ctk.CTkLabel(self.date_frame, text="End Date (YYYY-MM-DD):")
        self.end_label.grid(row=1, column=0, padx=(0, 10), pady=5, sticky='w')
        
        self.end_entry = ctk.CTkEntry(self.date_frame, width=200)
        self.end_entry.grid(row=1, column=1, pady=5, sticky='w')
        
        # Progress
        self.progress_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.progress_frame.pack(fill='x', pady=(0, 10))
        
        self.progress_label = ctk.CTkLabel(self.progress_frame, text="Progress (%):")
        self.progress_label.pack(side='left', padx=(0, 10))
        
        self.progress_var = tk.IntVar(value=0)
        self.progress_slider = ctk.CTkSlider(
            self.progress_frame,
            from_=0,
            to=100,
            number_of_steps=20,
            variable=self.progress_var
        )
        self.progress_slider.pack(side='left', fill='x', expand=True)
        
        self.progress_value = ctk.CTkLabel(self.progress_frame, text="0%", width=40)
        self.progress_value.pack(side='left', padx=(10, 0))
        
        # Update progress label when slider moves
        self.progress_var.trace_add("write", self.update_progress_label)
        
        # Assignee
        self.assignee_label = ctk.CTkLabel(self.main_frame, text="Assigned To:")
        self.assignee_label.pack(anchor='w', pady=(0, 5))
        
        self.assignee_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.assignee_frame.pack(fill='x', pady=(0, 10))
        
        self.assignee_var = tk.StringVar(value="Student")
        self.student_radio = ctk.CTkRadioButton(
            self.assignee_frame,
            text="Student",
            variable=self.assignee_var,
            value="Student"
        )
        self.student_radio.pack(side='left', padx=(0, 20))
        
        self.teacher_radio = ctk.CTkRadioButton(
            self.assignee_frame,
            text="Teacher",
            variable=self.assignee_var,
            value="Teacher"
        )
        self.teacher_radio.pack(side='left')

        # Goal selection
        self.goal_label = ctk.CTkLabel(self.main_frame, text="Associated Goal:")
        self.goal_label.pack(anchor='w', pady=(0, 5))

        self.goal_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.goal_frame.pack(fill='x', pady=(0, 10))

        # Get available goals
        self.goals = []
        self.goal_titles = ["None"]  # Default option
        self.goal_colors = {"None": "#6c757d"}  # Default color
        try:
            student_data = self.parent.app.students.get(self.parent.app.current_student, {})
            data_path = student_data.get("data_path", "")

            if data_path:
                data_file = os.path.join(data_path, "progress_data.json")
                if os.path.exists(data_file):
                    with open(data_file, 'r') as f:
                        data = json.load(f)
                        self.goals = data.get("goals", [])

                        # Create goal title lookup
                        for goal in self.goals:
                            self.goal_titles.append(goal.get('title', ''))
                            self.goal_colors[goal.get('title', '')] = goal.get('color', '#6c757d')
        except Exception:
            pass
        
        self.goal_var = tk.StringVar(value="None")
        self.goal_dropdown = ctk.CTkOptionMenu(
            self.goal_frame,
            values=self.goal_titles,
            variable=self.goal_var,
            command=self.on_goal_selected,
            width=300
        )
        self.goal_dropdown.pack(side='left', fill='x', expand=True)

        # Goal color indicator
        self.goal_color = ctk.CTkFrame(
            self.goal_frame,
            width=30,
            height=30,
            fg_color=self.goal_colors.get("None", "#6c757d")
        )
        self.goal_color.pack(side='right', padx=(10, 0))

        # Task description
        self.desc_label = ctk.CTkLabel(self.main_frame, text="Description:")
        self.desc_label.pack(anchor='w', pady=(0, 5))
        
        self.desc_text = ctk.CTkTextbox(self.main_frame, height=100)
        self.desc_text.pack(fill='x', pady=(0, 10))
        
        # Is milestone checkbox
        self.milestone_var = tk.BooleanVar(value=False)
        self.milestone_cb = ctk.CTkCheckBox(
            self.main_frame,
            text="Mark as Milestone",
            variable=self.milestone_var
        )
        self.milestone_cb.pack(anchor='w', pady=(0, 10))
        
        # Buttons
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(fill='x', pady=(10, 0))
        
        self.cancel_btn = ctk.CTkButton(
            self.button_frame,
            text="Cancel",
            command=self.destroy,
            fg_color=COLOR_SCHEME['inactive'],
            width=100
        )
        self.cancel_btn.pack(side='right', padx=(10, 0))
        
        self.save_btn = ctk.CTkButton(
            self.button_frame,
            text="Save Task",
            command=self.save_task,
            width=100
        )
        self.save_btn.pack(side='right')
        
        # Populate fields if editing existing task
        if existing_task:
            self.populate_fields(existing_task)
            
        # Set focus on title entry
        self.title_entry.focus_set()
        
        # Set default dates if adding new task
        if not existing_task:
            today = datetime.now().strftime("%Y-%m-%d")
            week_later = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            self.start_entry.insert(0, today)
            self.end_entry.insert(0, week_later)

    def on_goal_selected(self, goal_title):
        """Update the goal color indicator when a goal is selected"""
        color = self.goal_colors.get(goal_title, "#6c757d")
        self.goal_color.configure(fg_color=color)

    def update_progress_label(self, *args):
        """Update progress percentage label"""
        value = self.progress_var.get()
        self.progress_value.configure(text=f"{value}%")
    
    def populate_fields(self, task):
        """Populate dialog fields with task data"""
        self.title_entry.insert(0, task.get('title', ''))
        self.start_entry.insert(0, task.get('start_date', ''))
        self.end_entry.insert(0, task.get('end_date', ''))
        
        progress = task.get('progress', 0)
        self.progress_var.set(progress)
        self.progress_value.configure(text=f"{progress}%")
        
        assignee = task.get('assignee', 'Student')
        self.assignee_var.set(assignee)
        
        desc = task.get('description', '')
        self.desc_text.insert('1.0', desc)
        
        is_milestone = task.get('is_milestone', False)
        self.milestone_var.set(is_milestone)

        # Set goal if available
        goal_id = task.get('goal_id', '')
        if goal_id:
            # Find the goal title
            for goal in self.goals:
                if goal.get('id', '') == goal_id:
                    self.goal_var.set(goal.get('title', ''))
                    self.on_goal_selected(goal.get('title', ''))
                    break
    
    def save_task(self):
        """Save task data and close dialog"""
        # Validate fields
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Please enter a task title")
            return

        start_date = self.start_entry.get().strip()
        end_date = self.end_entry.get().strip()

        # Validate dates
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")

            if end < start:
                messagebox.showerror("Error", "End date must be after start date")
                return

        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
            return

        # Get progress value
        progress = self.progress_var.get()

        # Auto-mark task as completed if progress is 100%
        is_completed = self.existing_task.get('completed', False) if self.existing_task else False
        completion_date = self.existing_task.get('completion_date', None) if self.existing_task else None
        completed_by = self.existing_task.get('completed_by', None) if self.existing_task else None

        # Get the current user (teacher or student)
        # Access app mode and user information from the parent's app
        current_user = "Teacher" if self.parent.app.app_mode == "teacher" else "Student"

        if progress == 100 and not is_completed:
            is_completed = True
            completion_date = datetime.now().strftime("%Y-%m-%d")
            completed_by = current_user

        # Check if we need to add a progress history entry
        progress_history = self.existing_task.get('progress_history', []) if self.existing_task else []
        old_progress = self.existing_task.get('progress', 0) if self.existing_task else 0

        # Only add to history if progress changed
        if progress != old_progress:
            progress_history.append({
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'progress': progress,
                'previous_progress': old_progress,
                'modified_by': current_user
            })

        # Get selected goal
        goal_id = ""
        goal_color = ""
        goal_title = self.goal_var.get()

        if goal_title != "None":
            # Find the goal
            for goal in self.goals:
                if goal.get('title', '') == goal_title:
                    goal_id = goal.get('id', '')
                    goal_color = goal.get('color', '')
                    break

        # Create task data
        self.task_data = {
            'id': self.existing_task.get('id', str(int(time.time()))) if self.existing_task else str(int(time.time())),
            'title': title,
            'start_date': start_date,
            'end_date': end_date,
            'progress': progress,
            'assignee': self.assignee_var.get(),
            'description': self.desc_text.get('1.0', 'end-1c'),
            'is_milestone': self.milestone_var.get(),
            'completed': is_completed,
            'created_date': self.existing_task.get('created_date', datetime.now().strftime("%Y-%m-%d")) if self.existing_task else datetime.now().strftime("%Y-%m-%d"),
            'last_modified': datetime.now().strftime("%Y-%m-%d"),
            'last_modified_by': current_user,  # Add who last modified the task
            'progress_history': progress_history,
            'completion_date': completion_date,
            'completed_by': completed_by,  # Add who completed the task
            'goal_id': goal_id,
            'goal_color': goal_color,
        }

        # If task is marked as completed, ensure progress is 100%
        if self.task_data['completed']:
            self.task_data['progress'] = 100
        
        # Update goal statistics if the parent has the method
        if hasattr(self.parent, 'update_goal_statistics'):
            self.parent.update_goal_statistics()

        # Close dialog
        self.destroy()

    def mark_not_complete(self):
        """Mark task as not complete"""
        for i, t in enumerate(self.parent.tasks):
            if t.get('id', '') == self.task.get('id', ''):
                self.parent.tasks[i]['completed'] = False
                self.task = self.parent.tasks[i]
                break
            
        # Save data
        self.parent.save_student_data()

        # Close this dialog and refresh task list
        self.destroy()
        self.parent.apply_filter(self.parent.filter_var.get())

class NoteDialog(ctk.CTkToplevel):
    def __init__(self, parent, task):
        super().__init__(parent)
        self.parent = parent
        self.task = task
        self.note_data = None
        
        self.title("Add Note")
        self.geometry("500x450")
        self.resizable(True, True)
        
        # Center dialog on parent
        self.update_idletasks()
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        dialog_width = 500
        dialog_height = 450
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        
        # Create form fields
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Task info
        self.task_label = ctk.CTkLabel(
            self.main_frame,
            text=f"Task: {task['title']}",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.task_label.pack(anchor='w', pady=(0, 10))
        
        # Note title
        self.title_label = ctk.CTkLabel(self.main_frame, text="Note Title:")
        self.title_label.pack(anchor='w', pady=(0, 5))
        
        self.title_entry = ctk.CTkEntry(self.main_frame, width=460)
        self.title_entry.pack(fill='x', pady=(0, 10))
        
        # Note content
        self.content_label = ctk.CTkLabel(self.main_frame, text="Note Content:")
        self.content_label.pack(anchor='w', pady=(0, 5))
        
        self.content_text = ctk.CTkTextbox(self.main_frame, height=150)
        self.content_text.pack(fill='both', expand=True, pady=(0, 10))
        
        # Buttons
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(fill='x', pady=(10, 0))
        
        self.cancel_btn = ctk.CTkButton(
            self.button_frame,
            text="Cancel",
            command=self.destroy,
            fg_color=COLOR_SCHEME['inactive'],
            width=100
        )
        self.cancel_btn.pack(side='right', padx=(10, 0))
        
        self.save_btn = ctk.CTkButton(
            self.button_frame,
            text="Save Note",
            command=self.save_note,
            width=100
        )
        self.save_btn.pack(side='right')
        
        # Set focus on title entry
        self.title_entry.focus_set()
    
    def save_note(self):
        """Save note and close dialog"""
        # Validate fields
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Please enter a note title")
            return
        
        content = self.content_text.get('1.0', 'end-1c')
        if not content:
            messagebox.showerror("Error", "Please enter note content")
            return
        
        # Create note data
        self.note_data = {
            'id': str(int(time.time())),
            'task_id': self.task['id'],
            'title': title,
            'content': content,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'author': self.parent.app.current_student
        }
        
        # Close dialog
        self.destroy()

class TasksFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        
        # Task data
        self.tasks = []
        self.filtered_tasks = []
        
        # Setup UI
        self.setup_ui()
        
        # Load data if student is selected
        if self.app.current_student and self.app.current_student != "Add a student...":
            self.load_student_data()

    def setup_ui(self):
        # Top control panel
        self.control_panel = ctk.CTkFrame(self)
        self.control_panel.pack(fill='x', padx=20, pady=10)

        # Filter options
        self.filter_frame = ctk.CTkFrame(self.control_panel, fg_color="transparent")
        self.filter_frame.pack(side='left', padx=10)

        self.filter_label = ctk.CTkLabel(self.filter_frame, text="Filter:")
        self.filter_label.pack(side='left', padx=5)

        self.filter_var = tk.StringVar(value="All Tasks")
        self.filter_menu = ctk.CTkOptionMenu(
            self.filter_frame,
            values=["All Tasks", "In Progress", "Completed", "Overdue", "Milestones", "Student Tasks", "Teacher Tasks"],
            variable=self.filter_var,
            command=self.apply_filter,
            width=150
        )
        self.filter_menu.pack(side='left', padx=5)

        # Goal filter
        self.goal_filter_label = ctk.CTkLabel(self.filter_frame, text="Goal:")
        self.goal_filter_label.pack(side='left', padx=(20, 5))

        self.goal_filter_var = tk.StringVar(value="All Goals")
        self.goal_filter_menu = ctk.CTkOptionMenu(
            self.filter_frame,
            values=["All Goals"],  # Will be populated when tasks are loaded
            variable=self.goal_filter_var,
            command=self.apply_goal_filter,
            width=150
        )
        self.goal_filter_menu.pack(side='left', padx=5)

        # Search bar
        self.search_frame = ctk.CTkFrame(self.control_panel, fg_color="transparent")
        self.search_frame.pack(side='right', padx=10)

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Search tasks...",
            width=200
        )
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind("<KeyRelease>", self.search_tasks)

        self.search_btn = ctk.CTkButton(
            self.search_frame,
            text="Search",
            command=self.search_tasks,
            width=80
        )
        self.search_btn.pack(side='left', padx=5)

        # Add new task button
        self.add_task_btn = ctk.CTkButton(
            self.control_panel,
            text="Add New Task",
            command=self.add_task,
            width=120
        )
        self.add_task_btn.pack(side='right', padx=10)

        # Create main content area
        self.content_frame = ctk.CTkFrame(self, fg_color=COLOR_SCHEME['content_bg'])
        self.content_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Create scrollable task list
        self.task_list = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent"
        )
        self.task_list.pack(fill='both', expand=True, padx=10, pady=10)

    def apply_goal_filter(self, goal_title):
        """Apply goal filter and then reapply the main filter"""
        # The full filtering will be done in apply_filter
        self.apply_filter(self.filter_var.get())

    def load_student_data(self):
        """Load student data from JSON file"""
        try:
            # Clear any existing content first
            for widget in self.task_list.winfo_children():
                widget.destroy()

            student_data = self.app.students.get(self.app.current_student, {})
            data_path = student_data.get("data_path", "")

            if not self.app.current_student or self.app.current_student == "Add a student...":
                # Show message to select a student
                label = ctk.CTkLabel(
                    self.task_list,
                    text="Please select a student to view tasks",
                    font=ctk.CTkFont(size=14)
                )
                label.pack(pady=20)
                return

            if not data_path:
                messagebox.showinfo("Info", "No data path set for this student")
                return

            data_file = os.path.join(data_path, "progress_data.json")
            if not os.path.exists(data_file):
                # Create default data file if it doesn't exist
                default_data = {
                    "tasks": [],
                    "notes": [],
                    "goals": []
                }
                with open(data_file, 'w') as f:
                    json.dump(default_data, f, indent=2)
                self.tasks = []
                self.goals = []
            else:
                with open(data_file, 'r') as f:
                    data = json.load(f)
                    self.tasks = data.get("tasks", [])

                    # Load goals for filtering
                    self.goals = data.get("goals", [])

                    # Initialize goals array if it doesn't exist
                    if "goals" not in data:
                        data["goals"] = []
                        with open(data_file, 'w') as f:
                            json.dump(data, f, indent=2)

            # Get available goals for filtering
            goal_titles = ["All Goals"]
            for goal in self.goals:
                goal_titles.append(goal.get('title', ''))

            # Update goal dropdown
            self.goal_filter_menu.configure(values=goal_titles)

            # Apply default filter
            self.apply_filter(self.filter_var.get())

        except Exception as e:
            # Show error in the task list instead of a popup
            for widget in self.task_list.winfo_children():
                widget.destroy()

            error_label = ctk.CTkLabel(
                self.task_list,
                text=f"Error loading tasks: {str(e)}",
                font=ctk.CTkFont(size=14),
                text_color="#ff6b6b"
            )
            error_label.pack(pady=20)

            # Log the error for debugging
            print(f"Error loading student data: {str(e)}")
    
    def save_student_data(self):
        """Save student data to JSON file"""
        try:
            student_data = self.app.students.get(self.app.current_student, {})
            data_path = student_data.get("data_path", "")
            
            if not data_path:
                return
            
            data_file = os.path.join(data_path, "progress_data.json")
            
            # Load existing data to preserve notes
            if os.path.exists(data_file):
                with open(data_file, 'r') as f:
                    data = json.load(f)
            else:
                data = {"notes": []}
            
            # Update tasks
            data["tasks"] = self.tasks
            
            # Save updated data
            with open(data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save student data: {str(e)}")
    
    def apply_filter(self, filter_type):
        """Apply filter to task list"""
        if not self.tasks:
            self.filtered_tasks = []
            self.update_task_list()
            return

        today = datetime.now()

        # Apply primary filter
        if filter_type == "All Tasks":
            self.filtered_tasks = self.tasks
        elif filter_type == "In Progress":
            self.filtered_tasks = [t for t in self.tasks if not t.get('completed', False)]
        elif filter_type == "Completed":
            self.filtered_tasks = [t for t in self.tasks if t.get('completed', False)]
        elif filter_type == "Overdue":
            self.filtered_tasks = [
                t for t in self.tasks
                if not t.get('completed', False) and 
                datetime.strptime(t['end_date'], "%Y-%m-%d") < today
            ]
        elif filter_type == "Milestones":
            self.filtered_tasks = [t for t in self.tasks if t.get('is_milestone', False)]
        elif filter_type == "Student Tasks":
            self.filtered_tasks = [t for t in self.tasks if t.get('assignee', '') == "Student"]
        elif filter_type == "Teacher Tasks":
            self.filtered_tasks = [t for t in self.tasks if t.get('assignee', '') == "Teacher"]

        # Apply goal filter if set
        goal_filter = self.goal_filter_var.get()
        if goal_filter != "All Goals":
            # Find the goal ID for the selected title
            goal_id = ""
            for goal in self.goals:
                if goal.get('title', '') == goal_filter:
                    goal_id = goal.get('id', '')
                    break
                
            if goal_id:
                self.filtered_tasks = [t for t in self.filtered_tasks if t.get('goal_id', '') == goal_id]

        # Apply search filter if there's text in the search box
        search_text = self.search_entry.get().strip().lower()
        if search_text:
            self.filtered_tasks = [
                t for t in self.filtered_tasks
                if search_text in t['title'].lower() or
                search_text in t.get('description', '').lower()
            ]

        # Update task list
        self.update_task_list()
    
    def search_tasks(self, event=None):
        """Search tasks based on search entry"""
        self.apply_filter(self.filter_var.get())
    
    def update_task_list(self):
        """Update the task list display"""
        # Clear existing tasks
        for widget in self.task_list.winfo_children():
            widget.destroy()

        # Flag to track if we're showing the no tasks label
        no_tasks_label_visible = False

        if not self.app.current_student or self.app.current_student == "Add a student...":
            # Show message to select a student
            label = ctk.CTkLabel(
                self.task_list,
                text="Please select a student to view tasks",
                font=ctk.CTkFont(size=14)
            )
            label.pack(pady=20)
            return

        if not self.filtered_tasks:
            # Create the no tasks label for this instance
            no_tasks_label = ctk.CTkLabel(
                self.task_list,
                text="No tasks found. Add tasks using the 'Add New Task' button.",
                font=ctk.CTkFont(size=14)
            )
            no_tasks_label.pack(pady=20)
            return

        # Display tasks
        for task in self.filtered_tasks:
            self.create_task_item(task)
    
    def create_task_item(self, task):
        """Create a task item widget"""
        # Create frame for task item with appropriate color
        if task.get('completed', False):
            bg_color = COLOR_SCHEME['task_completed']
        elif task.get('is_milestone', False):
            bg_color = COLOR_SCHEME['milestone']
        elif datetime.strptime(task['end_date'], "%Y-%m-%d") < datetime.now() and not task.get('completed', False):
            bg_color = COLOR_SCHEME['task_late']
        elif task.get('goal_color'):
            # Use goal color for tasks with goals
            bg_color = task.get('goal_color')
        else:
            bg_color = COLOR_SCHEME['task_normal']

        task_frame = ctk.CTkFrame(self.task_list, fg_color=bg_color)
        task_frame.pack(fill='x', padx=5, pady=5)

        # Task content
        content_frame = ctk.CTkFrame(task_frame, fg_color="transparent")
        content_frame.pack(fill='x', padx=10, pady=10, expand=True)

        # Title and dates in first row
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill='x', expand=True)

        title_label = ctk.CTkLabel(
            header_frame,
            text=task['title'],
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLOR_SCHEME['text']
        )
        title_label.pack(side='left')

        # Format dates
        start_date = datetime.strptime(task['start_date'], "%Y-%m-%d").strftime("%d %b %Y")
        end_date = datetime.strptime(task['end_date'], "%Y-%m-%d").strftime("%d %b %Y")

        date_label = ctk.CTkLabel(
            header_frame,
            text=f"{start_date} to {end_date}",
            font=ctk.CTkFont(size=12),
            text_color=COLOR_SCHEME['text']
        )
        date_label.pack(side='right')

        # Details in second row
        details_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        details_frame.pack(fill='x', pady=(5, 0))

        # Status
        status = "Completed" if task.get('completed', False) else "In Progress"
        if datetime.strptime(task['end_date'], "%Y-%m-%d") < datetime.now() and not task.get('completed', False):
            status = "Overdue"
        if task.get('is_milestone', False):
            status = "Milestone"

        status_label = ctk.CTkLabel(
            details_frame,
            text=f"Status: {status}",
            font=ctk.CTkFont(size=12),
            text_color=COLOR_SCHEME['text']
        )
        status_label.pack(side='left')

        # Assignee
        assignee = task.get('assignee', 'Not assigned')
        assignee_label = ctk.CTkLabel(
            details_frame,
            text=f"Assigned to: {assignee}",
            font=ctk.CTkFont(size=12),
            text_color=COLOR_SCHEME['text']
        )
        assignee_label.pack(side='left', padx=(20, 0))

        # Goal information
        goal_title = "None"
        goal_color = None
        goal_id = task.get('goal_id', '')

        if goal_id:
            # Find the goal
            for goal in self.goals:
                if goal.get('id', '') == goal_id:
                    goal_title = goal.get('title', '')
                    goal_color = goal.get('color', None)
                    break

        if goal_title != "None":
            # Create a frame to hold the goal indicator and label
            goal_indicator_frame = ctk.CTkFrame(details_frame, fg_color="transparent")
            goal_indicator_frame.pack(side='left', padx=(20, 0))

            # Color indicator
            if goal_color:
                goal_color_indicator = ctk.CTkFrame(
                    goal_indicator_frame,
                    width=12,
                    height=12,
                    fg_color=goal_color
                )
                goal_color_indicator.pack(side='left', padx=(0, 5))

            # Goal label
            goal_label = ctk.CTkLabel(
                goal_indicator_frame,
                text=f"Goal: {goal_title}",
                font=ctk.CTkFont(size=12),
                text_color=COLOR_SCHEME['text']
            )
            goal_label.pack(side='left')

        # Progress
        progress = task.get('progress', 0)
        progress_text = f"Progress: {progress}%"

        progress_label = ctk.CTkLabel(
            details_frame,
            text=progress_text,
            font=ctk.CTkFont(size=12),
            text_color=COLOR_SCHEME['text']
        )
        progress_label.pack(side='right')

        # Add completion date and who completed it if completed
        if task.get('completed', False) and task.get('completion_date'):
            completion_date = datetime.strptime(task['completion_date'], "%Y-%m-%d").strftime("%d %b %Y")
            completed_by = task.get('completed_by', 'Unknown')
            completion_label = ctk.CTkLabel(
                content_frame,
                text=f"Completed on: {completion_date} by {completed_by}",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=COLOR_SCHEME['text']
            )
            completion_label.pack(anchor='w', pady=(5, 0))

        # Action buttons
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.pack(fill='x', pady=(10, 0))

        # View button
        view_btn = ctk.CTkButton(
            button_frame,
            text="View Details",
            command=lambda t=task: self.view_task(t),
            width=100,
            height=25
        )
        view_btn.pack(side='left', padx=5)

        # Edit button
        edit_btn = ctk.CTkButton(
            button_frame,
            text="Edit",
            command=lambda t=task: self.edit_task(t),
            width=80,
            height=25
        )
        edit_btn.pack(side='left', padx=5)

        # Complete button (only show if not completed)
        if not task.get('completed', False):
            complete_btn = ctk.CTkButton(
                button_frame,
                text="Mark Complete",
                command=lambda t=task: self.mark_complete(t),
                width=120,
                height=25
            )
            complete_btn.pack(side='left', padx=5)

        if task.get('completed', False):
            not_complete_btn = ctk.CTkButton(
                button_frame,
                text="Mark Not Complete",
                command=lambda t=task: self.mark_not_complete(t),
                width=140,
                height=25
            )
            not_complete_btn.pack(side='left', padx=5)

        # Delete button
        delete_btn = ctk.CTkButton(
            button_frame,
            text="Delete",
            command=lambda t=task: self.delete_task(t),
            width=80,
            height=25,
            fg_color="#dc3545",
            hover_color="#c82333"
        )
        delete_btn.pack(side='right', padx=5)
    
    def add_task(self):
        """Open dialog to add a new task"""
        if not self.app.current_student or self.app.current_student == "Add a student...":
            messagebox.showinfo("Info", "Please select a student first")
            return
        
        dialog = TaskDialog(self, "Add Task")
        self.wait_window(dialog)
        
        if dialog.task_data:
            # Add new task
            self.tasks.append(dialog.task_data)
            # Save data
            self.save_student_data()
            # Update goal statistics
            self.update_goal_statistics()
            # Update task list
            self.apply_filter(self.filter_var.get())
    
    def view_task(self, task):
        """View task details"""
        dialog = TaskViewDialog(self, task)
        self.wait_window(dialog)
    
    def edit_task(self, task):
        """Edit the selected task"""
        # In student mode, only allow editing tasks assigned to student
        if self.app.app_mode == "student" and task.get('assignee', '') != "Student":
            messagebox.showinfo("Permission Denied", 
                               "You can only edit tasks assigned to you.")
        dialog = TaskDialog(self, "Edit Task", task)
        self.wait_window(dialog)
        
        if dialog.task_data:
            # Update task data
            for i, t in enumerate(self.tasks):
                if t.get('id', '') == task.get('id', ''):
                    self.tasks[i] = dialog.task_data
                    break
            
            # Save data
            self.save_student_data()
            
            # Update task list
            self.apply_filter(self.filter_var.get())
    
    def mark_complete(self, task):
        """Mark task as complete"""
        # Get the current user (teacher or student)
        current_user = "Teacher" if self.app.app_mode == "teacher" else "Student"

        for i, t in enumerate(self.tasks):
            if t.get('id', '') == task.get('id', ''):
                self.tasks[i]['completed'] = True
                self.tasks[i]['progress'] = 100
                self.tasks[i]['completion_date'] = datetime.now().strftime("%Y-%m-%d")
                self.tasks[i]['completed_by'] = current_user
                self.tasks[i]['last_modified'] = datetime.now().strftime("%Y-%m-%d")
                self.tasks[i]['last_modified_by'] = current_user

                # Add progress history entry
                if 'progress_history' not in self.tasks[i]:
                    self.tasks[i]['progress_history'] = []

                # Only add to history if progress changed
                old_progress = task.get('progress', 0)
                if old_progress != 100:
                    self.tasks[i]['progress_history'].append({
                        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'progress': 100,
                        'previous_progress': old_progress,
                        'modified_by': current_user
                    })

                break
            
        # Save data
        self.save_student_data()
        # Update goal statistics
        self.update_goal_statistics()
        # Update task list
        self.apply_filter(self.filter_var.get())
    
    def mark_not_complete(self, task):
        """Mark task as not complete"""
        # Get the current user (teacher or student)
        current_user = "Teacher" if self.app.app_mode == "teacher" else "Student"

        for i, t in enumerate(self.tasks):
            if t.get('id', '') == task.get('id', ''):
                # Store current progress before changing
                old_progress = self.tasks[i]['progress']

                # Update task data
                self.tasks[i]['completed'] = False
                self.tasks[i]['last_modified'] = datetime.now().strftime("%Y-%m-%d")
                self.tasks[i]['last_modified_by'] = current_user

                # Add to progress history
                if 'progress_history' not in self.tasks[i]:
                    self.tasks[i]['progress_history'] = []

                # Only add entry if this changes progress from 100%
                if old_progress == 100:
                    # Keep same progress value but mark as not completed
                    self.tasks[i]['progress_history'].append({
                        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'progress': old_progress,
                        'previous_progress': old_progress,
                        'modified_by': current_user,
                        'action': 'Marked not complete'
                    })

                break

            # Save data
            self.save_student_data()
            # Update goal statistics
            self.update_goal_statistics()
            # Update task list
            self.apply_filter(self.filter_var.get())

    def delete_task(self, task):
        """Delete task after confirmation"""
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete the task '{task['title']}'?"
        )
        
        if confirm:
            # Remove task from list
            self.tasks = [t for t in self.tasks if t.get('id', '') != task.get('id', '')]
            
            # Save data
            self.save_student_data()
            # Update goal statistics
            self.update_goal_statistics()
            # Update task list
            self.apply_filter(self.filter_var.get())

    def update_goal_statistics(self):
        """Update task statistics for all goals based on associated tasks"""
        try:
            # Get student data
            student_data = self.app.students.get(self.app.current_student, {})
            data_path = student_data.get("data_path", "")

            if not data_path:
                return

            data_file = os.path.join(data_path, "progress_data.json")
            if not os.path.exists(data_file):
                return

            # Load tasks and goals
            with open(data_file, 'r') as f:
                data = json.load(f)

            tasks = data.get("tasks", [])
            goals = data.get("goals", [])

            # Reset statistics for all goals
            for i, goal in enumerate(goals):
                goals[i]['task_count'] = 0
                goals[i]['completed_count'] = 0
                goals[i]['total_progress'] = 0

            # Calculate task statistics for each goal
            for task in tasks:
                goal_id = task.get('goal_id', '')
                if goal_id:
                    # Find the goal with this ID
                    for i, goal in enumerate(goals):
                        if goal.get('id', '') == goal_id:
                            # Update task count
                            goals[i]['task_count'] = goals[i].get('task_count', 0) + 1

                            # Update completed count
                            if task.get('completed', False):
                                goals[i]['completed_count'] = goals[i].get('completed_count', 0) + 1

                            # Add to total progress
                            goals[i]['total_progress'] = goals[i].get('total_progress', 0) + task.get('progress', 0)
                            break
                        
            # Calculate average progress for each goal
            for i, goal in enumerate(goals):
                task_count = goals[i].get('task_count', 0)
                if task_count > 0:
                    avg_progress = goals[i].get('total_progress', 0) / task_count
                    goals[i]['progress'] = round(avg_progress)
                else:
                    goals[i]['progress'] = 0

            # Save updated goals
            data["goals"] = goals
            with open(data_file, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Error updating goal statistics: {str(e)}")

class TaskViewDialog(ctk.CTkToplevel):
    def __init__(self, parent, task):
        super().__init__(parent)
        self.parent = parent
        self.task = task
    
        self.title("Task Details")
        self.geometry("600x600")
    
        # Center dialog on parent
        self.update_idletasks()
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
    
        dialog_width = 600
        dialog_height = 600
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
    
        self.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
    
        # Create main frame
        self.main_frame = ctk.CTkScrollableFrame(self)
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
        # Task title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text=task['title'],
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.title_label.pack(anchor='w', pady=(0, 10))
    
        # Task details
        self.details_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.details_frame.pack(fill='x', pady=(0, 10))
    
        # Format dates
        start_date = datetime.strptime(task['start_date'], "%Y-%m-%d").strftime("%d %b %Y")
        end_date = datetime.strptime(task['end_date'], "%Y-%m-%d").strftime("%d %b %Y")
    
        # Calculate duration
        start = datetime.strptime(task['start_date'], "%Y-%m-%d")
        end = datetime.strptime(task['end_date'], "%Y-%m-%d")
        duration = (end - start).days + 1
    
        date_text = f"Start: {start_date} | End: {end_date} | Duration: {duration} days"
        if 'progress' in self.task:
            date_text += f" | Progress: {self.task['progress']}%"
    
        # Add completion date and who completed it if the task is completed
        if self.task.get('completed', False) and self.task.get('completion_date'):
            completion_date = datetime.strptime(self.task['completion_date'], "%Y-%m-%d").strftime("%d %b %Y")
            completed_by = self.task.get('completed_by', 'Unknown')
            date_text += f" | Completed: {completion_date} by {completed_by}"
    
        self.date_info = ctk.CTkLabel(
            self.details_frame,
            text=date_text,
            wraplength=560
        )
        self.date_info.pack(anchor='w', pady=2)
    
        # Assignee and status
        assignee = self.task.get('assignee', 'Not assigned')
        self.assignee_label = ctk.CTkLabel(
            self.details_frame,
            text=f"Assigned to: {assignee}",
            font=ctk.CTkFont(size=12)
        )
        self.assignee_label.pack(anchor='w', pady=2)
    
        # Goal information
        goal_id = task.get('goal_id', '')
        if goal_id:
            # Find the goal name and color
            goal_title = "Unknown"
            goal_color = None
            
            try:
                # Get student data
                student_data = self.parent.app.students.get(self.parent.app.current_student, {})
                data_path = student_data.get("data_path", "")
                
                if data_path:
                    data_file = os.path.join(data_path, "progress_data.json")
                    if os.path.exists(data_file):
                        with open(data_file, 'r') as f:
                            data = json.load(f)
                            goals = data.get("goals", [])
                            
                            # Find the goal
                            for goal in goals:
                                if goal.get('id', '') == goal_id:
                                    goal_title = goal.get('title', 'Unknown')
                                    goal_color = goal.get('color', None)
                                    break
            except Exception as e:
                print(f"Error loading goal information: {str(e)}")
            
            # Create goal info display
            goal_frame = ctk.CTkFrame(self.details_frame, fg_color="transparent")
            goal_frame.pack(anchor='w', pady=2)
            
            if goal_color:
                # Color indicator
                color_indicator = ctk.CTkFrame(
                    goal_frame,
                    width=12,
                    height=12,
                    fg_color=goal_color
                )
                color_indicator.pack(side='left', padx=(0, 5))
            
            goal_label = ctk.CTkLabel(
                goal_frame,
                text=f"Associated Goal: {goal_title}",
                font=ctk.CTkFont(size=12)
            )
            goal_label.pack(side='left')
    
        status = "Completed" if self.task.get('completed', False) else "In Progress"
        if end < datetime.now() and not self.task.get('completed', False):
            status = "Overdue"
        if self.task.get('is_milestone', False):
            status = "Milestone"
    
        self.status_label = ctk.CTkLabel(
            self.details_frame,
            text=f"Status: {status}",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(anchor='w', pady=2)
    
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.details_frame)
        self.progress_bar.pack(fill='x', pady=5)
        self.progress_bar.set(task.get('progress', 0) / 100)
    
        # Created and last modified dates and by whom
        created = task.get('created_date', '')
        modified = task.get('last_modified', '')
        modified_by = task.get('last_modified_by', '')
    
        if created:
            created_date = datetime.strptime(created, "%Y-%m-%d").strftime("%d %b %Y")
            self.created_label = ctk.CTkLabel(
                self.details_frame,
                text=f"Created: {created_date}",
                font=ctk.CTkFont(size=12)
            )
            self.created_label.pack(anchor='w', pady=2)
    
        if modified:
            modified_date = datetime.strptime(modified, "%Y-%m-%d").strftime("%d %b %Y")
            modified_text = f"Last Modified: {modified_date}"
            if modified_by:
                modified_text += f" by {modified_by}"
            self.modified_label = ctk.CTkLabel(
                self.details_frame,
                text=modified_text,
                font=ctk.CTkFont(size=12)
            )
            self.modified_label.pack(anchor='w', pady=2)
    
        # Progress history section
        if 'progress_history' in task and task['progress_history']:
            self.history_label = ctk.CTkLabel(
                self.main_frame,
                text="Progress History:",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            self.history_label.pack(anchor='w', pady=(10, 5))
    
            # Create progress history frame
            self.history_frame = ctk.CTkFrame(self.main_frame)
            self.history_frame.pack(fill='x', pady=(0, 10))
    
            # Add header
            header_frame = ctk.CTkFrame(self.history_frame, fg_color=COLOR_SCHEME['inactive'])
            header_frame.pack(fill='x', pady=(0, 5))
    
            date_header = ctk.CTkLabel(
                header_frame,
                text="Date",
                font=ctk.CTkFont(size=12, weight="bold"),
                width=150
            )
            date_header.pack(side='left', padx=5, pady=2)
    
            prev_progress_header = ctk.CTkLabel(
                header_frame,
                text="From",
                font=ctk.CTkFont(size=12, weight="bold"),
                width=50
            )
            prev_progress_header.pack(side='left', padx=5, pady=2)
    
            arrow_header = ctk.CTkLabel(
                header_frame,
                text="→",
                font=ctk.CTkFont(size=12, weight="bold"),
                width=30
            )
            arrow_header.pack(side='left', padx=5, pady=2)
    
            new_progress_header = ctk.CTkLabel(
                header_frame,
                text="To",
                font=ctk.CTkFont(size=12, weight="bold"),
                width=50
            )
            new_progress_header.pack(side='left', padx=5, pady=2)
    
            modified_by_header = ctk.CTkLabel(
                header_frame,
                text="Modified By",
                font=ctk.CTkFont(size=12, weight="bold"),
                width=100
            )
            modified_by_header.pack(side='left', padx=5, pady=2)
    
            # Sort history by date (most recent first)
            sorted_history = sorted(
                task['progress_history'],
                key=lambda entry: datetime.strptime(entry['date'], "%Y-%m-%d %H:%M:%S"),
                reverse=True
            )
    
            # Display progress history
            for entry in sorted_history:
                history_entry_frame = ctk.CTkFrame(self.history_frame, fg_color="transparent")
                history_entry_frame.pack(fill='x', pady=1)
    
                # Format date
                try:
                    date_obj = datetime.strptime(entry['date'], "%Y-%m-%d %H:%M:%S")
                    formatted_date = date_obj.strftime("%d %b %Y, %H:%M:%S")
                except ValueError:
                    formatted_date = entry['date']
    
                date_label = ctk.CTkLabel(
                    history_entry_frame,
                    text=formatted_date,
                    font=ctk.CTkFont(size=12),
                    width=150
                )
                date_label.pack(side='left', padx=5, pady=2)
    
                prev_progress_label = ctk.CTkLabel(
                    history_entry_frame,
                    text=f"{entry.get('previous_progress', 0)}%",
                    font=ctk.CTkFont(size=12),
                    width=50
                )
                prev_progress_label.pack(side='left', padx=5, pady=2)
    
                arrow_label = ctk.CTkLabel(
                    history_entry_frame,
                    text="→",
                    font=ctk.CTkFont(size=12),
                    width=30
                )
                arrow_label.pack(side='left', padx=5, pady=2)
    
                new_progress_label = ctk.CTkLabel(
                    history_entry_frame,
                    text=f"{entry.get('progress', 0)}%",
                    font=ctk.CTkFont(size=12, weight="bold"),
                    width=50
                )
                new_progress_label.pack(side='left', padx=5, pady=2)
    
                modified_by_label = ctk.CTkLabel(
                    history_entry_frame,
                    text=entry.get('modified_by', 'Unknown'),
                    font=ctk.CTkFont(size=12),
                    width=100
                )
                modified_by_label.pack(side='left', padx=5, pady=2)
    
        # Description section
        self.desc_label = ctk.CTkLabel(
            self.main_frame,
            text="Description:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.desc_label.pack(anchor='w', pady=(10, 5))
    
        description = task.get('description', '').strip()
        if not description:
            description = "No description provided."
    
        self.desc_text = ctk.CTkTextbox(self.main_frame, height=100)
        self.desc_text.pack(fill='x', pady=(0, 10))
        self.desc_text.insert('1.0', description)
        self.desc_text.configure(state="disabled")
    
        # Notes section
        self.notes_label = ctk.CTkLabel(
            self.main_frame,
            text="Notes:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.notes_label.pack(anchor='w', pady=(10, 5))
    
        # Load notes for this task
        self.notes_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.notes_frame.pack(fill='x', pady=(0, 10))
    
        self.load_task_notes()
    
        # Buttons
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(fill='x', pady=(10, 0))
    
        self.add_note_btn = ctk.CTkButton(
            self.button_frame,
            text="Add Note",
            command=self.add_note,
            width=100
        )
        self.add_note_btn.pack(side='left', padx=5)
    
        self.edit_btn = ctk.CTkButton(
            self.button_frame,
            text="Edit Task",
            command=self.edit_task,
            width=100
        )
        self.edit_btn.pack(side='left', padx=5)
    
        # Add Completed/Not Completed buttons based on task status
        if not task.get('completed', False):
            self.complete_btn = ctk.CTkButton(
                self.button_frame,
                text="Mark Complete",
                command=self.mark_complete,
                width=120
            )
            self.complete_btn.pack(side='left', padx=5)
        else:
            # Only show "Mark Not Complete" button if the task is completed
            self.not_complete_btn = ctk.CTkButton(
                self.button_frame,
                text="Mark Not Complete",
                command=self.mark_not_complete,
                width=140
            )
            self.not_complete_btn.pack(side='left', padx=5)
    
        self.close_btn = ctk.CTkButton(
            self.button_frame,
            text="Close",
            command=self.destroy,
            width=100
        )
        self.close_btn.pack(side='right', padx=5)

    def load_task_notes(self):
        """Load notes for this task"""
        # Clear existing notes
        for widget in self.notes_frame.winfo_children():
            widget.destroy()
        
        # Get notes for this task
        try:
            student_data = self.parent.app.students.get(self.parent.app.current_student, {})
            data_path = student_data.get("data_path", "")
            
            if not data_path:
                return
            
            data_file = os.path.join(data_path, "progress_data.json")
            if not os.path.exists(data_file):
                return
            
            with open(data_file, 'r') as f:
                data = json.load(f)
                notes = data.get("notes", [])
            
            # Filter notes for this task
            task_notes = [note for note in notes if note.get('task_id', '') == self.task.get('id', '')]
            
            if not task_notes:
                no_notes_label = ctk.CTkLabel(
                    self.notes_frame,
                    text="No notes found for this task.",
                    font=ctk.CTkFont(size=12)
                )
                no_notes_label.pack(pady=10)
                return
            
            # Sort notes by date (most recent first)
            sorted_notes = sorted(
                task_notes,
                key=lambda note: datetime.strptime(note.get('date', '2000-01-01 00:00:00'), "%Y-%m-%d %H:%M:%S"),
                reverse=True
            )
            
            # Display notes
            for note in sorted_notes:
                self.create_note_item(note)
        
        except Exception as e:
            print(f"Error loading notes: {e}")
            error_label = ctk.CTkLabel(
                self.notes_frame,
                text=f"Error loading notes: {str(e)}",
                font=ctk.CTkFont(size=12)
            )
            error_label.pack(pady=10)
    
    def create_note_item(self, note):
        """Create a note item widget"""
        note_frame = ctk.CTkFrame(self.notes_frame)
        note_frame.pack(fill='x', pady=5)
        
        # Note header
        header_frame = ctk.CTkFrame(note_frame, fg_color="transparent")
        header_frame.pack(fill='x', padx=10, pady=(10, 5))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=note.get('title', 'Note'),
            font=ctk.CTkFont(size=12, weight="bold")
        )
        title_label.pack(side='left')
        
        # Format date
        note_date = note.get('date', '')
        if note_date:
            try:
                date_obj = datetime.strptime(note_date, "%Y-%m-%d %H:%M:%S")
                formatted_date = date_obj.strftime("%d %b %Y, %H:%M")
            except ValueError:
                formatted_date = note_date
        else:
            formatted_date = ""
        
        date_label = ctk.CTkLabel(
            header_frame,
            text=formatted_date,
            font=ctk.CTkFont(size=10)
        )
        date_label.pack(side='right')
        
        # Note content
        content = note.get('content', '').strip()
        if content:
            content_text = ctk.CTkTextbox(note_frame, height=60)
            content_text.pack(fill='x', padx=10, pady=(0, 10))
            content_text.insert('1.0', content)
            content_text.configure(state="disabled")
    
    def add_note(self):
        """Add a note to the task"""
        dialog = NoteDialog(self.parent, self.task)
        self.wait_window(dialog)
        
        if dialog.note_data:
            # Get student data file path
            student_data = self.parent.app.students.get(self.parent.app.current_student, {})
            data_path = student_data.get("data_path", "")
            
            if not data_path:
                return
            
            data_file = os.path.join(data_path, "progress_data.json")
            
            try:
                # Load existing data
                with open(data_file, 'r') as f:
                    data = json.load(f)
                
                # Add note to notes list
                if "notes" not in data:
                    data["notes"] = []
                
                data["notes"].append(dialog.note_data)
                
                # Save updated data
                with open(data_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                # Reload notes
                self.load_task_notes()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save note: {str(e)}")
    
    def edit_task(self):
        """Edit the selected task"""
        # Check if task is completed
        if self.task.get('completed', False):
            messagebox.showinfo("Task Completed", 
                            "This task is marked as complete. Please mark it as not complete before editing.")
            return

        # In student mode, only allow editing tasks assigned to student
        if self.parent.app.app_mode == "student" and self.task.get('assignee', '') != "Student":
            messagebox.showinfo("Permission Denied", 
                             "You can only edit tasks assigned to you.")
            return
        dialog = TaskDialog(self.parent, "Edit Task", self.task)
        self.wait_window(dialog)

        if dialog.task_data:
            # Update task data
            for i, t in enumerate(self.parent.tasks):
                if t.get('id', '') == self.task.get('id', ''):
                    self.parent.tasks[i] = dialog.task_data
                    self.task = dialog.task_data
                    break
                
            # Save data
            self.parent.save_student_data()

            # Close this dialog and refresh task list
            self.destroy()
            self.parent.apply_filter(self.parent.filter_var.get())
    
    def mark_complete(self):
        """Mark task as complete"""
        # Get the current user (teacher or student)
        current_user = "Teacher" if self.parent.app.app_mode == "teacher" else "Student"

        for i, t in enumerate(self.parent.tasks):
            if t.get('id', '') == self.task.get('id', ''):
                self.parent.tasks[i]['completed'] = True
                self.parent.tasks[i]['progress'] = 100
                self.parent.tasks[i]['completion_date'] = datetime.now().strftime("%Y-%m-%d")
                self.parent.tasks[i]['completed_by'] = current_user
                self.parent.tasks[i]['last_modified'] = datetime.now().strftime("%Y-%m-%d")
                self.parent.tasks[i]['last_modified_by'] = current_user

                # Add progress history entry
                if 'progress_history' not in self.parent.tasks[i]:
                    self.parent.tasks[i]['progress_history'] = []

                # Only add to history if progress changed
                old_progress = self.task.get('progress', 0)
                if old_progress != 100:
                    self.parent.tasks[i]['progress_history'].append({
                        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'progress': 100,
                        'previous_progress': old_progress,
                        'modified_by': current_user
                    })

                self.task = self.parent.tasks[i]
                break
            
        # Save data
        self.parent.save_student_data()

        # Close this dialog and refresh task list
        self.destroy()
        self.parent.apply_filter(self.parent.filter_var.get())
        
    def mark_not_complete(self):
        """Mark task as not complete"""
        # Get the current user (teacher or student)
        current_user = "Teacher" if self.parent.app.app_mode == "teacher" else "Student"

        for i, t in enumerate(self.parent.tasks):
            if t.get('id', '') == self.task.get('id', ''):
                # Store current progress before changing
                old_progress = self.parent.tasks[i]['progress']

                # Update task data
                self.parent.tasks[i]['completed'] = False
                self.parent.tasks[i]['last_modified'] = datetime.now().strftime("%Y-%m-%d")
                self.parent.tasks[i]['last_modified_by'] = current_user

                # Add to progress history
                if 'progress_history' not in self.parent.tasks[i]:
                    self.parent.tasks[i]['progress_history'] = []

                # Only add entry if this changes progress from 100%
                if old_progress == 100:
                    # Keep same progress value but mark as not completed
                    self.parent.tasks[i]['progress_history'].append({
                        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'progress': old_progress,
                        'previous_progress': old_progress,
                        'modified_by': current_user,
                        'action': 'Marked not complete'
                    })

                self.task = self.parent.tasks[i]
                break
            
        # Save data
        self.parent.save_student_data()

        # Close this dialog and refresh task list
        self.destroy()
        self.parent.apply_filter(self.parent.filter_var.get())

class NotesFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        
        # Notes data
        self.notes = []
        self.filtered_notes = []
        self.tasks = []
        
        # Track if widgets are created
        self.widgets_created = False
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        # Top control panel
        self.control_panel = ctk.CTkFrame(self)
        self.control_panel.pack(fill='x', padx=20, pady=10)

        # Filter options
        self.filter_frame = ctk.CTkFrame(self.control_panel, fg_color="transparent")
        self.filter_frame.pack(side='left', padx=10)

        self.filter_label = ctk.CTkLabel(self.filter_frame, text="Filter by Task:")
        self.filter_label.pack(side='left', padx=5)

        self.filter_var = tk.StringVar(value="All Notes")
        self.filter_menu = ctk.CTkOptionMenu(
            self.filter_frame,
            values=["All Notes"],
            variable=self.filter_var,
            command=self.apply_filter,
            width=200
        )
        self.filter_menu.pack(side='left', padx=5)

        # Add goal filter dropdown
        self.goal_filter_label = ctk.CTkLabel(self.filter_frame, text="Goal:")
        self.goal_filter_label.pack(side='left', padx=(20, 5))

        self.goal_filter_var = tk.StringVar(value="All Goals")
        self.goal_filter_menu = ctk.CTkOptionMenu(
            self.filter_frame,
            values=["All Goals"],  # Will be populated when notes are loaded
            variable=self.goal_filter_var,
            command=self.apply_goal_filter,
            width=150
        )
        self.goal_filter_menu.pack(side='left', padx=5)

        # Add path management button when in student mode
        if self.app.app_mode == "student":
            self.path_frame = ctk.CTkFrame(self.control_panel, fg_color="transparent")
            self.path_frame.pack(side='right', padx=10)

            self.path_btn = ctk.CTkButton(
                self.path_frame,
                text="Manage Data Path",
                command=self.show_path_manager,
                width=150
            )
            self.path_btn.pack(side='left', padx=5)

        # Search bar
        self.search_frame = ctk.CTkFrame(self.control_panel, fg_color="transparent")
        self.search_frame.pack(side='right', padx=10)

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Search notes...",
            width=200
        )
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind("<KeyRelease>", self.search_notes)

        self.search_btn = ctk.CTkButton(
            self.search_frame,
            text="Search",
            command=self.search_notes,
            width=80
        )
        self.search_btn.pack(side='left', padx=5)

        # Refresh button
        self.refresh_btn = ctk.CTkButton(
            self.control_panel,
            text="Refresh Notes",
            command=lambda: self.apply_filter(self.filter_var.get()),
            width=120
        )
        self.refresh_btn.pack(side='right', padx=10)

        # Create main content area
        self.content_frame = ctk.CTkFrame(self, fg_color=COLOR_SCHEME['content_bg'])
        self.content_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Create container for the note list
        self.note_list_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.note_list_container.pack(fill='both', expand=True, padx=10, pady=10)

        # Create scrollable note list
        self.note_list = ctk.CTkScrollableFrame(
            self.note_list_container,
            fg_color="transparent"
        )
        self.note_list.pack(fill='both', expand=True)

        # Create a welcome label initially
        self.welcome_label = ctk.CTkLabel(
            self.note_list,
            text="Select a student to view notes",
            font=ctk.CTkFont(size=14)
        )
        self.welcome_label.pack(pady=20)

        if hasattr(self, 'no_notes_label') and self.no_notes_label.winfo_exists():
            self.no_notes_label.destroy()  # Destroy existing instance if it exists        
        # Create the no notes label but don't pack it yet
        self.no_notes_label = ctk.CTkLabel(
            self.note_list,
            text="No notes found. Add notes from the Tasks view.",
            font=ctk.CTkFont(size=14)
        )

        # Flag to track label visibility
        self.no_notes_label_visible = False
        self.widgets_created = True

    def apply_goal_filter(self, goal_title):
        """Apply goal filter and then reapply the main filter"""
        # The full filtering will be done in apply_filter
        self.apply_filter(self.filter_var.get())

    def show_path_manager(self):
        """Show dialog to manage student data path"""
        dialog = StudentPathManagerDialog(self)
        self.wait_window(dialog)
        # Reload data if path changed
        if hasattr(dialog, "path_changed") and dialog.path_changed:
            self.load_student_data()

    def load_student_data(self):
        """Load student notes data from JSON file"""
        try:
            # First, clear existing content
            if hasattr(self, 'note_list') and self.widgets_created:
                for widget in self.note_list.winfo_children():
                    widget.destroy()
                self.no_notes_label_visible = False

            # Check if student is selected
            if not self.app.current_student or self.app.current_student == "Add a student...":
                # Show welcome message
                if hasattr(self, 'note_list') and self.widgets_created:
                    welcome_label = ctk.CTkLabel(
                        self.note_list,
                        text="Please select a student to view notes",
                        font=ctk.CTkFont(size=14)
                    )
                    welcome_label.pack(pady=20)
                return

            # Get student data
            student_data = self.app.students.get(self.app.current_student, {})
            data_path = student_data.get("data_path", "")

            if not data_path:
                # Show no data path message
                if hasattr(self, 'note_list') and self.widgets_created:
                    no_path_label = ctk.CTkLabel(
                        self.note_list,
                        text="No data path set for this student",
                        font=ctk.CTkFont(size=14)
                    )
                    no_path_label.pack(pady=20)
                return

            data_file = os.path.join(data_path, "progress_data.json")
            if not os.path.exists(data_file):
                # Create default data file if it doesn't exist
                default_data = {
                    "tasks": [],
                    "notes": [],
                    "goals": []  # Add goals array
                }
                with open(data_file, 'w') as f:
                    json.dump(default_data, f, indent=2)
                self.notes = []
                self.tasks = []
                self.goals = []  # Initialize goals array
            else:
                with open(data_file, 'r') as f:
                    data = json.load(f)
                    self.notes = data.get("notes", [])
                    self.tasks = data.get("tasks", [])
                    self.goals = data.get("goals", [])  # Load goals

                    # Initialize goals array if it doesn't exist
                    if "goals" not in data:
                        data["goals"] = []
                        with open(data_file, 'w') as f:
                            json.dump(data, f, indent=2)

            # Update task filter dropdown
            self.update_task_filter()

            # Apply default filter
            self.apply_filter("All Notes")

        except Exception as e:
            print(f"Error loading student data: {str(e)}")

            # Show error message
            if hasattr(self, 'note_list') and self.widgets_created:
                for widget in self.note_list.winfo_children():
                    widget.destroy()

                error_label = ctk.CTkLabel(
                    self.note_list,
                    text=f"Error loading notes: {str(e)}",
                    font=ctk.CTkFont(size=14),
                    text_color="#ff6b6b"
                )
                error_label.pack(pady=20)
    
    def update_task_filter(self):
        """Update task filter dropdown with available tasks"""
        filter_options = ["All Notes"]
        goal_options = ["All Goals"]

        # Add task titles to filter options
        task_dict = {}
        for task in self.tasks:
            task_dict[task.get('id', '')] = task.get('title', '')

        # Add tasks that have notes
        task_ids = set(note.get('task_id', '') for note in self.notes)
        for task_id in task_ids:
            if task_id in task_dict:
                filter_options.append(task_dict[task_id])

        # Update dropdown
        self.filter_menu.configure(values=filter_options)

        # Get goals and update goal filter dropdown
        try:
            student_data = self.app.students.get(self.app.current_student, {})
            data_path = student_data.get("data_path", "")

            if data_path:
                data_file = os.path.join(data_path, "progress_data.json")
                if os.path.exists(data_file):
                    with open(data_file, 'r') as f:
                        data = json.load(f)
                        goals = data.get("goals", [])

                        # Add goal titles
                        for goal in goals:
                            goal_options.append(goal.get('title', ''))
        except Exception as e:
            print(f"Error loading goals: {str(e)}")

        # Update goal dropdown
        self.goal_filter_menu.configure(values=goal_options)
    
    def apply_filter(self, filter_value):
        """Apply filter to notes list"""
        if not self.notes:
            self.filtered_notes = []
            self.update_notes_list()
            return

        # Apply main filter (task filter)
        if filter_value == "All Notes":
            self.filtered_notes = self.notes
        else:
            # Find task_id by title
            task_id = None
            for task in self.tasks:
                if task.get('title', '') == filter_value:
                    task_id = task.get('id', '')
                    break
                
            # Filter notes by task_id
            if task_id:
                self.filtered_notes = [note for note in self.notes if note.get('task_id', '') == task_id]
            else:
                self.filtered_notes = []

        # Check if a goal filter is active
        goal_filter = self.goal_filter_var.get()
        if goal_filter != "All Goals":
            # Get the goal ID
            goal_id = ""
            try:
                student_data = self.app.students.get(self.app.current_student, {})
                data_path = student_data.get("data_path", "")

                if data_path:
                    data_file = os.path.join(data_path, "progress_data.json")
                    if os.path.exists(data_file):
                        with open(data_file, 'r') as f:
                            data = json.load(f)
                            goals = data.get("goals", [])

                            # Find the goal ID
                            for goal in goals:
                                if goal.get('title', '') == goal_filter:
                                    goal_id = goal.get('id', '')
                                    break
            except Exception as e:
                print(f"Error loading goals: {str(e)}")

            if goal_id:
                # Get tasks that belong to this goal
                goal_task_ids = []
                for task in self.tasks:
                    if task.get('goal_id', '') == goal_id:
                        goal_task_ids.append(task.get('id', ''))

                # Filter notes that belong to these tasks
                self.filtered_notes = [note for note in self.filtered_notes if note.get('task_id', '') in goal_task_ids]

        # Apply search filter if there's text in the search box
        search_text = self.search_entry.get().strip().lower()
        if search_text:
            self.filtered_notes = [
                note for note in self.filtered_notes
                if search_text in note.get('title', '').lower() or
                search_text in note.get('content', '').lower()
            ]

        # Update notes list
        self.update_notes_list()
    
    def search_notes(self, event=None):
        """Search notes based on search entry"""
        self.apply_filter(self.filter_var.get())
    
    def update_notes_list(self):
        """Update the notes list display"""
        # Make sure widgets are created
        if not hasattr(self, 'note_list') or not self.widgets_created:
            return

        # Clear existing notes
        for widget in self.note_list.winfo_children():
            widget.destroy()

        self.no_notes_label_visible = False

        if not self.app.current_student or self.app.current_student == "Add a student...":
            # Show message to select a student
            label = ctk.CTkLabel(
                self.note_list,
                text="Please select a student to view notes",
                font=ctk.CTkFont(size=14)
            )
            label.pack(pady=20)
            return

        if not self.filtered_notes:
            # Create a new no_notes_label if it doesn't exist or recreate it
            if not hasattr(self, 'no_notes_label') or not self.no_notes_label.winfo_exists():
                self.no_notes_label = ctk.CTkLabel(
                    self.note_list,
                    text="No notes found. Add notes from the Tasks view.",
                    font=ctk.CTkFont(size=14)
                )
            self.no_notes_label.pack(pady=20)
            self.no_notes_label_visible = True
            return

        # Sort notes by date (most recent first)
        try:
            sorted_notes = sorted(
                self.filtered_notes,
                key=lambda note: datetime.strptime(note.get('date', '2000-01-01 00:00:00'), "%Y-%m-%d %H:%M:%S"),
                reverse=True
            )

            # Create task title lookup
            task_titles = {task.get('id', ''): task.get('title', '') for task in self.tasks}

            # Display notes
            for note in sorted_notes:
                self.create_note_item(note, task_titles)
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.note_list,
                text=f"Error displaying notes: {str(e)}",
                font=ctk.CTkFont(size=14),
                text_color="#ff6b6b"
            )
            error_label.pack(pady=20)
    
    def create_note_item(self, note, task_titles):
        """Create a note item widget"""
        note_frame = ctk.CTkFrame(self.note_list)
        note_frame.pack(fill='x', pady=5)
        
        # Get associated task
        task_id = note.get('task_id', '')
        task_title = task_titles.get(task_id, 'Unknown Task')
        
        # Note header
        header_frame = ctk.CTkFrame(note_frame, fg_color="transparent")
        header_frame.pack(fill='x', padx=10, pady=(10, 5))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=note.get('title', 'Note'),
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title_label.pack(side='left')
        
        # Format date
        note_date = note.get('date', '')
        if note_date:
            try:
                date_obj = datetime.strptime(note_date, "%Y-%m-%d %H:%M:%S")
                formatted_date = date_obj.strftime("%d %b %Y, %H:%M")
            except ValueError:
                formatted_date = note_date
        else:
            formatted_date = ""
        
        date_label = ctk.CTkLabel(
            header_frame,
            text=formatted_date,
            font=ctk.CTkFont(size=10)
        )
        date_label.pack(side='right')
        
        # Task reference
        task_frame = ctk.CTkFrame(note_frame, fg_color="transparent")
        task_frame.pack(fill='x', padx=10, pady=(0, 5))
        
        task_ref_label = ctk.CTkLabel(
            task_frame,
            text=f"Task: {task_title}",
            font=ctk.CTkFont(size=12)
        )
        task_ref_label.pack(anchor='w')
        
        # Note content
        content = note.get('content', '').strip()
        if content:
            content_text = ctk.CTkTextbox(note_frame, height=80)
            content_text.pack(fill='x', padx=10, pady=(0, 10))
            content_text.insert('1.0', content)
            content_text.configure(state="disabled")
        
        # Action buttons
        button_frame = ctk.CTkFrame(note_frame, fg_color="transparent")
        button_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        view_task_btn = ctk.CTkButton(
            button_frame,
            text="View Task",
            command=lambda t_id=task_id: self.view_task(t_id),
            width=100,
            height=25
        )
        view_task_btn.pack(side='left', padx=5)
        
        delete_btn = ctk.CTkButton(
            button_frame,
            text="Delete Note",
            command=lambda n=note: self.delete_note(n),
            width=100,
            height=25,
            fg_color="#dc3545",
            hover_color="#c82333"
        )
        delete_btn.pack(side='right', padx=5)
    
    def view_task(self, task_id):
        """View the task associated with a note"""
        # Find the task
        task = None
        for t in self.tasks:
            if t.get('id', '') == task_id:
                task = t
                break
        
        if task:
            dialog = TaskViewDialog(self, task)
            self.wait_window(dialog)
        else:
            messagebox.showinfo("Info", "Task not found. It may have been deleted.")
    
    def delete_note(self, note):
        """Delete note after confirmation"""
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete the note '{note.get('title', '')}'?"
        )
        
        if confirm:
            # Get student data file path
            student_data = self.app.students.get(self.app.current_student, {})
            data_path = student_data.get("data_path", "")
            
            if not data_path:
                return
            
            data_file = os.path.join(data_path, "progress_data.json")
            
            try:
                # Load existing data
                with open(data_file, 'r') as f:
                    data = json.load(f)
                
                # Remove note
                data["notes"] = [n for n in data.get("notes", []) if n.get('id', '') != note.get('id', '')]
                
                # Save updated data
                with open(data_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                # Update notes list
                self.notes = data.get("notes", [])
                self.apply_filter(self.filter_var.get())
                
                messagebox.showinfo("Success", "Note deleted successfully")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete note: {str(e)}")

class StudentPathManagerDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.path_changed = False
        
        self.title("Manage Data Path")
        self.geometry("500x300")
        self.resizable(False, False)
        
        # Center dialog
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 500) // 2
        y = (self.winfo_screenheight() - 300) // 2
        self.geometry(f"500x300+{x}+{y}")
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Current path
        self.current_path_label = ctk.CTkLabel(
            self.main_frame,
            text="Current Data Path:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.current_path_label.pack(anchor='w', pady=(0, 5))
        
        current_path = self.parent.app.student_data_path
        self.path_display = ctk.CTkLabel(
            self.main_frame,
            text=current_path,
            font=ctk.CTkFont(size=12),
            wraplength=460
        )
        self.path_display.pack(anchor='w', pady=(0, 20))
        
        # New path
        self.new_path_label = ctk.CTkLabel(
            self.main_frame,
            text="New Data Path:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.new_path_label.pack(anchor='w', pady=(0, 5))
        
        self.path_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.path_frame.pack(fill='x', pady=(0, 20))
        
        self.path_entry = ctk.CTkEntry(self.path_frame, width=350)
        self.path_entry.pack(side='left', fill='x', expand=True)
        self.path_entry.insert(0, current_path)
        
        self.browse_btn = ctk.CTkButton(
            self.path_frame,
            text="Browse",
            command=self.browse_folder,
            width=80
        )
        self.browse_btn.pack(side='right', padx=(10, 0))
        
        # Description
        description = (
            "Changing the data path will move your student profile and all related "
            "tasks and notes to the new location. This is useful if you need to "
            "synchronize your data with your teacher using a different folder."
        )
        self.desc_label = ctk.CTkLabel(
            self.main_frame,
            text=description,
            wraplength=460,
            justify="left"
        )
        self.desc_label.pack(anchor='w', pady=(0, 20))
        
        # Buttons
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(fill='x', pady=(10, 0))
        
        self.cancel_btn = ctk.CTkButton(
            self.button_frame,
            text="Cancel",
            command=self.destroy,
            fg_color=COLOR_SCHEME['inactive'],
            width=100
        )
        self.cancel_btn.pack(side='right', padx=(10, 0))
        
        self.save_btn = ctk.CTkButton(
            self.button_frame,
            text="Update Path",
            command=self.update_path,
            width=120
        )
        self.save_btn.pack(side='right')
    
    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)
    
    def update_path(self):
        """Update the student data path"""
        new_path = self.path_entry.get().strip()
        old_path = self.parent.app.student_data_path
        
        if not new_path:
            messagebox.showerror("Error", "Please enter a valid path")
            return
        
        if new_path == old_path:
            messagebox.showinfo("Info", "The path has not changed")
            self.destroy()
            return
        
        try:
            # Create new directory if it doesn't exist
            os.makedirs(new_path, exist_ok=True)
            
            # Copy data files from old path to new path
            student_config_path = os.path.join(old_path, "student_config.json")
            progress_data_path = os.path.join(old_path, "progress_data.json")
            
            import shutil
            
            if os.path.exists(student_config_path):
                shutil.copy2(student_config_path, os.path.join(new_path, "student_config.json"))
            
            if os.path.exists(progress_data_path):
                shutil.copy2(progress_data_path, os.path.join(new_path, "progress_data.json"))
            
            # Update path in app
            self.parent.app.student_data_path = new_path
            
            # Update config
            self.parent.app.config_manager.set_student_path(new_path)
            
            # Update student record if needed
            student_name = self.parent.app.current_student
            if student_name and os.path.exists(os.path.join(new_path, "student_config.json")):
                try:
                    with open(os.path.join(new_path, "student_config.json"), 'r') as f:
                        student_config = json.load(f)
                    
                    if student_name in student_config:
                        student_config[student_name]["data_path"] = new_path
                        
                        with open(os.path.join(new_path, "student_config.json"), 'w') as f:
                            json.dump(student_config, f, indent=2)
                except Exception as e:
                    print(f"Error updating student config: {e}")
            
            # Set flag to indicate path changed
            self.path_changed = True
            
            # Close dialog
            messagebox.showinfo("Success", "Data path updated successfully")
            self.destroy()
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update path: {str(e)}")

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        # Create main container
        self.main_container = ctk.CTkFrame(self, fg_color=COLOR_SCHEME['content_bg'])
        self.main_container.pack(fill='both', expand=True, padx=20, pady=20)

        # Settings title
        self.title_label = ctk.CTkLabel(
            self.main_container,
            text="Settings",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(anchor='w', padx=20, pady=20)

        # Application Mode settings
        self.mode_frame = ctk.CTkFrame(self.main_container)
        self.mode_frame.pack(fill='x', padx=20, pady=10)

        self.mode_label = ctk.CTkLabel(
            self.mode_frame,
            text="Application Mode",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.mode_label.pack(anchor='w', padx=20, pady=10)

        # Mode selection options
        self.mode_options_frame = ctk.CTkFrame(self.mode_frame, fg_color="transparent")
        self.mode_options_frame.pack(fill='x', padx=20, pady=10)

        # Description text
        mode_desc = (
            "You can set the default mode for the next application startup.\n"
            "This is useful for testing how your students will see the data."
        )
        self.mode_desc_label = ctk.CTkLabel(
            self.mode_options_frame,
            text=mode_desc,
            justify="left",
            wraplength=600
        )
        self.mode_desc_label.pack(anchor='w', pady=(0, 10))

        # Default startup mode
        self.startup_mode_frame = ctk.CTkFrame(self.mode_options_frame, fg_color="transparent")
        self.startup_mode_frame.pack(fill='x', pady=5)

        self.startup_label = ctk.CTkLabel(
            self.startup_mode_frame,
            text="Default startup mode:",
            width=150,
            anchor="w"
        )
        self.startup_label.pack(side='left', padx=5)

        self.startup_var = tk.StringVar(value="teacher")

        # Check if a config manager exists and get the current setting
        if hasattr(self.app, 'config_manager'):
            current_mode = self.app.config_manager.get_app_mode()
            if current_mode:
                self.startup_var.set(current_mode)

        self.teacher_radio = ctk.CTkRadioButton(
            self.startup_mode_frame,
            text="Teacher Mode",
            variable=self.startup_var,
            value="teacher",
            command=self.update_startup_mode
        )
        self.teacher_radio.pack(side='left', padx=(10, 20))

        self.student_radio = ctk.CTkRadioButton(
            self.startup_mode_frame,
            text="Student Mode",
            variable=self.startup_var,
            value="student",
            command=self.update_startup_mode
        )
        self.student_radio.pack(side='left', padx=5)

        # Quick view button
        self.quick_view_frame = ctk.CTkFrame(self.mode_options_frame, fg_color="transparent")
        self.quick_view_frame.pack(fill='x', pady=10)

        self.view_as_student_btn = ctk.CTkButton(
            self.quick_view_frame,
            text="View as Student",
            command=self.view_as_student,
            width=150
        )
        self.view_as_student_btn.pack(side='left', padx=5)

        self.student_picker_frame = ctk.CTkFrame(self.quick_view_frame, fg_color="transparent")
        self.student_picker_frame.pack(side='left', padx=5, fill='x', expand=True)

        student_names = list(self.app.students.keys())
        if not student_names:
            student_names = ["No students available"]

        self.student_view_var = tk.StringVar(value=student_names[0] if student_names else "")
        self.student_picker = ctk.CTkOptionMenu(
            self.student_picker_frame,
            values=student_names,
            variable=self.student_view_var,
            width=200
        )
        self.student_picker.pack(side='left', padx=5)

        # Student management section
        self.students_frame = ctk.CTkFrame(self.main_container)
        self.students_frame.pack(fill='x', padx=20, pady=10)

        self.students_label = ctk.CTkLabel(
            self.students_frame,
            text="Student Management",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.students_label.pack(anchor='w', padx=20, pady=10)

        # Student list with scrollbar
        self.student_list_frame = ctk.CTkFrame(self.students_frame, fg_color="transparent")
        self.student_list_frame.pack(fill='x', padx=20, pady=10)

        # Create student list in a tabular format
        self.create_student_list()

        # Add student button
        self.add_student_btn = ctk.CTkButton(
            self.students_frame,
            text="Add New Student",
            command=self.add_student,
            width=150,
            height=35
        )
        self.add_student_btn.pack(anchor='w', padx=20, pady=10)

        # About section
        self.about_frame = ctk.CTkFrame(self.main_container)
        self.about_frame.pack(fill='x', padx=20, pady=10)

        self.about_label = ctk.CTkLabel(
            self.about_frame,
            text="About",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.about_label.pack(anchor='w', padx=20, pady=10)

        self.app_info = ctk.CTkLabel(
            self.about_frame,
            text=f"Meritum v{APP_VERSION}\n"
                 "A tool for tracking student progress using Gantt charts and task management."
        )
        self.app_info.pack(anchor='w', padx=20, pady=5)

    def update_startup_mode(self):
        """Update the default startup mode in config"""
        if hasattr(self.app, 'config_manager'):
            mode = self.startup_var.get()
            self.app.config_manager.set_app_mode(mode)

    def view_as_student(self):
        """Open the app in student mode with the selected student"""
        selected_student = self.student_view_var.get()

        if selected_student == "No students available":
            messagebox.showinfo("No Students", "Please add a student first before using this feature.")
            return

        # Get the student data path
        student_data = self.app.students.get(selected_student, {})
        student_path = student_data.get("data_path", "")

        if not student_path:
            messagebox.showerror("Error", "No data path found for this student.")
            return

        # Confirm with the user
        confirm = messagebox.askyesno(
            "Switch to Student Mode",
            f"This will close the current application and reopen it in student mode as '{selected_student}'.\n\n"
            f"Data path: {student_path}\n\n"
            "Continue?"
        )

        if not confirm:
            return

        # Save the configuration for student mode
        if hasattr(self.app, 'config_manager'):
            self.app.config_manager.set_app_mode("student")
            self.app.config_manager.set_student_name(selected_student)
            self.app.config_manager.set_student_path(student_path)

        # Close the current window and reopen in student mode
        # We need to use subprocess to ensure the app restarts properly
        try:
            # Get the current script path
            script_path = sys.argv[0]

            # Create a subprocess to restart the application
            import subprocess

            # Prepare the command
            # Use pythonw on Windows to avoid console window, python otherwise
            if platform.system() == "Windows":
                python_exe = "pythonw"
            else:
                python_exe = "python"

            # Notify user
            messagebox.showinfo(
                "Restarting in Student Mode",
                f"The application will now restart in student mode as '{selected_student}'."
            )

            # Start the new process
            subprocess.Popen([python_exe, script_path])

            # Close the current instance
            self.app.on_closing()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to restart application: {str(e)}")

    def create_student_list(self):
        """Create the student list in tabular format"""
        # Clear existing widgets
        for widget in self.student_list_frame.winfo_children():
            widget.destroy()
        
        # Create a scrollable frame for the table
        self.table_frame = ctk.CTkScrollableFrame(
            self.student_list_frame,
            width=600,
            height=200
        )
        self.table_frame.pack(fill='both', expand=True)
        
        # Create table header
        header_frame = ctk.CTkFrame(self.table_frame, fg_color=COLOR_SCHEME['inactive'])
        header_frame.pack(fill='x', pady=(0, 2))
        
        name_header = ctk.CTkLabel(
            header_frame,
            text="Student Name",
            font=ctk.CTkFont(weight="bold"),
            width=200
        )
        name_header.pack(side='left', padx=5, pady=5)
        
        path_header = ctk.CTkLabel(
            header_frame,
            text="Data Path",
            font=ctk.CTkFont(weight="bold"),
            width=250
        )
        path_header.pack(side='left', padx=5, pady=5)
        
        actions_header = ctk.CTkLabel(
            header_frame,
            text="Actions",
            font=ctk.CTkFont(weight="bold"),
            width=150
        )
        actions_header.pack(side='left', padx=5, pady=5)
        
        # Add students to table
        student_names = list(self.app.students.keys())
        if not student_names:
            no_students_label = ctk.CTkLabel(
                self.table_frame,
                text="No students added yet. Click 'Add New Student' to get started.",
                height=40
            )
            no_students_label.pack(pady=10)
        else:
            for name in student_names:
                student_data = self.app.students.get(name, {})
                data_path = student_data.get("data_path", "")
                
                row_frame = ctk.CTkFrame(self.table_frame)
                row_frame.pack(fill='x', pady=2)
                
                name_label = ctk.CTkLabel(
                    row_frame,
                    text=name,
                    width=200
                )
                name_label.pack(side='left', padx=5, pady=5)
                
                path_label = ctk.CTkLabel(
                    row_frame,
                    text=data_path,
                    width=250
                )
                path_label.pack(side='left', padx=5, pady=5)
                
                # Action buttons
                actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
                actions_frame.pack(side='left', padx=5, pady=5)
                
                edit_btn = ctk.CTkButton(
                    actions_frame,
                    text="Edit",
                    command=lambda n=name: self.edit_student(n),
                    width=60,
                    height=25
                )
                edit_btn.pack(side='left', padx=2)
                
                delete_btn = ctk.CTkButton(
                    actions_frame,
                    text="Delete",
                    command=lambda n=name: self.delete_student(n),
                    width=60,
                    height=25,
                    fg_color="#dc3545",
                    hover_color="#c82333"
                )
                delete_btn.pack(side='left', padx=2)
    
    def add_student(self):
        """Add a new student"""
        self.app.show_add_student_dialog()
        # Refresh the student list
        self.create_student_list()
    
    def edit_student(self, name):
        """Edit student data path"""
        dialog = EditStudentDialog(self, name)
        self.wait_window(dialog)
        # Refresh the student list
        self.create_student_list()
    
    def delete_student(self, name):
        """Delete a student after confirmation"""
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete student '{name}'?\n"
            "This will not delete the data files, but the student will be removed from the application."
        )
        
        if confirm:
            if name in self.app.students:
                del self.app.students[name]
                self.app.save_students_config()
                
                # If the deleted student was the current one, reset current_student
                if self.app.current_student == name:
                    student_names = list(self.app.students.keys())
                    if student_names:
                        self.app.current_student = student_names[0]
                        self.app.student_var.set(student_names[0])
                    else:
                        self.app.current_student = None
                        self.app.student_var.set("Add a student...")
                    
                    # Refresh current view
                    self.app.refresh_current_view()
                
                # Update student dropdown
                self.app.update_student_dropdown()
                
                # Refresh the student list
                self.create_student_list()
                
                messagebox.showinfo("Success", f"Student '{name}' deleted successfully")
    
    def change_appearance(self, mode):
        """Change application appearance mode"""
        ctk.set_appearance_mode(mode)
    
    def change_color_theme(self, theme):
        """Change application color theme"""
        ctk.set_default_color_theme(theme)
        messagebox.showinfo(
            "Theme Changed",
            "Color theme changed. Restart the application for the change to take full effect."
        )

class EditStudentDialog(ctk.CTkToplevel):
    def __init__(self, parent, student_name):
        super().__init__(parent)
        self.parent = parent
        self.student_name = student_name
        
        self.title(f"Edit Student: {student_name}")
        self.geometry("500x300")
        self.resizable(False, False)
        
        # Center dialog on parent
        self.update_idletasks()
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        dialog_width = 500
        dialog_height = 300
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
        
        # Create form fields
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.name_label = ctk.CTkLabel(self.main_frame, text="Student Name:")
        self.name_label.pack(anchor='w', pady=(0, 5))
        
        self.name_entry = ctk.CTkEntry(self.main_frame, width=460)
        self.name_entry.pack(fill='x', pady=(0, 10))
        self.name_entry.insert(0, student_name)
        self.name_entry.configure(state="disabled")  # Cannot change the name
        
        self.path_label = ctk.CTkLabel(self.main_frame, text="Data Folder Path:")
        self.path_label.pack(anchor='w', pady=(0, 5))
        
        self.path_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.path_frame.pack(fill='x', pady=(0, 10))
        
        self.path_entry = ctk.CTkEntry(self.path_frame, width=380)
        self.path_entry.pack(side='left', fill='x', expand=True)
        
        # Get current path
        current_path = self.parent.app.students.get(student_name, {}).get("data_path", "")
        self.path_entry.insert(0, current_path)
        
        self.browse_btn = ctk.CTkButton(
            self.path_frame,
            text="Browse",
            command=self.browse_folder,
            width=70
        )
        self.browse_btn.pack(side='right', padx=(10, 0))
        
        # Buttons
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(fill='x', pady=(10, 0))
        
        self.cancel_btn = ctk.CTkButton(
            self.button_frame,
            text="Cancel",
            command=self.destroy,
            fg_color=COLOR_SCHEME['inactive'],
            width=100
        )
        self.cancel_btn.pack(side='right', padx=(10, 0))
        
        self.save_btn = ctk.CTkButton(
            self.button_frame,
            text="Save Changes",
            command=self.save_changes,
            width=120
        )
        self.save_btn.pack(side='right')
    
    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)
    
    def save_changes(self):
        """Save updated student data"""
        path = self.path_entry.get().strip()
        
        if not path:
            messagebox.showerror("Error", "Please enter a data folder path")
            return
        
        try:
            # Create folder if it doesn't exist
            os.makedirs(path, exist_ok=True)
            
            # Update student data
            self.parent.app.students[self.student_name]["data_path"] = path
            
            # Save config
            self.parent.app.save_students_config()
            
            # Close dialog
            self.destroy()
            
            messagebox.showinfo("Success", "Student data updated successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update student data: {str(e)}")

class ModeSelectionAppStandalone:
    def __init__(self):
        # Create config manager
        self.config_manager = ConfigManager()

        # Get saved mode
        saved_mode = self.config_manager.get_app_mode()
        self.selected_mode = None
        self.selected_student = None
        self.student_data_path = None

        # If mode already saved, skip dialog and start app directly
        if saved_mode:
            if saved_mode == "teacher":
                self.selected_mode = "teacher"
                self.root = None  # No need for UI
                return
            elif saved_mode == "student":
                self.selected_mode = "student"
                self.selected_student = self.config_manager.get_student_name()
                self.student_data_path = self.config_manager.get_student_path()
                if self.selected_student and self.student_data_path:
                    self.root = None  # No need for UI
                    return

        # Create GUI for selection if no saved mode or missing data
        self.root = ctk.CTk()
        self.root.title("Select Mode")
        self.root.geometry("400x400")
        self.root.resizable(False, False)

        # Set protocol for window close
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

        # Center the dialog
        self.center_window(self.root, 400, 400)

        # Create main frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Show the mode selection UI
        self.show_mode_selection()

        # Run the window as modal
        self.root.focus_force()
        self.root.grab_set()
        self.root.wait_window()
    
    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def show_mode_selection(self):
        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Meritum",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=20)
        
        # Mode selection
        self.mode_label = ctk.CTkLabel(
            self.main_frame,
            text="Select Mode:",
            font=ctk.CTkFont(size=14)
        )
        self.mode_label.pack(pady=(10, 5))
        
        # Teacher mode button
        self.teacher_btn = ctk.CTkButton(
            self.main_frame,
            text="Teacher Mode",
            command=self.select_teacher_mode,
            width=200,
            height=40
        )
        self.teacher_btn.pack(pady=5)
        
        # Student mode button
        self.student_btn = ctk.CTkButton(
            self.main_frame,
            text="Student Mode",
            command=self.select_student_mode,
            width=200,
            height=40
        )
        self.student_btn.pack(pady=5)
        
        # Exit button
        self.exit_btn = ctk.CTkButton(
            self.main_frame,
            text="Exit",
            command=self.exit_app,
            width=200,
            height=30,
            fg_color=COLOR_SCHEME['inactive']
        )
        self.exit_btn.pack(pady=20)
    
    def select_teacher_mode(self):
        self.selected_mode = "teacher"
        self.config_manager.set_app_mode("teacher")
        self.root.destroy()

    def select_student_mode(self):
        self.selected_mode = "student"
        # Config will be saved after student setup is complete
        # Show student setup screen
        self.show_student_setup()
    
    def show_student_setup(self):
        # Clear the main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Student Setup",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=20)

        # Data folder path first
        self.path_label = ctk.CTkLabel(
            self.main_frame,
            text="Data Folder Path (shared with teacher):",
            font=ctk.CTkFont(size=14)
        )
        self.path_label.pack(anchor='w', pady=(10, 5))

        self.path_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.path_frame.pack(fill='x', pady=(0, 15))

        self.path_entry = ctk.CTkEntry(
            self.path_frame,
            width=280
        )
        self.path_entry.pack(side='left', fill='x', expand=True)

        # Set default path
        default_path = os.path.join(os.path.expanduser("~"), "Documents", "PhD_Progress")
        self.path_entry.insert(0, default_path)

        self.browse_btn = ctk.CTkButton(
            self.path_frame,
            text="Browse",
            command=self.browse_folder,
            width=70
        )
        self.browse_btn.pack(side='right', padx=(10, 0))

        # Check config button
        self.check_btn = ctk.CTkButton(
            self.main_frame,
            text="Check for Existing Profile",
            command=self.check_for_profile,
            width=200
        )
        self.check_btn.pack(pady=10)

        # Student info frame (initially hidden)
        self.student_info_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.student_info_frame.pack(fill='x', pady=(0, 10), padx=5)

        # Hide it initially
        self.student_info_frame.pack_forget()

        # Buttons
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(fill='x', pady=(20, 0))

        self.back_btn = ctk.CTkButton(
            self.button_frame,
            text="Back",
            command=self.show_mode_selection,
            width=100,
            fg_color=COLOR_SCHEME['inactive']
        )
        self.back_btn.pack(side='left')

        self.continue_btn = ctk.CTkButton(
            self.button_frame,
            text="Continue",
            command=self.setup_student,
            width=100
        )
        self.continue_btn.pack(side='right')

        # Initially disable continue button
        self.continue_btn.configure(state="disabled")

    def check_for_profile(self):
        """Check if student profile exists in the specified folder"""
        data_path = self.path_entry.get().strip()

        if not data_path:
            messagebox.showerror("Error", "Please enter a data folder path")
            return

        # Create folder if it doesn't exist
        try:
            os.makedirs(data_path, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create folder: {str(e)}")
            return

        # Check for student config file
        student_config_path = os.path.join(data_path, "student_config.json")

        if os.path.exists(student_config_path):
            try:
                with open(student_config_path, 'r') as f:
                    student_config = json.load(f)

                if student_config:
                    # Student profiles exist, let user select one
                    student_names = list(student_config.keys())

                    # Display student selection dropdown
                    self.show_student_selector(student_names, student_config)
                    return
            except Exception as e:
                messagebox.showwarning("Warning", f"Error reading configuration file: {str(e)}")

        # No existing profiles, show form to create new one
        self.show_new_profile_form()

    def show_student_selector(self, student_names, student_config):
        """Show UI to select from existing student profiles"""
        # Clear any existing widgets in student_info_frame
        for widget in self.student_info_frame.winfo_children():
            widget.destroy()

        # Show the frame
        self.student_info_frame.pack(fill='x', pady=(0, 10), padx=5)

        # Add a label
        select_label = ctk.CTkLabel(
            self.student_info_frame,
            text="Select Your Profile:",
            font=ctk.CTkFont(size=14)
        )
        select_label.pack(anchor='w', pady=(10, 5))

        # Add dropdown for student selection
        self.student_var = tk.StringVar(value=student_names[0])
        self.student_dropdown = ctk.CTkOptionMenu(
            self.student_info_frame,
            values=student_names,
            variable=self.student_var,
            width=300
        )
        self.student_dropdown.pack(pady=5)

        # Enable continue button
        self.continue_btn.configure(state="normal")

        # Store config for later use
        self.existing_student_config = student_config

    def show_new_profile_form(self):
        """Show form to create a new student profile"""
        # Clear any existing widgets in student_info_frame
        for widget in self.student_info_frame.winfo_children():
            widget.destroy()

        # Show the frame
        self.student_info_frame.pack(fill='x', pady=(0, 10), padx=5)

        # Add a label
        new_profile_label = ctk.CTkLabel(
            self.student_info_frame,
            text="Create New Profile:",
            font=ctk.CTkFont(size=14)
        )
        new_profile_label.pack(anchor='w', pady=(10, 5))

        # Student name
        self.name_label = ctk.CTkLabel(
            self.student_info_frame,
            text="Your Name:",
            font=ctk.CTkFont(size=12)
        )
        self.name_label.pack(anchor='w', pady=(5, 0))

        self.name_entry = ctk.CTkEntry(
            self.student_info_frame,
            width=300
        )
        self.name_entry.pack(fill='x', pady=(0, 10))

        # Email address
        self.email_label = ctk.CTkLabel(
            self.student_info_frame,
            text="Email Address:",
            font=ctk.CTkFont(size=12)
        )
        self.email_label.pack(anchor='w', pady=(5, 0))

        self.email_entry = ctk.CTkEntry(
            self.student_info_frame,
            width=300
        )
        self.email_entry.pack(fill='x', pady=(0, 10))

        # Program/Department
        self.program_label = ctk.CTkLabel(
            self.student_info_frame,
            text="Program/Department:",
            font=ctk.CTkFont(size=12)
        )
        self.program_label.pack(anchor='w', pady=(5, 0))

        self.program_entry = ctk.CTkEntry(
            self.student_info_frame,
            width=300
        )
        self.program_entry.pack(fill='x', pady=(0, 10))

        # Birth date
        self.birth_date_label = ctk.CTkLabel(
            self.student_info_frame,
            text="Birth Date (YYYY-MM-DD):",
            font=ctk.CTkFont(size=12)
        )
        self.birth_date_label.pack(anchor='w', pady=(5, 0))

        self.birth_date_entry = ctk.CTkEntry(
            self.student_info_frame,
            width=300
        )
        self.birth_date_entry.pack(fill='x', pady=(0, 10))

        # Profession
        self.profession_label = ctk.CTkLabel(
            self.student_info_frame,
            text="Profession (if applicable):",
            font=ctk.CTkFont(size=12)
        )
        self.profession_label.pack(anchor='w', pady=(5, 0))

        self.profession_entry = ctk.CTkEntry(
            self.student_info_frame,
            width=300
        )
        self.profession_entry.pack(fill='x', pady=(0, 10))

        # Telephone
        self.telephone_label = ctk.CTkLabel(
            self.student_info_frame,
            text="Telephone Number:",
            font=ctk.CTkFont(size=12)
        )
        self.telephone_label.pack(anchor='w', pady=(5, 0))

        self.telephone_entry = ctk.CTkEntry(
            self.student_info_frame,
            width=300
        )
        self.telephone_entry.pack(fill='x', pady=(0, 10))

        # Enable continue button
        self.continue_btn.configure(state="normal")

        # Set flag to indicate this is a new profile
        self.creating_new_profile = True

    def setup_student(self):
        """Set up student data and continue"""
        data_path = self.path_entry.get().strip()

        if not data_path:
            messagebox.showerror("Error", "Please enter a data folder path")
            return

        # Check if we're selecting existing profile or creating new one
        if hasattr(self, 'creating_new_profile') and self.creating_new_profile:
            # Creating new profile
            student_name = self.name_entry.get().strip()
            email = self.email_entry.get().strip()
            program = self.program_entry.get().strip()
            # New fields
            birth_date = self.birth_date_entry.get().strip()
            profession = self.profession_entry.get().strip()
            telephone = self.telephone_entry.get().strip()

            if not student_name:
                messagebox.showerror("Error", "Please enter your name")
                return

            # Validate birth date if provided
            if birth_date:
                try:
                    datetime.strptime(birth_date, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Error", "Invalid birth date format. Use YYYY-MM-DD")
                    return

            # Create student config file
            student_config_path = os.path.join(data_path, "student_config.json")

            try:
                # Load existing config if file exists
                if os.path.exists(student_config_path):
                    with open(student_config_path, 'r') as f:
                        student_config = json.load(f)
                else:
                    student_config = {}

                # Add or update student profile
                student_config[student_name] = {
                    "data_path": data_path,
                    "email": email,
                    "program": program,
                    "birth_date": birth_date,
                    "profession": profession,
                    "telephone": telephone,
                    "created_date": datetime.now().strftime("%Y-%m-%d")
                }

                # Save updated config
                with open(student_config_path, 'w') as f:
                    json.dump(student_config, f, indent=2)

                self.selected_student = student_name
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create configuration file: {str(e)}")
                return
        else:
            # Using existing profile
            if hasattr(self, 'student_var'):
                student_name = self.student_var.get()
                self.selected_student = student_name
            else:
                messagebox.showerror("Error", "Please select or create a student profile")
                return

        # Create default progress data file if it doesn't exist
        progress_data_path = os.path.join(data_path, "progress_data.json")
        try:
            if not os.path.exists(progress_data_path):
                default_data = {
                    "tasks": [],
                    "notes": []
                }
                with open(progress_data_path, 'w') as f:
                    json.dump(default_data, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create data file: {str(e)}")
            return

        # Set the student data path
        self.student_data_path = data_path

        # Save the configuration
        self.config_manager.set_app_mode("student")
        self.config_manager.set_student_path(data_path)
        self.config_manager.set_student_name(self.selected_student)

        # Close dialog
        self.root.destroy()

    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)
    
    def cancel_animations(self, widget):
        """Recursively cancel any animations for a widget and its children"""
        # Try to cancel any click animations
        widget_id = str(widget.winfo_id())
        for after_id in self.root.tk.call('after', 'info'):
            if widget_id in str(after_id):
                try:
                    self.root.after_cancel(after_id)
                except Exception:
                    pass
        
        # Recursively process children
        try:
            for child in widget.winfo_children():
                self.cancel_animations(child)
        except (AttributeError, tk.TclError):
            pass
    
    def exit_app(self):
        # This is the on_closing equivalent for the mode selection window
        # Disable all update callbacks
        try:
            #self.root.after_cancel("check_dpi_scaling")  # CustomTkinter specific
            self.root.after_cancel("update")  # CustomTkinter specific
        except Exception:
            pass
        
        # Cancel ALL after events before destroying widgets
        try:
            for after_id in self.root.tk.call('after', 'info'):
                self.root.after_cancel(after_id)
        except Exception:
            pass

        # Explicitly destroy all widgets first
        def destroy_widgets(parent):
            for widget in parent.winfo_children():
                if hasattr(widget, 'winfo_exists') and widget.winfo_exists():
                    if hasattr(widget, 'winfo_children'):
                        destroy_widgets(widget)  # Recurse to children first
                    if hasattr(widget, 'winfo_exists') and widget.winfo_exists():  # Check again as children might have destroyed it
                        widget.destroy()

        # Start destroying widgets from the top level
        destroy_widgets(self.root)

        # Release grab and destroy
        self.root.grab_release()
        self.root.quit()
        self.root.destroy()

def main():
    # Set appearance mode and default color theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Create mode selection window
    dialog = ModeSelectionAppStandalone()
    
    # Check if a mode was selected
    if dialog.selected_mode:
        try:
            # Create the main app with the selected configuration
            app = StudentProgressApp(
                app_mode=dialog.selected_mode,
                student_name=getattr(dialog, "selected_student", None),
                student_data_path=getattr(dialog, "student_data_path", None)
            )
            app.mainloop()
        except Exception as e:
            print(f"Error in main application: {e}")
        finally:
            # Make sure we exit properly
            sys.exit(0)
    else:
        # No mode selected, exit properly
        sys.exit(0)

if __name__ == "__main__":
    main()
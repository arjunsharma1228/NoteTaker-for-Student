import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import simpledialog, messagebox
from tkinter import scrolledtext
import qrcode
from tkinter import filedialog
import os
from datetime import datetime
import time
from PyDictionary import PyDictionary
import nltk
from nltk.corpus import wordnet



class NoteTakerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Note Taker 2.5")
        
        # Set initial window size and position
        self.root.geometry("1200x800+100+100")
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Using a basic theme
        
        # Menu bar
        self.menu_bar = tk.Menu(root)
        

        
        # About menu
        self.about_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.about_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="About", menu=self.about_menu)

        self.root.config(menu=self.menu_bar)

        # Create main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill="both", expand=True)
        
        # Header frame
        self.header_frame = tk.Frame(self.main_frame, bg="#333")
        self.header_frame.pack(side="top", fill="x")
        
        

        # Title label
        title_frame = tk.Frame(self.header_frame, bg="#333")
        title_frame.pack(side="left", padx=20, pady=10)

        self.title_label_1 = tk.Label(title_frame, text="Note Taker", font=("Arial", 24, "bold"), fg="white", bg="#333")
        self.title_label_1.pack(side="top")

        self.title_label_2 = tk.Label(title_frame, text="made with ❤ by Arjun Sharma", font=("Arial", 12), fg="white", bg="#333")
        self.title_label_2.pack(side="bottom")
        
        
        
        
        # Add a button in the top menu bar to open the documentation
        self.documentation_button_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.documentation_button_menu.add_command(label="Documentation", command=self.open_documentation)
        self.menu_bar.add_cascade(label="Documentation", menu=self.documentation_button_menu)
        
        # Add a button in the top menu bar to generate QR code
        self.qr_code_button_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.qr_code_button_menu.add_command(label="Generate QR Code", command=self.generate_qr_code_dialog)
        self.menu_bar.add_cascade(label="Generate QR Code", menu=self.qr_code_button_menu)
        
        
        

        
        
        
        
        
        

        # Social links
        social_links_frame = tk.Frame(self.header_frame, bg="#333")
        social_links_frame.pack(side="right", padx=20, pady=10)

        self.social_links_label = tk.Label(social_links_frame, text="Connect with me:", font=("Arial", 12), fg="white", bg="#333")
        self.social_links_label.pack(side="left")

        self.linkedin_link = tk.Label(social_links_frame, text="LinkedIn", font=("Arial", 12, "underline"), fg="white", bg="#333", cursor="hand2")
        self.linkedin_link.pack(side="left", padx=5)
        self.linkedin_link.bind("<Button-1>", lambda e: self.open_link("https://www.linkedin.com/in/arjunsharma1228/"))



        self.instagram_link = tk.Label(social_links_frame, text="Invite Friend ", font=("Arial", 12, "underline"), fg="white", bg="#333", cursor="hand2")
        self.instagram_link.pack(side="left", padx=5)
        self.instagram_link.bind("<Button-1>", lambda e: self.open_link("https://github.com/sharmaarjun1228/NoteTaker-for-Student"))
        
        # Create side navigation bar
        self.side_nav_frame = tk.Frame(self.main_frame, width=300, bg="#333")
        self.side_nav_frame.pack(side="left", fill="y")
        
        # Buttons on side navigation bar
        buttons = [
            ("Open", self.open_file),
            ("Save", self.save_file),
            ("Save As", self.save_as_file),
            ("Save as PDF", self.save_as_pdf),
            ("Export as Text", self.export_as_text),
            ("Export as HTML", self.export_as_html),
            ("Export as Markdown", self.export_as_markdown),
            ("How to Use", self.open_documentation),
            ("Exit", self.exit_app)
            
        ]
        
        # Initialize dialog box for documentation
        self.documentation_dialog = None
        
        for btn_text, command in buttons:
            btn = ttk.Button(self.side_nav_frame, text=btn_text, command=command, style="TButton")
            btn.pack(fill="x", padx=10, pady=5)
        
        # Main content frame
        self.content_frame = tk.Frame(self.main_frame, bg="white")
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Document Name and User Name section
        self.doc_user_frame = tk.Frame(self.content_frame, bg="white")
        self.doc_user_frame.pack(fill="x", padx=20, pady=20)
        
        # Add the "Share via Email" button
        self.share_email_button = ttk.Button(self.side_nav_frame, text="Share via Email", command=self.share_via_email)
        self.share_email_button.pack(fill="x", padx=10, pady=5)
        

        
        self.doc_name_label = ttk.Label(self.doc_user_frame, text="Document Name:", font=("Arial", 14))
        self.doc_name_label.pack(side="left", padx=10)
        
        self.doc_name_entry = ttk.Entry(self.doc_user_frame, font=("Arial", 12), width=30)
        self.doc_name_entry.pack(side="left", padx=10)
        
        self.user_name_label = ttk.Label(self.doc_user_frame, text="आप का नाम:", font=("Arial", 14))
        self.user_name_label.pack(side="left", padx=10)
        
        self.user_name_entry = ttk.Entry(self.doc_user_frame, font=("Arial", 12), width=30)
        self.user_name_entry.pack(side="left", padx=10)
        

        # Frame to hold the text widget (simulating A4 page)
        self.page_frame = tk.Frame(self.content_frame, bg="white", bd=5, relief="groove", width=800, height=800)
        self.page_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Text widget for notes
        self.notes_text = tk.Text(self.page_frame, wrap="word", font=("Arial", 12), bd=0, highlightthickness=0)
        self.notes_text.pack(fill="both", expand=True)
        
        # Add a vertical scrollbar
        self.scrollbar = tk.Scrollbar(self.content_frame, orient="vertical", command=self.notes_text.yview)
        self.scrollbar.place(relx=1, rely=0, relheight=1, anchor="ne")
        self.notes_text.config(yscrollcommand=self.scrollbar.set)
        


        
        


        
        # Footer
        self.footer_frame = tk.Frame(self.content_frame, bg="white")
        self.footer_frame.pack(side="bottom", fill="x", padx=20, pady=10)
        
        
        self.developer_label = tk.Label(self.footer_frame, text=f"All Rights Reserve to @ArjunSharma for more INFO Contact Arjunkumarsharma1228@gmail.com", font=("Arial", 10), bg="white")
        self.developer_label.pack(side="right")


        # Initialize clipboard content and serial number
        self.clipboard_content = ""
        self.serial_number = 1
        self.root.after(1000, self.monitor_clipboard)
        
        # File path for saving
        self.file_path = None
        
        # Show/Hide How to use widget
        self.how_to_use_visible = False
        
        







    def open_link(self, url):
        import webbrowser
        webbrowser.open(url)

    def monitor_clipboard(self):
        current_clipboard = self.root.clipboard_get()
        if current_clipboard != self.clipboard_content:
            self.clipboard_content = current_clipboard
            self.record_clipboard_content()
        self.root.after(1000, self.monitor_clipboard)
        
    nltk.download('wordnet')

    def record_clipboard_content(self):
        if self.clipboard_content.strip() != "":
            clipboard_content = self.clipboard_content.strip()
            if len(clipboard_content.split()) == 1:  # If copied content is a single word
                synsets = wordnet.synsets(clipboard_content)
                if synsets:
                    meaning = synsets[0].definition()
                    self.notes_text.insert("end", f"{self.serial_number}. [{clipboard_content}]: ({meaning})\n")
                else:
                    self.notes_text.insert("end", f"{self.serial_number}. [{clipboard_content}]: (No meaning found)\n")
            else:  # If copied content is a paragraph
                self.notes_text.insert("end", f"{self.serial_number}. {clipboard_content}\n")
            self.notes_text.insert("end", "-" * 50 + "\n")  # Insert horizontal line
            self.serial_number += 1

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r") as f:
                    content = f.read()
                    self.notes_text.delete("1.0", "end")
                    self.notes_text.insert("end", content)
                    self.file_path = file_path  # Store the file path
            except Exception as e:
                messagebox.showerror("Error", f"Dikkat hai yrr kuch open karne mai: {str(e)}")

    def save_file(self):
        if self.file_path:
            self.save_content()
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "w") as f:
                    f.write(self.notes_text.get("1.0", "end-1c"))
                self.file_path = file_path  # Update the file path
                messagebox.showinfo("Success", "Haa Bhaii...File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving the file: {str(e)}")

    def save_content(self):
        # Save the content using the stored file path
        try:
            with open(self.file_path, "w") as f:
                f.write(self.notes_text.get("1.0", "end-1c"))
            messagebox.showinfo("Success", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the file: {str(e)}")

    def save_as_pdf(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            try:
                doc_name = self.doc_name_entry.get() if self.doc_name_entry.get() else "Untitled Document"
                current_date = datetime.now().strftime("%d-%m-%y")
                user_name = self.user_name_entry.get() if self.user_name_entry.get() else "Unknown User"
                doc = SimpleDocTemplate(file_path, pagesize=letter)
                styles = getSampleStyleSheet()
                
                # Heading
                heading_text = f"{doc_name} ({current_date}) by {user_name}"
                heading = Paragraph(heading_text, styles["Heading1"])
                
                # Notes content
                notes_content = self.notes_text.get("1.0", "end-1c")
                notes = [heading, PageBreak()]  # Add page break after heading
                notes.extend([Paragraph(note.strip(), styles["Normal"]) for note in notes_content.split("\n")])
                
                doc.build(notes)
                messagebox.showinfo("Success", "Notes saved as PDF successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def export_as_text(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                # Get document name, date, and user name
                doc_name = self.doc_name_entry.get() if self.doc_name_entry.get() else "Untitled Document"
                current_date = datetime.now().strftime("%d-%m-%Y")
                user_name = self.user_name_entry.get() if self.user_name_entry.get() else "Unknown User"

                # Prepare content with document details
                content = f"Document Name: {doc_name}\nDate: {current_date}\nUser: {user_name}\n\n"
                content += self.notes_text.get("1.0", "end-1c")

                # Write content to file
                with open(file_path, "w") as f:
                    f.write(content)

                messagebox.showinfo("Success", "Haa BHaii!! Notes exported as plain text successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def export_as_html(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
        if file_path:
            # Code for exporting as HTML
            with open(file_path, "w") as f:
                f.write("<html><body>\n")
                f.write(self.notes_text.get("1.0", "end-1c"))
                f.write("\n</body></html>")
            messagebox.showinfo("Success", "Notes exported as HTML successfully!")

    def export_as_markdown(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown files", "*.md")])
        if file_path:
            # Code for exporting as Markdown
            with open(file_path, "w") as f:
                f.write(self.notes_text.get("1.0", "end-1c"))
            messagebox.showinfo("Success", "Notes exported as Markdown successfully!")

    def exit_app(self):
        self.root.destroy()
        
        
        
    def generate_qr_code_dialog(self):
        # Create a dialog box to enter the link
        link = simpledialog.askstring("Generate QR Code", "Enter the link:")

        if link:
            # Ask user to select the folder to save the QR code
            save_folder = filedialog.askdirectory(title="Select Folder to Save QR Code")

            if save_folder:
                # Generate QR code
                qr = qrcode.QRCode(version=1.9, box_size=20, border=5)
                qr.add_data(link)
                qr.make(fit=True)

                # Create image object
                qr_image = qr.make_image(fill_color="black", back_color="white")

                # Generate a unique file name for the QR code
                qr_code_name = f"qr_code_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"

                # Save QR code to the specified location
                qr_image.save(os.path.join(save_folder, qr_code_name))

                # Display success message with the name of the saved QR code file
                messagebox.showinfo("Success", f"QR Code '{qr_code_name}' saved successfully!")
        
        

        

    def show_about(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("About Note Taker")
        about_window.geometry("400x300")
        about_window.resizable(False, False)

        # App details
        details_frame = tk.Frame(about_window)
        details_frame.pack(pady=10)

        app_name_label = tk.Label(details_frame, text="Note Taker", font=("Arial", 16, "bold"))
        app_name_label.pack(pady=5)

        version_label = tk.Label(details_frame, text=f"Version: 2.5")
        version_label.pack(pady=2)

        description_label = tk.Label(details_frame, text="A simple and elegant note-taking app\nto capture your thoughts and ideas.", wraplength=300, justify="center")
        description_label.pack(pady=10)

        developer_label = tk.Label(details_frame, text=f"Developed by Arjun Sharma")
        developer_label.pack(pady=5)

        # Close button
        close_button = ttk.Button(about_window, text="Close", command=about_window.destroy)
        close_button.pack(pady=10)
        

        

    def share_via_email(self):
        # Prompt user for sender's email address
        sender_email = simpledialog.askstring("Sender's Email Address", "Enter your email address:")
    
        if not sender_email:
            messagebox.showwarning("Warning", "Sender's email address is required.")
            return
    
        # Prompt user for recipient's email address
        recipient_email = simpledialog.askstring("Recipient's Email Address", "Enter recipient's email address:")
    
        if not recipient_email:
            messagebox.showwarning("Warning", "Recipient's email address is required.")
            return
    
        # Capture content from the notes or document
        content = self.notes_text.get("1.0", "end-1c")
    
        try:
            # Compose email
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = "Shared Notes"
    
            body = f"Hello,\n\nPlease find the notes attached below:\n\n{content}"
            msg.attach(MIMEText(body, 'plain'))
    
            # Send email
            with smtplib.SMTP('smtp.example.com', 587) as server:
                server.starttls()
                server.login(sender_email, "your_password")
                server.sendmail(sender_email, recipient_email, msg.as_string())
    
            messagebox.showinfo("Success", "Notes shared via email successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while sending the email: {str(e)}")    
            


    def open_documentation(self):
        # Documentation content (replace with the actual content of your documentation)
        documentation_content = """
=======================================================================
                    Note Taker Desktop Application
=======================================================================

1. Introduction:
----------------
The Note Taker Desktop Application is a user-friendly and efficient tool designed to streamline the note-taking process for students. This application provides a convenient platform for capturing, organizing, and managing notes from various sources, ultimately enhancing productivity and study efficiency.

2. Features:
------------
   - Clipboard Integration: Seamlessly capture text from any source by copying it using the mouse or keyboard shortcut (Ctrl+C).
   - Intuitive User Interface: User-friendly interface with essential features readily accessible, ensuring a smooth and seamless experience.
   - File Management: Support for creating, opening, and saving notes, enabling efficient organization and easy access.
   - Flexible Export Options: Notes can be saved in multiple formats (plain text, PDF, HTML, Markdown) to suit different preferences and requirements.
   - Email Sharing: Built-in email sharing feature facilitates collaboration by allowing users to share notes directly via email from within the application.

3. Installation:
-----------------
   - Download the provided executable (.exe) file from the designated folder.
   - Run the executable file and follow the on-screen instructions to complete the installation process.
   - Once installed, the application is ready for use.

4. Usage:
----------
   - Upon launching the application, users are presented with a welcoming interface showcasing essential features and options.
   - To create a new note, simply copy text from any source using the mouse or Ctrl+C keyboard shortcut and paste it into the text editor within the application.
   - Existing notes can be opened, edited, and saved using familiar file operations.

5. File Formats:
------------------
   - Notes can be saved in various formats, including plain text (.txt), PDF (.pdf), HTML (.html), and Markdown (.md).
   - Users have the flexibility to choose the format that best meets their needs or preferences, ensuring compatibility with different platforms and applications.

6. Email Sharing:
-------------------
   - Collaboration and communication are facilitated with the built-in email sharing feature.
   - Users can compose emails directly within the application, attach notes in the desired format, and send them to recipients with a single click.

7. Customization:
-------------------
   - While the application's primary focus is on simplicity and functionality, users have the option to customize their experience.
   - This includes selecting themes, adjusting font preferences, and configuring keyboard shortcuts to suit individual preferences and workflow.

8. Conclusion:
----------------
The Note Taker Desktop Application is a valuable companion for students seeking to streamline their note-taking process and enhance study efficiency. With its intuitive interface, flexible export options, and built-in email sharing feature, the application is poised to become an indispensable tool for students across various academic disciplines.

=======================================================================

    
        """
    
        # Create a dialog box for documentation if it doesn't exist
        if not self.documentation_dialog or not tk.Toplevel.winfo_exists(self.documentation_dialog):
            self.documentation_dialog = tk.Toplevel(self.root)
            self.documentation_dialog.title("Documentation")
            self.documentation_dialog.geometry("800x600")
    
            # Add a scrolled text widget to display documentation content
            self.documentation_text = scrolledtext.ScrolledText(self.documentation_dialog, wrap=tk.WORD, font=("Arial", 12))
            self.documentation_text.pack(fill="both", expand=True)
    
            # Insert documentation content into the text widget
            self.documentation_text.insert("1.0", documentation_content)
    
            # Disable text editing
            self.documentation_text.config(state="disabled")
    
            # Allow the dialog box to be closed without terminating the application
            self.documentation_dialog.protocol("WM_DELETE_WINDOW", self.close_documentation_dialog)
    
        # Bring the dialog box to the front
        self.documentation_dialog.lift()
    
    def close_documentation_dialog(self):
        # Close the documentation dialog
        if self.documentation_dialog and tk.Toplevel.winfo_exists(self.documentation_dialog):
            self.documentation_dialog.destroy()
        
        


def main():
    root = tk.Tk()
    app = NoteTakerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

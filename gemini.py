import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import hashlib
import time
import os
import datetime
import threading
import secrets
import random
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import google.generativeai as genai
from tkinter import StringVar, OptionMenu

# Global variables
convo = None
model = None
malicious_hashes = []
# Cybersecurity facts
cybersecurity_facts = [
    "Did you know? The first computer virus was created in the early 1970s.",
    "Fact: Strong passwords are crucial for online security. Make sure to use a mix of letters, numbers, and symbols.",
    "Cybersecurity Tip: Keep your software up to date to protect against known vulnerabilities.",
    "Fact: Social engineering attacks often target human psychology to gain unauthorized access.",
    "Did you know? Two-factor authentication adds an extra layer of security by requiring two forms of identification.",
    "Creating strong passwords is your first line of defense against cyber threats. Use a mix of uppercase letters, lowercase letters, numbers, and symbols.",
    "Regularly update your software to patch security vulnerabilities. Keeping your applications and operating system up to date is crucial for a secure digital environment.",
    "Enable Two-Factor Authentication (2FA) whenever possible. It adds an extra layer of protection by requiring a second form of identification in addition to your password.",
    "Be cautious of phishing emails and messages. Cybercriminals often use social engineering techniques to trick individuals into revealing sensitive information.",
    "Regularly backup your important data. In case of a ransomware attack or data loss, having a recent backup can help you recover your files.",
    "Secure your Internet of Things (IoT) devices. Change default passwords and keep firmware updated to prevent unauthorized access to your smart devices.",
    "Use encryption to protect sensitive data. Encrypting your files and communications adds an extra layer of security, making it harder for unauthorized users to access your information.",
    "Develop an incident response plan. Knowing how to respond to a cybersecurity incident can minimize damage and downtime in case of an attack.",
    "Stay informed about cybersecurity threats. Continuous education on the latest threats and best practices is essential for maintaining a strong security posture.",
    "Secure your mobile devices. Set a strong password, enable biometric authentication, and install security apps to protect your smartphone and tablet.",
]

# Function to calculate file hash


def calculate_hash(file_path):
    try:
        with open(file_path, 'rb') as f:
            bytes = f.read()
            readable_hash = hashlib.sha256(bytes).hexdigest()
            return readable_hash
    except Exception as e:
        print(f"Unable to calculate hash for file: {file_path}. Error: {str(e)}")
        return None

# Function to get file info


def get_file_info(file_path):
    size = os.path.getsize(file_path)
    creation_time = os.path.getctime(file_path)
    creation_time = datetime.datetime.fromtimestamp(creation_time)
    modification_time = os.path.getmtime(file_path)
    modification_time = datetime.datetime.fromtimestamp(modification_time)
    return size, creation_time, modification_time

# Function to display a random cybersecurity fact


def display_cybersecurity_fact():
    random_fact = random.choice(cybersecurity_facts)
    messagebox.showinfo("Cybersecurity Fact", random_fact)

# Function to animate the progress bar


def animate_progress(start, end, steps, duration, progress_var, label_var):
    step_size = (end - start) / steps
    for i in range(steps):
        progress_var.set(start + i * step_size)
        label_var.configure(text=f"{progress_var.get():.2f}%")
        root.update_idletasks()
        time.sleep(duration / steps)

# Function to perform the file check


def perform_check(file_path, progress_var, label_var):
    progress_bar.start()
    loading_label.pack(pady=5)
    animate_progress(0, 100, 5, 2, progress_var, label_var)  # Animate the progress bar
    
    # Get file details
    file_hash = calculate_hash(file_path)
    size, creation_time, modification_time = get_file_info(file_path)

    # Check if the file is malicious
    dangerous_extensions = [".exe", ".bat", ".cmd", ".ps1", ".vbs", ".js"]
    if file_hash in malicious_hashes:
        result = f"File: {file_path}\nSize: {size} bytes\nCreation Time: {creation_time}\nModification Time: {modification_time}\nHash: {file_hash}\nStatus: Malicious."
        is_malicious = "Yes"
    elif any(file_path.endswith(ext) for ext in dangerous_extensions):
        result = f"File: {file_path}\nSize: {size} bytes\nCreation Time: {creation_time}\nModification Time: {modification_time}\nHash: {file_hash}\nStatus: Potentially dangerous extension, but its hash doesn't match any known malicious hashes."
        is_malicious = "No, but has potentially dangerous extension"
    else:
        result = f"File: {file_path}\nSize: {size} bytes\nCreation Time: {creation_time}\nModification Time: {modification_time}\nHash: {file_hash}\nStatus: Safe."
        is_malicious = "No"

# Integrate Google Generative AI
    global convo, model
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)

        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_ONLY_HIGH"
            }
        ]

        model = genai.GenerativeModel(model_name="gemini-pro",
                                         generation_config=generation_config,
                                         safety_settings=safety_settings)
        convo = model.start_chat(history=[])
        convo.send_message(
            f"Summarize this file scan result in 2 lines and suggest one safety tip: {result}"
        )
        chatbot_response = convo.last.text
    else:
        chatbot_response = "Set GEMINI_API_KEY to enable Help Bot responses."

    # Display the result in the chat output text box
    chat_output_text.insert(tk.END, result + "\n\n")
    chat_output_text.insert(tk.END, "Help Bot: " + chatbot_response + "\n\n")

# Function to start the chatbot conversation


def start_chatbot_conversation(chat_input_field, chat_output_text):
    global convo
    convo = model.start_chat(history=[])

    # Calculate the result (replace this with your actual result calculation logic)
    result = "Some result based on your logic"

    # Get the chatbot's response
    if convo.last is not None:
        chatbot_response = convo.last.text
    else:
        chatbot_response = "No response from the chatbot."

    # Display the result in the chat output text box
    chat_output_text.insert(tk.END, result + "\n\n")
    chat_output_text.insert(tk.END, "Chatbot Response: " + chatbot_response + "\n\n")

    return result
def save_key_to_file(key, filename):
    with open(filename, 'wb') as file:
        file.write(key)

def encrypt_file():
    # Ask the user to select the input file
    input_file = filedialog.askopenfilename(title="Select Input File")
    if not input_file:
        return

    # Check for malicious behavior
    progress_var.set(0)
    percentage_label.config(text="0.00%")
    root.update_idletasks()
    
    # Perform the file check before encryption
    check_result = perform_check_before_encryption(input_file)

    if check_result == "Malicious":
        # Display a message indicating the file is malicious
        messagebox.showerror("Malicious File", "The selected file is malicious. Encryption cannot be performed.")
        return
    elif check_result == "Dangerous Extension":
        # Display a message indicating the file has a potentially dangerous extension
        messagebox.showwarning("Potentially Dangerous File", "The selected file has a potentially dangerous extension, but its hash doesn't match any known malicious hashes. Proceed with caution.")
    
    # Continue with the encryption process
    output_file = filedialog.asksaveasfilename(title="Save Encrypted File", defaultextension=".aes")
    if not output_file:
        return

    generate_random_key = messagebox.askyesno("Generate Random Key", "Do you want to generate a random key?")
    if generate_random_key:
        key = secrets.token_bytes(32)
    else:
        key = simpledialog.askstring("Encryption Key", "Enter Encryption Key")
        if key is None:
            return
        key = key.encode()

    # Update progress bar and label
    progress_var.set(50)  # Set to 50% to show progress during encryption
    percentage_label.config(text="50.00%")
    root.update_idletasks()

    try:
        backend = default_backend()
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()

        with open(input_file, 'rb') as file:
            plaintext = file.read()
            padded_data = padder.update(plaintext) + padder.finalize()
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        with open(output_file, 'wb') as file:
            file.write(ciphertext)

        key_file = output_file + ".key"
        save_key_to_file(key, key_file)

        # Complete progress bar
        progress_var.set(100)
        percentage_label.config(text="100.00%")
        root.update_idletasks()

        messagebox.showinfo("Success", "File encrypted successfully. Key saved to: " + key_file)
        display_cybersecurity_fact()  # Display a random cybersecurity fact
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to perform the file check before encryption
def perform_check_before_encryption(file_path):
    # Modify this function to perform the necessary file check before encryption
    # You can reuse the existing logic from the perform_check function

    # Example: Check if the file is malicious
    file_hash = calculate_hash(file_path)
    if file_hash in malicious_hashes:
        return "Malicious"
    
    # Example: Check if the file has a potentially dangerous extension
    dangerous_extensions = [".exe", ".bat", ".cmd", ".ps1", ".vbs", ".js"]
    if any(file_path.endswith(ext) for ext in dangerous_extensions):
        return "Dangerous Extension"
    
    # If the file is not identified as malicious or having a dangerous extension, return None or any other indicator
    return None

# Function to decrypt a file


def decrypt_file():
    input_file = filedialog.askopenfilename(title="Select Input File")
    if not input_file:
        return
    output_file = filedialog.asksaveasfilename(title="Save Decrypted File", defaultextension=".txt")
    if not output_file:
        return
    key_file = filedialog.askopenfilename(title="Select Key File")
    if not key_file:
        return

    # Update progress bar and label
    progress_var.set(50)  # Set to 50% to show progress during decryption
    percentage_label.config(text="50.00%")
    root.update_idletasks()
    try:
        backend = default_backend()
        cipher = Cipher(algorithms.AES(load_key_from_file(key_file)), modes.ECB(), backend=backend)
        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        with open(input_file, 'rb') as file:
            ciphertext = file.read()
            decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
            unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
        with open(output_file, 'wb') as file:
            file.write(unpadded_data)

        # Complete progress bar
        progress_var.set(100)  # Set to 100% to complete the progress bar
        percentage_label.config(text="100.00%")
        root.update_idletasks()
        messagebox.showinfo("Success", "File decrypted successfully.")
        display_cybersecurity_fact()  # Display a random cybersecurity fact
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to save file info to a text file


def save_file_info():
    filename = filedialog.asksaveasfilename(defaultextension=".txt")
    if not filename:
        return
    with open(filename, "w") as f:
        f.write("Hash: " + str(file_info["hash"]) + "\n")

# Function to load the key from a file
def load_key_from_file(filename):
    with open(filename, 'rb') as file:
        return file.read()

# Read malicious hashes from a text file


hashes_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hashes.txt")
if os.path.exists(hashes_file):
    with open(hashes_file, 'r') as f:
        malicious_hashes = [line.strip() for line in f if line.strip()]

# Create the main window


root = tk.Tk()
root.title("File Analysis and Security")
root.geometry("1200x1000")

# Default dark mode theme


root.configure(bg="black")

# Create a text box for the chatbot's outp

# Create a chatbot input field
chat_input_field = tk.Entry(root, width=0,bg="black")  # Adjust the width as needed

# Create a function to send a message when the "Send" button is clicked
def send_message():
    send_chatbot_message(None)  # Call the existing send_chatbot_message function

# Function to send a message to the chatbot and display the response


def send_chatbot_message(event):
    global convo
    if convo is not None:
        # Get the user's message from the input field
        user_message = chat_input_field.get()
        # Clear the input field
        chat_input_field.delete(0, tk.END)
        # Send the user's message to the chatbot
        convo.send_message(user_message)
        # Get the chatbot's response
        chatbot_response = convo.last.text
        # Display the chatbot's response in the chat output text box
        chat_output_text.insert(tk.END, "You: " + user_message + "\n")
        chat_output_text.insert(tk.END, "Chatbot Response: " + chatbot_response + "\n\n")

# Bind the Enter key to the send_chatbot_message function
chat_input_field.bind("<Return>", send_chatbot_message)
chat_input_field.pack(pady=10)

# Create a label
label = tk.Label(root, text="PLEASE CHOOSE AN ACTION AND UPLOAD A FILE.", bg="black", fg="blue",font=("Segoe Script", 16))
label.pack(pady= 10)
# Create buttons for actions
check_button = tk.Button(root, text="Check for Malicious Behavior", command=lambda: perform_check(filedialog.askopenfilename(), progress_var, percentage_label),bg="light blue",fg="black",font=("Times New Roman",14))
check_button.pack(pady=10)
encrypt_button = tk.Button(root, text="Encrypt File", command=encrypt_file, bg="red", fg="black",font=("Times New Roman",14))
encrypt_button.pack(pady=10)
decrypt_button = tk.Button(root, text="Decrypt File", command=decrypt_file, bg="green", fg="black",font=("Times New Roman",14))
decrypt_button.pack(pady=10)
# Create a label for the chat input box
chat_input_label = tk.Label(root, text="HelpBox💡", bg="black", fg="white",font=("Times New Roman",10))
chat_input_label.pack(pady=1)
# Create a chatbot input field
chat_input_field = tk.Entry(root, width=80)  # Adjust the width as needed
chat_input_field.pack(pady=10)

# Create a StringVar to store the selected FAQ
selected_faq = StringVar()
selected_faq.set("Select FAQ")  # Default value

# Pre-defined FAQs
faqs = [
    "Select FAQ",
    "What is AES",
    "How is AES better than other algorithms",
    "What is a file hash",
    "how does encryption work",
    "How does decryption work",
    "Can I trust the chatbot responses",
    "How can I get more information about cybersecurity?",
    "What are the dangerous file extensions",
    "Tell me a cybersecurity tip",
]

# Create a dropdown menu for FAQs
faq_dropdown = OptionMenu(root, selected_faq, *faqs)
faq_dropdown.pack(pady=5)

# Create a "Send" button
send_button = tk.Button(root, text="Send", command=send_message, bg="darkgray", fg="black")
send_button.pack(pady=10)

# Function to handle FAQ selection
def on_faq_select(*args):
    selected_message = selected_faq.get()
    if selected_message != "Select FAQ":
        chat_input_field.delete(0, tk.END)
        chat_input_field.insert(tk.END, selected_message)

# Bind the callback function to the FAQ dropdown
selected_faq.trace_add("write", on_faq_select)

# Create a text box for the chatbot's output
chat_output_text = tk.Text(root, wrap=tk.WORD, width=160, height=20, bg="black", fg="white",font=("Sans Serif",14))
chat_output_text.pack(pady=30)


# Create a progress bar and label


progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=200, mode='determinate', variable=progress_var)
progress_bar.pack()
percentage_label = tk.Label(root, text="0.00%", bg="black", fg="white")
percentage_label.pack()

# Loading icon label


loading_label = ttk.Label(root, text="Loading...", style="TLabel", font="Arial 10 bold", foreground="white", background="black")

# Start the main GUI loop


root.mainloop()


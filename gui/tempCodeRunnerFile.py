import customtkinter as ctk
from tkinter import filedialog, messagebox
from backend.hash_router import route_hash
from backend.md4_handler import forge_md4
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Hash Forgery Tool")
app.geometry("700x600")

selected_file = None

# ------------ Functions ------------
def browse_file():
    global selected_file
    selected_file = filedialog.askopenfilename()
    if selected_file:
        file_label.configure(text=os.path.basename(selected_file))

def get_hash_function(name):
    return {
        "MD2": MD2,
        "MD4": MD4,
        "MD5": MD5,
        "SHA1": SHA1
    }.get(name, None)

def forge():
    if not selected_file:
        messagebox.showerror("Error", "No file selected.")
        return

    hash_name = hash_dropdown.get()
    content = inject_textbox.get("1.0", "end").encode()

    try:
        with open(selected_file, "rb") as f:
            original_data = f.read()

        original_hash = route_hash(hash_name, original_data)
        forged_data = original_data + content
        forged_hash = route_hash(hash_name, forged_data)

        original_hash_var.set(original_hash)
        forged_hash_var.set(forged_hash)

        app.forged_data = forged_data
        match = "✅ Match" if original_hash == forged_hash else "❌ Not Matching"
        match_label.configure(text=match, text_color="green" if match.startswith("✅") else "red")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def download_forged():
    if not hasattr(app, "forged_data"):
        messagebox.showwarning("Warning", "Nothing to save yet!")
        return
    save_path = filedialog.asksaveasfilename(defaultextension=".bin")
    if save_path:
        with open(save_path, "wb") as f:
            f.write(app.forged_data)
        messagebox.showinfo("Saved", f"Forged file saved to:\n{save_path}")

# ------------ Widgets ------------
title = ctk.CTkLabel(app, text="🔐 Hash Forgery Tool", font=ctk.CTkFont(size=24, weight="bold"))
title.pack(pady=20)

file_frame = ctk.CTkFrame(app)
file_frame.pack(pady=10)
ctk.CTkLabel(file_frame, text="📁 Upload File:").pack(side="left", padx=5)
ctk.CTkButton(file_frame, text="Browse", command=browse_file).pack(side="left")
file_label = ctk.CTkLabel(file_frame, text="No file selected")
file_label.pack(side="left", padx=10)

hash_dropdown = ctk.CTkOptionMenu(app, values=["MD2", "MD4", "MD5", "SHA1"])
hash_dropdown.set("MD5")
hash_dropdown.pack(pady=10)
ctk.CTkLabel(app, text="Hash Function").pack()

ctk.CTkLabel(app, text="📝 Inject Content Below").pack(pady=(10, 0))
inject_textbox = ctk.CTkTextbox(app, width=500, height=100)
inject_textbox.pack()

ctk.CTkButton(app, text="🚀 Forge Now", command=forge).pack(pady=15)

output_frame = ctk.CTkFrame(app)
output_frame.pack(pady=10)

original_hash_var = ctk.StringVar()
forged_hash_var = ctk.StringVar()

ctk.CTkLabel(output_frame, text="Original Hash:").grid(row=0, column=0, sticky="e", padx=5)
ctk.CTkEntry(output_frame, textvariable=original_hash_var, width=400).grid(row=0, column=1)

ctk.CTkLabel(output_frame, text="Forged Hash:").grid(row=1, column=0, sticky="e", padx=5)
ctk.CTkEntry(output_frame, textvariable=forged_hash_var, width=400).grid(row=1, column=1)

match_label = ctk.CTkLabel(app, text="", font=ctk.CTkFont(size=16))
match_label.pack(pady=5)

ctk.CTkButton(app, text="📥 Download Forged File", command=download_forged).pack(pady=20)

app.mainloop()

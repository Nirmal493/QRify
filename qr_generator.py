import qrcode
from tkinter import *
from tkinter import messagebox, colorchooser, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
from datetime import datetime

# ----- Generate QR -----
def generate_qr():
    text = data_entry.get()
    title = title_entry.get()

    if not text.strip():
        messagebox.showerror("Input Error", "Please enter text or URL for QR generation.")
        return

    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill=fg_color.get(), back_color=bg_color.get()).convert('RGB')
    img = img.resize((250, 250))

    if title:
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        w, h = draw.textsize(title, font)
        draw.rectangle([0, 0, 250, 20], fill=bg_color.get())
        draw.text(((250 - w) / 2, 2), title, fill=fg_color.get(), font=font)

    img.save("preview.png")
    img_tk = ImageTk.PhotoImage(img)
    qr_label.config(image=img_tk)
    qr_label.image = img_tk

    save_btn.config(state=NORMAL)

# ----- Save QR -----
def save_qr():
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = filedialog.asksaveasfilename(defaultextension=".png", 
                    initialfile=f"qr_{now}.png", filetypes=[("PNG File", "*.png")])
    if file_path:
        img = Image.open("preview.png")
        img.save(file_path)
        messagebox.showinfo("Success", "QR Code saved successfully!")

# ----- Color Picker -----
def choose_fg():
    color = colorchooser.askcolor(title="Choose QR color")
    if color[1]:
        fg_color.set(color[1])
        fg_display.config(bg=color[1])

def choose_bg():
    color = colorchooser.askcolor(title="Choose background color")
    if color[1]:
        bg_color.set(color[1])
        bg_display.config(bg=color[1])

# ----- GUI Setup -----
root = Tk()
root.title("QRify - QR Code Generator")
root.geometry("450x600")
root.resizable(False, False)
root.config(bg="#f7f7f7")

Label(root, text="QRify", font=("Arial", 24, "bold"), fg="#333", bg="#f7f7f7").pack(pady=10)
Label(root, text="Enter Text or URL", font=("Arial", 12), bg="#f7f7f7").pack()
data_entry = Entry(root, font=("Arial", 12), width=35, bd=2, relief=GROOVE)
data_entry.pack(pady=5)

Label(root, text="Add a Label (Optional)", font=("Arial", 12), bg="#f7f7f7").pack()
title_entry = Entry(root, font=("Arial", 12), width=35, bd=2, relief=GROOVE)
title_entry.pack(pady=5)

# Color Options
fg_color = StringVar(value="black")
bg_color = StringVar(value="white")

color_frame = Frame(root, bg="#f7f7f7")
color_frame.pack(pady=10)

Label(color_frame, text="QR Color:", font=("Arial", 12), bg="#f7f7f7").grid(row=0, column=0, padx=5)
fg_display = Label(color_frame, bg=fg_color.get(), width=3, relief=SUNKEN)
fg_display.grid(row=0, column=1)
Button(color_frame, text="Choose", command=choose_fg).grid(row=0, column=2, padx=10)

Label(color_frame, text="Background:", font=("Arial", 12), bg="#f7f7f7").grid(row=1, column=0, padx=5)
bg_display = Label(color_frame, bg=bg_color.get(), width=3, relief=SUNKEN)
bg_display.grid(row=1, column=1)
Button(color_frame, text="Choose", command=choose_bg).grid(row=1, column=2, padx=10)

# Buttons
Button(root, text="Generate QR", font=("Arial", 14), bg="#4CAF50", fg="white", command=generate_qr).pack(pady=10)

qr_label = Label(root, bg="#f7f7f7")
qr_label.pack(pady=10)

save_btn = Button(root, text="Save QR", font=("Arial", 14), bg="#2196F3", fg="white", state=DISABLED, command=save_qr)
save_btn.pack(pady=10)

root.mainloop()

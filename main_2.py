import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
import qrcode
from PIL import Image, ImageTk

def generate_qr_code():
    url = url_entry.get()
    file_path = file_path_entry.get()
    fill_color = fill_color_entry.get()
    back_color = back_color_entry.get()
    logo_path = logo_path_entry.get()

    if not url or not file_path:
        messagebox.showerror("Error", "URL and File Path are required")
        return

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGB')

    if logo_path:
        try:
            logo = Image.open(logo_path)
            logo_size = (img.size[0] // 3, img.size[1] // 3)
            logo = logo.resize(logo_size, Image.LANCZOS)
            logo_position = ((img.size[0] - logo_size[0]) // 2, (img.size[1] - logo_size[1]) // 2)
            img.paste(logo, logo_position, mask=logo)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add logo: {e}")
            return

    img.save(file_path)
    img_tk = ImageTk.PhotoImage(img)
    qr_label.config(image=img_tk)
    qr_label.image = img_tk

def browse_file_path():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, file_path)

def browse_logo_path():
    logo_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    logo_path_entry.delete(0, tk.END)
    logo_path_entry.insert(0, logo_path)

def choose_fill_color():
    color = colorchooser.askcolor()[1]
    if color:
        fill_color_entry.delete(0, tk.END)
        fill_color_entry.insert(0, color)
        fill_color_preview.config(bg=color)

def choose_back_color():
    color = colorchooser.askcolor()[1]
    if color:
        back_color_entry.delete(0, tk.END)
        back_color_entry.insert(0, color)
        back_color_preview.config(bg=color)

root = tk.Tk()
root.title("QR Code Generator")

# Frame for URL and File Path
frame1 = tk.Frame(root)
frame1.grid(row=0, column=0, padx=10, pady=10)

tk.Label(frame1, text="URL:").grid(row=0, column=0, sticky=tk.W)
url_entry = tk.Entry(frame1, width=50)
url_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

tk.Label(frame1, text="File Path:").grid(row=1, column=0, sticky=tk.W)
file_path_entry = tk.Entry(frame1, width=50)
file_path_entry.grid(row=1, column=1, padx=5, pady=5)
tk.Button(frame1, text="Browse", command=browse_file_path).grid(row=1, column=2, padx=5, pady=5)

# Frame for Colors
frame2 = tk.Frame(root)
frame2.grid(row=1, column=0, padx=10, pady=10)

tk.Label(frame2, text="Fill Color:").grid(row=0, column=0, sticky=tk.W)
fill_color_entry = tk.Entry(frame2, width=50)
fill_color_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame2, text="Choose", command=choose_fill_color).grid(row=0, column=2, padx=5, pady=5)
fill_color_preview = tk.Label(frame2, width=2, bg="white")
fill_color_preview.grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame2, text="Background Color:").grid(row=1, column=0, sticky=tk.W)
back_color_entry = tk.Entry(frame2, width=50)
back_color_entry.grid(row=1, column=1, padx=5, pady=5)
tk.Button(frame2, text="Choose", command=choose_back_color).grid(row=1, column=2, padx=5, pady=5)
back_color_preview = tk.Label(frame2, width=2, bg="white")
back_color_preview.grid(row=1, column=3, padx=5, pady=5)

# Frame for Logo Path
frame3 = tk.Frame(root)
frame3.grid(row=2, column=0, padx=10, pady=10)

tk.Label(frame3, text="Logo Path:").grid(row=0, column=0, sticky=tk.W)
logo_path_entry = tk.Entry(frame3, width=50)
logo_path_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame3, text="Browse", command=browse_logo_path).grid(row=0, column=2, padx=5, pady=5)

# Frame for Generate Button and QR Code
frame4 = tk.Frame(root)
frame4.grid(row=3, column=0, padx=10, pady=10)

tk.Button(frame4, text="Generate QR Code", command=generate_qr_code).grid(row=0, column=0, columnspan=4, pady=10)
qr_label = tk.Label(frame4)
qr_label.grid(row=1, column=0, columnspan=4, pady=10)

root.mainloop()
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont

def get_text_size(font, text):
    bbox = font.getbbox(text)
    return (bbox[2] - bbox[0], bbox[3] - bbox[1])

def generate_college_id_card(student_info, photo_path):
    width, height = 400, 350
    id_card = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(id_card)

    try:
        small_font = ImageFont.truetype("arial.ttf", 12)
        medium_font = ImageFont.truetype("arial.ttf", 14)
        large_font = ImageFont.truetype("arial.ttf", 16)
    except:
        small_font = medium_font = large_font = ImageFont.load_default()

    default_font = ImageFont.load_default()
    text_color = (0, 0, 122)
    govt_text_color = (0, 128, 0)

    # Headers
    govt_text = "Govt. of Bihar"
    w, h = get_text_size(small_font, govt_text)
    draw.text(((width - w) // 2, 10), govt_text, font=small_font, fill=govt_text_color)

    dept_text = "Department of Science & Technology"
    w, h2 = get_text_size(small_font, dept_text)
    draw.text(((width - w) // 2, 10 + h + 5), dept_text, font=small_font, fill=text_color)

    college_text = "GAYA COLLEGE OF ENGINEERING, GAYA"
    w, h3 = get_text_size(large_font, college_text)
    draw.text(((width - w) // 2, 10 + h + h2 + 10), college_text, font=large_font, fill=text_color)

    address_text = "Sri Krishan Nagar P.O Nagriyawan Khizersari, Gaya-823003"
    w, h4 = get_text_size(small_font, address_text)
    draw.text(((width - w) // 2, 10 + h + h2 + h3 + 15), address_text, font=small_font, fill=text_color)

    # ID Card Banner
    student_id_text = "STUDENT IDENTITY CARD"
    w, h5 = get_text_size(medium_font, student_id_text)
    rect_x1, rect_y1 = (width - w) // 2 - 5, 10 + h + h2 + h3 + h4 + 20 - 5
    rect_x2, rect_y2 = rect_x1 + w + 10, rect_y1 + h5 + 10
    draw.rectangle([rect_x1, rect_y1, rect_x2, rect_y2], fill="purple")
    draw.text(((width - w) // 2, rect_y1 + 5), student_id_text, font=medium_font, fill="white")

    # Student photo
    photo = Image.open(photo_path).resize((70, 80))
    photo_position = (width - 80, rect_y2 + 15)
    id_card.paste(photo, photo_position)

    # Student details
    info_x = 10
    y = rect_y2 + 15
    draw.text((info_x, y), "NAME: " + student_info['NAME'], font=default_font, fill=text_color); y += 25
    draw.text((info_x, y), "F_NAME: " + student_info['F_NAME'], font=default_font, fill=text_color); y += 25
    draw.text((info_x, y), "Roll NO: " + 'x' * len(student_info['roll_no']), font=default_font, fill=text_color); y += 25
    draw.text((info_x, y), "BRANCH: " + student_info['Branch'], font=default_font, fill=text_color); y += 25
    draw.text((info_x, y), "SESSION: " + student_info['Session'], font=default_font, fill=text_color); y += 25

    draw.text((info_x, y), "BLOOD GROUP: ", font=default_font, fill=text_color)
    blood_w, _ = get_text_size(default_font, "BLOOD GROUP: ")
    draw.text((info_x + blood_w, y), student_info['blood_group'], font=default_font, fill=(255, 0, 0))
    draw.text((info_x + blood_w + 50, y), "DOB: " + student_info['DOB'], font=default_font, fill=text_color); y += 25
    draw.text((info_x, y), "Add.: " + student_info['ADD.'], font=default_font, fill=text_color)

    return id_card

# GUI
def submit_form():
    student_info = {
        'NAME': name_var.get(),
        'F_NAME': fname_var.get(),
        'roll_no': roll_var.get(),
        'Branch': branch_var.get(),
        'Session': session_var.get(),
        'blood_group': blood_var.get(),
        'DOB': dob_var.get(),
        'ADD.': addr_var.get()
    }
    photo_path = filedialog.askopenfilename(title="Select Student Photo", filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
    id_card = generate_college_id_card(student_info, photo_path)
    id_card.save("generated_id_card.jpg")
    id_card.show()

# Create form
root = tk.Tk()
root.title("Student ID Card Generator")

labels = ["Name", "Father's Name", "Roll No", "Branch", "Session", "Blood Group", "DOB", "Address"]
entries = []
name_var, fname_var, roll_var, branch_var, session_var, blood_var, dob_var, addr_var = [tk.StringVar() for _ in range(8)]

for i, label_text in enumerate(labels):
    tk.Label(root, text=label_text).grid(row=i, column=0, sticky="e")
    entry = tk.Entry(root, width=40, textvariable=[name_var, fname_var, roll_var, branch_var, session_var, blood_var, dob_var, addr_var][i])
    entry.grid(row=i, column=1)
    entries.append(entry)

tk.Button(root, text="Generate ID Card", command=submit_form).grid(row=len(labels), column=0, columnspan=2, pady=10)

root.mainloop()

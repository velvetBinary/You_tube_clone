import tkinter as tk
from tkinter import messagebox, Scrollbar
from PIL import Image, ImageTk
import os

class YouTubeClone:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1280x720")
        self.root.title("Fake YouTube")
        self.theme = "light"
        self.root.configure(bg="#f9f9f9")

        self.videos = [
            ("thumb1.jpg", "Cat Invasion", "CatNews", "1.2M views", "12:45"),
            ("thumb2.jpg", "Morning Workout", "FitDaily", "890K views", "10:00"),
            ("thumb3.jpg", "Study With Me", "QuietRoom", "2.1M views", "1:59:32"),
            ("thumb4.jpg", "Coding Mistakes", "CodeCraft", "712K views", "7:13"),
            ("thumb5.jpg", "SpaceX Recap", "GalacticNow", "3.4M views", "9:48"),
            ("thumb6.jpg", "Lo-fi Mix", "Beats&Vibes", "4.5M views", "2:03:00"),
        ]

        self.shorts = [
            ("short1.jpg", "Meow!"),
            ("short2.jpg", "1 Min Abs!"),
            ("short3.jpg", "Coding Hack"),
            ("short4.jpg", "Starship Lift"),
            ("short5.jpg", "Lo-fi chill"),
        ]

        self.setup_ui()

    def setup_ui(self):
        self.create_sidebar()
        self.create_topbar()
        self.create_categories()
        self.create_video_grid()
        self.create_shorts_strip()

    def create_sidebar(self):
        sidebar = tk.Frame(self.root, bg="#ffffff", width=150)
        sidebar.pack(side="left", fill="y")

        buttons = ["🏠 Home", "🎬 Shorts", "📺 Subscriptions", "📚 Library", "🕒 History"]
        for btn in buttons:
            tk.Button(sidebar, text=btn, font=("Segoe UI", 10), bg="#ffffff", relief="flat", anchor="w", padx=10).pack(fill="x", pady=5)

    def create_topbar(self):
        navbar = tk.Frame(self.root, bg="#ffffff", height=60)
        navbar.pack(fill="x", side="top")

        logo = tk.Label(navbar, text="▶ YouTube", font=("Segoe UI", 18, "bold"), fg="#FF0000", bg="#ffffff")
        logo.pack(side="left", padx=15)

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(navbar, textvariable=self.search_var, font=("Segoe UI", 12), width=40, relief="flat", bd=2)
        search_entry.pack(side="left", padx=10, ipady=5)

        search_btn = tk.Button(navbar, text="🔍", command=self.search_video, bg="#eeeeee", font=("Arial", 12), relief="flat")
        search_btn.pack(side="left")

        upload_btn = tk.Button(navbar, text="⬆ Upload", font=("Segoe UI", 11), bg="#ffffff", relief="flat")
        upload_btn.pack(side="right", padx=10)

        self.theme_btn = tk.Button(navbar, text="🌙", command=self.toggle_theme, bg="#ffffff", relief="flat", font=("Arial", 12))
        self.theme_btn.pack(side="right")

        profile_btn = tk.Button(navbar, text="👤", bg="#ffffff", font=("Arial", 12), relief="flat")
        profile_btn.pack(side="right", padx=10)

    def create_categories(self):
        cat_frame = tk.Frame(self.root, bg=self.root["bg"])
        cat_frame.pack(fill="x", padx=170, pady=5)

        categories = ["All", "Trending", "Music", "Live", "News", "Gaming"]
        for cat in categories:
            btn = tk.Button(cat_frame, text=cat, font=("Segoe UI", 10), bg="#e6e6e6", relief="flat", padx=10, pady=5)
            btn.pack(side="left", padx=5)

    def create_video_grid(self):
        grid_frame = tk.Frame(self.root, bg=self.root["bg"])
        grid_frame.pack(padx=170, pady=(10, 0), fill="both", expand=False)

        for index, (file, title, channel, views, duration) in enumerate(self.videos):
            row = index // 3
            col = index % 3
            card = self.create_video_card(grid_frame, file, title, channel, views, duration)
            card.grid(row=row, column=col, padx=15, pady=15)

    def create_video_card(self, parent, img_file, title, channel, views, duration):
        frame = tk.Frame(parent, bg="#ffffff", width=260, height=250, relief="raised", bd=1)
        frame.propagate(False)

        try:
            img = Image.open(img_file).resize((260, 150))
            photo = ImageTk.PhotoImage(img)
        except:
            photo = ImageTk.PhotoImage(Image.new("RGB", (260, 150), color="gray"))

        thumb_label = tk.Label(frame, image=photo, bg="#ffffff")
        thumb_label.image = photo
        thumb_label.pack()

        # Duration overlay
        duration_lbl = tk.Label(frame, text=duration, bg="black", fg="white", font=("Arial", 8), padx=4, pady=1)
        duration_lbl.place(in_=thumb_label, relx=1.0, rely=1.0, anchor="se", x=-5, y=-5)

        title_label = tk.Label(frame, text=title, bg="#ffffff", font=("Segoe UI", 11, "bold"), wraplength=240, anchor="w", justify="left")
        title_label.pack(padx=5, anchor="w")

        channel_label = tk.Label(frame, text=f"{channel} • {views}", bg="#ffffff", fg="gray", font=("Segoe UI", 9))
        channel_label.pack(padx=5, anchor="w")

        for widget in (frame, thumb_label, title_label):
            widget.bind("<Button-1>", lambda e: self.show_popup(title, channel, views))

        return frame

    def create_shorts_strip(self):
        shorts_label = tk.Label(self.root, text="Shorts", font=("Segoe UI", 14, "bold"), bg=self.root["bg"])
        shorts_label.pack(anchor="w", padx=170, pady=(20, 5))

        canvas = tk.Canvas(self.root, height=200, bg=self.root["bg"], highlightthickness=0)
        canvas.pack(fill="x", padx=170)

        shorts_frame = tk.Frame(canvas, bg=self.root["bg"])
        canvas.create_window((0, 0), window=shorts_frame, anchor="nw")

        for file, title in self.shorts:
            frame = tk.Frame(shorts_frame, bg="#ffffff", width=140, height=180, relief="raised", bd=1)
            frame.propagate(False)

            try:
                img = Image.open(file).resize((140, 100))
                photo = ImageTk.PhotoImage(img)
            except:
                photo = ImageTk.PhotoImage(Image.new("RGB", (140, 100), color="gray"))

            img_label = tk.Label(frame, image=photo, bg="#ffffff")
            img_label.image = photo
            img_label.pack()

            title_label = tk.Label(frame, text=title, font=("Segoe UI", 10, "bold"), bg="#ffffff", wraplength=120)
            title_label.pack(pady=5)

            frame.pack(side="left", padx=10)

        shorts_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        x_scroll = Scrollbar(self.root, orient="horizontal", command=canvas.xview)
        canvas.configure(xscrollcommand=x_scroll.set)
        x_scroll.pack(fill="x", padx=170)

    def show_popup(self, title, channel, views):
        messagebox.showinfo(
            title=title,
            message=f"{title}\n\nBy: {channel}\nViews: {views}\n\nDescription:\nThis is a fake popup for a fake video."
        )

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.root.configure(bg="#1e1e1e" if self.theme == "dark" else "#f9f9f9")
        self.theme_btn.config(text="☀️" if self.theme == "dark" else "🌙")
        for widget in self.root.winfo_children():
            widget.destroy()
        self.setup_ui()

    def search_video(self):
        query = self.search_var.get().strip()
        if query:
            print(f"Searching for: {query}")
        else:
            messagebox.showinfo("Empty", "Type something to search!")

# Launch
if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeClone(root)
    root.mainloop()

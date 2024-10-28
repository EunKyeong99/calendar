import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel
import calendar
from datetime import datetime

class MyScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("My Scheduler")
        self.root.geometry("400x600")

        self.year = datetime.now().year
        self.month = datetime.now().month
        self.schedules = {}

        self.category_colors = {
            "업무": "lightgreen",
            "기념일": "lightcoral",
            "개인 일정": "lightyellow"
        }

        self.create_widgets()

    def create_widgets(self):
        self.header_frame = tk.Frame(self.root)
        self.header_frame.pack(pady=10)

        self.year_label = tk.Label(self.header_frame, text=f"{self.year}년", font=("Arial", 16))
        self.year_label.pack()

        self.month_frame = tk.Frame(self.root)
        self.month_frame.pack(pady=5)

        self.prev_button = tk.Button(self.month_frame, text="◀", command=self.before_month, width=5)
        self.prev_button.grid(row=0, column=0, padx=5)

        self.month_label = tk.Label(self.month_frame, text=f"{self.month}월", font=("Arial", 14))
        self.month_label.grid(row=0, column=1, padx=5)

        self.next_button = tk.Button(self.month_frame, text="▶", command=self.next_month, width=5)
        self.next_button.grid(row=0, column=2, padx=5)

        self.calendar_frame = tk.Frame(self.root)
        self.calendar_frame.pack(pady=10)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.search_button = tk.Button(self.button_frame, text="날짜 검색", command=self.search_date, width=10)
        self.search_button.grid(row=0, column=0, padx=5)

        self.add_button = tk.Button(self.button_frame, text="일정 등록", command=self.open_add_window, width=10)
        self.add_button.grid(row=0, column=1, padx=5)

        self.reset_button = tk.Button(self.button_frame, text="초기화", command=self.reset_schedule, width=10)
        self.reset_button.grid(row=0, column=2, padx=5)

        self.schedule_frame = tk.Frame(self.root)
        self.schedule_frame.pack(pady=10)
        self.schedule_frame.pack_forget()

        self.schedule_label = tk.Label(self.schedule_frame, text="일정 목록", font=("Arial", 14, "bold"))
        self.schedule_label.pack(anchor="center")

        self.schedule_listbox = tk.Listbox(self.schedule_frame, width=40, height=8)
        self.schedule_listbox.pack(pady=5)

        self.display_calendar()

    def display_calendar(self):
        self.year_label.config(text=f"{self.year}년")
        self.month_label.config(text=f"{self.month}월")

        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        days = ["월", "화", "수", "목", "금", "토", "일"]

        for col, day in enumerate(days):
            tk.Label(self.calendar_frame, text=day, font=("Arial", 10, "bold")).grid(row=0, column=col)

        cal = calendar.monthcalendar(self.year, self.month)

        for row, week in enumerate(cal, start=1):
            for col, day in enumerate(week):
                if day != 0:
                    date_str = f"{self.year}-{self.month:02d}-{day:02d}"
                    btn_color = self.get_button_color(date_str)

                    btn = tk.Button(
                        self.calendar_frame, text=str(day), width=4, height=2,
                        bg=btn_color,
                        command=lambda d=day: self.show_schedule(d)
                    )
                    btn.grid(row=row, column=col, padx=2, pady=2)

    def get_button_color(self, date):
        if date in self.schedules:
            return self.category_colors[self.schedules[date][0][1]]
        return "white"

    def show_schedule(self, day):
        date = f"{self.year}-{self.month:02d}-{day:02d}"

        self.schedule_listbox.delete(0, tk.END)
        if date in self.schedules:
            for index, (text, category) in enumerate(self.schedules[date]):
                self.schedule_listbox.insert(tk.END, f"{index + 1}. {date}: {text} (카테고리: {category})")
        else:
            self.schedule_listbox.insert(tk.END, f"{date}: 등록된 일정이 없습니다.")

        self.schedule_frame.pack()

    def open_add_window(self):
        add_window = Toplevel(self.root)
        add_window.title("일정 등록")
        add_window.geometry("300x250")

        tk.Label(add_window, text="날짜 (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=10)
        date_entry = tk.Entry(add_window)
        date_entry.grid(row=0, column=1, padx=10)

        tk.Label(add_window, text="일정 내용:").grid(row=1, column=0, padx=10, pady=5)
        schedule_entry = tk.Entry(add_window, width=20)
        schedule_entry.grid(row=1, column=1, padx=10)

        tk.Label(add_window, text="카테고리:").grid(row=2, column=0, padx=10, pady=5)
        category_var = tk.StringVar(value="업무")

        categories = ["업무", "기념일", "개인 일정"]
        for i, category in enumerate(categories):
            tk.Radiobutton(add_window, text=category, variable=category_var, value=category).grid(row=2 + i, column=1, sticky="w")

        save_button = tk.Button(add_window, text="저장", command=lambda: self.save_schedule(date_entry, schedule_entry, category_var, add_window))
        save_button.grid(row=5, column=0, columnspan=2, pady=10)

    def save_schedule(self, date_entry, schedule_entry, category_var, add_window):
        date = date_entry.get()
        text = schedule_entry.get()
        category = category_var.get()

        try:
            datetime.strptime(date, "%Y-%m-%d")
            if date and text:
                self.schedules.setdefault(date, []).append((text, category))
                messagebox.showinfo("저장", f"{date} 일정이 등록되었습니다.")
                add_window.destroy()
                self.display_calendar()
            else:
                messagebox.showwarning("경고", "날짜와 일정을 모두 입력해주세요.")

        except ValueError:
            messagebox.showerror("오류", "날짜 형식이 잘못되었습니다.")

    def reset_schedule(self):
        self.schedules.clear()
        messagebox.showinfo("초기화", "모든 일정이 초기화되었습니다.")
        self.display_calendar()

    def before_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.display_calendar()

    def next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.display_calendar()

    def search_date(self):
        date_str = simpledialog.askstring("날짜 검색", "검색할 날짜를 입력하세요 (YYYY-MM-DD)")
        if date_str:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                if date_str in self.schedules:
                    self.show_schedule(int(date_str.split("-")[2]))
                else:
                    messagebox.showinfo("검색 결과", f"{date_str}: 등록된 일정이 없습니다.")
            except ValueError:
                messagebox.showerror("오류", "날짜 형식이 잘못되었습니다.")

root = tk.Tk()
app = MyScheduler(root)
root.mainloop()
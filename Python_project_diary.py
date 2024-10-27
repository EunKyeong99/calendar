import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel
import calendar
from datetime import datetime


class CalendarScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar Scheduler")
        self.root.geometry("400x500")

        self.current_year = datetime.now().year
        self.current_month = datetime.now().month

        self.schedules = {}
        self.color_map = {
            "업무": "lightgreen",
            "기념일": "lightcoral",
            "개인 약속": "lightyellow"
        }

        self.create_widgets()

    def create_widgets(self):
        self.header_frame = tk.Frame(self.root)
        self.header_frame.pack(pady=10)

        self.year_label = tk.Label(self.header_frame, text=f"{self.current_year}년", font=("Arial", 16))
        self.year_label.pack()

        self.month_frame = tk.Frame(self.root)
        self.month_frame.pack(pady=5)

        self.prev_button = tk.Button(self.month_frame, text="◀", command=self.prev_month, width=5)
        self.prev_button.grid(row=0, column=0, padx=5)

        self.month_label = tk.Label(self.month_frame, text=f"{self.current_month}월", font=("Arial", 14))
        self.month_label.grid(row=0, column=1, padx=5)

        self.next_button = tk.Button(self.month_frame, text="▶", command=self.next_month, width=5)
        self.next_button.grid(row=0, column=2, padx=5)

        self.calendar_frame = tk.Frame(self.root)
        self.calendar_frame.pack(pady=10)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.search_button = tk.Button(self.button_frame, text="날짜 검색", command=self.search_date, width=10)
        self.search_button.grid(row=0, column=0, padx=5)

        self.add_schedule_button = tk.Button(self.button_frame, text="일정 등록", command=self.open_add_schedule_window,
                                             width=10)
        self.add_schedule_button.grid(row=0, column=1, padx=5)

        # 두 번째 줄에 버튼 추가
        self.delete_schedule_button = tk.Button(self.button_frame, text="일정 삭제", command=self.delete_schedule, width=10)
        self.delete_schedule_button.grid(row=1, column=0, padx=5)

        self.reset_button = tk.Button(self.button_frame, text="초기화", command=self.reset_schedule, width=10)
        self.reset_button.grid(row=1, column=1, padx=5)

        self.schedule_frame = tk.Frame(self.root)
        self.schedule_frame.pack(pady=10)
        self.schedule_frame.pack_forget()

        self.schedule_label = tk.Label(self.schedule_frame, text="일정 목록", font=("Arial", 14, "bold"))
        self.schedule_label.pack(anchor="center")

        self.schedule_listbox = tk.Listbox(self.schedule_frame, width=40, height=8)
        self.schedule_listbox.pack(pady=5)

        self.display_calendar()

    def display_calendar(self):
        self.year_label.config(text=f"{self.current_year}년")
        self.month_label.config(text=f"{self.current_month}월")

        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        days = ["월", "화", "수", "목", "금", "토", "일"]
        for col, day in enumerate(days):
            tk.Label(self.calendar_frame, text=day, font=("Arial", 10, "bold")).grid(row=0, column=col)

        cal = calendar.monthcalendar(self.current_year, self.current_month)
        for row, week in enumerate(cal, start=1):
            for col, day in enumerate(week):
                if day != 0:
                    date_str = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
                    has_schedule = date_str in self.schedules

                    # 첫 번째 일정의 카테고리로 색상 결정
                    if has_schedule:
                        btn_color = self.color_map[self.schedules[date_str][0][1]]
                    else:
                        btn_color = "white"

                    btn = tk.Button(
                        self.calendar_frame, text=str(day), width=4, height=2,
                        bg=btn_color,
                        command=lambda d=day: self.show_day_schedule(d)
                    )
                    btn.grid(row=row, column=col, padx=2, pady=2)

    def show_day_schedule(self, day):
        date = f"{self.current_year}-{self.current_month:02d}-{day:02d}"

        self.schedule_listbox.delete(0, tk.END)
        if date in self.schedules:
            for index, schedule in enumerate(self.schedules[date]):
                self.schedule_listbox.insert(tk.END, f"{index + 1}. {date}: {schedule[0]} (카테고리: {schedule[1]})")
        else:
            self.schedule_listbox.insert(tk.END, f"{date}: 등록된 일정이 없습니다.")

        self.schedule_frame.pack()

    def open_add_schedule_window(self):
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

        # 카테고리를 아래로 정렬
        categories = ["업무", "기념일", "개인 약속"]
        for i, category in enumerate(categories):
            tk.Radiobutton(add_window, text=category, variable=category_var, value=category).grid(row=2 + i, column=1,
                                                                                                  sticky="w")

        def save_schedule():
            date = date_entry.get()
            schedule_text = schedule_entry.get()
            category = category_var.get()

            try:
                datetime.strptime(date, "%Y-%m-%d")
                if date and schedule_text:
                    if date in self.schedules:
                        self.schedules[date].append((schedule_text, category))
                    else:
                        self.schedules[date] = [(schedule_text, category)]
                    messagebox.showinfo("Saved", f"{date} 일정이 등록되었습니다.")
                    add_window.destroy()
                    self.display_calendar()
                else:
                    messagebox.showwarning("Warning", "날짜와 일정을 모두 입력해주세요.")

            except ValueError:
                messagebox.showerror("Error", "날짜 형식이 잘못되었습니다. YYYY-MM-DD 형식으로 입력해주세요.")

        save_button = tk.Button(add_window, text="저장", command=save_schedule)
        save_button.grid(row=5, column=0, columnspan=2, pady=10)

    def delete_schedule(self):
        selected_index = self.schedule_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "삭제할 일정을 선택해주세요.")
            return

        selected_schedule = self.schedule_listbox.get(selected_index[0])
        selected_date = selected_schedule.split(":")[0].strip()  # 삭제할 일정의 날짜
        schedule_text = selected_schedule.split(":")[1].strip().split(" (")[0]  # 일정 내용 추출

        # 선택된 일정 삭제
        if selected_date in self.schedules:
            # 삭제하려는 일정과 일치하지 않는 일정만 남김
            self.schedules[selected_date] = [
                s for s in self.schedules[selected_date] if s[0] != schedule_text
            ]

            # 일정이 비어있으면 해당 날짜 삭제
            if not self.schedules[selected_date]:
                del self.schedules[selected_date]

            messagebox.showinfo("Deleted", f"일정 '{schedule_text}'가 삭제되었습니다.")
            self.display_calendar()  # 달력을 갱신
            self.schedule_listbox.delete(0, tk.END)  # 일정 목록 초기화
            self.schedule_frame.pack_forget()  # 일정 목록 숨기기
        else:
            messagebox.showwarning("Warning", "삭제할 일정을 찾을 수 없습니다.")

    def reset_schedule(self):
        """일정을 초기화하는 함수"""
        self.schedules.clear()  # 모든 일정을 삭제
        messagebox.showinfo("초기화", "모든 일정이 초기화되었습니다.")
        self.display_calendar()  # 달력을 갱신

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.display_calendar()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.display_calendar()

    def search_date(self):
        date_str = simpledialog.askstring("날짜 검색", "검색할 날짜를 입력하세요 (YYYY-MM-DD):")
        if date_str:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                if date_str in self.schedules:
                    self.show_day_schedule(int(date_str.split("-")[2]))
                else:
                    messagebox.showinfo("검색 결과", f"{date_str}: 등록된 일정이 없습니다.")
            except ValueError:
                messagebox.showerror("Error", "날짜 형식이 잘못되었습니다. YYYY-MM-DD 형식으로 입력해주세요.")


if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarScheduler(root)
    root.mainloop()

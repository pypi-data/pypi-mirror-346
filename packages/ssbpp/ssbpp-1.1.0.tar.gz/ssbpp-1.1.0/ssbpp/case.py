import json
import os
import random
import string
import time
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import webbrowser
import uuid
from datetime import datetime
from tkinter import ttk
from tkinter import *
import warnings

warnings.filterwarnings("ignore")
import calendar
import tkinter.font as tkFont

# pip install urllib3==1.26.15
datetime = calendar.datetime.datetime
timedelta = calendar.datetime.timedelta


def my_get_city(lat, lon):
    url = f"http://www.metakssdcoabundance.link/kssdtree/v2/get_city?lat={lat}&lon={lon}"
    try:
        r = requests.get(url, timeout=5)
        result = json.loads(r.text)
        if result['code'] == 200:
            city = result['city']
            if city is not None:
                return city
            else:
                return None
    except requests.Timeout:
        print("The request timed out. Please check your network connection or try again later.")
        return ''
    except Exception:
        return ''


def my_get_lat_lon(city):
    url = f"http://www.metakssdcoabundance.link/kssdtree/v2/get_lat_lon?city={city}"
    try:
        r = requests.get(url, timeout=5)
        result = json.loads(r.text)
        if result['code'] == 200:
            lat = result['lat']
            lon = result['lon']
            if lat is not None and lon is not None:
                return lat, lon
            else:
                return None
    except requests.Timeout:
        print("The request timed out. Please check your network connection or try again later.")
        return '', ''
    except Exception:
        return '', ''


class Calendar:

    def __init__(s, x, y):
        s.master = tk.Toplevel()
        s.master.withdraw()
        fwday = calendar.SUNDAY

        year = datetime.now().year
        month = datetime.now().month
        locale = None
        sel_bg = '#ecffc4'
        sel_fg = '#05640e'

        s._date = datetime(year, month, 1)
        s._selection = None

        s.G_Frame = ttk.Frame(s.master)

        s._cal = s.__get_calendar(locale, fwday)

        s.__setup_styles()
        s.__place_widgets()
        s.__config_calendar()

        s.__setup_selection(sel_bg, sel_fg)

        s._items = [s._calendar.insert('', 'end', values='') for _ in range(6)]

        s._update()

        s.G_Frame.pack(expand=1, fill='both')
        s.master.overrideredirect(1)
        s.master.update_idletasks()
        width, height = s.master.winfo_reqwidth(), s.master.winfo_reqheight()

        s.master.geometry('%dx%d+%d+%d' % (width, height, x, y))
        s.master.after(300, s._main_judge)
        s.master.deiconify()
        s.master.focus_set()
        s.master.wait_window()

    def __get_calendar(s, locale, fwday):
        if locale is None:
            return calendar.TextCalendar(fwday)
        else:
            return calendar.LocaleTextCalendar(fwday, locale)

    def __setitem__(s, item, value):
        if item in ('year', 'month'):
            raise AttributeError("attribute '%s' is not writeable" % item)
        elif item == 'selectbackground':
            s._canvas['background'] = value
        elif item == 'selectforeground':
            s._canvas.itemconfigure(s._canvas.text, item=value)
        else:
            s.G_Frame.__setitem__(s, item, value)

    def __getitem__(s, item):
        if item in ('year', 'month'):
            return getattr(s._date, item)
        elif item == 'selectbackground':
            return s._canvas['background']
        elif item == 'selectforeground':
            return s._canvas.itemcget(s._canvas.text, 'fill')
        else:
            r = ttk.tclobjs_to_py({item: ttk.Frame.__getitem__(s, item)})
            return r[item]

    def __setup_styles(s):
        style = ttk.Style(s.master)
        arrow_layout = lambda dir: (
            [('Button.focus', {'children': [('Button.%sarrow' % dir, None)]})]
        )
        style.layout('L.TButton', arrow_layout('left'))
        style.layout('R.TButton', arrow_layout('right'))

    def __place_widgets(s):
        Input_judgment_num = s.master.register(s.Input_judgment)
        hframe = ttk.Frame(s.G_Frame)
        gframe = ttk.Frame(s.G_Frame)
        bframe = ttk.Frame(s.G_Frame)
        hframe.pack(in_=s.G_Frame, side='top', pady=5, anchor='center')
        gframe.pack(in_=s.G_Frame, fill=tk.X, pady=5)
        bframe.pack(in_=s.G_Frame, side='bottom', pady=5)

        lbtn = ttk.Button(hframe, style='L.TButton', command=s._prev_month)
        lbtn.grid(in_=hframe, column=0, row=0, padx=12)
        rbtn = ttk.Button(hframe, style='R.TButton', command=s._next_month)
        rbtn.grid(in_=hframe, column=5, row=0, padx=12)

        tk.Label(hframe, text='Year', justify='left').grid(in_=hframe, column=1, row=0, padx=(0, 5))
        s.CB_year = ttk.Combobox(hframe, width=5, values=[str(year) for year in
                                                          range(datetime.now().year, datetime.now().year - 11, -1)],
                                 validate='key', validatecommand=(Input_judgment_num, '%P'))
        s.CB_year.current(0)
        s.CB_year.grid(in_=hframe, column=2, row=0)
        s.CB_year.bind('<KeyPress>', lambda event: s._update(event, True))
        s.CB_year.bind("<<ComboboxSelected>>", s._update)

        tk.Label(hframe, text='Month', justify='left').grid(in_=hframe, column=3, row=0)
        s.CB_month = ttk.Combobox(hframe, width=3, values=['%02d' % month for month in range(1, 13)], state='readonly')
        s.CB_month.current(datetime.now().month - 1)
        s.CB_month.grid(in_=hframe, column=4, row=0)
        s.CB_month.bind("<<ComboboxSelected>>", s._update)

        s._calendar = ttk.Treeview(gframe, show='', selectmode='none', height=7)
        s._calendar.pack(expand=1, fill='both', side='bottom', padx=5)

        ttk.Button(bframe, text="Ok", width=6, command=lambda: s._exit(True)).grid(row=0, column=0, sticky='ns',
                                                                                   padx=20)
        ttk.Button(bframe, text="Cancel", width=6, command=s._exit).grid(row=0, column=1, sticky='ne', padx=20)

        tk.Frame(s.G_Frame, bg='#565656').place(x=0, y=0, relx=0, rely=0, relwidth=1, relheigh=2 / 200)
        tk.Frame(s.G_Frame, bg='#565656').place(x=0, y=0, relx=0, rely=198 / 200, relwidth=1, relheigh=2 / 200)
        tk.Frame(s.G_Frame, bg='#565656').place(x=0, y=0, relx=0, rely=0, relwidth=2 / 200, relheigh=1)
        tk.Frame(s.G_Frame, bg='#565656').place(x=0, y=0, relx=198 / 200, rely=0, relwidth=2 / 200, relheigh=1)

    def __config_calendar(s):
        # cols = s._cal.formatweekheader(3).split()
        cols = ['Sun', 'Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat']
        s._calendar['columns'] = cols
        s._calendar.tag_configure('header', background='grey90')
        s._calendar.insert('', 'end', values=cols, tag='header')
        font = tkFont.Font()
        maxwidth = max(font.measure(col) for col in cols)
        for col in cols:
            s._calendar.column(col, width=maxwidth, minwidth=maxwidth,
                               anchor='center')

    def __setup_selection(s, sel_bg, sel_fg):
        def __canvas_forget(evt):
            canvas.place_forget()
            s._selection = None

        s._font = tkFont.Font()
        s._canvas = canvas = tk.Canvas(s._calendar, background=sel_bg, borderwidth=0, highlightthickness=0)
        canvas.text = canvas.create_text(0, 0, fill=sel_fg, anchor='w')

        canvas.bind('<Button-1>', __canvas_forget)
        s._calendar.bind('<Configure>', __canvas_forget)
        s._calendar.bind('<Button-1>', s._pressed)

    def _build_calendar(s):
        year, month = s._date.year, s._date.month

        # update header text (Month, YEAR)
        header = s._cal.formatmonthname(year, month, 0)

        cal = s._cal.monthdayscalendar(year, month)
        for indx, item in enumerate(s._items):
            week = cal[indx] if indx < len(cal) else []
            fmt_week = [('%02d' % day) if day else '' for day in week]
            s._calendar.item(item, values=fmt_week)

    def _show_select(s, text, bbox):
        x, y, width, height = bbox

        textw = s._font.measure(text)

        canvas = s._canvas
        canvas.configure(width=width, height=height)
        canvas.coords(canvas.text, (width - textw) / 2, height / 2 - 1)
        canvas.itemconfigure(canvas.text, text=text)
        canvas.place(in_=s._calendar, x=x, y=y)

    def _pressed(s, evt=None, item=None, column=None, widget=None):
        if not item:
            x, y, widget = evt.x, evt.y, evt.widget
            item = widget.identify_row(y)
            column = widget.identify_column(x)

        if not column or not item in s._items:
            return

        item_values = widget.item(item)['values']
        if not len(item_values):
            return

        text = item_values[int(column[1]) - 1]
        if not text:
            return

        bbox = widget.bbox(item, column)
        if not bbox:
            s.master.after(20, lambda: s._pressed(item=item, column=column, widget=widget))
            return

        text = '%02d' % text
        s._selection = (text, item, column)
        s._show_select(text, bbox)

    def _prev_month(s):
        s._canvas.place_forget()
        s._selection = None

        s._date = s._date - timedelta(days=1)
        s._date = datetime(s._date.year, s._date.month, 1)
        s.CB_year.set(s._date.year)
        s.CB_month.set(s._date.month)
        s._update()

    def _next_month(s):
        s._canvas.place_forget()
        s._selection = None

        year, month = s._date.year, s._date.month
        s._date = s._date + timedelta(
            days=calendar.monthrange(year, month)[1] + 1)
        s._date = datetime(s._date.year, s._date.month, 1)
        s.CB_year.set(s._date.year)
        s.CB_month.set(s._date.month)
        s._update()

    def _update(s, event=None, key=None):
        if key and event.keysym != 'Return': return
        year = int(s.CB_year.get())
        month = int(s.CB_month.get())
        if year == 0 or year > 9999: return
        s._canvas.place_forget()
        s._date = datetime(year, month, 1)
        s._build_calendar()

        if year == datetime.now().year and month == datetime.now().month:
            day = datetime.now().day
            for _item, day_list in enumerate(s._cal.monthdayscalendar(year, month)):
                if day in day_list:
                    item = 'I00' + str(_item + 2)
                    column = '#' + str(day_list.index(day) + 1)
                    s.master.after(100, lambda: s._pressed(item=item, column=column, widget=s._calendar))

    def _exit(s, confirm=False):
        if not confirm: s._selection = None
        s.master.destroy()

    def _main_judge(s):
        try:
            if s.master.focus_displayof() == None or 'toplevel' not in str(s.master.focus_displayof()):
                s._exit()
            else:
                s.master.after(10, s._main_judge)
        except:
            s.master.after(10, s._main_judge)

    def selection(s):
        if not s._selection: return datetime.now().strftime("%Y-%m-%d")

        year, month = s._date.year, s._date.month
        return str(datetime(year, month, int(s._selection[0])))[:10]

    def Input_judgment(s, content):
        if content.isdigit() or content == "":
            return True
        else:
            return False


class DataEntryForm(tk.Frame):

    def __init__(self, master, window_width, window_height, x, y):
        super().__init__(master)
        self.window_width = window_width
        self.window_height = window_height
        self.x = x
        self.y = y
        hdr_txt = "SSBPP: A Real-time Strain Submission and Monitoring Platform \n for Epidemic Prevention Based on Phylogenetic Placement"
        hdr = tk.Label(master, text=hdr_txt, font=("Arial", 16, "bold"), bg='white')
        hdr.pack(pady=20)

        self.file_path_list = []
        self.file_type_list = []
        slframe = tk.Frame(master, pady=10, bg='white')
        slframe.pack()
        sign_1 = tk.Label(slframe, text="*", width=1, fg='red', font=("Arial", 10, "bold"), bg="white",
                          relief=FLAT)
        sign_1.pack(side=tk.LEFT)
        sltb = tk.Label(slframe, text="Select fasta/fastq files", font=("Arial", 10, "bold"), width=32, fg='black',
                        bg="lightgreen", relief=FLAT)
        sltb.pack(side=tk.LEFT)
        sltb.bind('<Button-1>', self.select_file)

        ctb = tk.Label(slframe, text="Clear", width=5, fg='black', font=("Arial", 10, "bold"), bg="red",
                       relief=FLAT)
        ctb.pack(side=tk.RIGHT, padx=10)
        ctb.bind('<Button-1>', self.clear)

        self.file_list_frame = tk.Frame(master)
        self.file_list_frame.pack(pady=5)
        self.file_list_label = tk.Label(self.file_list_frame, wraplength=300, bg='white', fg='gray',
                                        font=("Arial", 10, "bold"), relief=FLAT)
        self.file_list_label.pack()

        sampletimeframe = tk.Frame(master, width=10, pady=10, bg='white')
        sampletimeframe.pack()
        sign_2 = tk.Label(sampletimeframe, text="*", width=1, fg='red', font=("Arial", 10, "bold"), bg="white",
                          relief=FLAT)
        sign_2.pack(side=tk.LEFT)
        sampletimelabel = tk.Label(sampletimeframe, text='Sampling Date: ', bg='white', fg='black',
                                   font=("Arial", 10, "bold"), relief=FLAT)
        sampletimelabel.pack(side=tk.LEFT)

        self.stl = tk.Label(sampletimeframe, text="Select", width=5, fg='black', bg="lightgreen",
                            highlightthickness=1,
                            font=("Arial", 10, "bold"), relief=FLAT)
        self.stl.pack(side=tk.RIGHT, padx=2)
        self.stl.bind('<Button-1>', self.select_time)
        self.date_str = tk.StringVar()
        self.ste = tk.Entry(sampletimeframe, highlightthickness=1, fg='gray', font=("Arial", 10, "bold"),
                            width=20, relief=FLAT, textvariable=self.date_str, state='readonly')

        self.ste.pack(side=tk.RIGHT, padx=8)
        cur_date = datetime.now().strftime("%Y-%m-%d")
        self.date_str.set(cur_date)

        cityframe = tk.Frame(master, width=5, pady=10, bg='white')
        cityframe.pack()
        sign_3 = tk.Label(cityframe, text="*", width=1, fg='red', font=("Arial", 10, "bold"), bg="white",
                          relief=FLAT)
        sign_3.pack(side=tk.LEFT)
        citylabel = tk.Label(cityframe, text='Sampling City: ', bg='white', fg='black',
                             font=("Arial", 10, "bold"), relief=FLAT)
        citylabel.pack(side=tk.LEFT)
        self.city_str = tk.StringVar()
        self.city = ttk.Entry(cityframe, textvariable=self.city_str, width=25)
        self.city.pack(side=tk.RIGHT, padx=8)
        self.get_city()

        depframe = tk.Frame(master, pady=10, bg='white')
        depframe.pack()
        deplabel = tk.Label(depframe, text='Institute:', bg='white', fg='black',
                            font=("Arial", 10, "bold"), relief=FLAT)
        deplabel.pack(side=tk.LEFT)

        self.department = tk.Entry(depframe, highlightthickness=1, fg='gray', font=("Arial", 10, "bold"),
                                   width=33, relief=FLAT)
        self.department.pack(side=tk.RIGHT, padx=8)

        emailframe = tk.Frame(master, width=10, pady=10, bg='white')
        emailframe.pack()
        emaillabel = tk.Label(emailframe, text='E-mail: ', bg='white', fg='black',
                              font=("Arial", 10, "bold"), relief=FLAT)
        emaillabel.pack(side=tk.LEFT, padx=2)

        self.email = tk.Entry(emailframe, highlightthickness=1, fg='gray', font=("Arial", 10, "bold"),
                              width=33, relief=FLAT)
        self.email.pack(side=tk.RIGHT, padx=8)

        scframe = tk.Frame(master, pady=10, bg='white')
        scframe.pack()
        cantb = tk.Label(scframe, text="Cancel", width=18, fg='black', bg="red", highlightthickness=1,
                         font=("Arial", 10, "bold"), relief=FLAT)
        cantb.pack(side=tk.LEFT)
        cantb.bind('<Button-1>', self.cancel)

        subtb = tk.Label(scframe, text="Submit", width=18, fg='black', bg="lightgreen", highlightthickness=1,
                         font=("Arial", 10, "bold"), relief=FLAT)
        subtb.pack(side=tk.RIGHT, padx=20)
        subtb.bind('<Button-1>', self.submit)

        self.index = 0
        # self.uid = '00be43d77434'
        self.uid = uuid.UUID(int=uuid.getnode()).hex[-12:]
        url = f"http://www.metakssdcoabundance.link/kssdtree/v2/personal?uid={self.uid}"
        r = requests.get(url)
        result = json.loads(r.text)
        self.ids = []
        self.samples = []
        self.speciess = []
        self.sample_institutes = []
        self.sample_dates = []
        self.submission_dates = []
        self.emails = []
        self.ps = []
        self.views = []
        self.first = False
        if result['code'] == 200:
            data = result['result']
            if len(data) > 0:
                self.first = True
                for x in data:
                    self.ids.append(x['id'])
                    self.samples.append(x['sample'])
                    self.speciess.append(x['species'])
                    self.sample_institutes.append(x['sample_institute'])
                    self.sample_dates.append(x['sample_date'])
                    self.submission_dates.append(x['submission_date'])
                    self.views.append(x['view'])
                    self.ps.append(x['p'])
        if len(self.ids) > 0:
            line = tk.Label(self.master,
                            text="------------------------------------------------------------------------------------------------------------------------------------",
                            fg='lightgray', bg='white')
            line.pack(pady=2)
            my = tk.Label(master, text="My Submission", font=("Arial", 14, "bold"), bg='white')
            my.pack(pady=2)

            vdframe = tk.Frame(master, pady=5, bg='white')
            vdframe.pack(pady=10, padx=5)

            vtb = tk.Label(vdframe, text="View", width=5, fg='black', bg="lightgreen", highlightthickness=1,
                           font=("Arial", 10, "bold"), relief=FLAT)
            vtb.pack(side=tk.LEFT)
            vtb.bind('<Button-1>', self.view)

            dtb = tk.Label(vdframe, text="Delete", width=5, fg='black', bg="red", highlightthickness=1,
                           font=("Arial", 10, "bold"), relief=FLAT)
            dtb.pack(side=tk.RIGHT, padx=5)
            dtb.bind('<Button-1>', self.delete)

            f = ttk.Frame(self.master)
            s = ttk.Scrollbar(f)
            self.t = ttk.Treeview(f, columns=('c1', 'c2', 'c3', 'c4', 'c5', 'c6'), show="headings",
                                  yscrollcommand=s.set)
            s.config(command=self.t.yview)
            f.pack(pady=5)
            s.pack(side='right', fill='y')
            self.t.pack(side='left', fill='y')

            self.t.pack(pady=5)
            self.t.column('c1', width=80, anchor='center')
            self.t.column('c2', width=220, anchor='center')
            self.t.column('c3', width=220, anchor='center')
            self.t.column('c4', width=150, anchor='center')
            self.t.column('c5', width=150, anchor='center')
            self.t.column('c6', width=150, anchor='center')

            self.t.heading('c1', text='No')
            self.t.heading('c2', text='Sample')
            self.t.heading('c3', text='Species')
            self.t.heading('c4', text='Placement position')
            self.t.heading('c5', text='Sampling date')
            self.t.heading('c6', text='Submission date')

            for i in range(len(self.ids)):
                self.t.insert('', i + 1,
                              values=[i + 1, self.samples[i], self.speciess[i], self.ps[i], self.sample_dates[i],
                                      self.submission_dates[i]])
            self.t.bind("<<TreeviewSelect>>", self.on_item_selected)

    def on_item_selected(self, event):
        ss = self.t.selection()
        if len(ss) > 1:
            self.index = -1
        else:
            selected_item = self.t.selection()[0]
            item_value = self.t.item(selected_item)
            self.index = int(item_value['values'][0]) - 1
            print(self.index)

    def view(self, event):
        print('view: ', self.index)
        if self.index != -1:
            webbrowser.open(self.views[self.index])
        else:
            messagebox.showwarning("Warning", f"Don't support multiple view !!!", default="ok",
                                   icon="warning")

    def delete(self, event):
        print('delete: ', self.index)
        if self.index != -1:
            ok = messagebox.askyesno("Warning", f"Delete this record ?",
                                     icon="warning")
            if ok:
                id = self.ids[self.index]
                url = f"http://www.metakssdcoabundance.link/kssdtree/v2/personal_del?id={id}"
                r = requests.get(url)
                result = json.loads(r.text)
                if result['code'] == 200:
                    ID = self.t.get_children()[self.index]
                    self.t.delete(ID)
                    print('delete success')
                    self.clear_treeview()
                    url = f"http://www.metakssdcoabundance.link/kssdtree/v2/personal?uid={self.uid}"
                    r = requests.get(url)
                    result = json.loads(r.text)
                    self.ids = []
                    self.samples = []
                    self.speciess = []
                    self.sample_institutes = []
                    self.sample_dates = []
                    self.submission_dates = []
                    self.emails = []
                    self.ps = []
                    self.views = []
                    if result['code'] == 200:
                        data = result['result']
                        if len(data) > 0:
                            self.first = True
                            for x in data:
                                self.ids.append(x['id'])
                                self.samples.append(x['sample'])
                                self.speciess.append(x['species'])
                                self.sample_institutes.append(x['sample_institute'])
                                self.sample_dates.append(x['sample_date'])
                                self.submission_dates.append(x['submission_date'])
                                self.views.append(x['view'])
                                self.ps.append(x['p'])
                    if len(self.ids) > 0:
                        for i in range(len(self.ids)):
                            self.t.insert('', i + 1,
                                          values=[i + 1, self.samples[i], self.speciess[i], self.ps[i],
                                                  self.sample_dates[i],
                                                  self.submission_dates[i]])
                        self.t.bind("<<TreeviewSelect>>", self.on_item_selected)
        else:
            messagebox.showwarning("Warning", f"Don't support multiple delete !!!", default="ok",
                                   icon="warning")

    def clear_treeview(self):
        for item in self.t.get_children():
            self.t.delete(item)

    def allowed_fasta_file(self, filename):
        allowed_extensions = ['.fa', '.fa.gz', '.fasta', '.fasta.gz', '.fna', '.fna.gz']
        return any(filename.endswith(ext) for ext in allowed_extensions)

    def allowed_fastq_file(self, filename):
        allowed_extensions = ['.fastq', '.fastq.gz', '.fq', 'fq.gz']
        return any(filename.endswith(ext) for ext in allowed_extensions)

    def select_file(self, event):
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            valid_files = []
            valid_types = []
            for file_path in file_paths:
                if self.allowed_fasta_file(file_path):
                    valid_files.append(file_path)
                    valid_types.append(0)
                elif self.allowed_fastq_file(file_path):
                    valid_files.append(file_path)
                    valid_types.append(1)
                else:
                    messagebox.showwarning("Warning", f"{file_path} is not a valid fasta/fastq file !!!", default="ok",
                                           icon="warning")
            if len(valid_files) > 0:
                for path in valid_files:
                    self.file_path_list.append(path)
                for tp in valid_types:
                    self.file_type_list.append(tp)
                file_list_str = '\n'.join([path.split('/')[-1] for path in self.file_path_list])
                self.file_list_label.config(text=f"{file_list_str}")

    def select_time(self, event):
        s = Calendar(self.x + 50, self.y + 50).selection()
        print(s)
        self.date_str.set(s)

    def check_email(self, email):
        import re
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, email):
            return True
        else:
            return False

    def clear(self, event):
        if len(self.file_path_list) > 0:
            self.file_path_list = []
            self.file_list_label.config(text='')

    def get_parent_dir(self, file_paths):
        if not file_paths:
            return None
        common_dir = os.path.dirname(file_paths[0])
        for path in file_paths[1:]:
            while not path.startswith(common_dir):
                common_dir = os.path.dirname(common_dir)
        return common_dir

    def get_city(self):
        try:
            response = requests.get("http://httpbin.org/ip", timeout=5)
            ip_address = response.json()['origin']
            api_key = 'bc804966ff0fe2'
            url = f'https://ipinfo.io/{ip_address}/json?token={api_key}'
            response = requests.get(url, timeout=5)
            data = response.json()
            city = data.get('city')
            self.city_str.set(city)
            return city
        except requests.Timeout:
            self.city_str.set('')
            return ''

    def upload_file(self, file_path_list, lat, lon, city, sample_institute, sample_date, email,
                    submission_date):
        print('file_path_list: ', file_path_list)
        species_list = []
        common_dir = self.get_parent_dir(file_path_list)
        shuf_file = os.path.join(common_dir, 'L3K10.shuf')
        if not os.path.exists(shuf_file):
            print('Downloading...', shuf_file)
            start_time = time.time()
            url = 'http://www.metakssdcoabundance.link/kssdtree/v2/shuf/L3K10.shuf'
            headers = {'Accept-Encoding': 'gzip, deflate'}
            response = requests.get(url, headers=headers, stream=True)
            with open(shuf_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            end_time = time.time()
            if end_time - start_time > 200:
                print(
                    "Network timeout, please manually download from https://zenodo.org/records/12699159")
                return False
            print('Finished')
        success_nums = 0
        for i in range(len(file_path_list)):
            timeStamp = int(time.mktime(time.localtime(time.time())))
            letters = string.ascii_lowercase
            numbers = string.digits
            random_letters = ''.join(random.choice(letters) for i in range(6))
            random_numbers = ''.join(random.choice(numbers) for i in range(3))
            ln = 'ssbpp' + random_letters + random_numbers
            qry_sketch = ln + '_sketch_' + str(timeStamp)
            genome_files = file_path_list[i]
            import kssdutils
            print('shuf_file: ', shuf_file)
            print('genome_files: ', genome_files)
            file_type = ''
            if self.file_type_list[i] == 0:
                kssdutils.sketch(shuf_file=shuf_file, genome_files=genome_files, output=qry_sketch, abundance=False,
                                 set_opt=True)
                file_type = "fasta"
            else:
                kssdutils.sketch(shuf_file=shuf_file, genome_files=genome_files, output=qry_sketch, abundance=True,
                                 set_opt=True)
                file_type = "fastq"
            zip_file = qry_sketch + '.zip'
            zip = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED)
            for item in os.listdir(qry_sketch):
                zip.write(qry_sketch + os.sep + item)
            zip.close()

            url = "http://www.metakssdcoabundance.link/kssdtree/v2/upload"
            header = {
                "kssdtreev2": 'uploadlfastq'
            }

            sample = file_path_list[i].split('/')[-1]
            data = {
                'uid': self.uid,
                'sample': sample,
                "lon": lon,
                'lat': lat,
                'city': city,
                'sample_institute': sample_institute,
                "sample_date": sample_date,
                'email': email,
                "submission_date": submission_date,
                "file_type": file_type
            }
            print(data)
            current_path = os.getcwd()
            files = {'file': open(os.path.join(current_path, zip_file), "rb")}
            try:
                res = requests.post(url=url, headers=header, data=data, files=files, timeout=10)
                print('status_code: ', res.status_code)
                if res.status_code == 200:
                    response = res.text
                    json_data = json.loads(response)
                    code = json_data['code']
                    print('code: ', code)
                    if code == 200:
                        species = json_data['species']
                        if species != '':
                            species_list.append(species)
                            success_nums += 1
                    else:
                        self.file_path_list = []
                        self.file_list_label.config(text='')
                        message = json_data['message']
                        krona_url = json_data['krona_url']
                        messagebox.showerror("Error", f"{message} !!!", default="ok",
                                             icon="error")
                        if krona_url != '':
                            webbrowser.open(krona_url)
            except requests.exceptions.Timeout:
                self.file_path_list = []
                self.file_list_label.config(text='')
                messagebox.showerror("Error", f"Request timeout !!!", default="ok",
                                     icon="error")
            except requests.exceptions.RequestException as e:
                self.file_path_list = []
                self.file_list_label.config(text='')
                messagebox.showerror("Error", f"Request error !!!", default="ok",
                                     icon="error")
        if success_nums > 0:
            self.file_path_list = []
            self.file_list_label.config(text='')
            if self.first:
                self.clear_treeview()
                url = f"http://www.metakssdcoabundance.link/kssdtree/v2/personal?uid={self.uid}"
                r = requests.get(url)
                result = json.loads(r.text)
                self.ids = []
                self.samples = []
                self.speciess = []
                self.sample_institutes = []
                self.sample_dates = []
                self.submission_dates = []
                self.emails = []
                self.ps = []
                self.views = []
                if result['code'] == 200:
                    data = result['result']
                    if len(data) > 0:
                        self.first = True
                        for x in data:
                            self.ids.append(x['id'])
                            self.samples.append(x['sample'])
                            self.speciess.append(x['species'])
                            self.sample_institutes.append(x['sample_institute'])
                            self.sample_dates.append(x['sample_date'])
                            self.submission_dates.append(x['submission_date'])
                            self.views.append(x['view'])
                            self.ps.append(x['p'])
                if len(self.ids) > 0:
                    for i in range(len(self.ids)):
                        self.t.insert('', i + 1,
                                      values=[i + 1, self.samples[i], self.speciess[i], self.ps[i],
                                              self.sample_dates[i],
                                              self.submission_dates[i]])
                    self.t.bind("<<TreeviewSelect>>", self.on_item_selected)
                    webbrowser.open(self.views[0])
                    # n = len(species_list)
                    # for j in range(n):
                    #     webbrowser.open(self.views[j])
            else:
                url = f"http://www.metakssdcoabundance.link/kssdtree/v2/personal?uid={self.uid}"
                r = requests.get(url)
                result = json.loads(r.text)
                self.ids = []
                self.samples = []
                self.speciess = []
                self.sample_institutes = []
                self.sample_dates = []
                self.submission_dates = []
                self.emails = []
                self.ps = []
                self.views = []
                if result['code'] == 200:
                    data = result['result']
                    if len(data) > 0:
                        for x in data:
                            self.ids.append(x['id'])
                            self.samples.append(x['sample'])
                            self.speciess.append(x['species'])
                            self.sample_institutes.append(x['sample_institute'])
                            self.sample_dates.append(x['sample_date'])
                            self.submission_dates.append(x['submission_date'])
                            self.views.append(x['view'])
                            self.ps.append(x['p'])
                if len(self.ids) > 0:
                    line = tk.Label(self.master,
                                    text="------------------------------------------------------------------------------------------------------------------------------------",
                                    fg='lightgray', bg='white')
                    line.pack(pady=2)
                    my = tk.Label(self.master, text="My Submission", font=("Arial", 14, "bold"), bg='white')
                    my.pack(pady=2)

                    vdframe = tk.Frame(self.master, pady=5, bg='white')
                    vdframe.pack(pady=10, padx=5)

                    vtb = tk.Label(vdframe, text="View", width=5, fg='black', bg="lightgreen", highlightthickness=1,
                                   font=("Arial", 10, "bold"), relief=FLAT)
                    vtb.pack(side=tk.LEFT)
                    vtb.bind('<Button-1>', self.view)

                    dtb = tk.Label(vdframe, text="Delete", width=5, fg='black', bg="red", highlightthickness=1,
                                   font=("Arial", 10, "bold"), relief=FLAT)
                    dtb.pack(side=tk.RIGHT, padx=5)
                    dtb.bind('<Button-1>', self.delete)

                    f = ttk.Frame(self.master)
                    s = ttk.Scrollbar(f)
                    self.t = ttk.Treeview(f, columns=('c1', 'c2', 'c3', 'c4', 'c5', 'c6'), show="headings",
                                          yscrollcommand=s.set)
                    s.config(command=self.t.yview)
                    f.pack(pady=5)
                    s.pack(side='right', fill='y')
                    self.t.pack(side='left', fill='y')

                    self.t.pack(pady=5)
                    self.t.column('c1', width=80, anchor='center')
                    self.t.column('c2', width=220, anchor='center')
                    self.t.column('c3', width=220, anchor='center')
                    self.t.column('c4', width=150, anchor='center')
                    self.t.column('c5', width=150, anchor='center')
                    self.t.column('c6', width=150, anchor='center')

                    self.t.heading('c1', text='No')
                    self.t.heading('c2', text='Sample')
                    self.t.heading('c3', text='Species')
                    self.t.heading('c4', text='Placement position')
                    self.t.heading('c5', text='Sampling date')
                    self.t.heading('c6', text='Submission date')

                    for i in range(len(self.ids)):
                        self.t.insert('', i + 1,
                                      values=[i + 1, self.samples[i], self.speciess[i], self.ps[i],
                                              self.sample_dates[i],
                                              self.submission_dates[i]])
                    self.t.bind("<<TreeviewSelect>>", self.on_item_selected)
                    webbrowser.open(self.views[0])
                    # n = len(species_list)
                    # for j in range(n):
                    #     webbrowser.open(self.views[j])

    def submit(self, event):
        if len(self.file_path_list) == 0:
            messagebox.showwarning("Warning", f" Please select a fasta/fastq file or multiple fasta/fastq files !!!",
                                   default="ok",
                                   icon="warning")
        else:
            if self.ste.get() == '':
                messagebox.showwarning("Warning", f"Sampling date can not be empty !!!",
                                       default="ok",
                                       icon="warning")
            else:
                if self.city.get() == '':
                    messagebox.showwarning("Warning", f"Sampling city can not be empty !!!",
                                           default="ok",
                                           icon="warning")
                else:
                    city = self.city.get()
                    sample_institute = self.department.get()
                    sample_date = self.ste.get()
                    email = self.email.get()
                    submission_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    r = my_get_lat_lon(city)
                    if r is not None:
                        lat = r[0]
                        lon = r[1]
                        city = my_get_city(lat, lon)
                        self.upload_file(self.file_path_list, lat, lon, city, sample_institute, sample_date, email,
                                         submission_date)
                    else:
                        messagebox.showerror("Error",
                                             f"The parsing of the latitude and longitude of the sampling city is incorrect !!!",
                                             default="ok",
                                             icon="error")

    def cancel(self, event):
        self.quit()


def isConnected():
    try:
        html = requests.get("https://www.baidu.com", timeout=5)
        print("Network available")
        return 1
    except:
        print("Network connection exception")
        return 0


def show():
    print('show...')
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # print(screen_width, screen_height)
    if screen_width > 1400 and screen_height > 800:
        window_width = int(screen_width / 1.4)
        window_height = int(screen_height / 1.4)
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f'{window_width}x{window_height}+{x}+{y}')
        root.config(bg="#ffffff")
        root.title("SSBPP")
        root.resizable(height=False, width=False)
        DataEntryForm(root, window_width, window_height, x, y)
        root.mainloop()
    else:
        root.geometry(f'{screen_width}x{screen_height}')
        root.config(bg="#ffffff")
        root.title("SSBPP")
        root.resizable(height=False, width=False)
        DataEntryForm(root, screen_width, screen_height, 0, 0)
        root.mainloop()


def main():
    show()


if __name__ == "__main__":
    main()

import os
import sys
import tkinter as tk
from tktooltip import ToolTip
from pathlib import Path
from math import ceil
from dataclasses import dataclass
from datetime import timedelta


M_AND = 'AND'
M_OR = 'OR'

BG          = "#1E1F22"   # фон окна
PANEL       = "#2B2D31"   # панели
PANEL_LIGHT = "#313338"   # светлее
ACCENT      = "#3BA55D"   # зелёный
ACCENT_H    = "#4CC16F"   # зелёный hover
TEXT        = "#E8E8E8"
MUTED       = "#9A9A9A"


class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="", color='grey', *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, ' ' + self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()
            

class WidgetManager:
    @staticmethod
    def entry_base(parent, placeholder=""):
        return EntryWithPlaceholder(
            parent,
            bg=PANEL_LIGHT,
            fg=TEXT,
            insertbackground=TEXT,
            relief='flat',
            bd=0,
            width=12,
            placeholder=placeholder
        )

    @staticmethod
    def check_base(master, variable, text, tt="", needpack = True, *args, **kwargs):
        check = tk.Checkbutton(master, text=text, variable=variable,
                bg=PANEL, fg=TEXT, selectcolor=PANEL,
                activebackground=PANEL, activeforeground=TEXT)
        ToolTip(check, tt, bg=BG, fg=TEXT)
        if needpack:
            check.pack(*args, **kwargs)
        return check
    
    @staticmethod
    def radio_base(master, variable, text, value, tt="", needpack=True, *args, **kwargs):
        radio = tk.Radiobutton(master, text=text, variable=variable,
                bg=PANEL, fg=TEXT, selectcolor=PANEL,
                activebackground=PANEL, activeforeground=TEXT,
                value=value)
        ToolTip(radio, tt, bg=BG, fg=TEXT)
        if needpack:
            radio.pack(*args, **kwargs)
        return radio
            
    @staticmethod
    def entry_base(parent, placeholder="", tt="", needpack=True, *args, **kwargs):
        entry = EntryWithPlaceholder(
            parent,
            bg=PANEL_LIGHT,
            fg=TEXT,
            insertbackground=TEXT,
            relief='flat',
            bd=0,
            width=12,
            placeholder=placeholder
        )
    
        ToolTip(entry, tt, bg=BG, fg=TEXT)
        if needpack:
            entry.pack(*args, **kwargs)
        return entry
    
    @staticmethod
    def calc_btn_base(master, text, command, tt="", needpack=True, *args, **kwargs):
        btn = tk.Button(
            master,
            text=text,
            bg=ACCENT,
            fg=TEXT,
            bd=0,
            relief='flat',
            command=command
        )
        ToolTip(btn, tt, bg=BG, fg=TEXT)
        if needpack:
            btn.pack(*args, **kwargs)
        return btn
    
    @staticmethod
    def output_base(master, needpack=True, *args, **kwargs):
        output = tk.Text(
            master,
            bg=PANEL_LIGHT,
            fg=TEXT,
            insertbackground=TEXT,
            bd=0,
            relief='flat',
            wrap='word'
        )
        if needpack:
            output.pack(*args, **kwargs)
        return output
WM = WidgetManager

class FeaturesManager:
    @staticmethod
    def corrected(stat: str, default: int = 0):
        if not stat.strip().isdecimal():
            return default
        return int(stat)
    
    @staticmethod
    def res_path(relative):
        if getattr(sys, "frozen", False):
            base = sys._MEIPASS
        else:
            base = os.path.dirname(__file__)
            
        return Path(base) / relative

    @staticmethod
    def center_window(window):
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        w = window.winfo_width()
        h = window.winfo_height()
        x = (screen_width - w) // 2
        y = (screen_height - h) // 2
        window.geometry(f"+{x}+{y}")
FM = FeaturesManager


class App(tk.Tk):
    def __init__(self, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
    
        self.title('Wplace Calculator')
        self.iconbitmap(FM.res_path('Wc.ico'))
        self.geometry("500x350")
        FM.center_window(self)
        self.resizable(False, False)
        self.config(bg=BG)
        
        self.tabs = TabsFrame(self)
        self.tabs.pack(fill='x', padx=19, pady=(10, 6))
        
        self.content = tk.Frame(self, bg=PANEL, bd=0, highlightthickness=0)
        self.content.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        self.frames = {
            'lvl': Tab1Frame(self.content),
            'stat': Tab2Frame(self.content),
            'spent': Tab3Frame(self.content),
            'time': Tab4Frame(self.content)
        }
        
        for frame in self.frames.values():
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        self.show_tab('lvl')
    
    def show_tab(self, name):
        self.frames[name].tkraise()


class TabsFrame(tk.Frame):
    """List of Tabs"""
    def __init__(self, master):
        super().__init__(master, bg=PANEL, height=48)
        self.pack_propagate(False)
        
        self.buttons = []
        
        tabs = [
            ('lvl', 'lvl', 'Calculates statistics for each level'),
            ('to_stat', 'stat', 'Calculates the statistics to the desired one'),
            ('spent_drops', 'spent', 'Calculates the droplets spent'),
            ('time', 'time', 'Calculates time for from-to stats')
        ]
        
        for text, name, tip in tabs:
            b = tk.Button(
                self,
                text=text,
                bg=PANEL_LIGHT,
                fg=TEXT,
                activebackground=ACCENT,
                activeforeground=TEXT,
                bd=0,
                relief='flat',
                command=lambda n=name: master.show_tab(n)
            )
            b.pack(side='left', padx=6, pady=6, ipadx=10, ipady=4)
            ToolTip(b, tip, bg=BG, fg=TEXT)
            self.buttons.append(b)
        
    
class Tab1Frame(tk.Frame):
    """Lvl Caclulator Tab"""
    def __init__(self, master):
        super().__init__(master, bg=PANEL)
        
        self.top = tk.Frame(self, bg=PANEL)
        self.top.pack(fill='x', padx=12, pady=(12,8))
        
        self.time_var = tk.BooleanVar()
        self.total_pxs_var = tk.BooleanVar()
        self.max_pxs_var = tk.BooleanVar()
        self.drops_var = tk.BooleanVar()
        
        time_check = WM.check_base(self.top, self.time_var, 'time', 'Add time', side='left', padx=(0, 0))
        total_pxs_check = WM.check_base(self.top, self.total_pxs_var, 'total_pxs', 'Add total pixels', side='left', padx=(10, 0))
        max_pxs_check = WM.check_base(self.top, self.max_pxs_var, 'max_pxs', 'Add max pixels', side='left', padx=(10, 0))
        max_pxs_check = WM.check_base(self.top, self.drops_var, 'drops', 'Add droplets', side='left', padx=(10, 0))
        
        self.middle = tk.Frame(self, bg=PANEL)
        self.middle.pack(fill= 'x', padx=12, pady=(4, 10))
        
        self.start_entry = WM.entry_base(self.middle, 'start_lvl', "Start Level", side='left', padx=(0, 8))
        self.end_entry = WM.entry_base(self.middle, 'end_lvl', "End Level", side='left', padx=(0, 8))
        
        self.middle3 = tk.Frame(self, bg=PANEL)
        self.middle3.pack(fill= 'x', padx=12, pady=(4, 10))
        
        self.buyed_drops_entry = WM.entry_base(self.middle3, 'buyed_drops', "Buyed droplets for money", side='left', padx=(0, 8))
        self.spent_drops_entry = WM.entry_base(self.middle3, 'spent_drops', "Droplets spent not for max pixels", side='left', padx=(0, 8))
        
        calc_btn = WM.calc_btn_base(self.middle3, 'Calculate', self.calc, 'Ratatog', side='left', padx=8, ipadx=10, ipady=3)
        
        self.bottom = tk.Frame(self, bg=PANEL_LIGHT)
        self.bottom.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        
        self.output = WM.output_base(self.bottom, fill='both', expand=True, padx=10, pady=10)
   
    def calc(self):
        vs = VisibleStats(
            time=self.time_var.get(),
            total_pxs=self.total_pxs_var.get(),
            max_pxs=self.max_pxs_var.get(),
            drops=self.drops_var.get()
        )

        res = LvlCalculator(
            vs=vs,
            start_lvl=FM.corrected(self.start_entry.get()),
            end_lvl=FM.corrected(self.end_entry.get()),
            buyed_drops=FM.corrected(self.buyed_drops_entry.get()),
            spent_drops=FM.corrected(self.spent_drops_entry.get())
        ).main()
        
        self.output.delete('1.0', tk.END)
        self.output.insert('1.0', res)
    
        
class Tab2Frame(tk.Frame):
    """Stat Calculator Tab"""
    def __init__(self, master):
        super().__init__(master, bg=PANEL)
        
        self.top = tk.Frame(self, bg=PANEL)
        self.top.pack(fill='x', padx=12, pady=(12,8))
        
        self.mode_var = tk.StringVar(self.top, M_OR)
        self.accurate_var = tk.BooleanVar(self.top)
        
        mor_check = WM.radio_base(self.top, self.mode_var, 'OR', M_OR, 'Сalculates until at least one statistic matches', side='left', padx=(0, 0))
        mor_check = WM.radio_base(self.top, self.mode_var, 'AND', M_AND, 'Сalculates until all the statistics match', side='left', padx=(10, 0))
        accurate_check = WM.check_base(self.top, self.accurate_var, 'accurate', 'Perfect calculation up to each pixel placed', side='left', padx=(10, 0))
        
        self.middle = tk.Frame(self, bg=PANEL)
        self.middle.pack(fill='x', padx=12, pady=(4, 10))
        
        self.lvl_entry = WM.entry_base(self.middle, 'lvl', "Lvl to calculate", side='left', padx=(0, 8))
        self.total_pxs_entry = WM.entry_base(self.middle, 'total_pxs', "Total pixels to calculate", side='left', padx=(0, 8))
        self.remain_pxs_entry = WM.entry_base(self.middle, 'remain_pxs', "Remain pixels to calculate", side='left', padx=(0, 8))
        
        self.middle2 = tk.Frame(self, bg=PANEL)
        self.middle2.pack(fill='x', padx=12, pady=(4, 10))
        
        self.drops_entry = WM.entry_base(self.middle2, 'drops', "Droplets to calculate", side='left', padx=(0, 8))
        self.max_pxs_entry = WM.entry_base(self.middle2, 'max_pxs', "Max pixels to calculate", side='left', padx=(0, 8))
        self.time_entry = WM.entry_base(self.middle2, 'time', "Time in seconds to calculate", side='left', padx=(0, 8))
        
        self.middle3 = tk.Frame(self, bg=PANEL)
        self.middle3.pack(fill= 'x', padx=12, pady=(4, 10))
        
        self.buyed_drops_entry = WM.entry_base(self.middle3, 'buyed_drops', "Buyed droplets for money", side='left', padx=(0, 8))
        self.spent_drops_entry = WM.entry_base(self.middle3, 'spent_drops', "Droplets spent not for max pixels", side='left', padx=(0, 8))
        
        calc_btn = WM.calc_btn_base(self.middle3, 'Calculate', self.calc, 'Ratatog', side='left', padx=8, ipadx=10, ipady=3)
        
        self.bottom = tk.Frame(self, bg=PANEL_LIGHT)
        self.bottom.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        
        self.output = WM.output_base(self.bottom, fill='both', expand=True, padx=10, pady=10)

    def calc(self):
        wf = WaitFor(
            lvl=FM.corrected(self.lvl_entry.get()),
            total_pxs=FM.corrected(self.total_pxs_entry.get()),
            remain_pxs=FM.corrected(self.remain_pxs_entry.get()),
            drops=FM.corrected(self.drops_entry.get()),
            max_pxs=FM.corrected(self.max_pxs_entry.get()),
            time=FM.corrected(self.time_entry.get()),
        )

        res = StatCalculator(
            wf=wf,
            mode=self.mode_var.get(),
            accurate=self.accurate_var.get(),
            buyed_drops=FM.corrected(self.buyed_drops_entry.get()),
            spent_drops=FM.corrected(self.spent_drops_entry.get())
        ).main()

        self.output.delete('1.0', tk.END)
        self.output.insert('1.0', res)
    

class Tab3Frame(tk.Frame):
    """Spent Drops Calculator Tab"""
    def __init__(self, master):
        super().__init__(master, bg=PANEL)
        
        self.top = tk.Frame(self, bg=PANEL)
        self.top.pack(fill='x', padx=12, pady=(12,8))
        
        self.middle = tk.Frame(self, bg=PANEL)
        self.middle.pack(fill='x', padx=12, pady=(4, 10))
        
        self.total_pxs_now_entry = WM.entry_base(self.middle, 'total_pxs', "Your current Total pixels", side='left', padx=(0, 8))
        self.drops_now_entry = WM.entry_base(self.middle, 'drops', "Your current Droplets", side='left', padx=(0, 8))
        self.max_pxs_now_entry = WM.entry_base(self.middle, 'max_pxs', "Your current Max pixels", side='left', padx=(0, 8))
        
        self.middle2 = tk.Frame(self, bg=PANEL)
        self.middle2.pack(fill= 'x', padx=12, pady=(4, 10))
        
        self.buyed_drops_entry = WM.entry_base(self.middle2, 'buyed_drops', "Buyed droplets for money", side='left', padx=(0, 8))
        
        calc_btn = WM.calc_btn_base(self.middle2, 'Calculate', self.calc, 'Ratatog', side='left', padx=8, ipadx=10, ipady=3)
        
        self.bottom = tk.Frame(self, bg=PANEL_LIGHT)
        self.bottom.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        
        self.output = WM.output_base(self.bottom, fill='both', expand=True, padx=10, pady=10)
    
    def calc(self):
        res = SpentDropsCalculator(
            total_pxs_now=FM.corrected(self.total_pxs_now_entry.get()),
            drops_now=FM.corrected(self.drops_now_entry.get()),
            max_pxs_now=FM.corrected(self.max_pxs_now_entry.get()),
            buyed_drops=FM.corrected(self.buyed_drops_entry.get())
        ).main()

        self.output.delete('1.0', tk.END)
        self.output.insert('1.0', res)
    
    
class Tab4Frame(tk.Frame):
    """Time Calculator Tab"""
    def __init__(self, master):
        super().__init__(master, bg=PANEL)
        
        self.top = tk.Frame(self, bg=PANEL)
        self.top.pack(fill='x', padx=12, pady=(12,8))
        
        self.mode_var = tk.StringVar(self.top, M_OR)
        self.accurate_var = tk.BooleanVar(self.top)
        self.flag_var = tk.BooleanVar(self.top)
        
        mor_check = WM.radio_base(self.top, self.mode_var, 'OR', M_OR, 'Сalculates until at least one statistic matches', side='left', padx=(0, 0))
        mor_check = WM.radio_base(self.top, self.mode_var, 'AND', M_AND, 'Сalculates until all the statistics match', side='left', padx=(10, 0))
        accurate_check = WM.check_base(self.top, self.accurate_var, 'accurate', 'Perfect calculation up to each pixel placed', side='left', padx=(10, 0))
        flag_check = WM.check_base(self.top, self.flag_var, 'flag', 'Flag buff', side='left', padx=(10, 0))
        
        self.middle = tk.Frame(self, bg=PANEL)
        self.middle.pack(fill='x', padx=12, pady=(4, 10))
        
        self.total_pxs_now_entry = WM.entry_base(self.middle, 'total_pxs_now', "Your current total pixels", side='left', padx=(0, 8))
        self.buyed_drops_entry = WM.entry_base(self.middle, 'buyed_drops', "Buyed droplets for money", side='left', padx=(0, 8))
        self.spent_drops_entry = WM.entry_base(self.middle, 'spent_drops', "Droplets spent not for max pixels", side='left', padx=(0, 8))

        self.middle2 = tk.Frame(self, bg=PANEL)
        self.middle2.pack(fill='x', padx=12, pady=(4, 10))
        
        self.lvl_entry = WM.entry_base(self.middle2, 'lvl', "Lvl to calculate", side='left', padx=(0, 8))
        self.total_pxs_entry = WM.entry_base(self.middle2, 'total_pxs', "Total pixels to calculate", side='left', padx=(0, 8))
        self.remain_pxs_entry = WM.entry_base(self.middle2, 'remain_pxs', "Remain pixels to calculate", side='left', padx=(0, 8))
        
        self.middle3 = tk.Frame(self, bg=PANEL)
        self.middle3.pack(fill='x', padx=12, pady=(4, 10))

        self.drops_entry = WM.entry_base(self.middle3, 'drops', "Droplets to calculate", side='left', padx=(0, 8))
        self.max_pxs_entry = WM.entry_base(self.middle3, 'max_pxs', "Max pixels to calculate", side='left', padx=(0, 8))
        self.time_entry = WM.entry_base(self.middle3, 'time', "Time in seconds to calculate", side='left', padx=(0, 8))

        self.middle4 = tk.Frame(self, bg=PANEL)
        self.middle4.pack(fill= 'x', padx=12, pady=(4, 10))
        
        calc_btn = WM.calc_btn_base(self.middle4, 'Calculate', self.calc, 'Ratatog', side='left', padx=8, ipadx=10, ipady=3)
        
        self.bottom = tk.Frame(self, bg=PANEL_LIGHT)
        self.bottom.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        
        self.output = WM.output_base(self.bottom, fill='both', expand=True, padx=10, pady=10)

    def calc(self):
            wf = WaitFor(
                lvl=FM.corrected(self.lvl_entry.get()),
                total_pxs=FM.corrected(self.total_pxs_entry.get()),
                remain_pxs=FM.corrected(self.remain_pxs_entry.get()),
                drops=FM.corrected(self.drops_entry.get()),
                max_pxs=FM.corrected(self.max_pxs_entry.get()),
                time=FM.corrected(self.time_entry.get()),
            )
    
            res = TimeCalculator(
                wf=wf,
                mode=self.mode_var.get(),
                accurate=self.accurate_var.get(),
                flag=self.flag_var.get(),
                total_pxs_now=FM.corrected(self.total_pxs_now_entry.get()),
                buyed_drops=FM.corrected(self.buyed_drops_entry.get()),
                spent_drops=FM.corrected(self.spent_drops_entry.get())
            ).main()

            self.output.delete('1.0', tk.END)
            self.output.insert('1.0', res)
        
    
class Calculator:
    def __init__(self, lvl: int = 1, total_pxs: int = 0, remain_pxs: int = 30, drops: int = 0, max_pxs: int = 0, buyed_drops: int = 0, spent_drops: int = 0, time: int = 0):
        self.lvl = lvl
        self.total_pxs = total_pxs
        self.remain_pxs = remain_pxs
        self.drops = drops
        self.max_pxs = max_pxs
        self.buyed_drops = buyed_drops
        self.spent_drops = spent_drops
        self.time = time

    def data_calc(self):
        self.remain_pxs = ceil( (self.lvl * (30**.65)) ** (1/.65) - self.total_pxs )
                
        self.drops_diff = self.buyed_drops - self.spent_drops
        
        self.time = self.total_pxs / 2 * 60
        self.drops = ((self.lvl-1)*500) + self.total_pxs + self.drops_diff
        self.buyed_pxs = (self.drops // 500 * 5)
        self.max_pxs = 60 + (self.lvl*2) + (self.buyed_pxs if self.buyed_pxs >= 0 else 0)
    
    def end(self):
        if self.total_pxs > self.total_pxs_now:
            self.lvl -= 1
            self.total_pxs = self.total_pxs_now
            return True
        return False


@dataclass
class VisibleStats:
    lvl: bool = True
    total_pxs: bool = False
    remain_pxs: bool = True
    drops: bool = False
    max_pxs: bool = False
    time: bool = False


class LvlCalculator(Calculator):
    def __init__(self, start_lvl: int, end_lvl: int, vs: VisibleStats, buyed_drops: int = 0, spent_drops: int = 0, *args, **kwargs):
        super().__init__(buyed_drops=buyed_drops, spent_drops=spent_drops, *args, **kwargs)
        self.start_lvl = start_lvl if start_lvl > 1 else 1
        self.end_lvl = end_lvl
        self.vs = vs
    
    def main(self) -> str:
        res = ""
        self.lvl = self.start_lvl - 1
        self.data_calc()
        self.total_pxs += self.remain_pxs
        
        for i in range(self.start_lvl, self.end_lvl):
            self.lvl = i
            
            self.data_calc()
            
            text = self.text_gen()
            res += f"{text}\n"
            
            self.total_pxs += self.remain_pxs
            
        return res
    
    def text_gen(self) -> str:
        text = f"lvl {self.lvl} > {self.lvl+1} : {self.remain_pxs} pxs"
                    
        stat = {}
        if self.vs.time: stat['time'] = str(timedelta(seconds=self.time))
        if self.vs.total_pxs: stat['total_pxs'] = self.total_pxs
        if self.vs.max_pxs: stat['max_pxs'] = self.max_pxs
        if self.vs.drops: stat['drops'] = self.drops
        
        if stat: text = f"{text} {str(stat)}"
        
        return text


@dataclass
class WaitFor:
    lvl: int = None
    total_pxs: int = None
    remain_pxs: int = None
    drops: int = None
    max_pxs: int = None
    time: int = None
    
    def has_any(self):
        for_check = (self.lvl, self.total_pxs, self.remain_pxs, self.drops, self.max_pxs, self.time)
        return any(for_check)
        # return any((i is not None for i in for_check))


class StatCalculator(Calculator):
    def __init__(self, wf: WaitFor, mode: str, accurate: bool, buyed_drops: int = 0, spent_drops: int = 0, *args, **kwargs):
        super().__init__(buyed_drops=buyed_drops, spent_drops=spent_drops, *args, **kwargs)
        self.wf = wf
        self.mode = mode
        self.accurate = accurate
        
        self.status = {}
        self._accurate_handlers = {
            'lvl': self._handle_lvl,
            'total_pxs': self._handle_total_pxs,
            'remain_pxs': self._handle_remain_pxs,
            'drops': self._handle_drops,
            'max_pxs': self._handle_max_pxs,
            'time': self._handle_time
        }
        
        self._mode_handlers = {
            M_OR: self._mor_handler,
            M_AND: self._mand_handler
        }
    
    def main(self) -> str:
        if not self.wf.has_any():
            return "Nothing to Calculate"

        while True:
            self.data_calc()
            
            end_flag = self.end()
            
            if not end_flag:
                self.total_pxs += self.remain_pxs
                self.lvl += 1
                self.prev_remain_pxs = self.remain_pxs
                continue
            
            if self.accurate:
                self.accurating_stat()
            
            res = {
                'lvl': self.lvl,
                'total_pxs': self.total_pxs,
                'remain_pxs': self.remain_pxs,
                'drops': self.drops,
                'max_pxs': self.max_pxs,
                'time': str(timedelta(seconds=self.time))
            }
            res = '\n'.join([f"{k}: {v}" for k, v in res.items()])
            return str(res)
              
    def end(self):
        for k, v in self.wf.__dict__.items():
            if not v: continue
            self.status[k] = getattr(self, k) >= v

        handler = self._mode_handlers.get(self.mode, self._mode_handlers[M_OR])
        return handler()

    def _mor_handler(self):
        if any(self.status.values()):
            return True
        return False
    
    def _mand_handler(self):
        if all(self.status.values()):
            return True
        return False

    def accurating_stat(self):
        last = list(self.status)[-1]
                        
        handler = self._accurate_handlers.get(last, None)
        if handler:
            handler() 
            self.data_calc()
        
    def _handle_lvl(self):
        ...
    
    def _handle_total_pxs(self):
        if self.total_pxs > self.wf.total_pxs:
            self.lvl -= 1
            self.total_pxs = self.wf.total_pxs
    
    def _handle_remain_pxs(self):
        if self.remain_pxs > self.wf.remain_pxs:
            extra_remain_pxs = self.remain_pxs - self.wf.remain_pxs
            self.total_pxs += extra_remain_pxs
    
    def _handle_drops(self):
        if self.drops - 500 > self.wf.drops:
            self.lvl -= 1
            self.total_pxs -= self.prev_remain_pxs
            self.data_calc()
            self.total_pxs += self.wf.drops - self.drops
    
    def _handle_max_pxs(self):
        added_pxs = 2 + (5 if self.drops >= 500 else 0)
        if not (self.max_pxs - added_pxs >= self.wf.max_pxs):
            return
        
        self.lvl -= 1
        self.total_pxs -= self.prev_remain_pxs
        self.data_calc()
        
        missing_max_pxs = self.wf.max_pxs - self.max_pxs
        if missing_max_pxs > 0:
            curr_drops = (self.drops % 500) if self.drops > 0 else 0
            required_drops = (ceil(missing_max_pxs / 5) * 500) - curr_drops
            self.total_pxs = self.total_pxs + required_drops
    
    def _handle_time(self):
        if self.time > self.wf.time:
            self.lvl -= 1
            missing_pxs = (self.wf.time - self.time) / 30
            self.total_pxs = self.total_pxs - self.prev_remain_pxs + missing_pxs
            

class SpentDropsCalculator(Calculator):
    def __init__(self, total_pxs_now: int, drops_now: int, max_pxs_now: int, buyed_drops: int = 0, *args, **kwargs):
        super().__init__(buyed_drops=buyed_drops, *args, **kwargs)
        self.total_pxs_now = total_pxs_now
        self.drops_now = drops_now
        self.max_pxs_now = max_pxs_now

    def main(self) -> str:
        while True:
            end_flag = self.end()
            self.data_calc()

            if not end_flag:
                self.total_pxs += self.remain_pxs
                self.lvl += 1
                continue
            
            missing_max_pxs = self.max_pxs - self.max_pxs_now
            required_drops = (ceil(missing_max_pxs / 5) * 500)
            lose_drops = required_drops - self.drops_now
            
            res = lose_drops if lose_drops > 0 else 0
            res = f"spent_drops: {res}\nspent_drops + drops_now: {res + self.drops_now}"
            return res
            

class TimeCalculator(StatCalculator):
    def __init__(self, wf, mode, accurate, flag, total_pxs_now, buyed_drops = 0, spent_drops = 0, *args, **kwargs):
        super().__init__(wf, mode, accurate, buyed_drops, spent_drops, *args, **kwargs)
        self.flag = flag
        self.total_pxs_now = total_pxs_now
    
    def main(self):
        stat_res = super().main()
        res_time = (self.total_pxs - self.total_pxs_now) / 2 * 60

        sign = "-" if res_time < 0 else ""
        if sign:
            res_time *= -1
        if self.flag:
            res_time *= 0.9
        
        res = sign + str(timedelta(seconds=res_time))
        return res
        

if __name__ == "__main__":
    app = App()
    app.mainloop()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Thu Mar 13 14:32:31 2025

@author: Wiesinger Franz
'''


# Python 3+
import tkinter as tk
from tkinter import ttk
from . import tools as t
from .constants import AppFonts as af
import os


class ConvertView(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        vcmdcl = (
            self.register(t.InpValidator.val),
            self, '%P', '%S', '%V', '%i', '%d', '%W'
        )
        # valonleave = (
        #     self.register(self._onleave), self, '%P', '%W'
        # )

        cont_m = tk.Frame(self)
        cont_b = tk.Frame(self)
        frame_tz = tk.Frame(cont_b)
        frame_lbl = tk.Frame(cont_b)
        frame_loc = tk.Frame(cont_b)
        frame_utc = tk.Frame(cont_b)
        frame_ux = tk.Frame(cont_b)

        self._vars = {
            'timezone': tk.StringVar(),
            'time_ux': tk.IntVar(),
            'time_utc': tk.StringVar(),
            'time_loc': tk.StringVar()
        }
        self.path_l = os.path.dirname(os.path.normpath(__file__))
        self.logopath = os.path.join(
            self.path_l, 'ux_logo_white_64.png'
        )
        self.uxlogo = tk.PhotoImage(file=self.logopath)
        self.lbl_logo = tk.Label(cont_m, image=self.uxlogo)

        cbx_tzvalues = t.DateTimeChecker.get_timezonelist()

        # create all widgets
        # labels column 0
        lbl_main = ttk.Label(
            cont_m, text='Unixtime Converter', font=af.fontheader,
            anchor='sw', justify=tk.CENTER, relief=tk.FLAT,
            padding=(15, 15)
        )
        lbl_timezone = tk.Label(
            frame_tz, text="Timezone", anchor='w', relief='flat',
            padx=5, pady=5, width=20, font=af.fontdefault
        )
        lbl_unixtime_utc = tk.Label(
            frame_ux, text="Unixtime (UTC)", anchor='w', relief='flat',
            padx=5, pady=5, width=20, font=af.fontdefault
        )
        lbl_isotimeformat = tk.Label(
            frame_lbl, text="ISO Datetime", anchor='w', relief='flat',
            padx=5, pady=5, width=20, font=af.fontdefault
        )
        lbl_timeformat = tk.Label(
            frame_lbl, text='YYYY-mm-dd HH:MM:SS', anchor='w', relief='flat',
            padx=5, pady=5, width=35, font=af.fontdefault, foreground='red'
        )
        lbl_time_utc = tk.Label(
            frame_utc, text="Time UTC", anchor='w', relief='flat', padx=5,
            pady=5, width=20, font=af.fontdefault
        )
        lbl_time_local = tk.Label(
            frame_loc, text="Time local", anchor='w', relief='flat', padx=5,
            pady=5, width=20, font=af.fontdefault
        )
        btn_exit = ttk.Button(
            frame_ux, text='Exit', width=15, command=self.close
        )

        self.cbx_timezone = ttk.Combobox(
            frame_tz, values=cbx_tzvalues, textvariable=self._vars['timezone'],
            width=35
        )
        self.ent_time_loc = ttk.Entry(
            frame_loc, name='time_loc', textvariable=self._vars['time_loc'],
            width=35, justify=tk.LEFT, validate='key',
            validatecommand=vcmdcl
        )
        self.ent_time_utc = ttk.Entry(
            frame_utc, name='time_utc', textvariable=self._vars['time_utc'],
            width=35, justify=tk.LEFT, validate='key',
            validatecommand=vcmdcl
        )
        self.ent_time_ux = ttk.Entry(
            frame_ux, name='time_ux', textvariable=self._vars['time_ux'],
            width=35, justify=tk.LEFT, validate='key',
            validatecommand=vcmdcl
        )

        # buttons (column 2)
        btn_reset = ttk.Button(
            frame_ux, text='Reset', width=20,
            command=lambda: t.CheckEntryData.reset_time_entries(self)
        )
        btn_time_unix = ttk.Button(
            frame_ux, text='Convert Unixtime', width=20,
            command=lambda cbxpar=self.cbx_timezone.master,
            tlocpar=self.ent_time_ux.master:
            self._conv_timeux(self, cbxpar, tlocpar)
        )
        btn_time_utc = ttk.Button(
            frame_utc, text='Convert UTC', width=20,
            command=lambda cbxpar=self.cbx_timezone.master,
            tlocpar=self.ent_time_utc.master:
            self._conv_timeutc(self, cbxpar, tlocpar)
        )
        btn_time_loc = ttk.Button(
            frame_loc, text='Convert Local Time', width=20,
            command=lambda cbxpar=self.cbx_timezone.master,
            tlocpar=self.ent_time_loc.master:
            self._conv_timeloc(self, cbxpar, tlocpar)
        )

        # set the place for widgets
        cont_m.grid(row=0, column=0, padx=10, pady=10, sticky=(
                tk.N + tk.S + tk.W + tk.E
            )
        )
        cont_b.grid(row=1, column=0, padx=10, pady=10, sticky=(
                tk.N + tk.S + tk.W + tk.E
            )
        )

        # labels column 0
        self.lbl_logo.grid(column=0, row=0, sticky=tk.W)
        lbl_main.grid(column=1, row=0, rowspan=4, sticky=(tk.S + tk.W))
        lbl_timezone.grid(column=0, row=0, padx=5, pady=2, sticky=tk.W)
        lbl_isotimeformat.grid(column=0, row=0, padx=5, pady=2, sticky=tk.W)
        lbl_timeformat.grid(column=1, row=0, padx=0, pady=2, sticky=tk.W)
        lbl_time_local.grid(column=0, row=0, padx=5, pady=2, sticky=tk.W)
        lbl_time_utc.grid(column=0, row=0, padx=5, pady=2, sticky=tk.W)
        lbl_unixtime_utc.grid(column=0, row=0, padx=5, pady=2, sticky=tk.W)
        btn_exit.grid(column=0, row=4, padx=5, pady=3, sticky=tk.W)
        btn_reset.grid(column=1, row=4, padx=5, pady=2, sticky=tk.W)

        # widgets column 1
        frame_tz.grid(column=0, row=5, sticky=(tk.W + tk.E))
        frame_lbl.grid(column=0, row=6, sticky=(tk.W + tk.E))
        frame_loc.grid(column=0, row=7, sticky=(tk.W + tk.E))
        frame_utc.grid(column=0, row=8, sticky=(tk.W + tk.E))
        frame_ux.grid(column=0, row=9, sticky=(tk.W + tk.E))

        self.cbx_timezone.grid(
            column=1, row=0, padx=5, pady=0, sticky=(tk.W + tk.E)
        )
        self.ent_time_loc.grid(
            column=1, row=0, padx=5, pady=0, sticky=(tk.W + tk.E)
        )
        self.ent_time_utc.grid(
            column=1, row=0, padx=5, pady=0, sticky=(tk.W + tk.E)
        )
        self.ent_time_ux.grid(
            column=1, row=0, padx=5, pady=2, sticky=(tk.W + tk.E)
        )

        # buttons column 2
        btn_time_loc.grid(column=2, row=0, padx=5, pady=2, sticky=tk.W)
        btn_time_utc.grid(column=2, row=0, padx=5, pady=2, sticky=tk.W)
        btn_time_unix.grid(column=2, row=0, padx=5, pady=2, sticky=tk.W)
        # delete everything in entry unixtime:
        self.ent_time_ux.delete(0, tk.END)

    def _conv_timeloc(self, event, cbxpar, tlocpar):
        time = self.ent_time_loc.get()
        tzinfo = self.cbx_timezone.get()

        if not tzinfo:
            msg = 'Please select a timezone first!'
            exc = 'Warning - missing timezone'
            t.DateTimeChecker.show_warning(self, exc, msg)
            return

        if not time:
            msg = 'No time to convert entered'
            exc = 'Warning - missing time entry'
            t.DateTimeChecker.show_warning(self, exc, msg)
            return

        # check if input is valid:
        validity = t.CheckEntryData.check_input_data(self, name='time_loc')

        if validity is True:
            tdata = t.DateTimeChecker.local_utc_ux(self, time, tzinfo)
            self.ent_time_loc.delete(0, tk.END)
            self.ent_time_utc.delete(0, tk.END)
            self.ent_time_ux.delete(0, tk.END)
            self.ent_time_loc.insert(0, time)
            self.ent_time_utc.insert(0, tdata[0])
            self.ent_time_ux.insert(0, tdata[1])

    def _conv_timeutc(self, event, cbxpar, tlocpar):
        time = self.ent_time_utc.get()
        tzinfo = self.cbx_timezone.get()

        if not tzinfo:
            msg = 'Please select a timezone first!'
            exc = 'Warning - missing timezone'
            t.DateTimeChecker.show_warning(self, exc, msg)
            return

        if not time:
            msg = 'No time (utc) to convert entered'
            exc = 'Warning - missing time entry'
            t.DateTimeChecker.show_warning(self, exc, msg)
            return

        # check if input is valid:
        validity = t.CheckEntryData.check_input_data(self, name='time_utc')

        if validity is True:
            tdata = t.DateTimeChecker.utc_loc_ux(self, time, tzinfo)
            self.ent_time_loc.delete(0, tk.END)
            self.ent_time_utc.delete(0, tk.END)
            self.ent_time_ux.delete(0, tk.END)
            self.ent_time_loc.insert(0, tdata[2])
            self.ent_time_utc.insert(0, tdata[0])
            self.ent_time_ux.insert(0, tdata[1])

    def _conv_timeux(self, event, cbxpar, tlocpar):
        time = self.ent_time_ux.get()
        tzinfo = self.cbx_timezone.get()
        # t.CheckEntryData.clear_label(self)

        if not tzinfo:
            msg = 'Please select a timezone first!'
            exc = 'Warning - missing timezone'
            t.DateTimeChecker.show_warning(self, exc, msg)
            return

        if not time:
            msg = 'No unix timestamp to convert entered'
            exc = 'Warning - no ux timestamp entered'
            t.DateTimeChecker.show_warning(self, exc, msg)
            return

        # check if input is valid:
        validity = t.CheckEntryData.check_input_data(self, name='time_ux')

        if validity is True:
            tdata = t.DateTimeChecker.ux_utc_loc(self, time, tzinfo)
            self.ent_time_loc.delete(0, tk.END)
            self.ent_time_utc.delete(0, tk.END)
            self.ent_time_ux.delete(0, tk.END)
            self.ent_time_loc.insert(0, tdata[2])
            self.ent_time_utc.insert(0, tdata[0])
            self.ent_time_ux.insert(0, tdata[1])

    def close(self):
        self.quit()

    def get(self):
        data = dict()

        for key, variable in self._vars.items():
            try:
                data[key] = variable.get()
            except tk.TclError:
                message = f'Error in field: {key}. No data found'
                raise ValueError(message)
        return data

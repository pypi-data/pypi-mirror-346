#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Thu Mar 13 14:32:31 2025

@author: Wiesinger Franz
'''


# Python 3+
from datetime import datetime
from zoneinfo import ZoneInfo
import zoneinfo
import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkfont
import tkinter.scrolledtext as tkscroll
import re


class DateTimeChecker(datetime):

    def __init__(self):
        super().__init__(self)

    def get_timezonelist():
        tzlist = []
        tzl = zoneinfo.available_timezones()
        for row in tzl:
            tzlist.append(row)
        return sorted(tzlist)

    def get_localtime(zoneinfo):
        loc_time = datetime.now(tzinfo=ZoneInfo(key=zoneinfo))
        return loc_time

    def check_dt_string(dtimestr):
        valid = True
        formatstr = '%Y-%m-%d %H:%M:%S'
        try:
            ts = datetime.strptime(dtimestr, formatstr)
            if ts:
                valid = True
                return valid

        except ValueError:
            valid = False
            return False

    def show_warning(self, exc, msg):
        messagebox.showwarning(exc, msg)

    def local_utc_ux(self, time, tzinfo):
        tz = ZoneInfo(tzinfo)
        formatstr = '%Y-%m-%d %H:%M:%S'
        ts = datetime.strptime(time, formatstr)
        loc_ts = ts.astimezone(tz)
        time_uc = loc_ts.astimezone(ZoneInfo('UTC'))
        time_ux = int(loc_ts.astimezone(ZoneInfo('UTC')).timestamp())
        insert_utc = datetime.strftime(time_uc, formatstr)
        return insert_utc, time_ux

    def utc_loc_ux(self, time, tzinfo):
        formatstr = '%Y-%m-%d %H:%M:%S'
        tz_loc = ZoneInfo(tzinfo)
        tz_utc = ZoneInfo('UTC')
        utc_form = datetime.strptime(time, formatstr)
        localized_utc = utc_form.replace(tzinfo=tz_utc)
        # convert timestrin from utc to a utc-datetime incl. timezone
        loc_time = localized_utc.astimezone(tz_loc)
        # convert utc into unixtime
        time_ux = int(localized_utc.timestamp())
        ts = datetime.strftime(loc_time, formatstr)
        insert_utc = datetime.strftime(localized_utc, formatstr)
        return insert_utc, time_ux, ts

    def ux_utc_loc(self, time, tzinfo):
        # tz_loc = timezone local
        # tz_utc = timezone utc
        # tutc = time utc
        # ins_utc = insert utc value
        # ins_loc = insert local time value
        tz_loc = ZoneInfo(tzinfo)
        tz_utc = ZoneInfo('UTC')
        tutc = datetime.fromtimestamp(int(time), tz_utc)
        formatstr = '%Y-%m-%d %H:%M:%S'
        ins_utc = datetime.strftime(tutc, formatstr)
        time_loc = datetime.fromtimestamp(int(time), tz_loc)
        ins_loc = datetime.strftime(time_loc, formatstr)
        return ins_utc, int(time), ins_loc


class InpValidator:
    '''Adds validation functionality to entry fields'''

    def __init__(
            self, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

    def _toggle_error(self, on=False):
        self.configure(foreground=('red' if on else 'black'))

    def val(self, prop, char, event, index, action, framename):

        valid = True
        entryobjname = framename.split('.')[-1]

        if event == 'key' and entryobjname in ('time_loc', 'time_utc'):

            if len(char) > 5:
                dtimestr = char
                valid = DateTimeChecker.check_dt_string(dtimestr)
                if valid is True:
                    return valid
                elif valid is False:
                    return valid

            if action == '0':  # This is a delete action
                valid = True
            elif index in (
                '0', '1', '2', '3', '5', '6', '8', '9', '11', '12', '14', '15',
                '17', '18'
            ):
                valid = char.isdigit()

            elif index in ('4', '7'):
                valid = char == '-'
            elif index == '10':
                valid = char == ' '
            elif index in ('13', '16'):
                valid = char == ':'
            else:
                valid = False

            return valid

        elif event == 'key' and entryobjname == 'time_ux':
            valid = True

            if action == '0':  # This is a delete action
                valid = True
            elif index in (
                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'
            ):
                valid = char.isdigit()
            else:
                valid = False
            return valid


class CheckEntryData(DateTimeChecker):
    '''All functions and methods happened at focusout in entry objects'''

    def __init__(
            self, *args, error_var=None, **kwargs
    ):
        self.error = error_var or tk.StringVar()
        super().__init__(*args, **kwargs)

    def check_input_data(self, name):
        valid = True

        if name in ('time_loc', 'time_utc'):
            if name == 'time_loc':
                dtimestr = self.ent_time_loc.get()
            else:
                dtimestr = self.ent_time_utc.get()

            if dtimestr:
                valid = DateTimeChecker.check_dt_string(dtimestr)

                if valid is False:
                    msg = 'Not a valid date time!'
                    exc = 'Warning - Wrong datetime'
                    DateTimeChecker.show_warning(self, exc, msg)
                    valid = False
                    return

            formatstr = '%Y-%m-%d %H:%M:%S'
            vtimestamp = int(
                datetime.strptime(dtimestr, formatstr).timestamp()
            )

            if vtimestamp < 1:
                msg = (
                    'No valid unixtime! \n'
                    + 'Date and time before 1970-01-01 14:00:00! \n'
                    + 'this is before the Unix epoch!'
                    + 'the lowest value for converting is 1'
                )
                exc = 'Warning - Wrong Unixtime'
                DateTimeChecker.show_warning('', exc, msg)
                valid = False
                return

            elif vtimestamp > 99999999999:
                msg = (
                    'No valid unixtime! \n'
                    + 'Date and time after  5138-11-16 09:46:39! \n'
                    + 'We do not convert time after this date and time!'
                )
                exc = 'Warning - Wrong Unixtime'
                DateTimeChecker.show_warning(self, exc, msg)
                valid = False
                return

        elif name == 'time_ux':
            vux = int(self.ent_time_ux.get())

            if vux > 99999999999:
                msg = (
                    'No valid unixtime!\n' +
                    'The max value = 99999999999!'
                )
                exc = 'Warning - Invalid Unixtime'
                DateTimeChecker.show_warning(self, exc, msg)
                valid = False
                return

            if vux < 1:
                msg = (
                    'No valid unixtime!\n' +
                    'The min value = 1!'
                )
                exc = 'Warning - Invalid Unixtime'
                DateTimeChecker.show_warning(self, exc, msg)
                valid = False
                return

        return valid

    def reset_time_entries(self):
        t_loc = self.ent_time_loc
        t_utc = self.ent_time_utc
        t_ux = self.ent_time_ux

        timefields = [t_loc, t_utc, t_ux]

        for field in timefields:
            try:
                entryvalue = field.get()
                if not entryvalue:
                    pass
                else:
                    field.delete(0, tk.END)
            except Exception:
                msg = 'An error at the resetoperation happened'
                exc = 'Warning - reset error'
                DateTimeChecker.show_warning(self, exc, msg)


class SimpleMarkdownText(tkscroll.ScrolledText):
    '''
    Really basic Markdown display. Thanks to Bryan Oakley's RichText:
    https://stackoverflow.com/a/63105641/79125
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_font = tkfont.nametofont(self.cget('font'))

        em = default_font.measure('m')
        default_size = default_font.cget('size')
        bold_font = tkfont.Font(**default_font.configure())
        italic_font = tkfont.Font(**default_font.configure())

        bold_font.configure(weight='bold')
        italic_font.configure(slant='italic')

        # Small subset of markdown. Just enough to make text look nice.
        self.tag_configure('**', font=bold_font)
        self.tag_configure('*', font=italic_font)
        self.tag_configure('_', font=italic_font)
        self.tag_chars = '*_'
        self.tag_char_re = re.compile(r'[*_]')

        max_heading = 3
        for i in range(1, max_heading + 1):
            header_font = tkfont.Font(**default_font.configure())
            header_font.configure(
                size=int(default_size * i + 3), weight='bold'
            )
            self.tag_configure(
                '#' * (max_heading - i), font=header_font,
                spacing3=default_size
            )

        lmargin2 = em + default_font.measure('\u2022 ')
        self.tag_configure('bullet', lmargin1=em, lmargin2=lmargin2)
        lmargin2 = em + default_font.measure('1. ')
        self.tag_configure('numbered', lmargin1=em, lmargin2=lmargin2)

        self.numbered_index = 1

    def insert_bullet(self, position, text):
        self.insert(position, f'\u2022 {text}', 'bullet')

    def insert_numbered(self, position, text):
        self.insert(position, f"{self.numbered_index}. {text}", 'numbered')
        self.numbered_index += 1

    def insert_markdown(self, mkd_text):
        '''
        A very basic markdown parser.

        Helpful to easily set formatted text in tk. If you want actual markdown
        support then use a real parser.
        '''
        for line in mkd_text.split('\n'):
            if line == '':
                # Blank lines reset numbering
                self.numbered_index = 1
                self.insert('end', line)

            elif line.startswith('#'):
                tag = re.match(r'(#+) (.*)', line)
                line = tag.group(2)
                self.insert('end', line, tag.group(1))

            elif line.startswith('* '):
                line = line[2:]
                self.insert_bullet('end', line)

            elif line.startswith('1. '):
                line = line[2:]
                self.insert_numbered('end', line)

            elif not self.tag_char_re.search(line):
                self.insert('end', line)

            else:
                tag = None
                accumulated = []
                skip_next = False
                for i, c in enumerate(line):
                    if skip_next:
                        skip_next = False
                        continue
                    if c in self.tag_chars and (not tag or c == tag[0]):
                        if tag:
                            self.insert('end', ''.join(accumulated), tag)
                            accumulated = []
                            tag = None
                        else:
                            self.insert('end', ''.join(accumulated))
                            accumulated = []
                            tag = c
                            next_i = i + 1
                            if len(line) > next_i and line[next_i] == tag:
                                tag = line[i: next_i + 1]
                                skip_next = True

                    else:
                        accumulated.append(c)
                self.insert('end', ''.join(accumulated), tag)

            self.insert('end', '\n')

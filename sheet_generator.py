#!/usr/bin/env python
# coding: utf-8

# # Yearly Goal Checker

# ## Project Imports

# In[93]:


import os
import argparse
import IPython.display

from dateutil import rrule
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw


# ## Settings

# In[94]:

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--title', help='Title of the Goal', required=True, type=str)
parser.add_argument('-y', '--year', help='Year of the Goal', default=datetime.today().year, type=int)
parser.add_argument('-p', '--people', help='Number of People (1 or 2)', default=1, type=int)
parser.add_argument('-i', '--initials', help='Initials of the two people. String of length 2.', default=None, type=str)
parser.add_argument('-c', '--color', help='Color of the Sheet (Dark)', default='#2c5c74', type=str)
args = parser.parse_args()


# Parameters
num_people = args.people
initials = args.initials
title_txt = args.title
year = args.year
markup_color = args.color


# In[96]:


a4_size = 3508, 2480
bg_color = '#f3f3f3'
text_color = '#ffffff'

font_path = 'fonts\\Arial.ttf'

fnt_40 = ImageFont.truetype(font_path, 40)
fnt_60 = ImageFont.truetype(font_path, 60)
fnt_80 = ImageFont.truetype(font_path, 80)
fnt_100 = ImageFont.truetype(font_path, 100)

motivational_quote = "YOU CAN\nDO IT"

month_names = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

save_path = os.path.join('images')


# ## Transformations & Tests

# In[97]:


assert(num_people in [1,2])
if initials is not None:
    assert(len(initials) in [1,2])
    
if not os.path.exists(save_path):
    os.makedirs(save_path)

all_days = rrule.rrule(
    rrule.DAILY,
    dtstart=datetime.strptime(f'{year}0101', '%Y%m%d'),
    until=datetime.strptime(f'{year}1231', '%Y%m%d')
)

title_txt = title_txt.upper()
motivational_quote = motivational_quote.upper()


# ## Generate Image

# In[98]:


ig_img = Image.new('RGBA', (a4_size), color=bg_color)

bg_w, bg_h = ig_img.size

d = ImageDraw.Draw(ig_img)

title_line = 100 # space for the title on top
month_line = 408 # space for the name of the month in pixels
row_size = int(((bg_h-100)/12)) # size of each month line
day_size = (bg_w - month_line) / 31 # size of one day
height_adj = 1.3 # this adjustment needed (maybe due to border lines)

# Draw Frame
d.line(((0, 0), (0, bg_h)), markup_color, width=10) # left frame line
d.line(((bg_w, 0), (bg_w, bg_h)), markup_color, width=15) # right frame line
d.line(((month_line, 0), (month_line, bg_h)), markup_color, width=5) # month line

d.line(((0, 0), (bg_w, 0)), markup_color, width=10)
d.line(((0, bg_h), (bg_w, bg_h)), markup_color, width=15)

d.rectangle((0,0,month_line, bg_h), markup_color, markup_color, width=3) # shaded area for months on left
d.rectangle((0,0,bg_w, title_line), markup_color, markup_color, width=3) # shaded area for title

w, h = d.textsize(title_txt, font=fnt_60)
d.text(((bg_w-w)/2, (title_line-h)/2), title_txt, font=fnt_60, fill=text_color, align='center')

for row in range(12):
    ln = row + 1
    h_offset = int(row_size*ln) + title_line
    month_txt = month_names[row]
    w, h = d.textsize(month_txt, font=fnt_80)
    
    if row < 11:
        d.line(((0, h_offset), (bg_w, h_offset)), markup_color, width=5)
        d.line(((month_line, h_offset-row_size/2), (bg_w, h_offset-row_size/2)), markup_color, width=2)
        if num_people == 2:
            d.line(((month_line, h_offset-row_size/4), (bg_w, h_offset-row_size/4)), markup_color, width=2)
            if initials:
                person_1_txt = initials[0].upper()
                pw, ph = d.textsize(person_1_txt, font=fnt_40)
                d.text((month_line-pw*1.2, (h_offset-row_size/2)), person_1_txt, font=fnt_40, fill=text_color, align='center')
                person_1_txt = initials[1].upper()
                pw, ph = d.textsize(person_1_txt, font=fnt_40)
                d.text((month_line-pw*1.2, (h_offset-row_size/4)), person_1_txt, font=fnt_40, fill=text_color, align='center')
        
        d.text(((month_line-w)/2, h_offset-((row_size+h)/2)), month_txt, font=fnt_80, fill=text_color, align='center')
    else:
        d.line(((month_line, h_offset-row_size/2), (bg_w, h_offset-row_size/2)), markup_color, width=2)
        d.text(((month_line-w)/2, h_offset-((row_size+h)/2)), month_txt, font=fnt_80, fill=text_color, align='center')
        if num_people == 2:
            d.line(((month_line, h_offset-row_size/4), (bg_w, h_offset-row_size/4)), markup_color, width=2)
            if initials:
                person_1_txt = initials[0].upper()
                pw, ph = d.textsize(person_1_txt, font=fnt_40)
                d.text((month_line-pw*1.1, (h_offset-row_size/2)), person_1_txt, font=fnt_40, fill=text_color, align='center')
                person_1_txt = initials[1].upper()
                pw, ph = d.textsize(person_1_txt, font=fnt_40)
                d.text((month_line-pw*1.1, (h_offset-row_size/4)), person_1_txt, font=fnt_40, fill=text_color, align='center')
    
    month_days = [d for d in all_days if d.month == ln]
    
    for idx, day in enumerate(month_days):
        day_ln = idx + 1
        w_offset = int(day_size*day_ln)
        d.line(((month_line+w_offset, h_offset-row_size), (month_line+w_offset, h_offset)), markup_color, width=5)
        c = markup_color
        
        if day.weekday() in [5,6]:
            d.rectangle((
                month_line+w_offset-day_size, h_offset-row_size,
                month_line+w_offset, h_offset-row_size/2), markup_color, markup_color, width=3)
            c = text_color

        day_txt = str(day.day)
        w, h = d.textsize(day_txt, font=fnt_60)
        d.text((month_line+w_offset-day_size+((day_size-w)/2), (h_offset)-row_size+(h/3)), day_txt, font=fnt_60, fill=c, align='center')
    
    if day.day < 31:
        d.rectangle((
            month_line+w_offset, h_offset-row_size,
            bg_w, h_offset), markup_color, markup_color, width=3)
    
    # Write the year
    if day.day in [28,29]:
        txt_space = (31 - day.day) * day_size
        txt_fnt = fnt_60 if day.day == 28 else fnt_40
        txt_txt = str(motivational_quote)
        w, h = d.textsize(txt_txt, font=txt_fnt)
        d.text((month_line + w_offset + (txt_space-w)/2, h_offset-((row_size+h)/2)), txt_txt, font=txt_fnt, fill=text_color, align='center')
    
year_txt = str(year)
w, h = d.textsize(year_txt, font=fnt_80)
d.text(((month_line-w)/2, (title_line-h)/2), year_txt, font=fnt_80, fill=text_color, align='center')
    
timestamp_str = datetime.today().strftime('%Y%m%d')
save_file_name = os.path.join(save_path, f'{timestamp_str}_goals_calendar.png')
ig_img.save(save_file_name)


# In[ ]:





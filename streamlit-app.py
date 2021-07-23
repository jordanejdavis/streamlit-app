#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
from bokeh.plotting import figure
import math
from PIL import Image

st.set_page_config(layout="wide", page_title="Jordan Davis' Dashboard")
st.header("""**Jordan's Data Visualisation Dashboard**""")



# Data preprocessing


file = pd.ExcelFile(r"excel test1.xlsx")
df = pd.read_excel(file, "KPIs", index_col=0)  # index col set to the KPI column
df.iloc[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
         16, 21, 25, 26, 27, 29, 30, 31, 32]] = df.iloc[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                                         11, 12, 13, 14, 16, 21, 25, 26, 27, 29, 30,
                                                         31, 32]] * 100  # Decimal percentages to normal
df = df.round(2)

# Graph function


def graph():
        global options2
        global options
        # if statement to change the y-axis label based on KPI
        if options2 == "Housekeeping payroll (per room sold)" or options2 == "ADR" or options2 == "RevPAR" or                 options2 == "Laundry cost (per room sold)" or                 options2 == "Accommodation payroll (per room sold)" or options2 == "Utilities cost (per room sold)" or                options2 == "C/C commission (per room sold)":
                y = "£"
        else:
                y = "%"
        TOOLTIPS = [(f"{options2}  {y}", "@y"), ("Hotel & Month", "@x")]  # Tooltips for the hover tool,
        # Enter a list of tuples. First tuple is the KPI, which is why it is a variable (it needs to be able to change
        # with the graph). The second tuple displays the Hotel and Year from the x-axis. The @ signs mean the data is
        # tied to the data displayed. Alternatively, the $ would allow a movement of the data (but we don't want that,
        # especially on the x-axis as we are using categorical data)
        p = figure(x_range=list(df.iloc[0][options].index), title=options2, x_axis_label="Hotel & Month",
                   y_axis_label=y, tooltips=TOOLTIPS)

        p.title.text_font_size = "35px"
        p.title.align = "center"
        p.xaxis.axis_label_text_font_size = "25pt"
        p.xaxis.major_label_text_font_size = "10pt"
        p.yaxis.axis_label_text_font_size = "25pt"
        p.yaxis.major_label_text_font_size = "10pt"
        p.circle(list(df.loc[options2][options].index), df.loc[options2][options],
                 fill_color="blue", size=10, alpha=1)
        p.line(list(df.loc[options2][options].index), df.loc[options2][options], line_width=0.5)
        p.xaxis.major_label_orientation = math.pi/2.8
        return st.bokeh_chart(p, use_container_width=True)


def data():
        data_to_table = df.loc[options2][options]  # df.loc[rows][columns]
        return st.write(pd.DataFrame(data_to_table))

# Creating lists for the different "ALL" dates

l = list(df.columns)
l.append("All Data in Existence")

# Going through the df columns and adding them to a list if the column label contains the desired month
month_list = ["Jan", "Feb", "March", "April", "May", "June",
              "July", "August", "Sept", "Oct", "Nov", "Dec"]
year_list = [2019, 2020, 2021]
month_dict = {}
for j in year_list:
    for i in month_list:
        month_dict[i+" "+str(j)] = []

for i in month_dict:
    for j in list(df.columns):
        if i in j:
            month_dict[i].append(j)
months = list(month_dict.keys())
months.insert(0, "OFF")


# Sidebar and multiselect


start = month_dict["March 2021"]  # This list used for the multiselect

hotels = ["Consolidated", "Hotel A", "Hotel B", "Hotel C", "Hotel D", "Hotel E", "Hotel F", "Hotel G", "Hotel H", "Hotel I",
          "Hotel J", "Hotel K", "Hotel L"]  # This list is used for the button loop

st.sidebar.write("""**Hotel and month selector:**""")
options = st.sidebar.multiselect("", options=l, default=start)


if "All Data in Existence" in options:
        options = list(df.columns)


# KPI selector
st.sidebar.write("""**KPI selector**""")
options2 = st.sidebar.selectbox("", list(df.index))

####################################################################################################################
# HOTEL BUTTONS
st.sidebar.write("""**Hotel buttons:**""")

for j in hotels:
    j_button = st.sidebar.button(j)
    if j_button:
        options.clear()
        for i in list(df.columns):
            if j in i:
                options.append(i)

# Month slider
st.sidebar.write("""**Month Override:**""")
month = st.sidebar.select_slider("", months)
st.sidebar.write(r"Note this needs to be set to 'OFF' to unlock other interactive features")
if month != "OFF":
    options.clear()

for i in month_dict.keys():
    if month == i:
        options = month_dict[i]


# Calling graph function

graph()
data()

st.write("Raw Data:")
st.write(df)


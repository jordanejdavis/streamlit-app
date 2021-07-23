import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FactorRange, NumeralTickFormatter
from bokeh.palettes import Spectral5
from bokeh.transform import factor_cmap
import math
from PIL import Image


st.set_page_config(layout="wide", page_title="CWH Dashboard")


def start():
    my_page = st.sidebar.radio('Page Navigation', ['P&L KPIs', 'Forecast'])
    
    if my_page == "P&L KPIs":
        st.title("KPIs")

        # Data preprocessing


        file = pd.ExcelFile(r"excel test.xlsx")
        df = pd.read_excel(file, "KPIs", index_col=0)  # index col set to the KPI column
        df.iloc[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
                 16, 21, 25, 26, 27, 29, 30, 31, 32]] = df.iloc[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                                                 11, 12, 13, 14, 16, 21, 25, 26, 27, 29, 30,
                                                                 31, 32]] * 100  # Decimal percentages to normal
        df = df.round(2)

        # Creating lists for the different "ALL" dates
        l = list(df.columns)
        l.append("All Data in Existence")

        start = ["Consolidated April 2021", "Broome April 2021", "Cosmo April 2021", "Denham April 2021", "ESN April 2021",
                 "Harben April 2021", "HISN April 2021", "HIMSO April 2021", "Hunton April 2021", "Pendulum April 2021",
                 "Park Hall April 2021", "The Manor April 2021", "Whately April 2021"]  # This list used for the multiselect

        # Sidebar and multiselect
        st.sidebar.write("""**Hotel and month selector:**""")
        options = st.sidebar.multiselect("", options=l, default=start)

        # KPI selector
        st.sidebar.write("""**KPI selector**""")
        options2 = st.sidebar.selectbox("", list(df.index))


        def graph():
            # if statement to change the y-axis label based on KPI
            if options2 == "Housekeeping payroll (per room sold)" or options2 == "ADR" or options2 == "RevPAR" or options2 == "Laundry cost (per room sold)" or options2 == "Accommodation payroll (per room sold)" or options2 == "Utilities cost (per room sold)" or options2 == "C/C commission (per room sold)" or options2 == "Average F&B spend (per room sold)":
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
            p.xaxis.axis_label_text_font_style = "bold"
            p.xaxis.major_label_text_font_size = "10pt"
            p.xaxis.major_label_text_font_style = "bold"
            p.yaxis.axis_label_text_font_size = "25pt"
            p.yaxis.axis_label_text_font_style = "bold"
            p.yaxis.major_label_text_font_size = "10pt"
            p.yaxis.major_label_text_font_style = "bold"
            p.circle(list(df.loc[options2][options].index), df.loc[options2][options],
                     fill_color="blue", size=10, alpha=1.5)
            p.line(list(df.loc[options2][options].index), df.loc[options2][options], line_width=0.5, alpha = 1)
            p.xaxis.major_label_orientation = math.pi / 2.8
            return st.bokeh_chart(p, use_container_width=True)

        # Going through the df columns and adding them to a dict of lists if the column label contains the desired month
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



        hotels = ["Consolidated", "Broome", "Cosmo", "Denham", "ESN", "Harben", "HISN", "HIMSO", "Hunton", "Pendulum",
                  "Park Hall", "The Manor", "Whately"]  # This list is used for the button loop


        if "All Data in Existence" in options:
            options = list(df.columns)


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



    
    
    
    #################################################################################################################
    # NEXT PAGE
    else:
        st.title("Forecast example. Randomly generated data")
        df = pd.read_csv(r"bokeh_fc.csv", index_col=0, na_values="-")
        hotel_list = ["Consolidated", "Broome", "Chicheley", "Cosmo", "Denham", "ESN", "Harben", "HIMSO", "HISN",
                   "Hunton", "Manor", "Pendulum", "Park Hall", "Warwick", "Whately"]
        type = st.sidebar.selectbox(label="Hotel selector", options=hotel_list)
        month = st.sidebar.selectbox(label="Month selector", options=["CM", "CM+1", "CM+2"])

        df_reduced = df[:][[f"{type} {month}", f"{type} Budget {month}", f"{type} LY {month}"]]

        def graph2():
            streams = list(df_reduced.index)
            periods = list(df_reduced.columns)
            data = {"streams": list(df_reduced.index),
                    df_reduced.columns[0]: list(df_reduced.iloc[:][df_reduced.columns[0]]),
                    df_reduced.columns[1]: list(df_reduced.iloc[:][df_reduced.columns[1]]),
                    df_reduced.columns[2]: list(df_reduced.iloc[:][df_reduced.columns[2]])
            }
            x = [(x, y) for x in streams for y in periods]
            counts = sum(zip(data[df_reduced.columns[0]],
                             data[df_reduced.columns[1]],
                             data[df_reduced.columns[2]]), ())
            source = ColumnDataSource(data=dict(x=x, counts=counts))

            p = figure(x_range=FactorRange(*x), plot_height=500, tooltips ="@x: £@counts{,0.00}",
                       title=df_reduced.columns[0]+" Forecast",
                       y_axis_label="Revenue (£)")

            p.vbar(x='x', top='counts', width=0.9, source=source,
                   fill_color=factor_cmap('x', palette=Spectral5, factors=periods, start=1, end=2))


            p.x_range.range_padding = 0.1
            p.xaxis.major_label_orientation = 1
            p.xgrid.grid_line_color = None
            p.title.align = "center"
            p.yaxis.major_label_text_font_style = "bold"
            p.xaxis.major_label_text_font_style = "bold"
            p.xaxis.axis_label_text_font_style = "bold"


            p.yaxis.formatter = NumeralTickFormatter(format="00,")
            return st.bokeh_chart(p, use_container_width=True)

        graph2()
        
start()

import streamlit as st
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import time
import seaborn as sns
import datetime
import streamlit.components.v1 as components
import logging
import base64




from functools import wraps

logger = logging.getLogger(__name__)

logger.setLevel("INFO")
handler = logging.FileHandler(filename="log.txt", mode="a")
log_format = "%(asctime)s %(levelname)s -- %(message)s"
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)
logger.addHandler(handler)

logging.info('\nNew Execution at :', time.time(), "\n")

def timed(func):
    """This decorator prints the execution time for the decorated function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info("{} ran in {}s".format(func.__name__, round(end - start, 2)))
        return result

    return wrapper




st.title('Lab 2 Dashboard Germain Deffontaines')


option = st.selectbox(
'Wich dashboard do you want to see ?',
('Uber raw data', 'New York trip data'))


if option == 'Uber raw data' :

    st.title('Uber row data April 14')

    st.header('Head of the dataframe: ')

    @timed
    @st.cache(allow_output_mutation=True)
    def oponedf ():
        path = "uber-raw-data-apr14.csv"
        df = pd.read_csv(path, delimiter = ',')
        df['Date/Time'] = pd.to_datetime(df['Date/Time'])
        df['Date/Time'] = df['Date/Time'].map(pd.to_datetime)
        return df

    df1 = oponedf()

    @timed
    @st.cache(suppress_st_warning=True)
    def oponed2(df):

        def get_dom(dt):
            return dt.day
        df['dom'] = df['Date/Time'].map(get_dom)
        def get_weekday(dt):
            return dt.weekday()
        df['weekday'] = df['Date/Time'].map(get_weekday)
        def get_hour(dt):
            return dt.hour
        df['hour'] = df['Date/Time'].map(get_hour)
        return df

    df2 = oponed2(df1)
    st.write(df2.head())


    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Latitude Max", "42.1166°", "+2,0437°")
    col2.metric("Latitude Min", "40.0729°", "-2,0437°")
    col3.metric("Longitude Max", "-72.066°", "+2,7067°")
    col4.metric("Longitude Min", "-74.773°", "-2,7067°")

    st.header('Set a range of date for the two next charts :')
    d5 = st.date_input("", [datetime.date(2014, 4, 1), datetime.date(2014, 4, 30)])    #st.bar_chart(df2)
    @st.cache
    def count_rows(rows):
        return len(rows)

       
    by_date = df2.groupby('dom').apply(count_rows)

    st.header('Frequency by Date of the Month (Line chart):')
    st.line_chart(by_date.loc[(by_date.index >= d5[0].day) & (by_date.index <= d5[1].day)])
    
    st.header('Frequency by Date of the Month (Bar chart):')
    st.bar_chart(by_date.loc[(by_date.index >= d5[0].day) & (by_date.index <= d5[1].day)])

    @st.cache(suppress_st_warning=True)
    def plo(d5, df2): 
        by_hour = df2.groupby('hour').apply(count_rows)
        
        return by_hour
    by_hour = plo(d5, df2)

    st.header('Frequency by hours (Bar chart):')
    st.bar_chart(by_hour)

    @st.cache(suppress_st_warning=True)
    def week(df2):
        by_week = df2.groupby('weekday').apply(count_rows)
        return by_week
    by_week = week(df2)

    st.header('Frequency by Weekday (Bar chart):')
    st.bar_chart(by_week)

    @st.cache(suppress_st_warning=True)
    def df33(df2):
        df3 = df2.groupby(['weekday', 'hour']).apply(count_rows).unstack()
        return df3

    df3 = df33(df2)


    st.header('Frequency by hour of Weekday (Heatmap chart):')
    fig, ax = plt.subplots()
    sns.heatmap(df3, ax=ax)
    st.write(fig)



    st.header('Scatter plot of Uber - April 14 :')
    fig3, ay = plt.subplots(figsize=(15,15),dpi=100)
    ay.set_xlabel('Latitude')
    ay.set_ylabel('Longitude')
    ay.scatter(df2['Lat'].to_list(),df2['Lon'].to_list(),s=0.8, alpha=0.4)
    ay.set_xlim(40.7, 40.9)
    ay.set_ylim(-74.1, -73.9)
    st.write(fig3)
    
    file_ = open("chart1.png", "rb")
    contents = file_.read()
    data_url_chart1 = base64.b64encode(contents).decode("utf-8")
    file_.close()
    components.html(
        """
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        <div id="accordion">
        <div class="card">
            
        </div>
            <img src="data:image/gif;base64,{data_url_chart1}" style="width: 350px;height:auto;"></img>
        </div>
        """,
        height=600,
    )


if option == 'New York trip data' :
    st.title('New York trip data the 15/01/2015')
    st.header('Head of the dataframe: ')

    @st.cache(allow_output_mutation=True)
    def oponedfny ():
        path2 = 'ny-trips-data.csv'
        df4 = pd.read_csv(path2, delimiter = ',')
        return df4

    df4 = oponedfny()
    st.write(df4.head())

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col, col9 = st.columns(2)
    col1.metric("Total Tip Amount", " 166 923.44 $")
    col2.metric("Total fare Amount", " 1 207 726.96 $")
    col3.metric("Total Amount", " 1 517 640.93 $", '+142 991 $')
    col4.metric("Total extra Amount", " 142 991 $")
    col.metric(' Total distance ','278658 mi')
    col9.metric(' Total distance ','448456 km')
    st.metric(' Total passengers ','163602')

    st.header('Pickup longitude & latitude :')
    col5,col6 = st.columns(2)
    
    fig4, az = plt.subplots()
    az.hist(df4['pickup_latitude'], bins=100, range=(40.7,40.8))
    az.set_xlabel('Pickup latitude')
    az.set_ylabel('Frequency')
    az.set_title('Pickup latitude') 

    fig5, ag = plt.subplots()
    ag.hist(df4['pickup_longitude'], bins=100, range=(-74,-73.85))
    ag.set_xlabel('Pickup longitude')
    ag.set_ylabel('Frequency')
    ag.set_title('Pickup longitude')

    col5.write(fig4)
    col6.write(fig5)
    
    st.header('Dropoff longitude & latitude :')
    col7,col8 = st.columns(2)
    
    fig6, az = plt.subplots()
    az.hist(df4['dropoff_latitude'], bins=100, range=(40.7,40.8))
    az.set_xlabel('Dropoff latitude')
    az.set_ylabel('Frequency')
    az.set_title('Dropoff latitude') 

    fig7, ag = plt.subplots()
    ag.hist(df4['dropoff_longitude'], bins=100, range=(-74,-73.85))
    ag.set_xlabel('Dropoff longitude')
    ag.set_ylabel('Frequency')
    ag.set_title('Dropoff longitude')

    col7.write(fig6)
    col8.write(fig7)

    st.header('Pickup and dropoff location :')
    fig8, at = plt.subplots(figsize=(15,15),dpi=100)
    at.scatter(df4['dropoff_latitude'].to_list(),df4['dropoff_longitude'].to_list(),s=0.8, alpha=0.8, color = 'r', label = 'Dropoff location (red)')
    at.legend(loc = 'best')
    at.set_title('Dropoff and Pickup Locations')
    at.set_xlabel('Latitude')
    at.set_ylabel('Longitude')
    at.twiny()
    at.scatter(df4['pickup_latitude'].to_list(),df4['pickup_longitude'].to_list(),s=0.8,color = 'g', alpha = 0.5, label = 'Pickup location (green)')
    at.legend(loc = 'upper left')
    at.set_xlim(40.6, 40.9)
    at.set_ylim(-74.05, -73.75)
    st.write(fig8)

    @st.cache
    def count_rows(rows):
        return len(rows)
    @st.cache
    def get_hour(dt):
        return dt.hour
    @st.cache
    def convert(df4):
        df4['tpep_pickup_datetime'] = df4['tpep_pickup_datetime'].map(pd.to_datetime)
        df4['tpep_dropoff_datetime'] = df4['tpep_dropoff_datetime'].map(pd.to_datetime)
        df4['pickup_hour'] = df4['tpep_pickup_datetime'].map(get_hour)
        df4['dropoff_hour'] = df4['tpep_dropoff_datetime'].map(get_hour)
        return df4

    df4 = convert(df4)
    col9,col10 = st.columns(2)

   
    fig9, ar = plt.subplots()
    
    ar.hist(df4.pickup_hour, bins=24,rwidth=0.8,range=(.5,24))
    ar.set_xlabel('Pickup Hour')
    ar.set_ylabel('Frequency')
    ar.set_title('Frequency by Pickup Hour')
    ar.set_xticks(np.arange(24))
  

    col9.header('Frequency by pickup hour:')
    col9.write(fig9)


    fig10, ah = plt.subplots()
       
    ah.hist(df4.dropoff_hour, bins=24,rwidth=0.8,range=(.5,24))
    ah.set_xlabel('Dropoff Hour')
    ah.set_ylabel('Frequency')
    ah.set_title('Frequency by Dropoff Hour')
    ah.set_xticks(np.arange(24))

    col10.header('Frequency by dropoff hour:')
    col10.write(fig10)



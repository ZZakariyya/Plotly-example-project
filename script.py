import pandas as pd
import pyarrow as pa
import numpy as np
import streamlit as st

import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import plotly.offline as pyo

from PIL import Image
from io import StringIO

import pickle
import os

st.set_page_config(layout="wide")

image = Image.open('data-visualization-illustration.jpg')
new_image = image.resize((1600, 800))

col1, col2 = st.columns(2)

with col1:
    st.header("What is data visualization?") 
    st.write("Data visualization is the representation of data through use of common graphics, such as charts, plots, infographics, and even animations. These visual displays of information communicate complex data relationships and data-driven insights in a way that is easy to understand.")
    st.write("Data visualization can be utilized for a variety of purposes, and it’s important to note that is not only reserved for use by data teams. Management also leverages it to convey organizational structure and hierarchy while data analysts and data scientists use it to discover and explain patterns and trends.")
    st.write("Source: https://www.ibm.com/cloud/learn/data-visualization")
    st.write("##")
    st.write("##")
    st.write("I used plotly library to visualize all the graphs and charts in this web page. If you wanna learn about plotly, check the link below:")
    st.write("https://plotly.com/python/")

with col2:
    st.image(new_image)


st.write("##")
st.write("##")
st.write("##")
st.write("##")

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

with col2:
    try:
        st.dataframe(df)
    except:
        print("Please upload your file")

st.write("##")
st.write("##")
st.write("##")
st.write("##")

option = st.selectbox(
    'Please choose your graph',
    ('None', 'Pie Chart', 'Scatter Plot', 'Box Plot'))

if option == "Pie Chart":
    tup = tuple(df.columns)
    col = st.selectbox(
        'Please pick your column',
        tup
    )
    
    values = []
    for i in list(df[col].unique()):
        count = 0
        for j in range(len(df[col])):
            if df[col][j] == i:
                count +=1
        values.append(count)

    fig = go.Figure(data=[go.Pie(labels=df[col].unique(), values=values)])

    colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']

    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))

    fig.update_layout(
        autosize=False,
        width=800,
        height=800,)

    st.plotly_chart(fig, use_container_width=True)
elif option == "Scatter Plot":
    weight = st.selectbox(
        "Do you wanna see scatter matrix for all variable or just a scatter plot for 2 variables?",
        ("None", "Scatter Matrix", "Scatter Plot")
    )
    numerical_variables = [i for i in df.columns if df[i].dtype == "int64" or df[i].dtype == "float64"]
    if weight == "Scatter Matrix": 

        fig = px.scatter_matrix(df,
        dimensions=numerical_variables,
        color="loan_status",
        labels={col:col.replace('_', ' ') for col in numerical_variables})

        fig.update_layout(
            title='Scatter Matrix',
            dragmode='select',
            width=1500,
            height=1500,
            hovermode='closest',
        )

        fig.update_traces(diagonal_visible=False)

        st.plotly_chart(fig, use_container_width=True)
    elif weight == "Scatter Plot":
        col1, col2, col3 = st.columns(3)
        tup = tuple(numerical_variables)
        with col1:
            val1 = st.selectbox(
                "Please pick your X axis variable",
                tup
            )

        with col2:
            val2 = st.selectbox(
                "Please pick your Y axis variable",
                tup
            )

        with col3:
            hue = st.selectbox(
                "Please pick your hue variable",
                tup
            )

        fig = px.scatter(df, x=val1, y=val2, color = hue)

        fig.update_layout(
            autosize=False,
            width=1200,
            height=800,)

        st.plotly_chart(fig, use_container_width=True)
elif option == "Box Plot":
    numerical_variables = [i for i in df.columns if df[i].dtype == "int64" or df[i].dtype == "float64"] 
    tup = tuple(numerical_variables)
    var = st.selectbox(
        "Please pick your variable",
        tup
       )


    fig = px.box(df, y = var)

    fig.update_layout(
    autosize=False,
    width=700,
    height=700,)

    st.plotly_chart(fig, use_container_width=True)



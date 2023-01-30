import codecs

import pandas as pd
import streamlit as st
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import streamlit.components.v1 as comp
from streamlit_option_menu import option_menu
import sweetviz as sv
import dtale
from streamlit_folium import folium_static
import folium



def st_sweetviz(report_html,width=1000,height=500):
    report_file=codecs.open(report_html,'r')
    page=report_file.read()
    comp.html(page,width=width,height=height,scrolling=True)


def main():
    menu=["Home","Profiling","Geomap"]
    choice=option_menu(
        menu_title=None,
        options = ["Home", "Profiling", "Geomap"],
        icons=["house","book","map"],
        menu_icon="cast",
        orientation="horizontal",

    )


    if choice =="Home":
        st.title("Home")
        st.header("The EDA APP")
        box="""<h1 style="background-color:pink;text-align: center">Made your Daily data needs easier</h1>"""
        comp.html(box)

    elif choice =="Profiling":
        box = """<h1 style="background-color:#ffcccc;text-align: center">Let's take a look at Data insights</h1>"""
        comp.html(box)
        # fileupload
        st.header("Upload CSV Data")
        st.subheader("Enter Cleaned Data for better results")
        data = st.file_uploader("Upload CSV", type=["CSV"])

        if data is not None:
            file_details = {"File name": data.name, "Size": data.size}
            st.write(file_details)
            df = pd.read_csv(data)
            if st.checkbox("Preview"):
                st.dataframe(df)
            option = option_menu(
                menu_title=None,
                options=["Pandas Profiling", "Sweetviz","dtale"],
            )

            if option=="Pandas Profiling":
                st.title("Pandas Profiling")
                pr = ProfileReport(df, html={'style': {'full_width': True}})
                st_profile_report(pr)

            elif option=="Sweetviz":
                st.title("Sweetviz")
                st.subheader("Report will open in new page")
                report=sv.analyze(df)
                report.show_html()

            elif option=="dtale":
                st.title("dtale")
                st.subheader("Report will open in new page")
                report=dtale.show(df)
                report.open_browser()

    elif choice =="Geomap":
        st.title("Geo Map")
        st.header("Upload CSV Data")
        st.subheader("Data column names should contain Latitude,Longitude ")
        data = st.file_uploader("Upload CSV", type=["CSV"])

        if data is not None:
            file_details = {"File name": data.name, "Size": data.size}
            st.write(file_details)
            df = pd.read_csv(data)
            if st.checkbox("Preview"):
                st.dataframe(df)

            a=st.number_input("Latitude")
            b = st.number_input("Longitude")

            m = folium.Map(location=[a,b], zoom_start=11,min_zoom=8,max_zoom=14)
            i = 0
            dataList = []  # empty list
            for index, row in df.iterrows():
                mylist = [row.latitude, row.longitude]
                dataList.append(mylist)
            for coordinates in dataList:
                m.add_child(
                    folium.Marker(location=dataList[i],icon=folium.Icon(color="Blue")))
                i = i + 1
            folium_static(m)




if __name__=="__main__":
    main()

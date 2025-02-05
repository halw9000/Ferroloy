import streamlit as st
import pandas as pd
import numpy as np
import time, io, datetime
import fdnx_simulator as fx
import fdnx_scheduler as fs

buffer = io.BytesIO()
to_download = 0
is_comparing = 0

st.write("# Compare Schedules Here")
st.write("Upload additional FDNX schedule files to simulate and compare.")


col1, col2 = st.columns(2)
with col1:
  com_file1 = st.file_uploader("Upload FDNX Schedule A", type={"xlsx"})
  if com_file1 is not None:
    is_comparing = 1
    com1_fdnx1 = pd.read_excel(com_file1, sheet_name="FDNX1")
    com1_fdnx2 = pd.read_excel(com_file1, sheet_name="FDNX2")
    com1_fdnx3 = pd.read_excel(com_file1, sheet_name="FDNX3")
    com1_schedule = [com1_fdnx1,com1_fdnx2,com1_fdnx3]
    with st.spinner("Simulating..."):
        com1_ladles, com1_lanes, com1_sim_seconds = fx.fdnx_simulator(com1_schedule)   
    st.write("Schedule A: " + str(len(com1_ladles)) + " ladles")
    
    ## update Charts
    com1_mold_wt_chart_data = com1_ladles[['ladle_number', 'total_mold_wt','deck_weight']]
    com1_mold_count_chart_data = com1_ladles[['ladle_number', 'molds_filled']]
    com1_mold_avgwt_chart_data = com1_ladles[['ladle_number', 'avg_mold_wt']]
    
    com1_mold_wt_chart_data.rename(columns={'ladle_number': 'ladle_number', 'total_mold_wt': 'Poured A', 'deck_weight' : 'Deck A'}, inplace=True)
    com1_mold_count_chart_data.rename(columns={'ladle_number': 'ladle_number', 'molds_filled': 'Schedule A'}, inplace=True)
    com1_mold_avgwt_chart_data.rename(columns={'ladle_number': 'ladle_number', 'avg_mold_wt': 'Schedule A'}, inplace=True)
    
    new_mold_wt_chart_data = st.session_state.mold_wt_chart_data.merge(com1_mold_wt_chart_data,on="ladle_number",how="outer")
    new_mold_count_chart_data = st.session_state.mold_count_chart_data.merge(com1_mold_count_chart_data,on="ladle_number",how="outer")
    new_mold_avgwt_chart_data = st.session_state.mold_avgwt_chart_data.merge(com1_mold_avgwt_chart_data,on="ladle_number",how="outer")
    
    st.session_state.mold_wt_chart_data = new_mold_wt_chart_data
    st.session_state.mold_count_chart_data = new_mold_count_chart_data
    st.session_state.mold_avgwt_chart_data = new_mold_avgwt_chart_data
    
with col2:
  com_file2 = st.file_uploader("Upload FDNX Schedule B", type={"xlsx"})
  if com_file2 is not None:
    is_comparing = 1
    com2_fdnx1 = pd.read_excel(com_file2, sheet_name="FDNX1")
    com2_fdnx2 = pd.read_excel(com_file2, sheet_name="FDNX2")
    com2_fdnx3 = pd.read_excel(com_file2, sheet_name="FDNX3")
    com2_schedule = [com2_fdnx1,com2_fdnx2,com2_fdnx3]
    with st.spinner("Simulating..."):
        com2_ladles, com2_lanes, com2_sim_seconds = fx.fdnx_simulator(com2_schedule)   
      
    st.write("Schedule B: " + str(len(com2_ladles)) + " ladles")
    
    ## UPDATE CHARTS

    com2_mold_wt_chart_data = com2_ladles[['ladle_number', 'total_mold_wt','deck_weight']]
    com2_mold_count_chart_data = com2_ladles[['ladle_number', 'molds_filled']]
    com2_mold_avgwt_chart_data = com2_ladles[['ladle_number', 'avg_mold_wt']]
    
    com2_mold_wt_chart_data.rename(columns={'ladle_number': 'ladle_number', 'total_mold_wt':'Poured B', 'deck_weight' : 'Deck B'}, inplace=True)
    com2_mold_count_chart_data.rename(columns={'ladle_number': 'ladle_number', 'molds_filled': 'Schedule B'}, inplace=True)
    com2_mold_avgwt_chart_data.rename(columns={'ladle_number': 'ladle_number', 'avg_mold_wt': 'Schedule B'}, inplace=True)
    
    new_mold_wt_chart_data = st.session_state.mold_wt_chart_data.merge(com2_mold_wt_chart_data,on="ladle_number",how="outer")
    new_mold_count_chart_data = st.session_state.mold_count_chart_data.merge(com2_mold_count_chart_data,on="ladle_number",how="outer")
    new_mold_avgwt_chart_data = st.session_state.mold_avgwt_chart_data.merge(com2_mold_avgwt_chart_data,on="ladle_number",how="outer")
    
    st.session_state.mold_wt_chart_data = new_mold_wt_chart_data
    st.session_state.mold_count_chart_data = new_mold_count_chart_data
    st.session_state.mold_avgwt_chart_data = new_mold_avgwt_chart_data


if 'mold_wt_chart_data' in st.session_state:
  
  st.header("Poured Amount By Ladle:")
  st.line_chart(st.session_state.mold_wt_chart_data , x="ladle_number")
  
  st.header("Molds Filled Per Ladle:")
  st.line_chart(st.session_state.mold_count_chart_data, x="ladle_number")
  
  st.header("Average Pour Weight:")
  st.line_chart(st.session_state.mold_avgwt_chart_data, x="ladle_number")



if 'ladles' not in st.session_state:
    st.warning('No Schedule has been generated to compare.')
else:
    to_download = 1
    ladles = st.session_state.ladles
    lanes = st.session_state.lanes
    fdnx1 = st.session_state.fdnx1
    fdnx2 = st.session_state.fdnx2
    fdnx3 = st.session_state.fdnx3
    # weight chart
    mold_wt_chart_data = ladles[['ladle_number', 'total_mold_wt','deck_weight']]
    mold_wt_chart_data.rename(columns={'ladle_number': 'ladle_number', 'total_mold_wt': 'Sim - Poured','deck_weight':'Sim - Deck Weight'}, inplace=True)
    st.session_state.mold_wt_chart_data = mold_wt_chart_data
    
    mold_count_chart_data = ladles[['ladle_number', 'molds_filled']]
    mold_count_chart_data.rename(columns={'ladle_number': 'ladle_number', 'molds_filled': 'Simulated'}, inplace=True)
    st.session_state.mold_count_chart_data = mold_count_chart_data
    
    mold_avgwt_chart_data = ladles[['ladle_number', 'avg_mold_wt']]
    mold_avgwt_chart_data.rename(columns={'ladle_number': 'ladle_number', 'avg_mold_wt': 'Simulated'}, inplace=True)
    st.session_state.mold_avgwt_chart_data = mold_avgwt_chart_data
    

if to_download == 1:
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    # Write each dataframe to a different worksheet.
        fdnx1.to_excel(writer, sheet_name='FDNX1')
        fdnx2.to_excel(writer, sheet_name='FDNX2')
        fdnx3.to_excel(writer, sheet_name='FDNX3')
        ladles.to_excel(writer, sheet_name='sim_ladles')
        lanes[0].to_excel(writer, sheet_name='sim_lane1')
        lanes[1].to_excel(writer, sheet_name='sim_lane2')
        lanes[2].to_excel(writer, sheet_name='sim_lane3')
        lanes[3].to_excel(writer, sheet_name='sim_lane4')
        lanes[4].to_excel(writer, sheet_name='sim_lane5')
        lanes[5].to_excel(writer, sheet_name='sim_lane6')
        writer.close()
        # Get the current timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
       # Close the Pandas Excel writer and output the Excel file to the buffer
        selected_iron = st.session_state.selected_iron
        st.download_button(
            label= ("Download Latest Simulation File"),
            data=buffer,
            file_name= "FDNXSchedule_" + timestamp +".xlsx",
            mime="application/vnd.ms-excel"
        )

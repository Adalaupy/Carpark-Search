import streamlit as st
import app_function as af
import pandas as pd
import ui_data
# ==========================================================================================================
# Default Setting
# ==========================================================================================================

st.set_page_config(layout="wide", page_title="Carpark Search", page_icon="🚗")

display_cnt = 10

# ==========================================================================================================
# Prepare Data + Initial widget (Sidebar)
# ==========================================================================================================

af.Fn_Init()
af.Gen_SideBar_Element()
af.Fn_Main_Update_Elem()

# ==========================================================================================================
# Data paging
# ==========================================================================================================

page_display_data = st.session_state['display_data'][ display_cnt * st.session_state['CurrentPage'] : display_cnt * st.session_state['CurrentPage'] + display_cnt ]

# ==========================================================================================================
# Prepare Map color 
# ==========================================================================================================

colors = [
    "#e6194b",  # vivid red
    "#3cb44b",  # strong green
    "#ffe119",  # bright yellow
    "#4363d8",  # strong blue
    "#f58231",  # vivid orange
    "#911eb4",  # deep purple
    "#42d4f4",  # cyan
    "#f032e6",  # magenta
    "#bfef45",  # lime
    "#fabebe",  # soft pink
    "#008080",  # teal
    "#e6beff",  # lavender
    "#9a6324",  # brown
    "#800000",  # maroon
    "#aaffc3"   # mint
]


color_set = int(len(page_display_data)//len(colors)) + 1 
color_list = colors * color_set                                 # Ensure have enough color provided
color_list = color_list[:len(page_display_data)]



# ==========================================================================================================
# Prepare Map dataframe 
# ==========================================================================================================

lat = [item['Latitude'] for item in page_display_data]
lon = [item['Longitude'] for item in page_display_data]
name = [item['Name'] for item in page_display_data]

data = {
    'latitude' : lat,
    'longitude': lon,
    'city':name,
    'color' : [item +'55' for item in color_list],              # handle the transpancy by adding 2 digit at the end
}

df = pd.DataFrame(data)


# ==========================================================================================================
# Main Display
# ==========================================================================================================


split_win = st.columns([2,5])

with split_win[0]:
    
    st.map(df, latitude='latitude', longitude='lon', color='color')


# ==========================================================================================================
# Paging function
# ==========================================================================================================
 
def Fn_click_prev():
    
    
    if st.session_state['CurrentPage'] > 0:
    
        st.session_state['CurrentPage'] -= 1



def Fn_click_next():


    if (st.session_state['CurrentPage'] + 1) != max_page:
        
        st.session_state['CurrentPage'] += 1

# ==========================================================================================================
# Info Widget
# ==========================================================================================================


with split_win[1]:

    i = st.session_state['CurrentPage']

    
    full_html = ui_data.Fn_Gen_DisplayCard(page_display_data , color_list )

    st.html(full_html )


    max_page = (len(st.session_state['display_data']) + display_cnt - 1) // display_cnt
    

    # Button for paging
    split_btn = st.columns([7,2,1,2], gap = 'small' , vertical_alignment = 'center')

    with split_btn[1]:
        
        st.button('Previous', on_click = Fn_click_prev, width = 150,  disabled=st.session_state['CurrentPage'] == 0)

    with split_btn[2]:
        
         st.write(f"{0 if max_page == 0 else st.session_state['CurrentPage'] + 1}/{max_page}")


    with split_btn[3]:               

        st.button('Next', on_click = Fn_click_next , width = 150 , disabled = (max_page <= st.session_state['CurrentPage'] + 1))
       



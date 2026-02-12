import streamlit as st
import extract_data as data_src

Option_Labels = ['District', 'Car Type','Carpark Name']
Selected      = [None,None,None]

# ==========================================================================================================
# Prepare session state variables   
# ==========================================================================================================

def Fn_Init_Variables():
    

    if 'Init_Filter_List' not in st.session_state:
        
        st.session_state['Init_Filter_List'] = [[],[],[]]


    if 'Filter_Selected' not in st.session_state:

        st.session_state['Filter_Selected'] = [None,None,None]


    if 'IsOnlyOpen' not in st.session_state:
        
        st.session_state['IsOnlyOpen'] = False


    if 'CurrentPage' not in st.session_state :
        
        st.session_state['CurrentPage'] = 0


# ==========================================================================================================
# Function to Load data
# ==========================================================================================================

@st.cache_data
def Fn_load_data():
    

    data_load_state = st.text('Loading Data......')
    
    data_list = data_src.main()

    data_list = sorted(data_list, key=lambda x: x['District'])

    data_load_state.text('')

    return data_list


# ==========================================================================================================
# Function to handle Selectbox options list
# ==========================================================================================================


def Fn_Select_Options(data):

    districts = list(set([v['District'] for v in data]))
    cartypes  = list(set([v['Vehicle'] for row in data for v in row['Vacancy']]))
    cpnames   = list(set([v['Name'] for v in data]))


    return districts, cartypes, cpnames


# ==========================================================================================================
# Initial
# ==========================================================================================================

def Fn_Init():
    
    Fn_Init_Variables()

    data_list = Fn_load_data()    
    init_data = data_list[:70] #!!!!!


    # Data Source
    st.session_state['data']         = init_data
    st.session_state['display_data'] = init_data


    # Selectbox Options
    districts, cartypes, cpnames = Fn_Select_Options(init_data)
    st.session_state['Init_Filter_List'] = [districts, cartypes, cpnames]



    if 'New_Filter_List' not in st.session_state:
        
        st.session_state['New_Filter_List'] = st.session_state['Init_Filter_List']

    
# ==========================================================================================================
# Function Prepare Selectbox
# ==========================================================================================================

def Gen_SideBar_Element():
    
    global Option_Labels
    global Selected
    global IsOnlyOpen

    for id,label in enumerate(Option_Labels):
        
        options = st.session_state['New_Filter_List'][id]

        with st.sidebar:
            
            Selected[id] = st.selectbox(label, options, index = None, key = label.replace(' ','_') , on_change = Fn_Main_Update_Elem) #

            

    IsOnlyOpen = st.sidebar.checkbox('Only Opened Carpark', on_change= Fn_Main_Update_Elem)


# ==========================================================================================================
# Triggered Function to update State + Selectbox after modified selections
# ==========================================================================================================


def Fn_Main_Update_Elem():
    
    Fn_Update_State()
    Fn_Filter_Data( st.session_state['display_data'] )

    # Fn_Update_Options() #  Fail to render immediately for sidebar selectbox

   
# ==========================================================================================================
# Function to update selection state variable
# ==========================================================================================================


def Fn_Update_State():
    
    if (st.session_state['Filter_Selected'] != Selected) or (st.session_state['IsOnlyOpen'] != IsOnlyOpen):

        st.session_state['CurrentPage'] = 0
        st.session_state['Filter_Selected'] = Selected
        st.session_state['IsOnlyOpen'] = IsOnlyOpen

        Fn_Filter_Data( st.session_state['display_data'] )

        if Selected == [None,None,None] and IsOnlyOpen == False:

            st.session_state['New_Filter_List'] = st.session_state['Init_Filter_List']


# ==========================================================================================================
# Function to update list of select box option
# ==========================================================================================================

def Fn_Update_Options():

    districts, cartypes, cpnames = Fn_Select_Options( st.session_state['display_data'] )
    
    st.session_state['New_Filter_List'] = [districts, cartypes ,  cpnames]


# ==========================================================================================================
# Function to filter data source according to value of selectbox
# ==========================================================================================================


def Fn_Filter_Data(input_data):

    s_district = st.session_state['Filter_Selected'][0]
    s_cartype  = st.session_state['Filter_Selected'][1]
    s_cpname   = st.session_state['Filter_Selected'][2]
    is_only_open = st.session_state['IsOnlyOpen']


    if s_district != None:
        
        input_data = [item for item in input_data for k,v in item.items() if k == 'District' and v == s_district]

    if s_cartype != None:
        
        input_data = [veh for veh in input_data for sub in veh['Vacancy'] for va in sub['Vacant'] if sub['Vehicle'] == s_cartype and va['Vacant'] != 'data not provided']
    
    if s_cpname != None:
        
        input_data = [item for item in input_data for k,v in item.items() if k == 'Name' and v == s_cpname]


    
    if is_only_open == True:        

        input_data = [item for item in input_data for k,v in item.items() if k == 'OpenStatus' and v == 'OPEN']
   

    st.session_state['display_data'] = input_data




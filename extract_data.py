import requests


# ===================================================================================
# Function to Get Data from API
# ===================================================================================

def Fn_Get_Data_API(url):

    response = requests.get(url)
    response.encoding = 'utf-8-sig'

    if response.status_code == 200:
        
        data = response.json()
        
        return data
    
    else:

        print("Error: Unable to fetch data from the API.")
        
        return None


# ===================================================================================
# Function to Get two data
# ===================================================================================

def Fn_Get_Data():    

    data_info = Fn_Get_Data_API('https://resource.data.one.gov.hk/td/carpark/basic_info_all.json')
    data_info = data_info['car_park']

        
    data_vacancy = Fn_Get_Data_API('https://resource.data.one.gov.hk/td/carpark/vacancy_all.json')
    data_vacancy = data_vacancy['car_park']


    return data_info,data_vacancy


# ===================================================================================
# Vehicle code and name mapping
# ===================================================================================

vehicle_map = [
    ('P' , 'Cars/Vans') , 
    ('M' , 'Motor Cycles') , 
    ('L' , 'Light Goods Vehicles') , 
    ('H' , 'Heavy Goods Vehicle') , 
    ('C' , 'Coaches/Buses') , 
    ('T' , 'Container Vehicles') , 
    ('B' , 'Light Buses ') , 

]    

# ===================================================================================
# Combine carpark basic info and vacancy infor
# ===================================================================================

def main():

    data_info,data_vacancy = Fn_Get_Data()


    full_dict_list = []


    for cp in data_info:
        
        id = cp['park_id']
        vc = [row for row in data_vacancy if row['park_id'] == id][0]


    
        # Get Vacant info for each vehicle
        vehicles = vc['vehicle_type']
        vehicle_vacant_data = []
        
        for vehicle in vehicles:        
        
            # Vehicle Type
            for map in vehicle_map:
                
                if vehicle['type'][0] == map[0]:
                    
                    if vehicle['type'][-1] == 'D':
                        
                        vehicle_name = map[1] + ' (disable)'
                    
                    else:
                        
                        vehicle_name = map[1]

            
            # Vacancy for each vehicle
            services = vehicle['service_category']
            services_data = []

            for service in services:
                
                category = service['category']
                
                if service['vacancy_type'] == 'A':
                    
                    if service['vacancy'] == 0 :
                        
                        vacant = 'full'
                    
                    elif service['vacancy'] == -1:
                        
                        vacant = 'data not provided'
                    
                    else :
                        
                        vacant = service['vacancy']

                elif service['vacancy_type'] == 'B':                
                    
                    if service['vacancy'] == '0' :
                        
                        vacant = 'full'
                    
                    elif service['vacancy'] == '1':
                        
                        vacant = 'available'
                    
                    else:
                        
                        vacant = 'data not provided'                
                
                else:
                    
                    vacant = 'closed'


                services_data.append( {"Category" : category, "Vacant" : vacant } )

            vehicle_vacant_data.append({"Vehicle": vehicle_name, "Vacant" : services_data })



        if cp.get('remark_en'):
            

            remark_str = cp['remark_en'].replace('Height Limit: Height limit:','Height Limit<br> ').replace('\n','<br><br>')
            
            # Break into item and point 
            remark_list = remark_str.split('<br><br>')
            remark_list = [(item.split('<br>')[0].strip() , [elem.strip() for elem in item.split('<br>')[1:] if elem.strip() != '']) for item in remark_list]
            
            # Remove messy data
            remark_list = [item for item in remark_list if not (item[0] == 'Height Limit:' and len(item[1]) == 0) and not (item[0] == '' and len(item[1]) == 0 )]

                
            # Handle the bullet
            remark_list = [(  ('<u>' + item[0] + '</u>') if item[1] != [] else item[0]    , ['<li>' + point + '</li>' for point in item[1]]) for item in remark_list ]
            remark_list = [item[0] + '<ul>' + ''.join(item[1])  + '</ul>' for item in remark_list]


            remark = ''.join(remark_list)

        else:
            
            remark = ''
    
        full_dict = {
            
            "id" : cp['park_id'],
            "Name" : cp['name_en'],
            "District" : cp['district_en'],
            "Address" : cp['displayAddress_en'],
            "OpenStatus" : 'Not provided' if cp['opening_status'] == None else cp['opening_status'],
            "Remark" : remark,
            "Contact": cp['contactNo'],
            "Height": cp['height'],
            "Photo" : cp['carpark_photo'],
            "Website" : ('<a href = "' + cp['website_en'] +  '"> ' + cp['website_en'] + ' </a>') if cp['website_en'] else '',
            "Latitude" : cp['latitude'],
            "Longitude" : cp['longitude'],
            "Vacancy" : vehicle_vacant_data,
        }
        

        full_dict_list.append(full_dict)

    return full_dict_list

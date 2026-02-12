

def Fn_Gen_DisplayCard_Item(color,detail):
    
    vacant_info = [(veh['Vehicle'], v['Vacant']) for veh in detail['Vacancy'] for v in veh['Vacant']]
    others_info = {key: value for key,value in detail.items() if key in ['District', 'Address', 'Contact', 'Remark', 'Website'] and value != '' and value != 'Height Limit: \n' and (isinstance(value, str) or isinstance(value, int))}


        
    if detail['OpenStatus'].upper() == 'OPEN':
        
        status_color = 'green'

    elif detail['OpenStatus'].upper() == 'NOT PROVIDED':
        
        status_color = 'gray'
    
    else:
        
        status_color = 'red'



    html_str = f"""
        
        <style>

            .main-container {{
                margin: 20px;
                border: 2px solid white; 
                border-radius: 10px; 
                padding:10px; 

                display:flex; 
                justify-content: space-between; 

                align-items:start;

            }}

                        
            .info-container {{
                gap: 10px;
                display: grid;
                padding: 30px; 30px;
                width: 100%;                
            }}

            .vacancy-container{{
                margin-top: 20px;
                display:flex; 
                justify-content:left; 
                width: 100%;
                gap:20px;
                margin-bottom: 20px;
                border: 2px gray dashed;
                border-radius: 15px;
                padding: 15px;
                width: 100%;
                
            }}

            .vacancy {{
                display: grid;
                place-content: left;
                text-align:center;
                gap: 15px;
            
            }}

            .vehicle-name {{                  
                display: grid;               

            }}
            
            .vacant-cnt {{                
                display: grid;
                align-items: center;
                background-color: #858585;         
                width: 100px;
                height: 70px;                  
                border-radius: 10px;

            }}

            .title {{            
                font-weight: bold;
                
            }}

            .basic {{            
                display: flex;
                align-content: start;
                gap:5px; 
            }}

        </style>
                
        <div class="main-container">
            <div style="width:90%; display:flex; align-items:center; height:100% " class="cp-img"> 
                <img style="max-width:100%; object-fit: fill;" src="{detail['Photo']}"</img>
            </div>
           
            <div class="info-container"> 
                <div style="display: flex; justify-content: space-between; align-items:start; gap: 10px;">               
                    <div style="font-size: 25px; color: {color}" class="name">
                        {detail['Name']} 
                    </div>
                    {'' if not detail['OpenStatus'] else f"""
                        <div style="width: 100px; max-height:80px; border: 3px solid {status_color}; border-radius: 25px; padding: 10px; place-items:center; place-content:center; text-align: center; ">
                            {detail['OpenStatus']} 
                        </div>
                        """                     
                     }

                </div>

                <div class="vacancy-container">
                    {'\n'.join([f"""
                        
                        <div class="vacancy">                            
                            <div style="font-size:{f'15' if v_item[1] == 'data not provided' else '25'}px;" class="vacant-cnt">{v_item[1]}</div>                            
                            <div class="vehicle-name">{v_item[0]}</div>                                                
                        </div>                                    
                    """ for v_item in vacant_info])
                    }          
                </div>

                {'\n'.join([f"""
                             
                    <div class="basic">
                        <div class="title">{k}:</div>
                        <div>{v.replace('Height Limit: Height limit:','Height Limit - ')}</div>
                    </div>

                    """ for k,v in others_info.items()])               
                }

            </div>   
        </div>
                
    """

    return html_str



def Fn_Gen_DisplayCard(data, color_list):
    



    html_list = []

    for id, detail in enumerate(data):
        
        html = Fn_Gen_DisplayCard_Item(color_list[id], detail)

        html_list.append(html)
        


    full_html = f"""

        <div style="height: 100vh; display: grid; place-center: centers; gap: 20px ; height: 500px; overflow-y: auto; padding: 20px;">
            {'\n\n\t\t'.join(html_list)}
        </div>
    """

    return full_html
# Table of contents

- [General Information](#general-information)
- [Features](#features)
- [Installation](#installation)
- [Run](#run)
- [Room of Improvement](#room-of-improvement)
- [Remark](#remark)

# General Information

Hong Kong Car Park Explorer is a simple Streamlit web app that fetches car park information and vacancy data from the Hong Kong Government Data API (data.gov.hk). It displays basic car park details together with current vacancy status, and provides filtering and interactive map visualization.

# Features

- Fetches real-time car park information and vacancy data from Hong Kong Government open API
- Displays key details for each car park: name, address, district, type, opening hours/status, total spaces, current vacancies, price
- Interactive filtering options:
  - By district
  - By car type (private car, motorcycle, light goods vehicle, etc.)
  - By car park name (search with partial match)
  - Show only currently open car parks
- Plots car parks on an map
- Color-coded markers to distinguish different car parks

# Installation

```
pip install -r requirements.txt
```

OR

```
python.exe -m pip install --upgrade pip
pip install streamlit
```

# Run

```
streamlit run app.py
```

# Room of improvement

- Car park details and map markers are not clickable (no navigation to Google Maps / detailed popup / directions)
- No auto-refresh for real-time vacancy updates
- Only 4 filter options current — consider adding more
- Sidebar rendering delay when filtering datasets due to Streamlit limitation
- App is built in dark mode only (no light mode / theme toggle support)
- No closest distance calculation (cannot show/sort by distance from user location)

# Remark

Run below code in bash or Powershell to set the app in dark mode

```
@"
[theme]
base = "dark"
"@ | Out-File -FilePath "myenv\Lib\site-packages\streamlit\config.toml" -Encoding utf8 -Force
```

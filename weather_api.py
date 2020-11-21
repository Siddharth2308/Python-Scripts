import requests
import xlsxwriter
from pprint import pprint

workbk_out = xlsxwriter.Workbook("wind.xlsx")
sheet_out = workbk_out.add_worksheet()
sheet_out.write("A1", "Time")
sheet_out.write("B1", "Wind Speed")

api_address='http://api.openweathermap.org/data/2.5/weather?appid=1222ec2c19edb278b4e39377e4138b42&q='
city = input('City Name :')
url = api_address + city
json_data = requests.get(url).json()
#format_add = json_data['base']
wind = json_data['wind']['speed']
print('Wind Speed: {}'.format(wind))
sheet_out.write("B2", wind )
#pprint(wind)
workbook_output.close()

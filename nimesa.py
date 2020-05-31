import requests
import json
import datetime as dt

class my_dictionary(dict):  
  
    # _init_ function  
    def _init_(self):  
        self = dict()  
          
    # Function to add key:value  
    def add(self, key, value):  
        self[key] = value 

def tempcompare(dailylist):
    minviolated=[]
    maxviolated=[]
    for item in dailylist:
        if item['main']['temp']<item['main']['temp_min']:
            minviolated.push(item["dt_txt"]);
        if item['main']['temp']>item['main']['temp_max']:
            maxviolated.push(item["dt_txt"])
    if len(maxviolated) or len(maxviolated):
        print("minimum temp violated for following hours\n")
        for minhr in maxviolated:
            print(minhr)
        for mxhr in maxviolated:
            print(mxhr)
    else:
        print("no minimum and maximum temperature violations")
def wetherdes(code):
    atm_dec={701:"Mist",711:"Smoke",721:"Haze",731:"Dust",741:"Fog",751:"Sand",761:"Dust",762:"Ash",771:"Squall",781:"Tornado"}
    if code==800:
        return "ClearSky"
    elif code>800:
        return "Clouds"
    elif code>=200:
        return "Thunderstorm"
    elif code>=300:
        return "Drizzle"
    elif code>=500:
        return "Light Rain"
    elif code>=600:
        return "Snow"
    elif code>=700:
        return atm_dec[code];
    else:
        return "Unknown code";

def checkall4days(datalist):
    day_dic=my_dictionary()
    date_time = dt.datetime.strptime(datalist[0]["dt_txt"], '%Y-%m-%d %H:%M:%S')
    strtday=date_time.date()
    strttime=date_time.hour
    if(strttime==24):
        cntmax=3
    else:
        cntmax=4
    cnt=0 
    while cnt<=cntmax:
        date = (date_time + dt.timedelta(days=cnt)).date()
        day_dic.add(date,False)
        cnt=cnt+1
    
    for item in datalist:
        date_time = dt.datetime.strptime(item["dt_txt"], '%Y-%m-%d %H:%M:%S')
        date=date_time.date()
        day_dic.add(date,True)
        hour = date_time.hour
        # print('Date-time:', date,hour)
    misseddays=[key for (key, value) in day_dic.items() if value==False]

    if(len(misseddays)==0):
        print(" The response contains data for complete 4 days\n")
    else:
        print("Data is missing for following days\n",);
        for day in misseddays:
            print(day);

def checkeveryhour(datalist):
    hour_dic=my_dictionary()
    date_time = dt.datetime.strptime(datalist[0]["dt_txt"], '%Y-%m-%d %H:%M:%S')
    cnt=0 
    while cnt<96:
        date = (date_time + dt.timedelta(hours=cnt))
        hour_dic.add(date,False)
        cnt=cnt+1
    
    for item in datalist:
        date_time = dt.datetime.strptime(item["dt_txt"], '%Y-%m-%d %H:%M:%S')
        hour_dic.add(date_time,True)
        # print('Date-time:', date,hour)
        missedhurs=[key for (key, value) in hour_dic.items() if value==False]

    if(len(missedhurs)==0):
        print("Data is present for all hours of 4 days\n")
    else:
        print("Data is missing for following",len(missedhurs),"hours");
        for hour in missedhurs:
            print(hour)

responce = requests.get("https://samples.openweathermap.org/data/2.5/forecast/hourly?q=London,us&appid=b6907d289e10d714a6e88b30761fae22")
data=json.loads(responce.content);



wethercode = data['cod']
dailylist = data['list']

print("======================Wether Analyayis=======================")

checkall4days(dailylist)
checkeveryhour(dailylist)
tempcompare(dailylist)
print("wether type :",wetherdes(int(wethercode)),"(",wethercode,")")
print("\n-----------------* for weather id=500 *---------------\n")
print("DateTime\t\tcode\twether type")
print("----------------------------------------------------------")
for item in dailylist:
    if item['weather'][0]['id']==500:
        print(item['dt_txt'],end ="\t")
        print(item['weather'][0]['id'],end ="\t")
        print(item['weather'][0]['main'])

print("\n------------------* for weather id=800 *------------------")
print("DateTime\t\tcode\twether type")
print("----------------------------------------------------------")
for item in dailylist:
    if item['weather'][0]['id']==800:
        print(item['dt_txt'],end ="\t")
        print(item['weather'][0]['id'],end ="\t")
        print(item['weather'][0]['main'])
    
print("===========================END================================")
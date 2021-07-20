from flask import Flask, render_template, request
import requests as rq
from bs4 import BeautifulSoup as bsp
import datetime as dt
import webbrowser as wb

commodities = {
    137:"Ajwan",    325:"Almond(Badam)",    260:"Arhar Dal(Tur Dal)",    269:"Avare Dal",    28:"Bajra(Pearl Millet/Cumbu)",    204:"Bamboo",    29:"Barley (Jau)",    321:"Bay leaf (Tejpatta)",    262:"Beaten Rice",    
    263:"Bengal Gram Dal (Chana Dal)",    6:"Bengal Gram(Gram)(Whole)",    8:"Black Gram (Urd Beans)(Whole)",    264:"Black Gram Dal (Urd Dal)",    38:"Black pepper",    290:"Bran",    293:"Broken Rice",    40:"Cardamoms",    
    36:"Cashewnuts",    26:"Chili Red",    105:"Cloves",    138:"Coconut",    45:"Coffee",    91:"Dal (Avare)",    132:"Dry Chillies",    121:"Foxtail Millet(Navane)",    9:"Green Gram (Moong)(Whole)",    265:"Green Gram Dal (Moong Dal)",    63:"Lentil (Masur)(Whole)",   
    4:"Maize",    259:"Masur Dal",    237:"Millets",    106:"Nutmeg",    414:"Paddy(Dhan)(Basmati)",    2:"Paddy(Dhan)(Common)",    30:"Ragi (Finger Millet)",    7:"Red Gram",    3:"Rice",    286:"Soji",    48:"Sugar",    1:"Wheat"    
    }

app = Flask(__name__)

def n2m(m) :
    if m == "01" or m == "1" :
        return "Jan"
    elif m == "02" or m == "2" :
        return "Feb"
    elif m == "03" or m == "3" :
        return "Mar"
    elif m == "04" or m == "4" :
        return "Apr"
    elif m == "05" or m == "5" :
        return "May"
    elif m == "06" or m == "6" :
        return "Jun"
    elif m == "07" or m == "7" :
        return "Jul"
    elif m == "08" or m == "8" :
        return "Aug"
    elif m == "09" or m == "9" :
        return "Sep"
    elif m == "10" :
        return "Oct"
    elif m == "11" :
        return "Nov"
    else :
        return "Dec"



def disp_table(fd, td, ip) :
    d = dt.datetime.now()

    if td == "" :
        date_to = str(d.strftime("%d")) +"-"+ str(d.strftime("%b")) +"-"+ str(d.year)
    else :
        dto = td.split("-")
        date_to = str(dto[2]) + "-" + str(n2m(dto[1])) + "-" + str(dto[0])
    
    if fd == "" and td == "":
        date_from = str(d.strftime("%d")) +"-"+ str(d.strftime("%b")) +"-"+ str(d.year)
    elif fd == "" and td != "" :
        date_from = date_to
    else :
        df = fd.split("-")
        date_from = str(df[2]) + "-" + str(n2m(df[1])) + "-" + str(df[0])
    

    url = str("http://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=")+str(ip)+str("&Tx_State=0&Tx_District=0&Tx_Market=0&DateFrom=")+date_from+str("&DateTo=")+date_to+str("&Fr_Date=")+date_from+str("&To_Date=")+date_to+str("&Tx_Trend=0&Tx_CommodityHead=Castor+Seed&Tx_StateHead=--Select--&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--")

    r = rq.get(url)
    bs = bsp(r.text, "html.parser")
    data = bs.find("table", class_ = "tableagmark_new")

    # web = f'<div class="table_disp"> {data} </div>'
    ds = str(data)
    if "No Data Found" in ds :
        fdn = str(d.strftime("%d")) +"-"+ (str(int(d.strftime("%m"))-1)) +"-"+ str(d.year)
        tdn = str(d.strftime("%d")) +"-"+ str(d.strftime("%m")) +"-"+ str(d.year)
        data = disp_table(fdn,tdn,ip)
    
    
    if str(data.find("input")) != "None" :
        data.find("input").decompose()
        data.find("input").decompose()
    return data


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/test", methods = ["POST","GET"]) 
def test():
    if request.method == "GET" :
        return render_template("test.html")
    if request.method == "POST" :
        com = request.form.get("Commodity")
        fd = str(request.form.get("from"))
        td = str(request.form.get("to"))
        # print(fd,td)
        ds = disp_table(fd, td, int(com))
        val = commodities[int(com)]
        return render_template("test.html", ds = ds, com = com, val = val)

if __name__ == "__main__" :
    app.run()


# Website from 
# Commodity
# Date - From and to


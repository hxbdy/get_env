#Graph the temperature, humidity, pressure and upload it to the FTP server.
#LINE informs you when the pressure drops most recent 6 times.
#coding: utf-8
#2017/09/23

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import csv
from pylab import *
from ftplib import FTP
import re
import requests
import os

from linebot import LineBotApi
from linebot.models import TextSendMessage

MAX_RANGE=50
URL_PATH="/var/www/html/"

def drawingTemp():
    
    temp=[0 for i in range(MAX_RANGE)]
    date=[0 for i in range(MAX_RANGE)]
    span=[]

    for i in range(MAX_RANGE):
        span.append(1000/MAX_RANGE*i)

    fp=open(URL_PATH+"temp.csv","rb")
    reader=csv.reader(fp)
    for row in reader:
        temp.pop(0)
        temp.append(float(row[5]))
        date.pop(0)
        #month/date_hour:minute
        date.append("%02d"%int(row[1])+"/"+"%02d"%int(row[2])+"_"+"%02d"%int(row[3])+":"+"%02d"%int(row[4]))
    fp.close()

    fig=plt.figure(figsize=(16,9))
    ax=fig.add_subplot(1,1,1)
    plt.title("Temperature")
    plt.xlabel("month/date_hour:minute")
    plt.ylabel("degree Celsius")
    plt.plot(temp,color="m")
    plt.xticks(range(MAX_RANGE),date)
    grid(True)
    labels=ax.set_xticklabels(date,rotation=90,fontsize="small")

    plt.savefig(URL_PATH+"temp.png")

def drawingPressure():
    
    pressure=[0 for i in range(MAX_RANGE)]
    date=[0 for i in range(MAX_RANGE)]
    span=[]

    for i in range(MAX_RANGE):
        span.append(1000/MAX_RANGE*i)

    fp=open(URL_PATH+"pressure.csv","rb")
    reader=csv.reader(fp)
    for row in reader:
        pressure.pop(0)
        pressure.append(float(row[5]))
        date.pop(0)
        #month/date_hour:minute
        date.append("%02d"%int(row[1])+"/"+"%02d"%int(row[2])+"_"+"%02d"%int(row[3])+":"+"%02d"%int(row[4]))
    fp.close()

    #Warn if the air pressure acquired in the last 6 times keeps falling
    flg=True
    for i in range(MAX_RANGE-5,MAX_RANGE-1):
        if(pressure[i]<pressure[i+1]):
            flg=False
            break
    if(flg):
        sendMsgToLine("Barometric pressure keeps falling for 30 consecutive minutes")

    fig=plt.figure(figsize=(16,9))
    ax=fig.add_subplot(1,1,1)
    plt.title("Pressure")
    plt.xlabel("month/date_hour:minute")
    plt.ylabel("Hectopascals")
    plt.plot(pressure,color="c")
    plt.xticks(range(MAX_RANGE),date)
    grid(True)
    labels=ax.set_xticklabels(date,rotation=90,fontsize="small")

    plt.savefig(URL_PATH+"pressure.png")

def drawingHum():
    
    hum=[0 for i in range(MAX_RANGE)]
    date=[0 for i in range(MAX_RANGE)]
    span=[]

    for i in range(MAX_RANGE):
        span.append(1000/MAX_RANGE*i)

    fp=open(URL_PATH+"hum.csv","rb")
    reader=csv.reader(fp)
    for row in reader:
        hum.pop(0)
        hum.append(float(row[5]))
        date.pop(0)
        #month/date_hour:minute
        date.append("%02d"%int(row[1])+"/"+"%02d"%int(row[2])+"_"+"%02d"%int(row[3])+":"+"%02d"%int(row[4]))
    fp.close()

    fig=plt.figure(figsize=(16,9))
    ax=fig.add_subplot(1,1,1)
    plt.title("Humidity")
    plt.xlabel("month/date_hour:minute")
    plt.ylabel("percent")
    plt.plot(hum,color="g")
    plt.xticks(range(MAX_RANGE),date)
    grid(True)
    labels=ax.set_xticklabels(date,rotation=90,fontsize="small")

    plt.savefig(URL_PATH+"hum.png")

def sendMsgToLine(msg):
    Channel_Access_Token="XXXXX"
    User_Id="XXXXX"
    Line_Bot_Api=LineBotApi(Channel_Access_Token)
    Line_Bot_Api.push_message(User_Id,TextSendMessage(text=msg))

drawingTemp()
drawingPressure()
drawingHum()

ftp=FTP("FTP","USRID","PASSWRD")

#only first time
#send to html
#fp=open("../../var/www/html/index.html","rb")
#ftp.storbinary("STOR public_html/index.html",fp)
#fp.close()

#send http to temp
fp=open(URL_PATH+"temp.png","rb")
ftp.storbinary("STOR public_html/temp.png",fp)
fp.close()

#send http to pressure
fp=open(URL_PATH+"pressure.png","rb")
ftp.storbinary("STOR public_html/pressure.png",fp)
fp.close()

#send http to hum
fp=open(URL_PATH+"hum.png","rb")
ftp.storbinary("STOR public_html/hum.png",fp)
fp.close()

ftp.close()
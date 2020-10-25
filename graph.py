#Graph the temperature, humidity, pressure and upload it to the FTP server.
#coding: utf-8
#2019/09/08

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import csv
from pylab import *
from ftplib import FTP
import re
import os

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
    plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
    plt.xlabel("month/date_hour:minute")
    plt.ylabel("degree Celsius")
    plt.plot(temp,color="m")
    plt.xticks(range(MAX_RANGE),date)
    grid(True)
    labels=ax.set_xticklabels(date,rotation=90,fontsize="small")

    plt.savefig(URL_PATH+"temp.png",bbox_inches="tight")

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
    for i in range(MAX_RANGE-6,MAX_RANGE-1):
        if(pressure[i]<pressure[i+1]):
            break

    fig=plt.figure(figsize=(16,9))
    ax=fig.add_subplot(1,1,1)
    plt.title("Pressure")
    plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
    plt.xlabel("month/date_hour:minute")
    plt.ylabel("Hectopascals")
    plt.plot(pressure,color="c")
    plt.xticks(range(MAX_RANGE),date)
    grid(True)
    labels=ax.set_xticklabels(date,rotation=90,fontsize="small")

    plt.savefig(URL_PATH+"pressure.png",bbox_inches="tight")

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
    plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
    plt.xlabel("month/date_hour:minute")
    plt.ylabel("percent")
    plt.plot(hum,color="g")
    plt.xticks(range(MAX_RANGE),date)
    grid(True)
    labels=ax.set_xticklabels(date,rotation=90,fontsize="small")

    plt.savefig(URL_PATH+"hum.png",bbox_inches="tight")

print("start drawing Temp...")
drawingTemp()
print("successful")

print("start drawing Pressure...")
drawingPressure()
print("successful")

print("start drawing Hum...")
drawingHum()
print("successful")

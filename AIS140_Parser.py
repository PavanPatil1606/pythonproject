import tkinter as tk
from tkinter import filedialog
from tqdm import tqdm
import datetime
import csv
import pandas as pandasForSortingCSV
import pandas as pd

start_time = datetime.datetime.now()
date = datetime.datetime. now(). strftime("%Y%m%d%I%M%S%p")

root = tk. Tk()
root. withdraw()
filename = filedialog. askopenfilename()

with open(filename) as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]

#imei = input("Enter the Device IMEI Number: ")
available_imei = []
file1 = 'testg.csv'

with open(file1, 'w+', newline='') as csvfile:
    header = ['Header', 'Vendor_ID', 'FW_Version', 'Packet_Type', 'Alert_ID', 'Live/History', 'IMEI', 'Vehicle_No',
              'GPS_fix', 'Date', 'Time', 'Lat', 'Lat_Dir', 'Long', 'Long_Dir', 'Temp1', 'Temp2', 'Temp3', 'Temp4',
              'Temp5', 'Temp6', 'Profile', 'IGN_Status', 'Temp9', 'EXT_BAT', 'INT_BAT', 'EMR_Status', 'Case_Status',
              'Temp10', 'Temp11', 'Temp12', 'Temp13', 'Temp14', 'Temp15', 'Temp16', 'Temp17', 'Temp18', 'Temp19',
              'Temp20', 'Temp21', 'Temp22', 'Temp23', 'Temp24', 'Temp25', 'Temp26', 'DIN', 'DOUT', 'sequence_no',
              'AIN1', 'AIN2', 'AIN3', 'Delta_Dist', 'OTA', 'Checksum']
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)
    for i in tqdm(range(len(lines)), desc='Extracting available IMEI numbers......'):
        if len(lines[i]) > 200:
            temp = lines[i].split(',')
            if temp[6] not in available_imei:
                available_imei.append(temp[6])

    print("Available Imei Numbers are: ")
    for i in range(len(available_imei)):
        print(i+1, available_imei[i])
    imei = available_imei[int(input("Enter the IMEI index no of available IMEI: "))-1]
    print("Selected IMEI Number is: ", imei)
    for i in tqdm(range(len(lines)), desc='Parsing the data.......'):
        #print(len(lines[i]))
        if len(lines[i]) > 200:
            data = lines[i].split(',')
            if len(data) > 53:
                string = data[52] + ':' + data[53] + ':' + data[54]
                data[52] = string
                del data[53:55]
            data2 = data[52].split('*')
            data[52] = data2[0]
            data.append(data2[1])
            if data[6] == imei:
                csvwriter.writerow(data)
    csvfile.close()

csvData = pandasForSortingCSV.read_csv("testg.csv")
#print("\nBefore sorting:")
#print(csvData)

csvData.sort_values(["sequence_no"],
                    axis=0,
                    ascending=[True],
                    inplace=True)

#print("\nAfter sorting:")
#print(csvData)
#print(type(csvData))
csvData_reset = csvData.reset_index()
#csvData_reset = csvData_reset.astype(str)
csvData_reset.to_csv('testg.csv')
seq = csvData_reset.sequence_no
#seq = seq.astype(int)
timestamp = pd.read_csv("testg.csv", usecols=['Date', 'Time', 'IGN_Status', 'EMR_Status'])
profile = csvData_reset.Profile

x = 0
data1 = []
dublicate_packet = 0
dublicate_packet1 = []
data_loss = 0
data_loss1 = []
with open('result.csv', 'w+', newline='') as csvfile1:
    header = ['Curent_Seq_no', 'Date', 'Time', 'Previous_Seq_no', 'Date', 'Time', 'Data_loss', 'Result']
    csvwriter1 = csv.writer(csvfile1)
    csvwriter1.writerow(header)
    for x in tqdm(range(len(seq)-1), desc='Performing Operations.......'):
        dif = seq[x+1] - seq[x]
        print(dif)
        prof = profile[x]
        temp1 = timestamp.Time[x]
        print(type(temp1))
        if len(temp1) != 6:
            while(1):
                if len(temp1) == 6:
                    break
                temp1 = '0' + temp1
        temp2 = timestamp.Time[x+1]
        print("time1: ", temp1)
        temp1_sec = (temp1[0:2] * 3600) + (temp1[2:4] * 60) + temp1[4:6]
        temp2_sec = (temp2[0:2] * 3600) + (temp2[2:4] * 60) + temp2[4:6]
        time_dif = temp2_sec - temp1_sec
        print("time1: ",temp1)
        print("time2: ",temp2)
        print("time1 sec: ",temp1_sec)
        print("time2 sec: ",temp2_sec)
        print("Dif: ",time_dif)

        if 'airtel' != prof:
            if 'BSNL Mobile' != prof:
                data1.append(seq[x])
                data1.append(timestamp.Date[x])
                data1.append(timestamp.Time[x])
                data1.append('NA')
                data1.append('NA')
                data1.append('NA')
                data1.append(profile[x])
                data1.append('Profile mismatch')
                csvwriter1.writerow(data1)
                data1 = []
        if dif > 1:
            data1.append(seq[x+1])
            data1.append(timestamp.Date[x+1])
            data1.append(timestamp.Time[x+1])
            data1.append(seq[x])
            data1.append(timestamp.Date[x])
            data1.append(timestamp.Time[x])
            data1.append(dif-1)
            data1.append('Packet loss')
            data_loss = data_loss + dif - 1
            csvwriter1.writerow(data1)
            data1 = []
        elif dif == 0:
            data1.append(seq[x+1])
            data1.append(timestamp.Date[x+1])
            data1.append(timestamp.Time[x+1])
            data1.append(seq[x])
            data1.append(timestamp.Date[x])
            data1.append(timestamp.Time[x])
            data1.append(dif)
            data1.append('Dublicate Packet')
            dublicate_packet = dublicate_packet + 1
            csvwriter1.writerow(data1)
            data1 = []
    data_loss1.append('Total_data_loss= ')
    data_loss1.append(data_loss)
    dublicate_packet1.append('Total_dublicate= ')
    dublicate_packet1.append(dublicate_packet)
    csvwriter1.writerow(data_loss1)
    csvwriter1.writerow(dublicate_packet1)

print("-------------Completed----------")

import matplotlib.pyplot as plt
import numpy as np
import csv
import functools

countries = []
avgaltitudes = []
altitudes = []
moisture = []
defect1 = []
defect2 = []
defectsum = []
tcp = []

def get_data(data):
    country_altitude = {}
    global moisture, tcp, defect1, defect2, countries, altitudes, avgaltitudes
    for i in data:
        country = i[2]
        if country == 'Country of Origin' or i[8] == '':
            continue

        if not country in country_altitude.keys():
            country_altitude[country] = []

        c = ''
        for j in i[8]:
            if j != ' ' and not j.isdigit():
                c = j
                break;
        t = [int(j.strip()) for j in i[8].split(c)] if c != '' else [int(i[8])]
        alt = sum(t) / len(t)
        
        altitudes.append(alt)
        country_altitude[country].append(alt)
        moisture.append(float(i[32]))
        tcp.append(float(i[31]))
        defect1.append(int(i[33]))
        defect2.append(int(i[36]))
        defectsum.append(int(i[33]) + int(i[36]))
        
        
    for i in country_altitude:
        country_altitude[i] = functools.reduce(lambda x,y : x + y, country_altitude[i])/len(country_altitude[i]) 

    countries = list(country_altitude.keys())
    avgaltitudes = list(country_altitude.values())
    

def plot_country_altitude():
    plt.figure(figsize = (20, 10))
    plt.barh(countries, avgaltitudes)
    plt.xlabel('Altitude')
    plt.ylabel('Country')
    plt.title('Average Altitude of Coffee Plantations in Countries')
    plt.savefig('visualization1.png')


def plot_moisture_defect():
    plt.figure(figsize = (20,20))
    plt.subplot(121)
    plt.title('Amount of Category 1 Defects in Relation to Moisture Percentage')
    plt.ylabel('Category 1 Defects')
    plt.xlabel('Moisture Percentage')
    plt.scatter(moisture, defect1)
    plt.subplot(122)
    plt.title('Amount of Category 2 Defects in Relation to Moisture Percentage')
    plt.ylabel('Category 2 Defects')
    plt.xlabel('Moisture Percentage')
    plt.scatter(moisture, defect2)
    plt.suptitle('Amount of Defects in Relation to Moisture Percentage')
    plt.savefig('visualization2.png')


def plot_correlations():
    plt.rcParams.update({'font.size': 30})
    plt.figure(figsize = (60,30))
    plt.subplot(131)
    plt.title('Correlation Between Altitude and TCP')
    plt.xlabel('Altitude')
    plt.ylabel('TCP')
    plt.scatter(altitudes, tcp)
    plt.plot(np.unique(altitudes), np.poly1d(np.polyfit(altitudes, tcp, 1)) (np.unique(altitudes)), color='red')
    plt.subplot(132)
    plt.title('Correlation Between Moisture and TCP')
    plt.xlabel('Moisture')
    plt.ylabel('TCP')
    plt.scatter(moisture, tcp)
    plt.plot(np.unique(moisture), np.poly1d(np.polyfit(moisture, tcp, 1)) (np.unique(moisture)), color='red')
    plt.subplot(133)
    plt.title('Correlation Between Defect number and TCP')
    plt.xlabel('# of Defects')
    plt.ylabel('TCP')
    plt.scatter(defectsum, tcp)
    plt.plot(np.unique(defectsum), np.poly1d(np.polyfit(defectsum, tcp, 1)) (np.unique(defectsum)), color='red')
    plt.suptitle('Correlation Between Various Factors and Total Cup Points(TCP)')
    plt.savefig('visualization3.png')


def main():
    with open('df_arabica_clean.csv', mode = 'r') as file:
        data = csv.reader(file)
        get_data(data)
        plot_country_altitude()
        plot_moisture_defect()
        plot_correlations()


if __name__ == '__main__':
    main()

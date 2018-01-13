# from mpl_toolkits.mplot3d import axes3d
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
# import requests
import os
import geocoder
import googlemaps
# import time
import ephem
import math
import warnings

warnings.filterwarnings("ignore")

def DMStoDD(DMS):
    x = str(DMS)
    x = x.split(":")
    DD = (math.fabs(float(x[0]))+float(x[1])/60 +float(x[2])/3600) * np.sign(float(x[0]))
    return DD

def top_to_geo(lat, lon, elev=0):
    # ze stopniów do radianów
    lat = np.radians(lat)
    lon = np.radians(lon)
    # Promień ziemi
    R = ephem.earth_radius
    # Współczynnik spłaszczenia ziemi
    f = 1/298.257223563
    # Współczynniki do obliczeń
    F = (1-f)**2
    C = 1/(math.sqrt(math.cos(lat)**2 + F * math.sin(lat)**2))
    S = C*F
    # Obliczenie współrzędnych kartezjańwszystkich
    x = (R * C + elev)*math.cos(lat) * math.cos(lon)
    y = (R * C + elev)*math.cos(lat) * math.sin(lon)
    z = (R * S + elev)*math.sin(lat)
    return x, y, z

def sat_position():
    # Sprawdzenie czy dane zostały już ściągnięte
    if os.path.exists('TLE_SATELLITE.txt'):
        data = open('TLE_SATELLITE.txt', 'r').readlines()
    else:
        # Deklaracja strony do pobierania danych
        tle_url = 'http://www.celestrak.com/NORAD/elements/gps-ops.txt'
        # Zwrócenie danych ze strony
        satellite_data = requests.get(tle_url).text
        # Zapis danych do pliku txt
        sat_data = open('TLE_SATELLITE.txt','w')
        sat_data.write(satellite_data)
        sat_data.close()
        data = open('TLE_SATELLITE.txt', 'r').readlines()
    # Usunięcie znaków nowej lini
    data = [a for a in data if a != '\n']
    data = ''.join(data)
    data = data.split('\n')
    data2= [[0 for x in range(3)] for y in range(int(len(data)/3))]
    # zapisane TLE wybranej konstelacji satelitów w macierzy w postaci:
    # |Sat1Line0 Sat1Line1 Sat1Line2|
    # |Sat2Line0 ...................|
    # |.............................|
    # |SatnLine0 ......... SatnLine2|
    for a in range(int(len(data)/3)):
        for b in range(3):
            data2[a][b] = data[3*a+b]
    return data2

def obs_position():
    # Klucz do googlemaps elevation API
    key = open('key.txt', 'r').readlines()
    gmaps = googlemaps.Client(key = key[0])
    x = input('Określić twoje aktualne położenie jako miejsce obserwacji ? [t/n] ')
    # Jeżeli lokalizacja ma zostać wyznaczona dla aktualnej pozycji wyznacz się ją na podstawie IP
    if x.lower() == 't':
        g = geocoder.ip('me')
    else:
        # Jeżeli dla dowolnego miejsca na podstwaie google
        y = str(input('Dla jakiego miejsca ma zostać wyznaczone położenie ? '))
        g = geocoder.google(y)

    # Wyznaczenie długości, szerokości, przewyższenie
    lat = list(g.latlng)[0]
    lon = list(g.latlng)[1]
    e = gmaps.elevation(tuple(g.latlng))
    elev = e[0].get('elevation')
    place = g.city
    OPV = lat, lon
    return OPV, place

# funkcja określająca widoczność satelity w zadanym okresie czasu dla danego abserwatora
def sat_solving(number_of_satellite, OPV, cone_angle = 85,\
                delta_time=30, period_of_solving = 24,\
                start_date = ephem.now(), data = sat_position(),place = 'b/d'):
    # wyświetlanie ładowania
    print(str(number_of_satellite) + "...")
    # delta_time w sekundach, period_of_solving w godzinach
    amount_of_steps = int(period_of_solving*3600/delta_time)
    # rozwiązanie TLE,
    my_sat = ephem.readtle(data[number_of_satellite][0], data[number_of_satellite][1], data[number_of_satellite][2])
    # deklaracja list
    check_value_list = [] # wszystkie wartości sprawdzające
    sat_elev_list = [] # wartości elewancji przy przejściu przez granicę FOV
    sat_lat_list = [] # wartości szerokośći geograficznej przy przejściu przez granicę FOV
    sat_lon_list = [] # wartości długości geograficznej przy przejściu przez granicę FOV
    entry_lat = []
    entry_lon = []
    exit_lat = []
    exit_lon = []
    passage_counter = 0
    i1=0
    i2=0
    # tworzenie ściezki folderu, zapis wynikow do pliku
    os.makedirs(".\Wyniki - " + str(place) + str(cone_angle) + '\wejście-wyjście', exist_ok=True)
    files = open(".\Wyniki - " + str(place) + str(cone_angle) + "\wejście-wyjście\ " + str(data[number_of_satellite][0]) + '.txt','w')
    files.writelines(str(data[number_of_satellite][0]) + "\n\nData" + "\t\t\twej/wyj" +"\t" + "Szerokość" + "\t" + "Długość" + "\n")
    # pętla licząca długośc i szerokosc geograficzną satelity dla kolejnych kroków czasowych
    for a in range(amount_of_steps):
        my_sat.compute(start_date)
        # wysokośc satelity nad pow. Ziemi, w ephem nazwane 'elevation'
        sat_elev = my_sat.elevation
        # zamiana formatu położenia
        sat_lat = DMStoDD(my_sat.sublat)
        sat_lon = DMStoDD(my_sat.sublong)
        start_date = ephem.date(start_date + delta_time * ephem.second)
        # Satellite Position Vector
        SPV = np.array(top_to_geo(sat_lat,sat_lon,sat_elev))
        # Funkcja sprawdzająca położenie punktu w względem jedno stronnego stożka, ''+'' leży
            # wewnątrz, ograniczenie wartości do znaku +/-
        check_value = np.dot(OPV,np.subtract(SPV,OPV)) - \
                            np.linalg.norm(np.subtract(SPV,OPV))*np.linalg.norm(OPV) \
                            *math.cos(float(cone_angle)*np.pi/180)
        check_value_list = np.insert(check_value_list, a, np.sign(check_value))

        # listy współrzędnych satelity dla kolejnych kroków czasowych
        sat_lat_list = np.insert(sat_lat_list, a, sat_lat)
        sat_lon_list = np.insert(sat_lon_list, a, sat_lon)

        if a>0 and check_value_list[a] * check_value_list[a-1] < 0:
            if check_value_list[a] > 0:
                entry_lat = np.insert(entry_lat, i1,sat_lat)
                entry_lon = np.insert(entry_lon, i1,sat_lon)
                text = str(start_date) + "\twej" +"\t" + str(sat_lat) + "\t" + str(sat_lon) + "\n"
                files.writelines(text)
                i1=i1+1
            else:
                exit_lat = np.insert(exit_lat, i2,sat_lat)
                exit_lon = np.insert(exit_lon, i2,sat_lon)
                text = str(start_date) + "\twyj" +"\t" + str(sat_lat) + "\t" + str(sat_lon) + "\n"
                files.writelines(text)
                i2=i2+1
            passage_counter = passage_counter + 1
    files.close()
    entry_exit = [entry_lat,entry_lon,exit_lat,exit_lon]
    check_value_list = change_value(check_value_list, -1,0)
    return list(check_value_list), list(sat_lat_list), list(sat_lon_list), amount_of_steps

# funkcja rysująca wykresy na mapie
def plot_on_map(lat_sat, lon_sat, lat_obs = None, lon_obs = None,satellite = "b/d", place = "b/d"):
    # typ mapy
    m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,\
                llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
    # deklaracja i konwersja współrzędnych satelity
    lon_sat,lat_sat = m(lon_sat, lat_sat)
    m.scatter(lon_sat,lat_sat,marker='.',color = 'red', zorder=10)
    # deklaracja i konwersja współrzędnych obserwatora, gdy podano wsp.
    if lat_obs != None or lon_obs != None:
        lon_obs,lat_obs = m(lon_obs, lat_obs)
        m.scatter(lon_obs,lat_obs,marker='o',color = 'blue', zorder=10)
    # poprawa wyglądu
    m.drawcoastlines()
    m.fillcontinents(color='coral',lake_color='aqua')
    # draw parallels and meridians.
    m.drawparallels(np.arange(-90.,91.,10.),dashes = [1,3],labels = [1,0,0,0])
    m.drawmapboundary(fill_color='aqua')
    meridians = m.drawmeridians(np.arange(-180.,179.,10.),dashes=[1,3],labels=[0,0,0,1])
    for a in meridians:
        try:
            meridians[a][1][0].set_rotation(90)
        except:
            pass
    plt.title("Satellite: " + str(satellite) + "   Place: " + str(place))

def change_value(my_list,old_value,new_value):
    for a in range(len(my_list)):
        if my_list[a] == old_value:
            my_list[a] = new_value
    return my_list


#  wczytanie wektora polożenia obserwatora oraz, nazwy miejscowosci
OPV, place = obs_position()
# zapis położenia obserwatora wpostaci dl/szer. geograficzna
lat_obs_degrees = OPV[0]
lon_obs_degrees = OPV[1]
# zapis polozenia obserwatora we wpl. kartezjanskich
OPV = np.asarray(top_to_geo(OPV[0],OPV[1]))
# określenie czasu pooczątku ekspretymentu
date = ephem.now()
# wczytanie TLE w postaci macierzu dwuwymiarowej
TLE_list = sat_position()
# deklaracja tablic
great_check_list = [a for a in range(len(TLE_list))]
great_sat_lat_list = [a for a in range(len(TLE_list))]
great_sat_lon_list = [a for a in range(len(TLE_list))]

cone_angle = 80

# Rozwiązanie satelit, wspisanioe wyników do talbicy 2D
for a in range(len(TLE_list)):
    check, lat_sat, lon_sat, amount_of_steps = sat_solving(a, OPV, cone_angle,\
                                            delta_time=300, period_of_solving = 30,\
                                            start_date = date, data = TLE_list, place = place)
    great_check_list[a] = check
    great_sat_lat_list[a] = lat_sat
    great_sat_lon_list[a] = lon_sat
# Deklaracja tablic sumujących
sum_check_list = [a for a in range(len(check))]
# Wyliczenie tablicy sumujące, ilość widocznych satelitów w danej chwili czasu
for a in range(len(check)):
    val = 0
    for b in range(len(TLE_list)):
        val = great_check_list[b][a] + val
    sum_check_list[a] = val
# Deklaracja tablic
in_FOV = [a for a in range(len(TLE_list))]
# Wyliczanie 'czasu' obserwacji danej ilości satelitów (względnej)
text = '\nZadane wielkości:'+\
        '\nMiejsce obserwacji:\t\t' + str(place)+\
        '\nPółkąt stożka FOV:\t\t' + str(cone_angle)+ \
        '\nLiczba kroków obliczeniowych:\t'+ str(amount_of_steps)+ \
        '\n'+\
        '\nWzględny czas widoczności:'
print(text)
files = open(".\Wyniki - " + str(place) + str(cone_angle) + '\\raport ' + str(place) + str(cone_angle) +'.txt','w')
files.writelines(text)
for a in range(len(TLE_list)):
    in_FOV[a] = sum_check_list.count(a)/amount_of_steps
    if in_FOV[a] != 0:
        print("--", a , "satelitów:", "%0.4f" % in_FOV[a])
        files.writelines('\n--\t' + str(a) + ' satelitów\t' +str(in_FOV[a]))
files.close()
print('\nSprawdzenie: ', np.sum(in_FOV))

# wybór satelity do narysowania wykresu
for a in range(len(TLE_list)):
    print(a+1, TLE_list[a][0])
x = int(input('Wybierz numer satelity, którego wykres narysować [od 1 do ' + str(len(TLE_list)) + ']: ' ))
if type(x) == type(1) and x-1>=0 and x-1<= len(TLE_list):
    plot_on_map(great_sat_lat_list[x-1], great_sat_lon_list[x-1], lat_obs_degrees, lon_obs_degrees,TLE_list[x-1][0],place)
    plt.show()
    plt.close()
# zapisanie wykresów do folderu
os.makedirs(".\Wyniki - " + str(place) + str(cone_angle) + '\wykresy', exist_ok=True)
for a in range(len(TLE_list)):
    plot_on_map(great_sat_lat_list[a], great_sat_lon_list[a], lat_obs_degrees, lon_obs_degrees,TLE_list[a][0],place)
    plt.savefig(".\Wyniki - " + str(place) + str(cone_angle) + "\wykresy\ " + TLE_list[a][0] + ".png")
    plt.close()
    print("plot no. " +str(a+1) +" has been saved...")

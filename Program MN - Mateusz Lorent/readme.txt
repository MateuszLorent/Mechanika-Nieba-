Aby program działał prawidło niezbędne jest:
- posiadanie klucza aktywacyjnego Google API Elev - key.txt
- Pythona 3.x oraz bibliotek:
----mpl_toolkits.basemap 
----matplotlib.pyplot
----numpy
----os
----geocoder
----googlemaps
----ephem
----import math
----warnings
- połączenie z internetem 

Zadaniem programu jest wyliczenie widoczności konstelacji satelitów z wybranego miejsca na powierzchni Ziemi.
W miejscu, gdzie pojawi się prośba o podanie lokalizacji, należy wpisać dowolną miejscowość, opocjonalnie kraj (działa jak wyszukiwarka Google)
Po wykonaniu obliczeń powinien pojawić się folder o nazwie: Wyniki - [miejscowosc][polkat stożka obserwacji], w nim dwa folder: ze zdjęciami, wsp. wejśca i wyjścia w FOV oraz raport.txt

Funkcję określające położenie za pomocą Google oraz dane TLE na postawie projektu Pana KM

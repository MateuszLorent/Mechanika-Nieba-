Aby program dzia�a� prawid�o niezb�dne jest:
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
- po��czenie z internetem 

Zadaniem programu jest wyliczenie widoczno�ci konstelacji satelit�w z wybranego miejsca na powierzchni Ziemi.
W miejscu, gdzie pojawi si� pro�ba o podanie lokalizacji, nale�y wpisa� dowoln� miejscowo��, opocjonalnie kraj (dzia�a jak wyszukiwarka Google)
Po wykonaniu oblicze� powinien pojawi� si� folder o nazwie: Wyniki - [miejscowosc][polkat sto�ka obserwacji], w nim dwa folder: ze zdj�ciami, wsp. wej�ca i wyj�cia w FOV oraz raport.txt
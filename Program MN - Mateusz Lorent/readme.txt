Aby program dzia³a³ prawid³o niezbêdne jest:
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
- po³¹czenie z internetem 

Zadaniem programu jest wyliczenie widocznoœci konstelacji satelitów z wybranego miejsca na powierzchni Ziemi.
W miejscu, gdzie pojawi siê proœba o podanie lokalizacji, nale¿y wpisaæ dowoln¹ miejscowoœæ, opocjonalnie kraj (dzia³a jak wyszukiwarka Google)
Po wykonaniu obliczeñ powinien pojawiæ siê folder o nazwie: Wyniki - [miejscowosc][polkat sto¿ka obserwacji], w nim dwa folder: ze zdjêciami, wsp. wejœca i wyjœcia w FOV oraz raport.txt
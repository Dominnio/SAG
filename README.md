# SAG
Systemy agentowe, projekt zaliczeniowy

12-06-2020

Projekt testowałem używajac:
- Windows 10,
- Pycharm,
- Python **3.7**,
- tensorflow 1.14,
- keras 2.2.5,
- spade 3.1.4

W pliku agent_config.py są dane poszczególnych agentów. 
Argumenty:  
	'steps_per_epoch': '1',  
    'epochs': '1',  
    'validation_steps': '1'  
decydująo długości trenowania klasyfikatora - ja ustawiłem bardzo małe, ze względu  
na czas obliczeń. Klasyfikator zaczyna poprawnie klasyfikować przy ustawieniach:  
	'steps_per_epoch': '8000',  
    'epochs': '25',  
    'validation_steps': '2000'  

W pliku cnn.py znajduje się już gotowy klasyfikator.   
W pliku classifying_agent.py znajdudje się wstępnie przygotowany model agenta.   
W pliku agent_utilities.py znajdują się kody odpowiedzialne za komunikację.  
W pliku help_functions.py znajdują się funkcje pomocnicze.  

W pliku classifying_agent.py umieściłem w różnych miejscach znaczki #### TO_DO #### - w tych miejscach można program  
rozwijać. Starałem wypisać tam wszystko co przychodzi mi do głowy, a co trzeba zrobić. Warto odnosić się  
też do dokumentu google.


Program działa tak:
Agenci się inicjują, i wskakują do odpowiednich stanów: stan 1 jest dla agenta dowodzącego, stan 2 dla robotników.  
Więcej dowiecie się z pliku classifying_agent.py.


Dokument google z listą TO_DO : https://docs.google.com/document/d/1J1dj5VJ-9L6mhyIOI25qfgbYt2debQjXubj3QeXhrQ0/edit?fbclid=IwAR00acej3RGMEuV4IljcbPhuhkWYFhkz9bt_0NCmRg1dXqEsuvfvbCxQNo8  

Dokument LATEX z raportem końcowym do zedytowania(jako template dałem jakiś swój stary raport): https://www.overleaf.com/7617868931cvgvmcyqsdsc  

Polecam link do nauki: https://spade-mas.readthedocs.io/en/latest/usage.html

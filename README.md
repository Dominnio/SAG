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
decydują o długości trenowania klasyfikatora - domyślnei ustawione są na bardzo małe ze względu  
na czas obliczeń. Klasyfikator poprawnie klasyfikuje przy ustawieniach:  
	'steps_per_epoch': '8000',  
    'epochs': '25',  
    'validation_steps': '2000'  


W pliku cnn.py znajduje się już gotowy klasyfikator.   
W pliku classifying_agent.py znajdudje się wstępnie przygotowany model agenta.   
W pliku agent_utilities.py znajdują się kody odpowiedzialne za komunikację.  
W pliku help_functions.py znajdują się funkcje pomocnicze.  
Skrypt interface.py udostępnia interface użytkownikowi do komunikacji ze zrealizowanym systemem agentowym.  


Przed uruchomieniem projektu należy pobrać plik datasets, dostępny pod tym linkiem:  
https://drive.google.com/file/d/1t1iet3aDXxEGsDdubEJQKupeJ_g-1f-X/view?usp=sharing
Plik należy wypakować, a wypakowany folder datasets umieścić w katalogu głównym programu.

Program należy uruchamiać następująco: najpierw uruchamia się plik classifying_agent.py - ze względu na możliwe  
dosyć duże opóźnienia należy poczekać aż się prawidłowo zainicjuje (agenci bedą na zmianęwysyłali do siebie wiadomości).

Po inicjalizacji, należy uruchomić plik interface.py - jest to samodzielny program umożliwiający przekazywanie zdjęć  
klasyfikatorowi do rozpoznania oraz otrzymywanie wyników.

Klasyfikacja moze być też inicjowana ręcznie: po inicjacji classifying_agent.py, zdjecia do klasyfikacji należy umieścić  
w folderze data_to_recognize/recognize . Wyniki zapisywane są do pliku classification_results.txt.



Link do nauki SPADE: https://spade-mas.readthedocs.io/en/latest/usage.html

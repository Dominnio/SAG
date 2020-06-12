# SAG
Systemy agentowe, projekt zaliczeniowy

29-05-2020

Projekt testowałem używajac:
- Windows 10,
- Pycharm,
- Python **3.7**,
- tensorflow 1.14,
- keras 2.2.5,
- spade 3.1.4

W pliku agent_config.py są dane poszczególnych agentów. Należy pozmieniać ścieżki do danych trenujących.
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

** JAK działa classifying_agent.py? **
Zaimplementowałem 2 zachowania: 1 cykliczne to skrzynka pocztowa agenta dowodzącego - aktywowana jest
przez wysłanie do siebie maila przez agenta który został agentem dowodzącym. Po aktywacji odpowiada wszystkim
agentom kto dowodzi. Jak raz skrzynka zostanie aktywowwana to nie da siejej wyłaczyć - chyba że agent dowodzący zginie.  

2 to maszyna stanów - powoli realizuję projekt maszyny stanów ze zdjęcia które wysłałem. Jak agent dowodzi idzie do S1.
Jak nie, to idzie do S2.

Z dokumentu google, z listy TO_DO zrealizowałem 2 pierwsze punkty. Teraz powinno polecieć już łatwiej -
do zrobienia od punktu 3.


Dokument google z listą TO_DO : https://docs.google.com/document/d/1J1dj5VJ-9L6mhyIOI25qfgbYt2debQjXubj3QeXhrQ0/edit?fbclid=IwAR00acej3RGMEuV4IljcbPhuhkWYFhkz9bt_0NCmRg1dXqEsuvfvbCxQNo8  

Polecam link do nauki: https://spade-mas.readthedocs.io/en/latest/usage.html

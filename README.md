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
	'steps_per_epoch': '10',
    'epochs': '1',
    'validation_steps': '10'
decydująo długości trenowania klasyfikatora - ja ustawiłem bardzo małe, ze względu
na czas obliczeń. Klasyfikator zaczyna poprawnie klasyfikować przy ustawieniach:
	'steps_per_epoch': '8000',
    'epochs': '25',
    'validation_steps': '2000'

W pliku cnn.py znajduje się już gotowy klasyfikator.
W pliku dummyagent.py znajduje się przykłądowy agent używający klasyfikatora.

TO DO:
- zaimplementować sposób komunikacji agentów,
- zaimplementować sposób wybierania agenta dowodzącego,
- wizualizacja wyników ( najlepiej przez wbudowany w spadzie sposób przeglądarkowy)

Polecam link do nauki: https://spade-mas.readthedocs.io/en/latest/usage.html

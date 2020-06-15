#===============================MOTIVATION================================
#   This code was created for the semester project of Agent-Based Systems
#   course (SAG_2020L) of master studies programme at the Warsaw University
#   of Technology - Faculty of Electronics and Information Technology. 
#
#   Supervision and mentoring: PhD D.Ryżko
#
#===============================SUMMARY===================================
#
#   The agent system performs task of a distributed image classification.
#   System consists of agents that are communicating asynchronously. The decision
#   of the classifier is obtained by voting. A randomly selected commanding agent 
#   from ordinary agents is responsible for outsourcing tasks and collecting
#   classification results. System ensures operation even if contact with some
#   agents is lost.
#
#===============================LICENSE===================================
#
#   This code is a free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as 
#   published by the Free Software Foundation, either version 3 of the 
#   License, or any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details. It can be found
#   at <http://www.gnu.org/licenses/>.
#
#==========================================================================
#   2020 Warsaw University of Technology - M.Karcz, D.Orlinski, T.Szczepanski
#==========================================================================    
#
#   agent_config.py - used by classifying_agent.py - config file of agents
#   provides configuration of xmpp server that is used by gent, agents' models 
#   and its features are defined by learning data paths
#
#==========================================================================


import os

server_name = 'jabber.hot-chilli.net'

agents_dict = {
    'agent_1': { #detects - dogs
        'jid': 'spade_pro1@{}'.format(server_name),
        'password': '1qwerty8',
        'hostname': '127.0.0.1',
        'port': '10001',
        'training_set_path': os.path.join('..','SAG', 'datasets', 'dogs', 'training_set'),
        'test_set_path': os.path.join('..','SAG', 'datasets', 'dogs', 'test_set'),
        'purpose': 'dogs',
        'steps_per_epoch': '1',
        'epochs': '1',
        'validation_steps': '1'
    },
    'agent_2': { #detects - cats
        'jid': 'spade_pro2@{}'.format(server_name),
        'password': '1qwerty8',
        'hostname': '127.0.0.1',
        'port': '10002',
        'training_set_path': os.path.join('..','SAG', 'datasets', 'cats', 'training_set'),
        'test_set_path': os.path.join('..','SAG', 'datasets', 'cats', 'test_set'),
        'purpose': 'cats',
        'steps_per_epoch': '1',
        'epochs': '1',
        'validation_steps': '1'
    },
      'agent_3': { #detects - horses
        'jid': 'spade_pro3@{}'.format(server_name),
        'password': '1qwerty8',
        'hostname': '127.0.0.1',
        'port': '10003',
        'training_set_path': os.path.join('..','SAG', 'datasets', 'horses', 'training_set'),
        'test_set_path': os.path.join('..','SAG', 'datasets', 'horses', 'test_set'),
        'purpose': 'horses',
        'steps_per_epoch': '1',
        'epochs': '1',
        'validation_steps': '1'
      },
    'agent_4': { #detects - chickens
        'jid': 'spade_pro4@{}'.format(server_name),
        'password': '1qwerty8',
        'hostname': '127.0.0.1',
        'port': '10004',
        'training_set_path': os.path.join('..','SAG', 'datasets', 'chickens', 'training_set'),
        'test_set_path': os.path.join('..','SAG', 'datasets', 'chickens', 'test_set'),
        'purpose': 'chickens',
        'steps_per_epoch': '1',
        'epochs': '1',
        'validation_steps': '1'
    }
}

test_images = {
    'cat1': os.path.join('..','SAG', 'datasets', 'single_prediction', 'cat.1.jpg'),
    'cat2': os.path.join('..','SAG', 'datasets', 'single_prediction', 'cat.2.jpg'),
    'chicken1': os.path.join('..','SAG', 'datasets', 'single_prediction', 'chicken.1.jpeg'),
    'chicken2': os.path.join('..','SAG', 'datasets', 'single_prediction', 'chicken.2.jpeg'),
    'dog1': os.path.join('..','SAG', 'datasets', 'single_prediction', 'dog.1.jpg'),
    'dog2': os.path.join('..','SAG', 'datasets', 'single_prediction', 'dog.2.jpg'),
    'horse1': os.path.join('..','SAG', 'datasets', 'single_prediction', 'horse.1.jpeg'),
    'horse2': os.path.join('..','SAG', 'datasets', 'single_prediction', 'horse.2.jpeg')
}


# Templates
# To Commander Key, Values
CONTROL = "[CONTROL]"  # używ. do wys. sekw. kontrlonych. Wszyst. jest sekw. kontrolnymi wiec nie ma innych.
TO_CMB = "[TO_CMB]" # Behaviour do którego skierowana jest wiadomosc - to_cmb - CommanderMessageBox
TO_FSM = "[TO_FSM]" # Behaviour do którego skierowana jest wiadomosc - to_fsm - FSMBehaviour
# Control messages
WHO_IS_IN_COMMAND = "Who is in command?" # Wysyłane przez agentow pytajacych o istnienie agenta dowodzacego
WHO_IS_IN_COMMAND_RESPONSE = "[WIICR]" # Odpowiedz agenta dowodzącego na zapytanie "czy istniejesz"
MULTIPLE_COMMANDERS = "Are there multiple commanders?" # Kod na wypadek wystapienia wielu commanderów

WHO_IS_READY_TO_SERVE = "[WHO_IS_READY_TO_SERVE]" # Agent dowodzący sprawdza którzy agenci są gotowi do działania
ALIVE_SLAVE = "[ALIVE_SLAVE]" # informacja zwrotna dla agenta dowodzącego poszukującego agentów gotowych do działania

# Voting messages
COMMANDER_VOTING = "[CV]" # Kod oznaczający głosowanie między zduplikowanymi agentami dowodzącymi
AGENT_VOTING = "[AV]" # Kod oznaczający głosowanie na wybory nowego agenta dowodzacego


# Recognition codes
CLASSIFY_OBJECT = "[CLASSIFY_OBJECT]" # Kod który powinien być dołączany do wiadom. z linkiem do obrazka do klasyfikacji

CLASSIFIED = "[CLASSIFIED]"
NOT_CLASSIFIED = "[NOT_CLASSIFIED]"
# State codes

STATE_ZERO = "STATE_ZERO" # Oznaczenia stanów
STATE_ONE = "STATE_ONE"
STATE_TWO = "STATE_TWO"
STATE_THREE = "STATE_THREE"


#########################################################
# Recognize data folders

RECOGNIZE_FOLDER = os.path.join('..','SAG','data_to_recognize', 'recognize')
RECOGNIZED_FOLDER = os.path.join('..', 'SAG', 'data_to_recognize', 'recognized')
CLASSIFICATION_RESULTS_FILE = os.path.join('..', 'SAG', 'data_to_recognize', 'classification_results.txt')

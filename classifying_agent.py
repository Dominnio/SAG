from spade import quit_spade
from spade import agent
from spade.behaviour import CyclicBehaviour
from spade.behaviour import FSMBehaviour, State
from spade.behaviour import OneShotBehaviour
from spade.template import Template
import time
import asyncio
import agent_config as ac
import cnn
import help_functions as hf
import agent_utilities as au


### Finite State Machine and States

class FSMBehav(FSMBehaviour):
    async def on_start(self):
        print("Agent {} starting".format(self.agent.jid))


class StateZero(State):
    async def run(self):
        ##### TO_DO #####
        # Tutaj należy przeprowadzić trenowanie agenta(lub ewentualne pobranie gotowego wstępnie wytrenowanego modelu
        # klasyfikatora) - czyli odpalenie pliku cnn.py . Gotowy model będzie używany w stanie 2 i 1, więc należy
        # przemyśleć jak go tam udostępnić.

        # Co do pobierania gotowego modelu klasyfikatora - narazie olać, jak starczy czasu to zrobi się to pod koniec.

        print("Agent {} in state 0".format(self.agent.jid))
        await au.allocate_new_agent(self)


class StateOne(State):
    async def run(self):
        print("Agent {} is in state 1.".format(self.agent.jid))
        await au.prevent_multiple_commanders(self, 1)

        ##### TO_DO #####
        # Tutaj powinna byc zakodowana interakcja z uzytkownikiem, czyli pobieranie zdjęcia, rozsyłanie
        # jej do agentów i wyświetlanie wyników.I ewentualnie jakies inne
        # jak starczy czasu. Ważne jest też zrobienie funkcji monitorującej stan życia pozostałych agentów.
        # Napewno przyda się taki alive_check przed wysłaniem zdjęcia do agentów lub monitorowania ich stanu oraz liczby
        # Wydaje mi się że nie potrzeba do zrealizowania powyższych funkcji jakiś dodatkowych stanów.
        # Ogólnie idea jest taka, ze jak agent zostanie dowodzącym i nie bedzie innych dowodzących agentów, to się
        # solidnie zagnieżdża w stanie 1. Można przyjąć że jest tylko jeden agent dowodzacy który mozę udostępnić
        # interfejs. Tylko zabicie agenta powinno móc go z tego stanu usunąć.

        # Oczywiście konieczne jest również zrobienie funkcji która pobiera wyniki klasyfikacji od agentów.
        # Należy pamiętać, że agent dowodzący również klasyfikuje i w tym stanie również powinien móc dać wynik
        # klasyfikacji

        # Kolejna rzecz to umożliwienie użytkownikowi pobranie ostatniej wartości klasyfikacji od każdego z agentów
        # (na wypadek niefortunnej śmierci agenta dowodzącego)

        # W skrócie w tym stanie należy zrealizować interfejs do komunikacji z użytkownikiem

        # Należy przetestować co sie stanie jak zabijemy agenta dowodzącego będącego w trakcie interakcji
        # z użytkownikiem. Domyślnie powinna powstać funkcja is_commander_alive uruchamiana w stanie 2, sprawdzająca
        # co np. 3 sec czy commander żyje. Narzie jej nie ma, ale śmierć agenta powinna odblokowywać interfejs
        # dla nowego agenta dowodzacego

class StateTwo(State):
    async def run(self):
        print("Agent {} is in state 2.".format(self.agent.jid))

        ##### TO_DO #####
        # Tutaj powinna odbywać się klasyfikacja, czyli agent powinien oczekiwać na wiadomość albo o przeprowadzeniu
        # głosowania na nowego lidera, albo na wiadomość z obrazkiem(lub linkiem do obrazka), klasyfikować go i odesłać.
        # wynik klasyfikacji powinien być zapisany na wypadek utraty informacji (śmierć agenta dowodzącego) i możliwa
        # do ponownego wysłania

        # Będzie tutaj również funkcja sprawdzajaca co 3 sec, czy agent dowodzący zyje i przeprowadzajaca głosowanie
        # na wypadek śmierci.

        # najprawdopodobniej sam się tym zajmę, bo tutaj będzie najwięcej komunikacji między agentami.


class ClassifyingAgent(agent.Agent):
    class CommanderMessageBox(CyclicBehaviour):
        # async def on_start(self):
        #     # print("Agent {} box for commander mail is ready.".format(self.agent.jid))
        async def run(self):
            await au.new_commander_initialization(self)

    async def setup(self):
        print("Agent {} starting. Purpose : recognize {}.".format(self.jid, self._values['agent_data']['purpose']))
        cmb_template = Template()
        cmb_template.set_metadata(ac.CONTROL, ac.TO_CMB)

        fsm_template = Template()
        fsm_template.set_metadata(ac.CONTROL, ac.TO_FSM)

        au.initialize(self, cmb_template, fsm_template, FSMBehav, StateZero, StateOne, StateTwo)


if __name__ == "__main__":

    # jak agenci źle się inicjują to trzeba albo usunąć wszystkie time.sleep(x), albo ustawić je na min. 5 sec

    ##### TO_DO #####
    # To poniżej wygląda źle. Przydałaby się jakaś ładna funkcja:
    # - pozwalałaby na wybór ilu agetów chce się uruchomić, w jakiej kolejności, z jakimi opóźnieniami
    # albo przynajmniej mniej wiecej coś takiego. Ważne żeby można było operować opóźnieniami między tworzeniem agentów.


    agent1 = ClassifyingAgent(ac.agents_dict['agent_1']['jid'],
                              ac.agents_dict['agent_1']['password'])
    agent1.set('agent_data', ac.agents_dict['agent_1'])
    agent1.web.start(ac.agents_dict['agent_1']['hostname'], ac.agents_dict['agent_1']['port'])
    agent1.start()

    #time.sleep(5)
    #time.sleep(0.1)
    print("Initializing next agent...")

    agent2 = ClassifyingAgent(ac.agents_dict['agent_2']['jid'],
                              ac.agents_dict['agent_2']['password'])
    agent2.set('agent_data', ac.agents_dict['agent_2'])
    agent2.web.start(ac.agents_dict['agent_2']['hostname'], ac.agents_dict['agent_2']['port'])
    agent2.start()

    #time.sleep(5)
    print("Initializing next agent...")

    agent3 = ClassifyingAgent(ac.agents_dict['agent_3']['jid'],
                              ac.agents_dict['agent_3']['password'])
    agent3.set('agent_data', ac.agents_dict['agent_3'])
    agent3.web.start(ac.agents_dict['agent_3']['hostname'], ac.agents_dict['agent_3']['port'])
    agent3.start()

    #time.sleep(5)
    print("Initializing next agent...")

    agent4 = ClassifyingAgent(ac.agents_dict['agent_4']['jid'],
                              ac.agents_dict['agent_4']['password'])
    agent4.set('agent_data', ac.agents_dict['agent_4'])
    agent4.web.start(ac.agents_dict['agent_4']['hostname'], ac.agents_dict['agent_4']['port'])
    agent4.start()

print("Wait until user interrupts with ctrl+C")
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        agent1.stop()
        quit_spade()
        break

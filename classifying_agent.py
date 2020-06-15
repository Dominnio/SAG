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
#   classifying_agent.py - is the main script,
#   it uses: help_functions.py, agent_utilities.py, agent_config.py, cnn.py 
#
#==========================================================================

from spade import agent
from spade.behaviour import CyclicBehaviour
from spade.behaviour import FSMBehaviour, State
from spade.template import Template
import time
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
        print("Agent {} in state 0".format(self.agent.jid))

        # Latka - Symulacja śmierci agenta
        await hf.simulate_death(self)
        await au.allocate_new_agent(self)

class StateOne(State):
    async def run(self):
        print("Agent {} is in state 1.".format(self.agent.jid))
        # Latka - Symulacja śmierci agenta
        await hf.simulate_death(self)
        await au.prevent_multiple_commanders(self, 1)

        # Oczekuj na plik i rozpoznaj
        await au.wait_for_file_and_recognize(self)

class StateTwo(State):
    async def run(self):
        print("Agent {} is in state 2.".format(self.agent.jid))
        # Latka - Symulacja śmierci agenta
        await hf.simulate_death(self)

        # Sprawdz czy agent dowodzący żyje i zwróć jego jid
        commander_jid = await au.is_commander_alive(self)

        # Uruchom menedżera zadań
        await au.agent_task_manager(self, commander_jid)

class ClassifyingAgent(agent.Agent):
    class CommanderMessageBox(CyclicBehaviour):
        # Skrzynka pocztowa, do której pełen dostęp ma tylko aktywny i demokratycznie wybrany agent dowodzący.

        async def run(self):
            await au.new_commander_initialization(self)

    # Blok inicjujący SPADE'a - tutaj dodaje i modyfikuje się zachowania agenta
    async def setup(self):
        print("Agent {} starting. Purpose : recognize {}.".format(self.jid, self._values['agent_data']['purpose']))
        #Flaga do przyjmowania subskrypcji od wszystkich
        self.presence.approve_all = True
        ###############################
        # Przygotowywanie klasyfikatora
        self.model = cnn.initialize_classificator(self._values['agent_data'])
        #
        ###############################
        cmb_template = Template()
        cmb_template.set_metadata(ac.CONTROL, ac.TO_CMB)

        fsm_template = Template()
        fsm_template.set_metadata(ac.CONTROL, ac.TO_FSM)

        au.initialize(self, cmb_template, (fsm_template), FSMBehav, StateZero, StateOne, StateTwo)

if __name__ == "__main__":
 
    agents = []
    agent_names = ['agent_1', 'agent_2', 'agent_3']
    print = hf.print_wrapper(ac.LOGS_FILE)(print)

    for name in agent_names:
        print("Initializing next agent...")
        agent = ClassifyingAgent(ac.agents_dict[name]['jid'], ac.agents_dict[name]['password'])
        agent.set('agent_data', ac.agents_dict[name])
        agent.web.start(ac.agents_dict[name]['hostname'], ac.agents_dict[name]['port'])
        agent.start()
        time.sleep(7)
        agents.append(agent)
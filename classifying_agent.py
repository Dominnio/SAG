from spade import quit_spade
from spade import agent
from spade.behaviour import CyclicBehaviour
from spade.behaviour import FSMBehaviour, State
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template
import time
import asyncio
import agent_config
import cnn

# Templates
# To Commander Key, Values
CONTROL = "control"
TO_CMB = "to_cmb"
TO_FSM = "to_fsm"
# Control messages
WHO_IS_IN_COMMAND = "Who is in command?"
WHO_IS_IN_COMMAND_RESPONSE = "[WIICR]"

STATE_ZERO = "STATE_ZERO"
STATE_ONE = "STATE_ONE"
STATE_TWO = "STATE_TWO"
STATE_THREE = "STATE_THREE"


# Message codes


### Finite State Machine and States

class FSMBehav(FSMBehaviour):
    async def on_start(self):
        print("Agent {} starting".format(self.agent.jid))



class StateZero(State):
    async def run(self):
        print("Agent {} in state 0".format(self.agent.jid))
        i = 3  # Ask all agents who is in command 3 times
        print("Agent {} asking for commander {} time".format(self.agent.jid, i))
        promotion = True
        while i > 0:
            i -= 1
            for k, v in agent_config.agents_dict.items():
                print(k)
                print(v['jid'])
                if str(v['jid']) != str(self.agent.jid):
                    msg_to_send = Message(to=str(v['jid']))
                    msg_to_send.set_metadata(CONTROL, TO_CMB)
                    msg_to_send.body = WHO_IS_IN_COMMAND
                    print("Agent {} , message to {} has been sent.".format(self.agent.jid, v['jid']))
                    await self.send(msg_to_send)

                    msg = await self.receive(timeout=1)  # wait for response 1 sec
                    if msg and msg.body[:len(WHO_IS_IN_COMMAND_RESPONSE)] == WHO_IS_IN_COMMAND_RESPONSE:
                        print("Agent {} , got message from commander {}".format(self.agent.jid, v['jid']))
                        promotion = False
                        break
            if promotion == False:
                break
        if promotion == True:
            msg_to_send = Message(to=str(self.agent.jid))
            msg_to_send.set_metadata(CONTROL, TO_CMB)
            msg_to_send.body = "Taking the command."
            print("Agent {} , sending promotion note to himself.".format(self.agent.jid))
            await self.send(msg_to_send)

            self.set_next_state(STATE_ONE)
        elif promotion == False:
            self.set_next_state(STATE_TWO)


class StateOne(State):
    async def run(self):
        print("Agent {} is in state 1.".format(self.agent.jid))


class StateTwo(State):
    async def run(self):
        print("Agent {} is in state 2.".format(self.agent.jid))


class ClassifyingAgent(agent.Agent):

    class CommanderMessageBox(CyclicBehaviour):
        async def on_start(self):
            print("Agent {} box for commander mail is ready.".format(self.agent.jid))
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg and msg.sender == self.agent.jid:
                print("Agent {} takes command.".format(self.agent.jid))
                while True:
                    msg = await self.receive(timeout=10)
                    if msg and msg.body == WHO_IS_IN_COMMAND:
                        msg_to_send = Message(to=str(msg.sender))
                        msg_to_send.set_metadata(CONTROL, TO_FSM)
                        msg_to_send.body = WHO_IS_IN_COMMAND_RESPONSE + "Agent {} is in command.".format(self.agent.jid)
                        await self.send(msg_to_send)

    async def setup(self):
        print("Agent {} starting. Purpose : recognize {}.".format(self.jid, self._values['agent_data']['purpose']))
        cmb_template = Template()
        cmb_template.set_metadata(CONTROL, TO_CMB)
        b = self.CommanderMessageBox()
        self.add_behaviour(b, cmb_template)

        ############
        fsm_template = Template()
        fsm_template.set_metadata(CONTROL, TO_FSM)
        fsm = FSMBehav()
        fsm.add_state(name=STATE_ZERO, state=StateZero(), initial=True)
        fsm.add_state(name=STATE_ONE, state=StateOne())
        fsm.add_state(name=STATE_TWO, state=StateTwo())

        fsm.add_transition(source=STATE_ZERO, dest=STATE_ONE)
        fsm.add_transition(source=STATE_ZERO, dest=STATE_TWO)
        self.add_behaviour(fsm, fsm_template)

if __name__ == "__main__":
    agent1 = ClassifyingAgent(agent_config.agents_dict['agent_1']['jid'],
                              agent_config.agents_dict['agent_1']['password'])
    agent1.set('agent_data', agent_config.agents_dict['agent_1'])
    agent1.web.start(agent_config.agents_dict['agent_1']['hostname'], agent_config.agents_dict['agent_1']['port'])
    agent1.start()

    time.sleep(10)
    print("Initializing next agent...")


    agent2 = ClassifyingAgent(agent_config.agents_dict['agent_2']['jid'],
                              agent_config.agents_dict['agent_2']['password'])
    agent2.set('agent_data', agent_config.agents_dict['agent_2'])
    agent2.web.start(agent_config.agents_dict['agent_2']['hostname'], agent_config.agents_dict['agent_2']['port'])
    agent2.start()

    time.sleep(10)
    print("Initializing next agent...")


    agent3 = ClassifyingAgent(agent_config.agents_dict['agent_3']['jid'],
                              agent_config.agents_dict['agent_3']['password'])
    agent3.set('agent_data', agent_config.agents_dict['agent_3'])
    agent3.web.start(agent_config.agents_dict['agent_3']['hostname'], agent_config.agents_dict['agent_3']['port'])
    agent3.start()

print("Wait until user interrupts with ctrl+C")
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        agent1.stop()
        quit_spade()
        break

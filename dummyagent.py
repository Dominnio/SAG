from spade import quit_spade
from spade import agent
from spade.behaviour import CyclicBehaviour
from spade.behaviour import OneShotBehaviour
from spade.message import Message
from spade.template import Template
import time
import asyncio
import agent_config
import cnn

#("spade_pro@protonxmpp.ch", "6qwerty8")
#("spade_pro@jabber.sytes24.pl", "6qwerty8")
#C:\Users\mk666\AppData\Local\Programs\Python\Python37\python.exe


class SenderAgent(agent.Agent):
    class InformBehav(CyclicBehaviour):
        async def run(self):
            print("InformBehav running")
            # msg = Message(to=agent_config.agent_2['jjd'])     # Instantiate the message
            # msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            # msg.body = "Hello World"                    # Set the message content
            #
            # await self.send(msg)
            # print("Message sent!")
            #
            #
            # await asyncio.sleep(5)
            # # stop agent from behaviour
            # #await self.agent.stop()
            self.agent = cnn.CNN(agent_config.agent_1)
            self.res = self.agent.predict(str(agent_config.test_images['dog1']))
            if self.res == 1:
                print('dog')
            else:
                print('not dog')

            await asyncio.sleep(5)

    async def setup(self):
        print("SenderAgent started")
        b = self.InformBehav()
        self.add_behaviour(b)

class ReceiverAgent(agent.Agent):
    class RecvBehav(CyclicBehaviour):
        async def run(self):
            print("RecvBehav running")

            msg = await self.receive(timeout=200) # wait for a message for 200 seconds
            if msg:
                print("Message received with content: {}".format(msg.body))
            else:
                print("Did not received any message after 200 seconds")

            # stop agent from behaviour
            #await self.agent.stop()

    async def setup(self):
        print("ReceiverAgent started")
        b = self.RecvBehav()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)



if __name__ == "__main__":
    # receiveragent = ReceiverAgent(agent_config.agent_2['jjd'], agent_config.agent_2['password'])
    # future = receiveragent.start()
    # future.result() # wait for receiver agent to be prepared.
    senderagent = SenderAgent(agent_config.agent_1['jjd'], agent_config.agent_1['password'])
    senderagent.start()
    #
    # while receiveragent.is_alive():
    #     try:
    #         time.sleep(1)
    #     except KeyboardInterrupt:
    #         senderagent.stop()
    #         receiveragent.stop()
    #         break
    # print("Agents finished")

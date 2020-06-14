import agent_config as ac
import help_functions as hf


## async def setup(self):
def initialize(obj, template1, template2, fsmbehav, state0, state1, state2):
    # inicjalizacja zachowan
    b = obj.CommanderMessageBox()
    obj.add_behaviour(b, template1)

    fsm = fsmbehav()
    fsm.add_state(name=ac.STATE_ZERO, state=state0(), initial=True)
    fsm.add_state(name=ac.STATE_ONE, state=state1())
    fsm.add_state(name=ac.STATE_TWO, state=state2())

    fsm.add_transition(source=ac.STATE_ZERO, dest=ac.STATE_ONE)
    fsm.add_transition(source=ac.STATE_ZERO, dest=ac.STATE_TWO)
    fsm.add_transition(source=ac.STATE_ONE, dest=ac.STATE_TWO)
    fsm.add_transition(source=ac.STATE_TWO, dest=ac.STATE_TWO)
    fsm.add_transition(source=ac.STATE_TWO, dest=ac.STATE_ONE)
    obj.add_behaviour(fsm, template2)


# class CommanderMessageBox(CyclicBehaviour):
#     async def run(self):
async def new_commander_initialization(obj):
    # kod bedzie krecil sie wokolo msg = await self.receive(timeout=1)
    # az agent sam sobie nie wysle wiadomosci - czyli awansuje do dowodzacego
    # jesli awansuje to:
    # 1. najpierw sprawdza czy są inni dowodzacy
    # 2. Jesli jest jakis stary dowodzacy, to funkcja wraca do msg = await self.receive(timeout=1)
    # 3. jesli jest kilku nowych dowodzacych, to funkcja wysyla do fsm wiadomosc z prosba o przeprowadzenie losowania
    # 4. W stanie1 jest ona odbierana przez pierwsze kilka sekund nowego dowodzacego. Jeśli taka wiadomosc nie przyjdzie
    #    to znaczy ze agent zostal jedynym agentem dowodzacym i program leci dalej
    # 5. Jesli nic nie przyjdzie po wyslaniu widomosci MULTIPLE_COMMANDERS ( czyli agent wygral losowanie w stanie 1,
    #    lub jest jedynym dowodzacym) to agent uruchamia auto-respodner agenta dowodzacego, czyli oddzielny proces
    #    niezaleznie odpowiadajacy na wiadomosci do agenta dowodzacego

    while True:
        commander = True

        # Latka - Symulacja śmierci agenta
        await hf.simulate_death(obj)

        msg = await obj.receive(timeout=1)

        # # Latka na wypadek wystapienia agenta w stanie 1 bez ustawionego autorespondera, po głosowaniu.
        #
        # if msg and msg.sender == obj.agent.jid and msg.body == ac.AM_I_THE_COMMANDER:
        #     msg_to_send = hf.prep_msg(obj.agent.jid, ac.CONTROL, ac.TO_FSM, ac.NOT_A_COMMANDER)
        #     await obj.send(msg_to_send)
        #     msg = None

        if msg and msg.sender == obj.agent.jid:  # if true agents becomes commander
            print("Agent {} is trying to take command.".format(obj.agent.jid))

            # Kod zabezpieczający przed wystąpieniem więcej niż jednego dowodzącego

            for k, v in ac.agents_dict.items():
                if str(v['jid']) != str(obj.agent.jid):
                    msg_to_send = hf.prep_msg(v['jid'], ac.CONTROL, ac.TO_CMB,
                                              ac.MULTIPLE_COMMANDERS)  # Asking if there are multiple commanders?
                    # print("Agent {} , message to {} has been sent.".format(self.agent.jid, v['jid']))
                    await obj.send(msg_to_send)

                    msg = await obj.receive(timeout=0.1)
                    if msg and msg.body == ac.WHO_IS_IN_COMMAND_RESPONSE:
                        # print("Agent {} WHO_IS_IN_COMMAND_RESPONSE".format(obj.agent.jid))

                        commander = False
                        break
                    if msg and msg.body == ac.MULTIPLE_COMMANDERS:
                        # print("Agent {} MULTIPLE_COMMANDERS".format(obj.agent.jid))
                        msg_to_send = hf.prep_msg(obj.agent.jid, ac.CONTROL, ac.TO_FSM,
                                                  ac.MULTIPLE_COMMANDERS)
                        await obj.send(msg_to_send)
                        commander = False
                        break

            if commander:
                break

    await commander_autoresponder(obj)


async def commander_autoresponder(obj):
    print("New Commander is Agent {} (autoresponder-on)".format(obj.agent.jid))
    while True:

        # Latka - Symulacja śmierci agenta
        await hf.simulate_death(obj)

        msg = await obj.receive(timeout=1)
        if msg and msg.body == ac.WHO_IS_IN_COMMAND:
            msg_to_send = hf.prep_msg(msg.sender, ac.CONTROL, ac.TO_FSM,
                                      ac.WHO_IS_IN_COMMAND_RESPONSE + "Agent {} is in command.".format(
                                          obj.agent.jid))
            await obj.send(msg_to_send)
        # To ewentualnie do zmiany ( zabezpiecza przypadek, gdyby mimo
        # istnienia agenta dowodzącego, pojawił się nowy agent dowodzący)
        if msg and msg.body == ac.MULTIPLE_COMMANDERS:
            msg_to_send = hf.prep_msg(msg.sender, ac.CONTROL, ac.TO_CMB,
                                      ac.WHO_IS_IN_COMMAND_RESPONSE + "Agent {} is in command.".format(
                                          obj.agent.jid))
            await obj.send(msg_to_send)

        # if msg and msg.body == ac.AM_I_THE_COMMANDER:
        #     msg_to_send = hf.prep_msg(msg.sender, ac.CONTROL, ac.TO_FSM,
        #                               ac.WHO_IS_IN_COMMAND_RESPONSE + "Agent {} is in command.".format(
        #                                   obj.agent.jid))
        #     await obj.send(msg_to_send)


# class StateZero(State):
#     async def run(self):
async def allocate_new_agent(obj):
    # Funkcja decyduje czy nowy agent zostaje dowodzacym, czy nie.



    i = 1  # Ask all agents who is in command 1 time
    # print("Agent {} asking for commander {} time".format(obj.agent.jid, i))
    promotion = True
    while i > 0:
        i -= 1
        for k, v in ac.agents_dict.items():
            # print(k)
            # print(v['jid'])
            if str(v['jid']) != str(obj.agent.jid):
                msg_to_send = hf.prep_msg(v['jid'], ac.CONTROL, ac.TO_CMB, ac.WHO_IS_IN_COMMAND)
                # print("Agent {} , message to {} has been sent.".format(self.agent.jid, v['jid']))
                await obj.send(msg_to_send)

                msg = await obj.receive(timeout=0.7)  # wait for response
                if msg and msg.body[:len(ac.WHO_IS_IN_COMMAND_RESPONSE)] == ac.WHO_IS_IN_COMMAND_RESPONSE:
                    # print("Agent {} , got message from commander {}".format(self.agent.jid, v['jid']))
                    promotion = False
                    break
        if not promotion:
            break
    if promotion:
        await hf.promotion_to_commanding(obj)
        obj.set_next_state(ac.STATE_ONE)
    elif not promotion:
        obj.set_next_state(ac.STATE_TWO)


# class StateOne(State):
#     async def run(self):
async def prevent_multiple_commanders(obj, timeout):
    # funkcja zapobiega powstawaniu wielu agentów dowodzących
    # Jest powiązana z funkcją new_commander_initialization(obj) - przez określony czas (timeout) nasłuchuje
    # czy nie zostało wywołane MULTIPLE_COMMANDERS - jeśli tak to przeprowaza głosowanie między agentami dowodzącymi
    # po wybraniu agenta dowodzącego będzie on oczekiwał na dane przychodzące od użytkownika. Reszta agentów
    # przechodzi do stanu 2 - czyli domyślnego stanu zwykłych agentów.

    msg = await obj.receive(timeout=timeout)
    if msg and msg.body == ac.MULTIPLE_COMMANDERS:  # Głosowanie!
        voting_result = await hf.start_voting(obj, ac.CONTROL, ac.TO_FSM, type_of_voting=ac.COMMANDER_VOTING)
        # print("Agent {} voting result: {}".format(obj.agent.jid, voting_result))
        if voting_result:
            await hf.promotion_to_commanding(obj)
            # obj.set_next_state(ac.STATE_ONE)      # Funkcja wywoływana jset ze stanu pierwszego
        else:
            obj.set_next_state(ac.STATE_TWO)

    # Wszyscy agenci, którzy z jakiegoś powodu wrócili do stanu pierwszego, a nie są agentami dowodzącymi zostają
    # zdegradowani

    # msg_to_send = hf.prep_msg(obj.agent.jid, ac.CONTROL, ac.TO_CMB, ac.AM_I_THE_COMMANDER)
    # # print("Agent {} , message to {} has been sent.".format(self.agent.jid, v['jid']))
    # await obj.send(msg_to_send)
    #
    # msg = await obj.receive(timeout=0.5)  # wait for response
    # if msg and msg.body[:len(ac.NOT_A_COMMANDER)] == ac.NOT_A_COMMANDER:
    #     msg = None
    #     obj.set_next_state(ac.STATE_TWO)

async def get_alive_agents(obj):
    # funkcja pobiera listę żywych agentów, porównuje ją z poprzednią listą i dodaje, lub usuwa agentów
    contacts = obj.presence.get_contacts()

    contacts = hf.get_contacts_from_roster(str(contacts))
    #print("From roster of contacts: {}".format(contacts))

    await hf.send_to_all(obj, ac.CONTROL, ac.TO_FSM, ac.WHO_IS_READY_TO_SERVE)
    alive_agents_list = []
    while True:
        collecting_messages = True
        msg = await obj.receive(timeout=1)  # waiting 1 sec from last gathered agent
        if msg and msg.body[:len(ac.ALIVE_SLAVE)] == ac.ALIVE_SLAVE:
            # dodawanie do listy znajomych żywych agentów
            # obj.presence.subscribe(str(msg.sender))   # subskrypcja działa dziwnie - czasami subskrybujesz tego samego
            alive_agents_list.append(str(msg.sender))   # wielokrotnie

            collecting_messages = False
        if collecting_messages:
            break
    #print("Alive agents list: {}".format(alive_agents_list))

    old_contacts = list(set(contacts) - set(alive_agents_list))
    #print("Stare kontakty: {}".format(old_contacts))
    for old_contact in old_contacts:
        pass
        # obj.presence.unsubscribe(str(old_contact)) # Z jakiegoś powodu program nie chce odsubsrybować - można umieścić
                                                     # w podsumowaniu że to nie działą
    return alive_agents_list



async def send_image_for_recognition(obj,img_path):
    # funkcja pobiera ścieżkę do obrazeka, wysyła ją do agentów i zwraca wynik klasyfikacji
    pass





















# class StateTwo(State):
#     async def run(self):
async def get_commander_info(obj):
    # funkcja pobiera informacje o aktualnym agencie dowodzacym i zwraca jego jid, lub None jak nie istnieje
    commander_jid = None
    await hf.send_to_all(obj, ac.CONTROL, ac.TO_CMB, ac.WHO_IS_IN_COMMAND)

    msg = await obj.receive(timeout=2)  # oczekiwanie na odpowiedź agenta dowodzącego
    if msg and msg.body[:len(ac.WHO_IS_IN_COMMAND_RESPONSE)] == ac.WHO_IS_IN_COMMAND_RESPONSE:
        commander_jid = msg.sender
        # print(commander_jid)

    return commander_jid


### Nie użyte
async def is_commander_alive(obj, commander_jid):
    # Funkcja zwraca False jak commander nie odpowiada i True jak commander żyje
    alive = False

    msg_to_send = hf.prep_msg(commander_jid, ac.CONTROL, ac.TO_CMB, ac.WHO_IS_IN_COMMAND)
    await obj.send(msg_to_send)

    msg = await obj.receive(timeout=1)
    if msg and msg.body[:len(ac.WHO_IS_IN_COMMAND_RESPONSE)] == ac.WHO_IS_IN_COMMAND_RESPONSE:
        alive = True

    return alive

    #     msg_to_send = hf.prep_msg(msg.sender, ac.CONTROL, ac.TO_FSM,
    #                               ac.WHO_IS_IN_COMMAND_RESPONSE + "Agent {} is in command.".format(
    #                                   obj.agent.jid))
    #
    # # control, to cmb, mutliple commanders
    # async def send_to_all(obj, meta_key, meta_value, msg_body):
    #     for k, v in ac.agents_dict.items():
    #         if str(v['jid']) != str(obj.agent.jid):
    #             msg_to_send = prep_msg(v['jid'], meta_key, meta_value, msg_body)
    #             # print("Agent {} , message to {} has been sent.".format(self.agent.jid, v['jid']))
    #             await obj.send(msg_to_send)
    #
    #
    #
    #     while True:
    #         msg = await obj.receive(timeout=1)
    #         if msg and msg.body == ac.WHO_IS_IN_COMMAND:
    #             msg_to_send = hf.prep_msg(msg.sender, ac.CONTROL, ac.TO_FSM,
    #                                       ac.WHO_IS_IN_COMMAND_RESPONSE + "Agent {} is in command.".format(
    #                                           obj.agent.jid))
    #             await obj.send(msg_to_send)
    #         # To ewentualnie do zmiany ( zabezpiecza przypadek, gdyby mimo
    #         # istnienia agenta dowodzącego, pojawił się nowy agent dowodzący)
    #         if msg and msg.body == ac.MULTIPLE_COMMANDERS:
    #             msg_to_send = hf.prep_msg(msg.sender, ac.CONTROL, ac.TO_CMB,
    #                                       ac.WHO_IS_IN_COMMAND_RESPONSE + "Agent {} is in command.".format(
    #                                           obj.agent.jid))
    #             await obj.send(msg_to_send)

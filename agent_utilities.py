import agent_config as ac
import help_functions as hf
import asyncio
import os
import cnn
import shutil

## async def setup(self):
def initialize(obj, template1, template2, fsmbehav, state0, state1, state2):
    # inicjalizacja nowych agentów - dodanie zachowań wraz z template'ami
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


async def is_commander_alive(obj):
    # Funkcja sprawdza czy agent dowodzący istnieje - jak nie to zostaje przeprowadzone głosowanie na nowego agenta

    await asyncio.sleep(3)  # Time for new commander for initializing
    commander_jid = await get_commander_info(obj)

    if commander_jid == None:
        # nie testowany kod - ale program skrajnie rzadko wchodzi do do tego case'a. Przetestować
        print("Agent {} cannot contact with commander".format(obj.agent.jid))
        print("Voting time! Started by Agent {}".format(obj.agent.jid))
        voting_resoult = await hf.start_voting(obj, ac.CONTROL, ac.TO_FSM, ac.AGENT_VOTING)
        if voting_resoult:
            await hf.promotion_to_commanding(obj)
            obj.set_next_state(ac.STATE_ONE)
        else:
            obj.set_next_state(ac.STATE_TWO)

    return commander_jid



async def wait_for_file_and_recognize(obj):
    # Funkcja co 3 sec sprawdza czy w folderze ac.RECOGNIZE_FOLDER pojawiły się jakieś pliki do rozpoznania. Jeśli
    # tak, to sprawdza dostepnych agentów, wysyła im zdjęcie do rozpoznania, zbiera odpowiedzi i drukuje wynik
    # (uwzględniajac własny wynik klasyfikacji)

    # Wstępne opóźnienie - oczekiwanie na agentów przed rozpoczęciem zadania klasyfikacji
    await asyncio.sleep(10)

    while True:
        # Latka - Symulacja śmierci agenta
        await hf.simulate_death(obj)

        await asyncio.sleep(3)
        while len(os.listdir(ac.RECOGNIZE_FOLDER)) != 0:
            print("Agent {} wykryl obrazek do rozpoznania!".format(obj.agent.jid))
            # Znajdz zywych agentow
            alive_agent_list = await get_alive_agents(obj)
            alive_agents_number = len(alive_agent_list) + 1
            # print(alive_agent_list)

            # Pobierz 1 lub wiecej zdjec (sciezek do zdjec)
            images_to_recognize = hf.get_file_paths(ac.RECOGNIZE_FOLDER)
            print("Agent {} poznal co trzeba rozpoznac: {}.".format(obj.agent.jid, images_to_recognize))
            # Wyslij je agentom do rozpoznania
            for image_to_recognize in images_to_recognize:
                print("Agent {} wysyla obrazek 1 {}.".format(obj.agent.jid, image_to_recognize))
                classif_list = []
                not_classif_list = []

                # glos agenta dowodzacego
                commander_prediction = cnn.predict_one(obj.agent.model, image_to_recognize)

                if commander_prediction[:len(ac.CLASSIFIED)] == ac.CLASSIFIED:
                    feature = commander_prediction[len(ac.CLASSIFIED):]
                    classif_list.append(str(feature))
                else:
                    feature = commander_prediction[len(ac.NOT_CLASSIFIED):]
                    not_classif_list.append(str(feature))

                # wyslanie zdjecia do wszystkich agentow

                msg_body = ac.CLASSIFY_OBJECT + image_to_recognize
                for alive_agent in alive_agent_list:
                    msg_to_send = hf.prep_msg(alive_agent, ac.CONTROL, ac.TO_FSM, msg_body)
                    await obj.send(msg_to_send)

                # zbieranie odpowiedzi po każdym z obrazków z osobna żeby sie nie pomyliło

                while True:
                    classification_end = True
                    msg = await obj.receive(timeout=1)  # waiting 1 sec from last gathered recognison

                    if msg and msg.body[:len(ac.CLASSIFIED)] == ac.CLASSIFIED:
                        feature = msg.body[len(ac.CLASSIFIED):]
                        classif_list.append(str(feature))
                        classification_end = False

                    if msg and msg.body[:len(ac.NOT_CLASSIFIED)] == ac.NOT_CLASSIFIED:
                        feature = msg.body[len(ac.NOT_CLASSIFIED):]
                        not_classif_list.append(str(feature))
                        classification_end = False

                    if classification_end:
                        break

                classification_results = hf.ballot_box(classif_list, not_classif_list)

                hf.log_results(obj.agent.jid, alive_agents_number, image_to_recognize, classification_results)

                ###
                # avoid overwriting files in case they have indentical name but not indetical content
                # check if file with similar name exists in recognized folder and rename by index suffix
                hypotetic_filename = os.path.join(ac.RECOGNIZED_FOLDER, os.path.basename(image_to_recognize))                
                if(os.path.isfile(hypotetic_filename)):
                    image_to_recognize_filename = os.path.basename(image_to_recognize)
                    old_name = os.path.splitext(image_to_recognize_filename)[0]
                    file_extension = os.path.splitext(image_to_recognize_filename)[1]
                    new_name = ""  
                    i = 1                  
                    while(os.path.isfile(hypotetic_filename)):
                        i += 1
                        if (i > 10):
                            print ("too much copies in recognized folder")
                            new_name = ""
                            break
                        new_name = old_name + "_" +str(i) + file_extension 
                        hypotetic_filename = os.path.join(os.path.dirname(hypotetic_filename), new_name)  
                    if (new_name != ""):    
                        os.rename(image_to_recognize, os.path.join(os.path.dirname(image_to_recognize), new_name))
                        shutil.move(image_to_recognize, ac.RECOGNIZED_FOLDER) # copy file properly renamed to avoid duplicates
                else:
                    shutil.move(image_to_recognize, ac.RECOGNIZED_FOLDER)

async def agent_task_manager(obj, commander_jid):
    # Funkcja obsługująca zachowania i odpowiedzi agentów w zależności od odebranych odpowiedzi

    # Przygotowanie okresowo wysyłanej wiadomości sprawdzajacej stan życia agenta dowodzącego
    msg_health_check = hf.prep_msg(commander_jid, ac.CONTROL, ac.TO_CMB, ac.WHO_IS_IN_COMMAND)

    alive_check = True

    while True:
        # pętla głowna zwykłego robotnika - agent oczekuje na wiadomości i odpowiednio reaguje
        # Latka - Symulacja śmierci agenta
        await hf.simulate_death(obj)

        send_health_check = True

        # print("Agent {} at the start of state2 loop".format(self.agent.jid))

        # oczekiwanie na wiadomość
        msg = await obj.receive(timeout=5)
        if msg and msg.sender == commander_jid and msg.body[:len(
                ac.WHO_IS_IN_COMMAND_RESPONSE)] == ac.WHO_IS_IN_COMMAND_RESPONSE:
            print("Agent {} received msg_health_check".format(obj.agent.jid))
            send_health_check = False  # te dwie flagi zapobiegają nadmiarowemu wykon. alive_check na commanderze
            alive_check = True  # powinny byc w każdym if statemencie

        if msg and msg.sender == commander_jid and msg.body[:len(ac.CLASSIFY_OBJECT)] == ac.CLASSIFY_OBJECT:
            img = msg.body[len(ac.CLASSIFY_OBJECT):]
            print("Agent {} received {} for classification from {} ".format(obj.agent.jid, img, commander_jid))

            # rozpoznawanie i odsyłanie odpowiedzi
            single_prediction = cnn.predict_one(obj.agent.model, img)

            msg_ready = hf.prep_msg(commander_jid, ac.CONTROL, ac.TO_FSM, single_prediction)
            await obj.send(msg_ready)

            send_health_check = False
            alive_check = True

        if msg and msg.sender == commander_jid and msg.body[:len(ac.WHO_IS_READY_TO_SERVE)] == ac.WHO_IS_READY_TO_SERVE:
            msg_ready = hf.prep_msg(commander_jid, ac.CONTROL, ac.TO_FSM, ac.ALIVE_SLAVE)
            await obj.send(msg_ready)

            # Kod odpowiadający agentowi dowodzacemu, że jest gotowy do służby

            send_health_check = False
            alive_check = True

        if not alive_check:
            print("Voting time! Started by Agent {}".format(obj.agent.jid))
            voting_resoult = await hf.start_voting(obj, ac.CONTROL, ac.TO_FSM, ac.AGENT_VOTING)
            # await asyncio.sleep(3)  # wait for voting result
            break

        if send_health_check:
            print("Agent {} prepared msg_health_check".format(obj.agent.jid))
            await obj.send(msg_health_check)  # wiadomość wysyłana jest co timeout z początku pętli
            print("Agent {} send msg_health_check".format(obj.agent.jid))

            alive_check = False

    if voting_resoult:
        await hf.promotion_to_commanding(obj)
        obj.set_next_state(ac.STATE_ONE)
    else:
        obj.set_next_state(ac.STATE_TWO)


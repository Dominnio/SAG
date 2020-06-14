import agent_config as ac
from spade.message import Message
from spade.template import Template
import random
import asyncio
import os
import glob
import re
from collections import Counter


# f = []
# for (dirpath, dirnames, filenames) in os.walk(r'..\SAG_agents\data_to_recognize\recognize'):
#     f.extend(filenames)
#     break
# print(f)

def get_file_paths(d):
    return glob.glob(os.path.join(d, '*'))



# control, to cmb, mutliple commanders
async def send_to_all(obj, meta_key, meta_value, msg_body):
    for k, v in ac.agents_dict.items():
        if str(v['jid']) != str(obj.agent.jid):
            msg_to_send = prep_msg(v['jid'], meta_key, meta_value, msg_body)
            # print("Agent {} , message to {} has been sent.".format(self.agent.jid, v['jid']))
            await obj.send(msg_to_send)


def prep_msg(to, meta_key, meta_value, msg_body):
    msg_to_send = Message(to=str(to))
    msg_to_send.set_metadata(meta_key, meta_value)
    msg_to_send.body = msg_body

    return msg_to_send


def make_vote():
    return '{' + str(random.uniform(0, 10)) + '}'


def get_vote(vote):
    return float(vote[vote.find("{") + 1:vote.find("}")])


def did_you_win(all_votes, your_vote):
    if len(all_votes) == 0 or float(max(all_votes)) <= float(your_vote):
        return True
    else:
        return False


# Tutaj ktoś mógłby się zastanowić, że co jak będą 2 wyniki takie same?
# Będzie 2 dowodzących? A więc przy 100 000 agentów prawdopodobieństwo
# że 2 z nich będzie miało taki sam numer to 0.0000000001% . A nawet jeśli
# to każdy nowo powstały agent dowodzący upewnia się że jest jedynym agentem dowodzącym,
# wysyłając wiadomość MULTIPLE_COMMANDERS . W razie dubla głosowanie przeprowadzane jest jeszcze raz


async def start_voting(obj, meta_key, meta_value, type_of_voting):
    # funkcja do przeprowadzania glosowania. Ogolnie w programie wyrozniam 2 typy glosowan:
    # miedzy zwyklymi agentami i zabezpieczajace między kilkoma agentami dowodzacymi.

    print("Agent {} is voting!".format(obj.agent.jid))
    my_vote = make_vote()
    all_votes = []

    msg_body = type_of_voting + my_vote + " Vote of Agent {}.".format(obj.agent.jid)
    await send_to_all(obj, meta_key, meta_value, msg_body)

    while True:
        voting_end = True
        msg = await obj.receive(timeout=1)  # waiting 1 sec from last gathered vote
        if msg and msg.body[:len(type_of_voting)] == type_of_voting:
            all_votes.append(get_vote(msg.body))  # zbieranie glosow
            # print(all_votes)
            voting_end = False
        if voting_end:
            break
    if did_you_win(all_votes, get_vote(my_vote)):
        print("Agent {} won! He will become the new Commander!".format(obj.agent.jid))
        return True
    else:
        return False


async def promotion_to_commanding(obj):
    # Funkcja ustanawiajaca nowego agenta dowodzącego - po ustaleniu ze jest tylko jeden agent dowodzący
    # ponizszy kod zostanie wywołany. Agent z pomocą tej funkcji wysyła sam sobie wiadomosc, awansując na agenta
    # dowodzacego. Agent powinien przejść do stanu pierwszego

    msg_to_send = prep_msg(obj.agent.jid, ac.CONTROL, ac.TO_CMB, "Taking the command.")
    print("Agent {} , sending promotion note to himself.".format(obj.agent.jid))
    await obj.send(msg_to_send)

    # obj.set_next_state(ac.STATE_ONE)


async def simulate_death(obj):
    # Okazuje się, że agenci oraz behaviour's SPAD'a są nieśmiertelne i nie da się ich zabić. Poniższa łatka ma
    # za zadanie zatrzymać wykonywanie takiego agenta
    if obj.is_killed():
        print("Agent {} was killed?: {}".format(obj.agent.jid, obj.is_killed()))
        while True:
            await asyncio.sleep(1000)

    # if not obj.is_killed():
    #     print("Agent {} is killed".format(obj.agent.jid))
    #     while True:
    #         time.sleep(100)
    #         #print("Agent {} dying".format(obj.agent.jid))
    #         pass

def get_contacts_from_roster(roster):
    # funkcja do wydobywania kontaktow ze SPAD'e w formie listy
    contact_list = []
    con_str = str(roster)
    indexes = [m.start() for m in re.finditer('t=\'(.+?)\',', con_str)]
    for x in indexes:
       tmp = re.search('\'(.+?)\'', con_str[x:x + 20]).group(0)
       tmp = tmp[1:-1] + '@' + ac.server_name
       contact_list.append(tmp)
    return contact_list

def ballot_box(classif_list,not_classif_list):
    # funkcja pobiera głosy za, przeciw i zwraca słownik z wynikami klasyfikacji.
    # Jesli wynik jest negatywny np. horse : -3, to znaczy ze agenci twierdza ze na obrazku nie ma konia.
    # Wynik 0 oznacza ze glosow za i przeciw bylo tyle samo
    classif_list_counter = Counter(classif_list)
    not_classif_list_counter = Counter(not_classif_list)
    classif_list_counter.subtract(not_classif_list_counter)

    return dict(classif_list_counter)

#
# a = ['dog','dog','cat','chicken']
# b = ['dog','cat','horse','chicken','chicken']
#
# print(ballot_box(a,b))

#
# print("classif_lits : {}".format(classif_list))
# print("not_classif_list : {}".format(not_classif_list))
#
# count_clas = Counter(classif_list)
# count_not_clas = Counter(not_classif_list)
#
# # dict_count_clas = count_clas.items()
# # ditc_count_not_clas = count_not_clas.items()
# #
# # # for k, v in dict_count_clas:
#
# print("classif_lits Counter: {}".format(count_clas))
# print("not_classif_list Counter: {}".format(count_not_clas))
#
# count_clas.subtract(count_not_clas)
#
# print("Result: {}".format(count_clas))



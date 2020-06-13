import agent_config as ac
from spade.message import Message
from spade.template import Template
import random
import asyncio


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

# all_votes = []
# all_votes.append(get_vote(make_vote()))
# Trump_vote = 11
# print(all_votes)
# print(all_votes)
# print(did_you_win(all_votes, Trump_vote))

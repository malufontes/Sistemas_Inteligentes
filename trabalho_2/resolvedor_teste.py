from aiohttp_jinja2 import template
from jinja2 import FileSystemBytecodeCache
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.behaviour import OneShotBehaviour
from spade.template import Template
from spade.message import Message
from spade.behaviour import FSMBehaviour, State
from colorama import Fore
import random
import time

INITIAL_STATE = "ASK_TIPOFUNCAO"
SELECTGRAU_STATE = "SELECT_GRAU"
GRAU1_STATE = "GRAU_1"
GRAU2_STATE = "GRAU_2"
GRAU3_STATE = "GRAU_3"

class Resolvedor(Agent):
    async def setup(self):
        print("Agente Resolvedor {} instanciado".format(str(self.jid)))

        # definindo o tipo de mensagem que será recebida pelo resolvedor
        template = Template()
        template.set_metadata("performative", "inform") # vai recer uma msg do tipo "inform"

        # definindo o tipo de comportamento
        comp = comportamentos()

        # adicionando os possíveis subcomportamentos (States)
        comp.add_state(name=INITIAL_STATE, state=ask_tipofuncao(), initial=True)
        comp.add_state(name=SELECTGRAU_STATE, state=select_tipofuncao())
        comp.add_state(name=GRAU1_STATE, state=resolvedor_1grau())
        comp.add_state(name=GRAU2_STATE, state=resolvedor_2grau())
        comp.add_state(name=GRAU3_STATE, state=resolvedor_3grau())

        # adicionando as possíveis transições de estado
        comp.add_transition(source=INITIAL_STATE, dest=SELECTGRAU_STATE)
        comp.add_transition(source=SELECTGRAU_STATE, dest=GRAU1_STATE)
        comp.add_transition(source=SELECTGRAU_STATE, dest=GRAU2_STATE)
        comp.add_transition(source=SELECTGRAU_STATE, dest=GRAU3_STATE)

        # adicionando os comportamentos ao agente
        self.add_behaviour(comp,template)


#comportamento principal, ele que vai gerenciar os subcomportamentos (States)
class comportamentos(FSMBehaviour):
    async def on_start(self):
        print()
        
    async def on_end(self):
        print()
        await self.agent.stop() 

class ask_tipofuncao(State):
    async def run(self):
        print()

class select_tipofuncao(State):
    async def run(self):
        print()

class resolvedor_1grau(State):
    async def run(self):
        print()

class resolvedor_2grau(State):
    async def run(self):
        print()

class resolvedor_3grau(State):
    async def run(self):
        print()

receiver_jid = "maluf@jix.im"
receiver_password = "RelouSI"
sender_jid = "andre@jix.im"
sender_password = "RelouSI"

resolvedor = Resolvedor(receiver_jid, receiver_password)
future = resolvedor.start()
future.result()

while resolvedor.is_alive():
    try:
        time.sleep(1)
    except:
        print(Fore.WHITE + "Keyboard  Interrupt")
        resolvedor.stop()
        break
print(Fore.WHITE + "Resolvedor finalizado!") 
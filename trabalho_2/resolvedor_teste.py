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
        comp.add_state(name=GRAU1_STATE, state=resolvedor_1grau())
        comp.add_state(name=GRAU2_STATE, state=resolvedor_2grau())
        comp.add_state(name=GRAU3_STATE, state=resolvedor_3grau())

        # adicionando as possíveis transições de estado
        comp.add_transition(source=INITIAL_STATE, dest=GRAU1_STATE)
        comp.add_transition(source=INITIAL_STATE, dest=GRAU2_STATE)
        comp.add_transition(source=INITIAL_STATE, dest=GRAU3_STATE)

        # adicionando os comportamentos ao agente
        self.add_behaviour(comp,template)


#comportamento principal, ele que vai gerenciar os subcomportamentos (States)
class comportamentos(FSMBehaviour):
    async def on_start(self):
        print()
        
    async def on_end(self):
        print()
        await self.agent.stop() 

# perguntar para o Gerador qual o tipo de função que será utilizada
class ask_tipofuncao(State):
    async def run(self):
        print("Perguntando o tipo de função ...")

        # o Gerador (tipo_funcao()) recebe essa pergunta como "request"
        # logo, a msg é setada como "request"
        msg = Message(to=gerador_jid)
        msg.set_metadata("performative", "request")
        msg.body = "Qual o tipo da função?"             # nesse caso, não importa oq eu tÕ mandando só o tipo da msg 
                                                        # mas isso só pq o gerador não trata oq ele receber na tipo_funcao()
        await self.send(msg)
        print("... pergunta enviada")

        recebeu_resp = False
        while(not recebeu_resp):
            resp = await self.receive(timeout=10)
            if(resp):
                recebeu_resp = True
            else:
                print("Timeout -> ask_tipofuncao")

        # selecionando qual subcompotamento (state) será selecionado
        if(resp.body == "1grau"):
            print()
        else:
            if(resp.body == "2grau"):
                print()
            else:
                if(resp.body == "3grau"):
                    print()
                else:
                    print("resposta recebida inválida")

class resolvedor_1grau(State):
    async def run(self):
        print()

class resolvedor_2grau(State):
    async def run(self):
        print()

class resolvedor_3grau(State):
    async def run(self):
        print()

resolvedor_jid = "maluf@jix.im"
resolvedor_password = "RelouSI"
gerador_jid = "andre@jix.im"
gerador_password = "RelouSI"

resolvedor = Resolvedor(resolvedor_jid, resolvedor_password)
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
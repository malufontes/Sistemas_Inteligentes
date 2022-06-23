from aiohttp_jinja2 import template
from spade.agent import Agent
from spade.template import Template
from spade.message import Message
from spade.behaviour import FSMBehaviour, State
from colorama import Fore
import random
import time

INITIAL_STATE = "ASK_TIPOFUNCAO"
TESTE_EXTREMIDADESUP_STATE =  "TESTE_EXTREMIDADESUP"
TESTE_EXTREMIDADEINF_STATE =  "TESTE_EXTREMIDADEINF"
TESTE_RAIZ_STATE = "TESTE_RAIZ"
CHECAR_RESP_STATE = "CHECAR_RESP"

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
        comp.add_state(name=TESTE_EXTREMIDADEINF_STATE, state=teste_extremidade_superior())
        comp.add_state(name=TESTE_EXTREMIDADESUP_STATE, state=teste_extremidade_inferior())
        comp.add_state(name=TESTE_RAIZ_STATE, state=bisseccao())



        # adicionando as possíveis transições de estado
        # comp.add_transition(source=INITIAL_STATE, dest=ACHAR_RAIZ_STATE)

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
                print("Resposta recebida: " + resp.body)
            else:
                print("Timeout -> ask_tipofuncao")

        # selecionando qual subcompotamento (state) será selecionado
        if(resp.body == "1grau"):
            print("Resolvendo para função de 1 grau")
            self.set_next_state(TESTE_EXTREMIDADEINF_STATE)
        else:
            if(resp.body == "2grau"):
                print("Resolvendo para função de 2 grau")
                self.set_next_state(TESTE_EXTREMIDADEINF_STATE)
            else:
                if(resp.body == "3grau"):
                    print("Resolvendo para função de 3 grau")
                    self.set_next_state(TESTE_EXTREMIDADEINF_STATE)
                else:
                    print("resposta recebida inválida")

class teste_extremidade_inferior(State):
    async def run(self):
        print()

class teste_extremidade_superior(State):
    async def run(self):
        print()

class bisseccao(State):
    async def run(self):
        print("Dentro do resolvedor:")

        msg = Message(to=gerador_jid)
        msg.set_metadata("performative", "subscribe")
        tol = 0.1
        a = -1000
        b = 1000
        msg.body = str(a)
        await self.send(msg)
        res_a = await self.receive(timeout=5)
        fx_a = float(res_a.body)

        msg.body = str(b)
        await self.send(msg)
        res_b = await self.receive(timeout=5)
        fx_b = float(res_b.body)

        c = a
        fx_c = fx_a
        while (abs(fx_c) >= tol):
            c = int((a+b)/2)

            msg.body = str(c)
            await self.send(msg)
            res_c = await self.receive(timeout=5)
            fx_c = float(res_c.body)

            print(f"x={c}, fx={fx_c}")
            if (fx_c == 0.0):
                break
        
            msg.body = str(a)
            await self.send(msg)
            res_a = await self.receive(timeout=5)
            fx_a = float(res_a.body)

            if (fx_c * fx_a < 0):
                b = c
            else:
                a = c     


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
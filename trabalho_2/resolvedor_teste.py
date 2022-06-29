from aiohttp_jinja2 import template
from spade.agent import Agent
from spade.template import Template
from spade.message import Message
from spade.behaviour import FSMBehaviour, State
from colorama import Fore
import random
import time

INITIAL_STATE = "ASK_TIPOFUNCAO"
TESTE_EXTREMIDADEINF_STATE =  "TESTE_EXTREMIDADEINF"
TESTE_EXTREMIDADESUP_STATE =  "TESTE_EXTREMIDADESUP"
BISSECCAO_STATE = "BISSECCAO"
CHECAR_RESP_STATE = "CHECAR_RESP"
FINAL_STATE = "FINAL_STATE"

class Resolvedor(Agent):

    #definidos as extremidades do intervalo de possíveis raizes
    sup = 1000
    inf = -1000
    fsup = -1
    finf = -1
    aux = -1
    faux = -1
    checkpoint = 1001

    teste_superior = True
    teste_inferior = False
    bisseccao_first = True

    async def setup(self):
        print("Agente Resolvedor {} instanciado".format(str(self.jid)))

        # definindo o tipo de mensagem que será recebida pelo resolvedor
        template = Template()
        template.set_metadata("performative", "inform") # vai recer uma msg do tipo "inform"

        # definindo o tipo de comportamento
        comp = comportamentos()

        # adicionando os possíveis subcomportamentos (States)
        comp.add_state(name=INITIAL_STATE, state=ask_tipofuncao(), initial=True)
        comp.add_state(name=TESTE_EXTREMIDADEINF_STATE, state=teste_extremidade_inferior())
        comp.add_state(name=TESTE_EXTREMIDADESUP_STATE, state=teste_extremidade_superior())
        comp.add_state(name=BISSECCAO_STATE, state=bisseccao())
        comp.add_state(name=CHECAR_RESP_STATE, state=checar_resp())
        comp.add_state(name=FINAL_STATE, state=final())



        # adicionando as possíveis transições de estado
        comp.add_transition(source=INITIAL_STATE, dest=TESTE_EXTREMIDADEINF_STATE)
        comp.add_transition(source=TESTE_EXTREMIDADEINF_STATE, dest=CHECAR_RESP_STATE)
        comp.add_transition(source=CHECAR_RESP_STATE, dest=TESTE_EXTREMIDADESUP_STATE)
        comp.add_transition(source=TESTE_EXTREMIDADESUP_STATE, dest=CHECAR_RESP_STATE)
        comp.add_transition(source=CHECAR_RESP_STATE, dest=BISSECCAO_STATE)
        comp.add_transition(source=BISSECCAO_STATE, dest=CHECAR_RESP_STATE)
        comp.add_transition(source=CHECAR_RESP_STATE, dest=FINAL_STATE)

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

class checar_resp(State):
    async def run(self):
        resp = await self.receive(timeout=5)
        if resp:
            if int(resp.body) == 0:
                print("Solução encontrada!")
                self.set_next_state(FINAL_STATE)
                #ir para o estado final
            else:
                if(Resolvedor.teste_superior and Resolvedor.teste_inferior):
                    Resolvedor.faux = float(resp.body)

                if not Resolvedor.teste_superior:
                    Resolvedor.fsup = float(resp.body)
                    self.set_next_state(BISSECCAO_STATE)
                    Resolvedor.teste_superior = True
                if not Resolvedor.teste_inferior:
                    Resolvedor.finf = float(resp.body)
                    self.set_next_state(TESTE_EXTREMIDADESUP_STATE)
                    Resolvedor.teste_inferior = True
                    Resolvedor.teste_superior = False


        else:
            print("Timeout -> checar_resp")

class teste_extremidade_inferior(State):
    async def run(self):
        print("Teste extremidade inferior")

        msg = Message(to=gerador_jid)
        msg.set_metadata("performative", "subscribe")
        msg.body = str(Resolvedor.inf)
        await self.send(msg)
        self.set_next_state(CHECAR_RESP_STATE)

class teste_extremidade_superior(State):
    async def run(self):
        print("Teste extremidade superior")

        msg = Message(to=gerador_jid)
        msg.set_metadata("performative", "subscribe")
        msg.body = str(Resolvedor.sup)
        await self.send(msg)
        self.set_next_state(CHECAR_RESP_STATE)

class bisseccao(State):
    async def run(self):
        print("Bisseccao")
        print(Resolvedor.bisseccao_first)


        if Resolvedor.bisseccao_first:  
            print("Entrou aqui")
            Resolvedor.aux = Resolvedor.inf + (Resolvedor.sup - Resolvedor.inf)/2
            print(Resolvedor.aux)
            msg = Message(to=gerador_jid)
            msg.set_metadata("performative", "subscribe")
            msg.body = str(int(Resolvedor.aux))
            await self.send(msg)
            Resolvedor.bisseccao_first = False
        else:
            if(Resolvedor.finf*Resolvedor.faux>0):
                Resolvedor.inf = Resolvedor.aux
                print("Resolvedor inf")
                print(resolvedor.inf)
                Resolvedor.finf = Resolvedor.faux
            else:
                print("ENTROUUU ELSE")
                Resolvedor.sup = Resolvedor.aux

            print(Resolvedor.sup - Resolvedor.inf)

            Resolvedor.aux = Resolvedor.inf + (Resolvedor.sup - Resolvedor.inf)/2

            if (Resolvedor.aux == Resolvedor.checkpoint):
                print("Erro")
                
            print(resolvedor.aux)
            Resolvedor.checkpoint = Resolvedor.aux
            msg = Message(to=gerador_jid)
            msg.set_metadata("performative", "subscribe")
            msg.body = str(int(Resolvedor.aux))
            await self.send(msg)

            if (Resolvedor.checkpoint > 999.5):
                Resolvedor.sup = -1000
                Resolvedor.inf = -1
                Resolvedor.fsup = -1
                Resolvedor.finf = -1
                Resolvedor.aux = -1000
                Resolvedor.faux = -1000
                Resolvedor.checkpoint = -999.4

                
            if (Resolvedor.checkpoint < -999.5):
                print("entrou AA")
                Resolvedor.sup = 1000
                Resolvedor.inf = 1
                Resolvedor.fsup = 1000
                Resolvedor.finf = 1
                Resolvedor.aux = 1000
                Resolvedor.faux = 1000
                Resolvedor.checkpoint = 999.4
                
        self.set_next_state(CHECAR_RESP_STATE)


class final(State):
    async def run(self):
        print("é isso, chegamos ao final meus amigos")


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
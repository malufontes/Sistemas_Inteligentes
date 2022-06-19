from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from spade.message import Message
import random
import time

class Gerador(Agent):
    #definindo o grau da função criada pelo Gerador
    grau = random.randint(1,3)
    # coloquei isso aq só pq tava testando a de primeiro grau, lembrar de apagar dps
    grau = 1

    # gerando as funções
    # lembrar de conferir se as funções tem raíz (ela precisa ter algum x que o y dê 0)
    if (grau == 1):
        x = random.randint(-1000,1000)
        a=0
        while a == 0:
            a = random.randint(-100,100)
        y = -1 * (a*x)
    # fiz essa parte do segundo grau cagada só pra dar ideia do q fazer, fique a vontade pra melhorar
    if (grau == 2):
        a=0
        while a == 0:
            a = random.randint(-100,100)
        b=0
        while b == 0:
            b = random.randint(-100,100)
        c=0
        while c == 0:
            c = random.randint(-100,100)
    if (grau == 3):
        print()
   
    class funcao_1grau(CyclicBehaviour):
        async def run(self):
            res = await self.receive(timeout=5)
            if res:
                x = float(res.body)
                x = float( Gerador.a*x + Gerador.y )
                print("Enviou para " + str(res.sender) + " f(",res.body,")= ",x,"=>",int(x))
                msg = Message(to=str(res.sender)) 
                msg.set_metadata("performative", "inform")  
                msg.body = str(int(x))
                await self.send(msg)
    
    class funcao_2grau(CyclicBehaviour):
        async def run(self):
            res = await self.receive(timeout=5)
            if res:
                x = float(res.body)

                # tem que substituir o x (que o Resolvedor manda) pelo x na função que o
                # gerador gera pra desolver o y resultante disso pro Resolvedor
                # só seguir o exemplo da função de primeiro grau

                msg = Message(to=str(res.sender)) 
                msg.set_metadata("performative", "inform")  
                msg.body = str(int(x))
                await self.send(msg)

    class funcao_3grau(CyclicBehaviour):
        async def run(self):
            res = await self.receive(timeout=5)
            if res:
                x = float(res.body)

                # tem que substituir o x (que o Resolvedor manda) pelo x na função que o
                # gerador gera pra desolver o y resultante disso pro Resolvedor
                # só seguir o exemplo da função de primeiro grau

                msg = Message(to=str(res.sender)) 
                msg.set_metadata("performative", "inform")  
                msg.body = str(int(x))
                await self.send(msg)
   
    class tipo_funcao(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                msg = Message(to=str(msg.sender))
                msg.set_metadata("performative", "inform")
                msg.body = "1grau" 
                await self.send(msg)
                print("Respondeu para " + str(msg.sender) + " com " + msg.body)
                

    async def setup(self):
        print("Hello World! I'm agent {}".format(str(self.jid)))
        
        t = Template()
        t.set_metadata("performative","subscribe")

        if(Gerador.grau == 1):
            tf = self.funcao_1grau()
            print("Funcao de 1o grau: ", Gerador.x)
            print("Funcao: ", Gerador.a, "x + (", Gerador.y, ")")
            self.add_behaviour(tf,t)
        if(Gerador.grau == 2):
            tf = self.funcao_2grau()
            print("Funcao de 2o grau: ")
            self.add_behaviour(tf,t)
        if(Gerador.grau == 3):
            tf = self.funcao_3grau()
            print("Funcao de 3o grau: ")
            self.add_behaviour(tf,t)

        ft = self.tipo_funcao()
        template = Template()
        template.set_metadata("performative", "request")
        self.add_behaviour(ft, template)

gerador = Gerador("andre@jix.im", "RelouSI")
#gerador.web.start(hostname="127.0.0.1", port="10000")
future = gerador.start()
future.result()

while gerador.is_alive():
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        gerador.stop()
        break
print("Agente encerrou!")
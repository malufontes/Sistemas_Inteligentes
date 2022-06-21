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
    grau = 3
    coefs = {}
    # gerando as funções
    # lembrar de conferir se as funções tem raíz (ela precisa ter algum x que o y dê 0)
    if (grau == 1):
        x = random.randint(-1000,1000)
        # coloquei isso aq só pq tava testando a de primeiro grau, lembrar de apagar dps
        x = -997
        a=0
        while a == 0:
            a = random.randint(-100,100)
        y = -1 * (a*x)
    # fiz essa parte do segundo grau cagada só pra dar ideia do q fazer, fique a vontade pra melhorar
    # lembrar de conferir se as funções tem raíz (ela precisa ter algum x que o y dê 0)
    if (grau == 2):
        x1 = random.randint(-500, 500)
        x2 = random.randint(-500, 500)
        c = 0
        while c == 0:
         c = random.randint(-100, 100)
    
        b = -(x1 + x2) * c
        a =  (x1 * x2) * c

        coefs = {"a": a, "b": b, "c": c}

        print(f"Funcao de 2o grau. Raizes: x1={x1}, x2={x2}")
        print(f"Funcao: {c}x^2 + ({b})x + ({a})")
        
    if (grau == 3):
        x1 = random.randint(-500, 500)
        x2 = random.randint(-500, 500)
        x3 = random.randint(-500, 500)
    
        d = 0
        while d == 0:
          d = random.randint(-100, 100)

        c = -(x1 + x2 + x3) * d
        b = (x1*x2 + x2*x3 + x1*x3) * d
        a = -(x1 * x2 * x3) * d

        coefs = {"a": a, "b": b, "c": c, "d": d}

        print(f"Funcao de 3o grau. Raizes: x1={x1}, x2={x2}, x3={x3}")
        print(f"Funcao: {d}x^3 + ({c})x^2 + ({b})x + ({a})")
   
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
                fx = self.TestaX(x, self.coefs)
                msg = Message(to=str(res.sender))
                msg.set_metadata("performative", "inform")
                msg.body = str(fx)
                await self.send(msg)

    class funcao_3grau(CyclicBehaviour):
        async def run(self):
            res = await self.receive(timeout=5)
            if res:
                x = float(res.body)
                fx = self.TestaX(x, self.coefs)
                msg = Message(to=str(res.sender))
                msg.set_metadata("performative", "inform")
                msg.body = str(fx)
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
#essa parte aí do host pode ficar comentada, n serve pra nada nesse código
#e tenho medo de dar xabu se descomentar
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
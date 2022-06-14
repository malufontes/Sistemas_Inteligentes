import time
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

class Sender(Agent):
    class enviar_msg(CyclicBehaviour):
        async def run(self):
            print("run -> enviar_msg")

            msg = Message(to="andre@jix.im")     # Instantiate the message
            msg.set_metadata("performative", "inform")  # Set the "inform" FIPA performative
            msg.body = "Oi sumida rs"                    # Set the message content

            await self.send(msg)
            print("mensagem enviada!")

        async def on_end(self):
            await self.agent.stop()

    async def setup(self):
        print("Sender inicializado")
        b = self.enviar_msg()
        self.add_behaviour(b)

class Receiver(Agent):
    class receber_msg(CyclicBehaviour):
        async def run(self):
            print("run -> receber_msg")

            msg = await self.receive(timeout = 10)
            if (msg):
                print("msg recebida: " + msg.body)
            else:
                print("timeout")
        
        async def on_end(self):
            await self.agent.stop()

    async def setup(self):
        print("Receiver inicializado")
        b = self.receber_msg()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)

senderAgent = Sender("andre@jix.im", "RelouSI")
receiverAgent = Receiver("maluf@jix.im", "RelouSI")

future = senderAgent.start()
future.result()
receiverAgent.start()

while receiverAgent.is_alive():
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        senderAgent.stop()
        receiverAgent.stop()
print("Agentes assassinados! ;)")





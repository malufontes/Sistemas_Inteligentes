import time
from spade import quit_spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import colorama
from colorama import Fore


class Receiver(Agent):
    class receber_msg(CyclicBehaviour):
        async def run(self):
            # print(Fore.BLUE +"run -> receber_msg")

            msg = await self.receive(timeout = 10)
            if (msg):
                print(Fore.BLUE +"Recebido: " + msg.body)

                msg2 = Message(to="andre@jix.im")     # Instantiate the message
                msg2.set_metadata("performative", "request")  # Set the "inform" FIPA performative
                msg2.body = "Mais ou menos"                    # Set the message content

                await self.send(msg2)
                print(Fore.BLUE + "Enviado: " + msg2.body)
            else:
                print(Fore.BLUE +"timeout")
        
        async def on_end(self):
            await self.agent.stop()

    async def setup(self):
        print(Fore.BLUE +"****** Receiver inicializado")
        b = self.receber_msg()
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(b, template)



receiver_jid = "maluf@jix.im"
receiver_password = "RelouSI"
sender_jid = "andre@jix.im"
sender_password = "RelouSI"

receiverAgent = Receiver(receiver_jid, receiver_password)
receiverAgent.start()
future = receiverAgent.start()
future.result()


while receiverAgent.is_alive():
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        print(Fore.WHITE +"Keyboard Interrupt")
        receiverAgent.stop()
print(Fore.WHITE +"Agentes assassinados! ;)")
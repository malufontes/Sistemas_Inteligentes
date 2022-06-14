import time
from spade import quit_spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import colorama
from colorama import Fore


class Sender(Agent):
    class enviar_msg(CyclicBehaviour):
        async def run(self):
            # print(Fore.WHITE + "run -> enviar_msg")

            msg = Message(to="maluf@jix.im")             # Instantiate the message
            msg.set_metadata("performative", "inform")   # Set the "inform" FIPA performative
            msg.body = "Oi, tudo bem?"                    # Set the message content

            await self.send(msg)
            print(Fore.RED + "Enviado: " + msg.body)

        async def on_end(self):
            await self.agent.stop()

    class sendback_msg(CyclicBehaviour):
        async def run(self):
            # print(Fore.RED +"run -> sendback_msg")

            msg = await self.receive(timeout=10)
            if msg:
                # msg = Message(to="maluf@jix.im")     # Instantiate the message
                # msg.set_metadata("performative", "request")  # Set the "inform" FIPA performative
                # msg.body = "Bora!"                    # Set the message content

                # await self.send(msg)
                # print("mensagem respondida!")
                print(Fore.RED + "Recebido: " + msg.body)
            else:
                print(Fore.WHITE + "timeout")


    async def setup(self):
        print(Fore.RED +"******** Sender inicializado")
        b = self.enviar_msg()
        self.add_behaviour(b)

        c = self.sendback_msg()
        template = Template()
        template.set_metadata("performative", "request")
        self.add_behaviour(c, template)



receiver_jid = "maluf@jix.im"
receiver_password = "RelouSI"
sender_jid = "andre@jix.im"
sender_password = "RelouSI"


senderAgent = Sender(sender_jid, sender_password)
future = senderAgent.start()
future.result()


while senderAgent.is_alive():
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        print(Fore.WHITE +"Keyboard Interrupt")
        senderAgent.stop()
print(Fore.WHITE +"Agentes assassinados! ;)")
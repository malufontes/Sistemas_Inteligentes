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
            msg.body = "Oi sumida rs"                    # Set the message content

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


class Receiver(Agent):
    class receber_msg(CyclicBehaviour):
        async def run(self):
            # print(Fore.BLUE +"run -> receber_msg")

            msg = await self.receive(timeout = 10)
            if (msg):
                print(Fore.BLUE +"Recebido: " + msg.body)

                msg2 = Message(to="andre@jix.im")     # Instantiate the message
                msg2.set_metadata("performative", "request")  # Set the "inform" FIPA performative
                msg2.body = "Bora?"                    # Set the message content

                await self.send(msg2)
                print(Fore.BLUE + "Enviado" + msg2.body)
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

senderAgent = Sender(sender_jid, sender_password)
senderAgent.start()


while receiverAgent.is_alive():
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        print(Fore.WHITE +"Keyboard Interrupt")
        senderAgent.stop()
        receiverAgent.stop()
print(Fore.WHITE +"Agentes assassinados! ;)")
import discord
import commands_
import assistants
import conversation_machine as cm
from discord.ext import commands as discord_commands
INTENTS = discord.Intents.default()
INTENTS.message_content = True


class MyClient(discord_commands.Bot):
    def __init__(self, assistant, intents=discord.Intents.default(), **options):
        self.in_conversation = False
        self.assistant = assistant
        self.cm = cm.ConversationMachine(self, assistant)
        self.cmds = {"!ping": commands_.ping}
        self.cmds_set = {cmd for cmd in self.cmds}
        super().__init__(command_prefix="Fixa så det inte krashar senare", intents=intents, **options)

    async def on_ready(self):
        print(f"Running {self.user} ({self.assistant.name})")

    async def handle_cmd(self, ctx):
        try:
            split_msg = ctx.content.split(" ")
            print("Trying to print intersect",self.cmds_set.intersection(set(split_msg)))
            print("Trying to print split sets", self.cmds_set, set(split_msg))
            indx = split_msg.index(list(self.cmds_set.intersection(set(split_msg)))[0])
            command, arg = split_msg[indx], split_msg[indx+1]
            await self.cmds[command](arg,ctx)
        except Exception as e:
            print("Failed to handle command", ctx.content, e)
            self.cm.impossible_command(ctx)

    async def conversation(self, ctx):
        response = self.cm.conduct_conversation(ctx) #kanske borde awaitas?
        ended = self.cm.conversation_check()
        await ctx.channel.send((response+ended))

    async def on_message(self, ctx):
        if ctx.author != self.user:
            if (not set(ctx.content.split(" ")).isdisjoint(self.cmds_set)): await self.handle_cmd(ctx)
            if (self.assistant.name in ctx.content) or self.in_conversation:
                self.in_conversation = True
                await self.conversation(ctx)
            #print(f"The client just recived the following message:\n{ctx.content}")



def run_discord_bot(assistant: assistants.Assistant):
    INTENTS = discord.Intents.default()
    INTENTS.message_content = True
    client = MyClient(assistant, intents=INTENTS)
    client.run(assistant.TOKEN)



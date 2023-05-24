import discord
async def ping(to_ping, ctx): await ctx.channel.send(f"Ping confirmed: {ctx.content}. Commands arg: {to_ping}")
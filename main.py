from dotenv import load_dotenv
import os
import re

import discord
import discord.ext.commands as commands

from helpClass import EmbedHelpCommand

load_dotenv()

bot = commands.Bot(command_prefix='!2',
                   case_insensitive=True,
                   activity=discord.Activity(name='Innerve Bot-a-thon', type=5),
                   status=discord.Status.idle,
                   intents=discord.Intents.all(),
                   strip_after_prefix=True,
                   help_command=EmbedHelpCommand())

rollNumber = re.compile(r'\d{3}-' +
                        r'(UG-(CSAI|CSE|ECAI|ECE|IT|MAE|EEE|CE)|' +
                        r'PG-(PD|AE|CH|CE|EE|ME|ED|MV|ER|QT|RAS|AI|CS|CP)|' +
                        r'D-(BE|CHE|CHEM|CE|AI|RAS|CS|CP|CG|CC|VLSI|EV|DES))' +
                        r'-\d{4}', re.IGNORECASE)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')


@bot.event
async def on_message(message: discord.Message):
    if message.channel.name == 'verification' or message.channel.id == 899194919263019018:
        if rollNumber.fullmatch(message.content) is not None:
            await message.author.add_roles(discord.utils.get(message.guild.roles, id=899119347753185291))
            await message.add_reaction("✔")
    await bot.process_commands(message)


@bot.command(name='Ping', brief="Bot's Ping", help=f"Displays bot's latency\n\tUsage: **{bot.command_prefix} ping**")
async def _ping(ctx):
    await ctx.send(f"Pong! Bot latency is {bot.latency}")


@bot.command(name='Invite', brief="invite all Students",
             help="Sends a DM to all students with the invite link to the new server\n" +
                  "\tUsage: **!2 invite <invite link/invite code>**")
async def _invite(ctx, invite: str):
    invite.lstrip("https://discord.gg/")
    embed = discord.Embed(
        name="Invite to all Students",
        colour=0xFF6900,
        description=f"[You have been invited to join the new server](https://discord.gg/{invite})"
    )
    role: discord.Role = ctx.guild.get_role(899119347753185291)
    unableToSend = []
    for member in role.members:
        try:
            await member.send(embed=embed)
        except discord.Forbidden:
            unableToSend.append(member.mention)
    if unableToSend:
        await ctx.send(f"Following members have DMs off, cannot invite them to the new server:\n")
        msg = ''
        for i in unableToSend:
            if len(msg) < 1970:
                msg += i + '\n'
            else:
                await ctx.send(msg)
                msg = i + '\n'
        await ctx.send(msg)


@bot.command(hidden=True)
async def test(ctx, role: discord.Role):
    if ctx.author.id != 437491079869104138:
        return
    await ctx.author.remove_roles(role, reason="It was just a test for heirarchy.")


@bot.command(name="Quit", brief="Quits Bot", help=f"Logs out the Bot. **(Owner)**\n\tUsage : **!2 quit**", hidden=True)
async def _quit(ctx):
    if ctx.author.id == 437491079869104138:
        await ctx.send(f"Disconnecting sequence invoked by {ctx.author.display_name}...")
        await bot.logout()
    else:
        print(f"{ctx.author} tried to log out the bot.")


bot.run(os.getenv('TOKEN'))

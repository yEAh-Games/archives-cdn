import discord
import os
import requests
import json
from keep_alive import keep_alive

client = discord.Client()


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author.bot:
        return
    elif "yeahtest30303" in message.content.lower():
        await message.channel.send(f"test\n test2")
    elif "yeahinvis" in message.content.lower():
        await client.change_presence(status=discord.Status.invisible)
    elif "yeahidle" in message.content.lower():
        await client.change_presence(status=discord.Status.idle)
    elif "yeahon" in message.content.lower():
        await client.change_presence(status=discord.Status.online)
    elif "yeahdnd" in message.content.lower():
        await client.change_presence(status=discord.Status.dnd)
    elif "yeahgame" in message.content.lower():
        await client.change_presence(activity=discord.Activity(
            type=discord.ActivityType.playing, name="yEAhhelp"))
    elif "imagine" in message.content.lower():
        await message.channel.send(
            f"{message.author.mention} [*Imagine*]... **Dragons!**")
    elif "imagining dragons" in message.content.lower():
        await message.channel.send(
            f"{message.author.mention} [*Imagining Dragons*]... **Deez nuts across your face!**"
        )
    elif "bruh" in message.content.lower():
        await message.delete()
        await message.channel.send(
            f"{message.author.mention} 🛑 Illegal terminology! Next time, please use **eden** instead of *bruh*."
        )
    elif "b ruh" in message.content.lower():
        await message.delete()
        await message.channel.send(
            f"{message.author.mention} 🛑 Illegal terminology! Next time, please use **eden** instead of *bruh*."
        )
    elif "sus" in message.content.lower():
        await message.delete()
        await message.channel.send(
            f"{message.author.mention} 🛑 Illegal terminology! Next time, please use **07** instead of *sus*."
        )
    elif "amogus" in message.content.lower():
        await message.delete()
        await message.channel.send(
            f"{message.author.mention} 🛑 Illegal terminology! Next time, please use **07** instead of *amogus*."
        )
    elif "ඞ" in message.content.lower():
        await message.delete()
        await message.channel.send(
            f"{message.author.mention} 🛑 Illegal terminology! Next time, please use **07** instead of *ඞ*."
        )
    elif "among us" in message.content.lower():
        await message.delete()
        await message.channel.send(
            f"{message.author.mention} 🛑 Illegal terminology! Next time, please use **07** instead of *among us*."
        )
    elif "pog" in message.content.lower():
        await message.delete()
        await message.channel.send(
            f"{message.author.mention} 🛑 Illegal terminology! Next time, please use **frog** instead of *pog*."
        )
    elif "poggers" in message.content.lower():
        await message.delete()
        await message.channel.send(
            f"{message.author.mention} 🛑 Illegal terminology! Next time, please use **froggers** instead of *poggers*."
        )
    elif "gamer" in message.content.lower():
        await message.delete()
        await message.channel.send(
            f"{message.author.mention} 🛑 Illegal terminology! Next time, please use **gaemer (pronounced 'ghamer')** instead of *gamer*."
        )
    elif "fuck" in message.content.lower():
        await message.delete()
        await message.channel.send(
            f"{message.author.mention} 🛑 Illegal terminology! Next time, please use **phoque** instead of *fuck*."
        )
    elif "garbage" in message.content.lower():
        await message.delete()
        await message.channel.send(
            f"{message.author.mention} 🛑 Illegal terminology! Next time, please use **junk** instead of *garbage*."
        )
    elif "trash" in message.content.lower():
        await message.delete()
        await message.channel.send(
            f"{message.author.mention} 🛑 Illegal terminology! Next time, please use **junk** instead of *trash*."
        )
    elif "mason" in message.content.lower():
        await message.delete()
        await message.channel.send(
            f"{message.author.mention} 🛑 Illegal terminology! Next time, please use **Marcus** instead of *Mason*."
        )
    elif "east side mario's" in message.content.lower():
        await message.delete()
        await message.channel.send(
            f"{message.author.mention} 🛑 Illegal terminology! Next time, please use **West Side Luigi's** instead of *East Side Mario's*."
        )
    elif "sabotage" in message.content.lower():
        await message.delete()
        await message.channel.send(
            f"{message.author.mention} 🛑 Illegal terminology! Next time, please use **sab** instead of *sabotage*."
        )
    elif "east side marios" in message.content.lower():
        await message.delete()
        await message.channel.send(
            f"{message.author.mention} 🛑 Illegal terminology! Next time, please use **West Side Luigi's** instead of *East Side Marios*."
        )
    if message.content.startswith('yeahhello'):
        await message.channel.send('Hello!')
    if message.content.startswith('yeahquote'):
        quote = get_quote()
        await message.channel.send(quote)
    if message.content.startswith('yeahwww+rules'):
        embedVar = discord.Embed(
            title="Wa Wa West+ rules",
            description="View the WWW+ official rule sheet."
            "Everyone starts with 0 ammo. You win by being the last one alive. Every turn, all players show what they're using that turn at the same time. At this point, all of the individual items' rules apply. Repeat until there is only one person left.",
            color=0xff4747)
        embedVar.set_author(
            name="yEAh Games",
            url="https://discord.gg/GNnPQ2h5",
            icon_url=
            "https://media.discordapp.net/attachments/887065655487119381/895986163020627980/yeahgames.png?width=751&height=422"
        )
        embedVar.add_field(
            name="Optional rules",
            value=
            "Any weapon will be defeated by a weapon of the same type greater than it. If there is a conflict between two or more weapons of the same type and level, the first to fire survives while the others will be hit. Ties are possible. If the first to fire can't be decided, the round will be concluded as a tie between those involved. This game is very flexible. Add your own items if you want!",
            inline=False)
        embedVar.add_field(
            name="Variations",
            value=
            " You may decide to exclude some items and/or rules before the game. **Headstart**: Everyone starts with 1 ammo instead of 0. **Lightning**: The game must be played as fast as possible. **Presicision Laser**: Laser Gun only attacks one player of your choice. **Teams**: Split all players into 2 teams. Kill all players on the other team to win. No friendly fire. **Thief**: When you kill a player, you get all their ammo.",
            inline=False)
        embedVar.add_field(name="𝗜𝘁𝗲𝗺𝘀",
                           value="________________",
                           inline=False)
        embedVar.add_field(
            name="**Reload**",
            value="View this item by using the command: **yeahwww+reload**.",
            inline=False)
        embedVar.add_field(
            name="**Gun**",
            value="View this item by using the command: **yeahwww+gun**.",
            inline=False)
        embedVar.add_field(
            name="**Shield**",
            value="View this item by using the command: **yeahwww+shield**.",
            inline=False)
        embedVar.add_field(
            name="**Orange Juice (unactivated)**",
            value="View this item by using the command: **yeahwww+OJun**.",
            inline=False)
        embedVar.add_field(
            name="**Orange Juice (activated)**",
            value="View this item by using the command: **yeahwww+OJa**.",
            inline=False)
        embedVar.add_field(
            name="**Laser Gun**",
            value="View this item by using the command: **yeahwww+LG**.",
            inline=False)
        embedVar.add_field(
            name="**Reinforced Shield**",
            value="View this item by using the command: **yeahwww+RS**.",
            inline=False)
        embedVar.add_field(
            name="**Grenade**",
            value="View this item by using the command: **yeahwww+grenade**.",
            inline=False)
        embedVar.add_field(
            name="**Bazooka**",
            value="View this item by using the command: **yeahwww+bazooka**.",
            inline=False)
        embedVar.add_field(
            name="**Mirror**",
            value="View this item by using the command: **yeahwww+mirror**.",
            inline=False)
        embedVar.add_field(
            name="**Necromancy**",
            value=
            "View this item by using the command: **yeahwww+necromancy**.",
            inline=False)
        embedVar.set_footer(text="©yEAh Games™ - 2021")
        await message.channel.send(embed=embedVar)
    if message.content.startswith('yeahhelp'):
        embedVar = discord.Embed(
            title="yEAh Games' bot help page",
            description=
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  𝗧𝗵𝗶𝘀 𝗯𝗼𝘁 𝗶𝘀 𝘀𝘁𝗶𝗹𝗹 𝘂𝗻𝗱𝗲𝗿 𝗰𝗼𝗻𝘀𝘁𝗿𝘂𝗰𝘁𝗶𝗼𝗻, 𝗽𝗹𝗲𝗮𝘀𝗲 𝗯𝗲 𝗽𝗮𝘁𝗶𝗲𝗻𝘁 𝗮𝘀 𝗺𝗮𝗻𝘆 𝗳𝗲𝗮𝘁𝘂𝗿𝗲𝘀 𝗽𝗿𝗼𝗯𝗮𝗯𝗹𝘆 𝗱𝗼 𝗻𝗼𝘁 𝘄𝗼𝗿𝗸. 𝗗𝗠 <@892883621076156416> 𝗳𝗼𝗿 𝗮𝗻𝘆 𝗾𝘂𝗲𝘀𝘁𝗶𝗼𝗻𝘀. ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                 Need some help operating this bot? You've come to the right place! The main prefix for this bot, is, 'yeah'; however, to view rules and information for certain games, you will need to add sub-prefixes. There is a sub-prefix for each of our games. For example: to see the rules for Random Guy TCG, you'll need to type in 'yeahrgrules'; the main prefix is 'yeah', and the sub-prefix is 'rg'.",
            color=0xff4747)
        embedVar.set_author(
            name="yEAh Games, Nnillat",
            url="https://discord.gg/GNnPQ2h5",
            icon_url=
            "https://media.discordapp.net/attachments/887065655487119381/895986163020627980/yeahgames.png?width=751&height=422")
        embedVar.add_field(name="Random Guy TCG",
                           value="――――――――― \n `yeahrg` -- This command allows you to view all commands relating to Random Guy TCG; this includes all seperate card commands.\n`yeahrgrules` -- View the Random Guy TCG Rules.",
                           inline=False)
        embedVar.set_footer(text="Bot developed by Nnillat#2657")
        await message.channel.send(embed=embedVar)
    if message.content.startswith('yeahrg'):
        embedVar = discord.Embed(
            title="Random Guy TCG",
            description="View all the Random Guy TCG-related commands", color=0xff4747)
        embedVar.set_author(
            name="yEAh Games, Nnillat",
            url="https://discord.gg/GNnPQ2h5",
            icon_url=
            "https://media.discordapp.net/attachments/887065655487119381/895986163020627980/yeahgames.png?width=751&height=422")
        embedVar.add_field(name="Cards",
                           value="――――――――― \n `yeahrgscamartist` -- View the Scam Artist card.",
                           inline=False)
        embedVar.set_footer(text="Bot developed by Nnillat#2657")
        await message.channel.send(embed=embedVar)
    if message.content.startswith('yeahbalance<@637006296234721320>'):
        embedVar = discord.Embed(
            title="Yank account balance for <@637006296234721320>",
            description="This is the yank account balance of this member, it will show their balance in online yollars, and their balance in paper money; it also shows the exact yenominations that they have. Exchanging paper money for online money, or vice versa, is available in <#910282955132395530>; please follow the format provided.", color=0xff4747)
        embedVar.set_author(
            name="yEAh Games, Nnillat",
            url="https://discord.gg/GNnPQ2h5",
            icon_url=
            "https://media.discordapp.net/attachments/887065655487119381/895986163020627980/yeahgames.png?width=751&height=422")
        embedVar.add_field(name="Cards",
                           value="――――――――― \n `yeahrgscamartist` -- View the Scam Artist card.",
                           inline=False)
        embedVar.set_footer(text="Bot developed by Nnillat#2657")
        await message.channel.send(embed=embedVar)

keep_alive()
client.run("ODk1NjIzMzI3ODgyODI1NzI4.YV7QOQ.ERrfwNOzAl8vYL1FPIRTn7bMkVg")

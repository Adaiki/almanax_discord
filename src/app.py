import os
import discord
import requests
from discord.ext import commands, tasks
from datetime import date, timedelta

client = commands.Bot(command_prefix='.')
loop_chan = None

@client.event
async def on_ready():
    activity = discord.activity.Game("Dofus")
    await client.change_presence(status=discord.Status.online, activity=activity)

@tasks.loop(hours=24)
async def test():
    await client.wait_until_ready()
    if loop_chan != None:
        embed = await send_request(date.today().strftime("%d-%m"))
        await loop_chan.send(embed=embed)

@client.command()
async def enable(ctx):
        if ctx.message.author.guild_permissions.administrator:
            global loop_chan
            if ctx.message.channel != loop_chan:
                loop_chan = ctx.message.channel
                if test.is_running():
                    test.restart()
                else:
                    test.start()
            await ctx.message.delete()

@client.command()
async def almanax(ctx, arg=date.today().strftime("%d-%m")):
    if arg == "demain":
        day = date.today() + timedelta(days=1)
        arg = day.strftime("%d-%m")
    embed = await send_request(arg)
    await ctx.send(embed=embed)


async def send_request(day):
    try:
        r = requests.get(os.getenv('API_URL') + day)
        r.raise_for_status()
    except requests.exceptions.RequestException as err:
        embed=discord.Embed(title="RequestException", description=err)        
    except requests.exceptions.HTTPError as errh:
        embed=discord.Embed(title="HTTPError", description=errh)
    except requests.exceptions.ConnectionError as errc:
        embed=discord.Embed(title="ConnectionError", description=errc)
    except requests.exceptions.Timeout as errt:
        embed=discord.Embed(title="Timeout", description=errt)
    if r.status_code == 200:
        data = r.json()
        embed=discord.Embed(title=data['quest'])
        embed.add_field(name=data['type'], value=data['effect'], inline=False)
        embed.add_field(name="Offrande", value=data['offering'], inline=False)
        embed.set_thumbnail(url="https://static.ankama.com/dofus/www/game/items/200/{0}.png".format(data['itemImage']))
    embed.set_footer(text="Almanax du " + day.replace('-', '/'))
    return embed

client.run(os.getenv('BOT_SECRET'))
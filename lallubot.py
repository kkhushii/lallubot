import discord
from discord.ext import commands
import os
import random
import youtube_dl

#client=discord.Client()
bot=commands.Bot(command_prefix='-')
responding=1

quotes=["Does nt matter yaar","Dhinka chika dhinka chika","I don't have time for this rubbish","aukat teri itni hoti toh tere paas gaadi hoti","Abbe ja na lawde","Rom Rom bhai! Sab theek hojayega","Agar apni maa se pyaar karte ho toh sojao","Dp BaTtLe kAreGa?","Ladoo khayega","hutt"]

trigger1=["ok","okay","okie","okayy","okayyy","omkay","omkie","op","op bhai op"]

trigger2=["hemlo","hi","rom rom","hello","samd","sad","maza","haan","no","nahi","aaja","aajao","suno","guys","gaiz"]

r=["!responding"]
@bot.event
async def on_ready():
    print("I'm ready!!This is {0.user}".format(bot))

@bot.event
async def on_message(message):
    if message.author==bot.user:
        return
    msg=message.content
    
    if any(word in msg for word in r):
        value=msg.split('!responding',1)[1]

        if value.lower()=='on':
            global responding
            responding=1
            await message.channel.send("Responding is on.")
        elif value.lower()=='off':
            responding=0
            await message.channel.send("Responding is off.")
    
    if responding:
        if any(word in msg for word in trigger1):
            await message.channel.send("Haan toh")
        elif any(word in msg for word in trigger2):
            await message.channel.send(random.choice(quotes))

    await bot.process_commands(message)

@bot.command()
async def play(ctx , url: str):
    song_there = os.path.isfile('song.mp3')
    try:
        if song_there:
            os.remove('song.mp3')
    except PermissionError:
        await ctx.send("Wait for the current song to end or use the stop command")
        return

    voice_channel=discord.utils.get(ctx.guild.voice_channels, name='General')
    await voice_channel.connect()
    voice = discord.utils.get(bot.voice_clients,guild = ctx.guild)
    


    ydl_opts = {
        'format':'bestaudio/best',
        'postprocessors':[{
            'key':'FFmpegExtractAudio',
            'preferredcodec':'mp3',
            'preferredquality':'192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file,"song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))

@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    await voice.disconnect()
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("Lallu is not connected to a voice channel you dumbass.")

@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()

@bot.command()
async def pause(ctx):
    voice= discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Lallu is not playing anything ok.")

@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild = ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("It's not even paused!")


#client.run('ODM1NjAwMTk2OTU5ODYyNzk2.YIRzUw.1LbkJgGXmP19wIo8Yq8y96zn11w')
bot.run('ODM1NjAwMTk2OTU5ODYyNzk2.YIRzUw.1LbkJgGXmP19wIo8Yq8y96zn11w')


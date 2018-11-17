import os
from discord.ext import commands
import discord
import asyncio
import youtube_dl

client = commands.Bot(command_prefix="!!")
player_dict = dict()



from discord import opus
OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll',
             'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']


def load_opus_lib(opus_libs=OPUS_LIBS):
    if opus.is_loaded():
        return True

    for opus_lib in opus_libs:
            try:
                opus.load_opus(opus_lib)
                return
            except OSError:
                pass

    raise RuntimeError('Could not load an opus lib. Tried %s' %
                       (', '.join(opus_libs)))
opts = {
    'default_search': 'auto',
    'quiet': True,
}  

# youtube_dl options



load_opus_lib()

servers_songs={}
player_status={}
now_playing={}
song_names={}
paused={}


@client.event
async def on_ready():
    print("Discord-Bot BBot ist jetzt bereit.")
    print('--------------------------------------')
    print('Eingeloggt als:')
    print(client.user.name)
    print('ID:')
    print(client.user.id)


@client.command(pass_context=True)
async def play(ctx, url):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)
    server = ctx.message.server
    voice = client.voice_client_in(server)
    player = await voice.create_ytdl_player(url)
    player_dict[server.id] = player
    await client.send_message(ctx.message.channel, "Spiele `%s` ab..." % player.title)
    player.start()


@client.command(pass_context=True)
async def stop(ctx):
    server = ctx.message.server
    player = player_dict[server.id]
    await client.send_message(ctx.message.channel, "Beende abspielen von `%s`..." % player.title)
    player.stop()
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()
    del player_dict[server.id]


@client.command(pass_context=True)
async def pause(ctx):
    server = ctx.message.server
    player = player_dict[server.id]
    player.pause()
    await client.send_message(ctx.message.channel, "Pausiere abspielen von `%s`..." % player.title)


@client.command(pass_context=True)
async def resume(ctx):
    server = ctx.message.server
    player = player_dict[server.id]
    player.resume()
    await client.send_message(ctx.message.channel, "Setze abspielen von `%s` fort..." % player.title)


@client.command(pass_context=True)
async def volume(ctx, sound_volume=None):
    server = ctx.message.server
    player = player_dict[server.id]
    if sound_volume is None:
        await client.send_message(ctx.message.channel, "Lautstärke: `{}%`".format(player.volume * 100))
    else:
        if sound_volume.isnumeric():
            player.volume = int(sound_volume) / 100
        elif sound_volume == "-":
            player.volume = player.volume - 0.05
        elif sound_volume == "+":
            player.volume = player.volume + 0.05

        await client.send_message(ctx.message.channel, "Setze Lautstärke auf: `{}%`".format(player.volume * 100))


@client.command(pass_context=True)
async def clear(ctx):
    await client.send_message(ctx.message.channel, 'Löscht Nachrichten in diesem Channel.')
    async for msg in client.logs_from(ctx.message.channel):
        await client.delete_message(msg)


@client.command(pass_context=True)
async def info(ctx):
    await client.send_message(ctx.message.channel, 'BBot Information')
    await client.send_message(ctx.message.channel, 'Befehle :grinning:')
    await client.send_message(ctx.message.channel, '!!play [URL] ; Musik abspielen')
    await client.send_message(ctx.message.channel, '!!stop ; Stoppt Musik abspielen')
    await client.send_message(ctx.message.channel, '!!clear ; Reinigt den ganzen Chatverlauf des Kanals [Berechtigung ben.] ')
    await client.send_message(ctx.message.channel, '!!foto ; Zeigt Landschaftsfoto...')
    await client.send_message(ctx.message.channel, '!!info ; Dieser Befehl')
    await client.send_message(ctx.message.channel, '!!volume ; [-;+;Zahl]')
    await client.send_message(ctx.message.channel, '!!pause ; Pausiert abspielen')
    await client.send_message(ctx.message.channel, '!!resume ; Setzt abspielen fort')
    await client.send_message(ctx.message.channel, 'Programmierer:')
    await client.send_message(ctx.message.channel, ':smiley: **@BerndHD#9422** :smiley:')


@client.command(pass_context=True)
async def foto(ctx):
    await client.send_message(ctx.message.channel, 'https://www.fewo-alpenwelt.de/img/wallpaper/landschaft.jpg')


@client.command(pass_context=True)
async def hallo(ctx):
        await client.send_message(ctx.message.author, "Hallo `@%s`!" % ctx.message.author)
        await client.send_message(ctx.message.author, "Du befindest dich auf dem Server `%s`!" % ctx.message.server)
        await client.send_message(ctx.message.channel, "Nachricht an @%s gesandt!" % ctx.message.author)



client.run(str(os.environ.get('BOT_TOKEN')))

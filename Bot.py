from discord.ext import commands
import discord
from discord.ext import opus

client = commands.Bot(command_prefix="!!")
player_dict = dict()


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
    await client.send_message(ctx.message.channel, '!!play [URL] ; Musik abspielen ')
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



client.run('NTA4NTcxMDE4OTk5MzY1NjUz.DtAHbg.-l-dDYIPM0RNWk7X1RN7NMazFCo')

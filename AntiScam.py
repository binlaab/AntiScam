import discord
from discord.ext import commands

message_content = ''
last_message = ''
last_message_content = ''
spam_counter = 0

whitelist = [] # IDs of whitelisted users. They will not be affected by this system.
logs_channel=None # ID of the channel where logs will be sent.

async def AntiScam(message, bot, whitelist, muted_role, verified_role, logs_channel):
    global message_content, last_message, last_message_content, spam_counter
    message_content = f'{message.author.id}: {message.content}'
    message_content = message_content.replace("'", "`")

    # AntiScam-System
    if message_content == last_message_content and message.content != '' and message.author.id not in whitelist: # Checks if the message was identical to the last one sent and if the author is not whitelisted, then it will delete the message.
        spam_counter += 1
        await message.delete()
    else:
        last_message = message
        last_message_content = message_content
        spam_counter = 0

    if len(message.mentions) > 10 and message.author.id not in whitelist:
        await message.delete()
        spam_counter = 2

    if spam_counter > 1 and message.author.id not in whitelist: # Mutes users if they spammed more than once and resets the counter to zero.
        spam_counter = 0
        muted = discord.utils.get(message.author.guild.roles, name=muted_role)
        verified = discord.utils.get(message.author.guild.roles, name=verified_role)
        await last_message.delete()
        await message.author.add_roles(muted)
        await message.author.remove_roles(verified)
        channel = bot.get_channel(logs_channel)
        await channel.send(f'USUARIO MUTEADO: {message_content}')
    await bot.process_commands(message)


bot = commands.Bot(command_prefix=">") # This means you are able to run bot commands using ">".
# bot.remove_command('help') Uncomment this line if you want a "help" command.

@bot.listen()
async def on_message(message):
	await AntiScam(message, bot = bot, whitelist = whitelist, muted_role='Muted', verified_role='Verified', logs_channel=logs_channel) # Here you can change the names of the roles.
bot.run("token")

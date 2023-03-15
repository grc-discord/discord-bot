import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from src.discord_bot import responses
from src.chatgpt.openai import chatgpt_response

load_dotenv()

discord_token = os.getenv('DISCORD_TOKEN')


class Bot(discord.Client):
    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.channel_number = 1044095575322425906

        self.client = commands.Bot(command_prefix='$', intents=intents)

    async def on_ready(self):
        print(f'Successfully logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'Message from {message.author}: {message.content} ({message.channel} channel)')

        if user_message.startswith('?'):
            user_message = user_message[1:]
            if user_message == 'hello':
                response = responses.get_response(user_message)
                await message.author.send(response)
            else:
                raise ValueError('Invalid message format. Message should be "?hello"')
        else:
            response = responses.get_response(user_message)
            await message.channel.send(response)

    async def on_member_join(self, member):
        channel = self.get_channel(self.channel_number)
        await channel.send(f'{member} Hello and welcome to the server!')
        await member.send(
            f'Hello {member}! Welcome. '
            f'check out the announcements channel for important information about the club! '
            f'https://discord.com/channels/1043278905806692442/1043279855938191381')

    async def on_member_remove(self, member):
        channel = self.get_channel(self.channel_number)
        await channel.send(f'{member} has left the server.')

    def get_channel(self, number):
        return self.client.get_channel(number)

    # async def on_ready(self):
    #     print(f'Successfully logged in as {self.user}')
    #
    # async def on_message(self, message):
    #     print(f'Message from {message.author}: {message.content}')
    #     if message.author == self.user:
    #         return
    #     command, user_message = None, None
    #
    #     if message.content.startswith(('/ai', '/bot', '/chatgpt')):
    #         command = message.content.split(' ')[0]
    #         user_message = message.content.replace(command, '').strip()
    #         print(f'Command: {command}, User Message: {user_message}')
    #
    #     if command in ['/ai', '/bot', '/chatgpt']:
    #         bot_response = chatgpt_response(prompt=user_message)
    #         await message.channel.send(f'Answer: {bot_response}')


async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        print(e)


async def resources(ctx):
    response = responses.get_response('resources')
    await ctx.send(response)


async def events(ctx):
    response = responses.get_response('events')
    await ctx.send(response)


async def join(ctx):
    response = responses.get_response('join')
    await ctx.send(response)


async def contact(ctx):
    response = responses.get_response('contact')
    await ctx.send(response)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.typing = False
intents.presences = False

bot = Bot(intents=intents)
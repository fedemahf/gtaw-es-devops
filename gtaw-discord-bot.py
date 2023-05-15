#!/usr/bin/env python3

import os
import subprocess

import discord
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

allowedUsers = [
        919790456492159046,
        458417449457680435,
        900119403268542565
]

SCRIPT_DIR=os.path.realpath(os.path.dirname(__file__))

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def deploy(ctx):
    if ctx.message.author.id not in allowedUsers:
        await ctx.send('You are not allowed to use this bot. Contact Lateralus#4351 for more info.')
        return

    await ctx.send('Starting deploy')
    subprocess.check_output(['bash', '-c', SCRIPT_DIR + '/gtaw-es-prod-deploy.sh'])
    await ctx.send('Deploy done')

@bot.command(name='qa-start')
async def qa_start(ctx):
    if ctx.message.author.id not in allowedUsers:
        await ctx.send('You are not allowed to use this bot. Contact Lateralus#4351 for more info.')
        return

    await ctx.send('Starting deploy to QA')
    result = subprocess.check_output(['bash', '-c', 'ssh -i ~/.ssh/gtaw-qa-server-ssh-key gtaw@gtaw-qa-server ./start-ragemp.sh'])
    await ctx.send('Result: ' + result.decode('utf-8'))


@bot.command(name='qa-stop')
async def qa_stop(ctx):
    if ctx.message.author.id not in allowedUsers:
        await ctx.send('You are not allowed to use this bot. Contact Lateralus#4351 for more info.')
        return

    await ctx.send('Stopping QA server')
    result = subprocess.check_output(['bash', '-c', 'ssh -i ~/.ssh/gtaw-qa-server-ssh-key gtaw@gtaw-qa-server ./stop-ragemp.sh'])
    await ctx.send('Result: ' + result.decode('utf-8'))

@bot.command(name='qa-deploy')
async def qa_deploy(ctx):

    if ctx.message.author.id not in allowedUsers:
        await ctx.send('You are not allowed to use this bot. Contact Lateralus#4351 for more info.')
        return

    await ctx.send('Deploying to QA')
    result = subprocess.check_output(['bash', '-c', '~/copy-gtaw-build-files.sh'])
    await ctx.send('Result: ' + result.decode('utf-8'))


bot.run(TOKEN)


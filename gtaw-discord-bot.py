#!/usr/bin/env python3

import os
import subprocess

import discord
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN: str = os.getenv('DISCORD_TOKEN')
GTAW_SSH_USER: str = os.getenv('GTAW_SSH_USER')
GTAW_SSH_HOST: str = os.getenv('GTAW_SSH_HOST')
GTAW_SSH_KEY_PATH: str = os.getenv('GTAW_SSH_KEY_PATH')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

allowedUsers = [
    919790456492159046, # Obituary
    458417449457680435, # empty
    900119403268542565, # Sweetvon
    134680883318751234, # Livamyrd
    348711124239253509, # Benyi
    140601452513984513, # Dhraax
]

SCRIPT_DIR=os.path.realpath(os.path.dirname(__file__))
ERROR_USER_NOT_ALLOWED = 'You are not allowed to use this bot. Contact Lateralus#4351 for more info.'

async def userNotAllowed(ctx):
    if ctx.message.author.id not in allowedUsers:
        await ctx.send(ERROR_USER_NOT_ALLOWED)
        return True
    return False

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def deploy(ctx):
    if await userNotAllowed(ctx):
        return

    await ctx.send('Starting deploy')
    subprocess.check_output(['bash', '-c', f'{SCRIPT_DIR}/gtaw-es-prod-deploy.sh'])
    await ctx.send('Deploy done')

@bot.command(name='qa-start')
async def qa_start(ctx):
    if await userNotAllowed(ctx):
        return

    await ctx.send('Starting deploy to QA')
    result = subprocess.check_output(['bash', '-c', f'ssh -i {GTAW_SSH_KEY_PATH} {GTAW_SSH_USER}@{GTAW_SSH_HOST} ./start-ragemp.sh'])
    await ctx.send('Result: ' + result.decode('utf-8'))

@bot.command(name='qa-stop')
async def qa_stop(ctx):
    if await userNotAllowed(ctx):
        return

    await ctx.send('Stopping QA server')
    result = subprocess.check_output(['bash', '-c', f'ssh -i {GTAW_SSH_KEY_PATH} {GTAW_SSH_USER}@{GTAW_SSH_HOST} ./stop-ragemp.sh'])
    await ctx.send('Result: ' + result.decode('utf-8'))

@bot.command(name='qa-restart')
async def qa_restart(ctx):
    if await userNotAllowed(ctx):
        return

    await qa_stop(ctx)
    await qa_start(ctx)

@bot.command(name='qa-deploy')
async def qa_deploy(ctx):
    if await userNotAllowed(ctx):
        return

    await ctx.send('Starting deploy to QA from Discord')
    subprocess.check_output(['bash', '-c', f'{SCRIPT_DIR}/gtaw-es-qa-deploy.sh'])
    await ctx.send('Deploy to QA from Discord done')

@bot.command(name='docker-prune')
async def docker_prune(ctx):
    if await userNotAllowed(ctx):
        return

    await ctx.send('Running `docker system prune -f`')
    result = subprocess.check_output(['bash', '-c', 'docker system prune -f'])
    await ctx.send('Result: ' + result.decode('utf-8'))

bot.run(DISCORD_TOKEN)

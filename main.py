import discord
from discord.ext import commands

intents = discord.Intents.default()
bot = discord.Bot(intents=intents)  # ✅ Esto sí funciona con py-cord 2.x

import os
import discord
import openai
import logging

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

logging.basicConfig(filename="logs.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

intents = discord.Intents.default()
bot = discord.Bot(intents=intents)  # ← Pycord sí lo permite

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

@bot.slash_command(name="pregunta", description="Hacé una pregunta a la IA")
async def pregunta(ctx: discord.ApplicationContext, consulta: str):
    await ctx.defer()
    logging.info(f"[{ctx.author}] preguntó: {consulta}")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": consulta}]
        )
        respuesta = response.choices[0].message["content"]
        respuesta = respuesta[:2000]  # Discord limit

        await ctx.respond(f"**🤖 Respuesta a:** `{consulta}`\n\n{respuesta}")
    except Exception as e:
        logging.error(f"Error con OpenAI: {str(e)}")
        await ctx.respond(f"❌ Error al generar la respuesta: `{e}`")

bot.run(DISCORD_TOKEN)

import os
import discord
import openai
import logging

# 🔐 Claves de entorno (no hardcodear)
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configurar cliente OpenAI
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Configurar logs
logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

# Crear instancia del bot
intents = discord.Intents.default()
bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    try:
        await bot.sync_commands()
        print("✅ Comandos sincronizados")
    except Exception as e:
        print(f"❌ Error al sincronizar comandos: {e}")

@bot.slash_command(name="pregunta", description="Hacé una pregunta a la IA")
async def pregunta(ctx: discord.ApplicationContext, consulta: str):
    await ctx.defer()
    logging.info(f"[{ctx.author}] preguntó: {consulta}")

    try:
        # Nuevo formato para openai>=1.0.0
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": consulta}
            ]
        )
        respuesta = response.choices[0].message.content
        respuesta = respuesta[:2000]  # Discord límite de caracteres

        await ctx.respond(f"**🤖 Respuesta a:** `{consulta}`\n\n{respuesta}")
    except Exception as e:
        logging.error(f"Error con OpenAI: {str(e)}")
        await ctx.respond("❌ Hubo un error al generar la respuesta.")

# Iniciar el bot
bot.run(DISCORD_TOKEN)
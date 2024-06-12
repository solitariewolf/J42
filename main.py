import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from datetime import datetime, timedelta

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True  # Habilita a permissão de conteúdo das mensagens

bot = commands.Bot(command_prefix='!', intents=intents)

user_times = {} 
user_totals = {} 

@bot.event
async def on_ready():
    print(f'{bot.user.name} conectado com sucesso!')

@bot.event
async def on_voice_state_update(member, before, after):
    user_id = member.id
    now = datetime.now()

    if before.channel is None and after.channel is not None:  # O usuário entrou em um canal de voz
        user_times[user_id] = now  # Registra o horário de entrada
        channel_id = '1249533394325344268'  # Substitua pelo ID do canal em que você quer que o bot informe os usuários que entraram
        channel = bot.get_channel(int(channel_id))
        await channel.send(f'{member.name} entrou no canal de voz {after.channel.name}.')
    elif before.channel is not None and after.channel is None:  # O usuário saiu de um canal de voz
        start_time = user_times.pop(user_id, None)  # Obtém e remove o horário de entrada
        if start_time is not None:
            duration = now - start_time  # Calcula a duração
            total = user_totals.get(user_id, timedelta()) + duration  # Obtém o total anterior e adiciona a nova duração
            user_totals[user_id] = total  # Atualiza o total

            # Carregar tempos existentes
            user_durations = {}
            try:
                with open('user_times.txt', 'r') as f:
                    for line in f:
                        try:
                            name, time_str = line.strip().rsplit(' ', 1)
                            user_durations[name] = timedelta(seconds=float(time_str))
                        except ValueError:
                            print(f"Erro ao processar a linha: {line}")
            except FileNotFoundError:
                pass

            # Atualizar tempo do usuário atual
            user_durations[member.name] = user_durations.get(member.name, timedelta()) + duration

            # Salvar tempos atualizados
            with open('user_times.txt', 'w') as f:
                for name, total_duration in user_durations.items():
                    f.write(f'{name} {total_duration.total_seconds()}\n')

async def load_extensions():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            await bot.load_extension(f'commands.{filename[:-3]}')

# Executar carregamento de extensões de forma assíncrona
@bot.event
async def on_ready():
    await load_extensions()
    print(f'{bot.user.name} conectado com sucesso!')

bot.run(token)
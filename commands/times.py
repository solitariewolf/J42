from discord.ext import commands
from datetime import timedelta
import os

class Times(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='times')
    async def times(self, ctx):
        try:
            with open('user_times.txt', 'r') as f:
                lines = f.readlines()
            if lines:
                response = "Tempo total dos usuários nos canais de voz (HH:mm:ss):\n"
                for line in lines:
                    try:
                        name, time_str = line.strip().rsplit(' ', 1)
                        total_duration = timedelta(seconds=float(time_str))
                        hours, remainder = divmod(total_duration.total_seconds(), 3600)
                        minutes, seconds = divmod(remainder, 60)
                        formatted_duration = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
                        response += f'{name} passou um total de {formatted_duration} no canal de voz.\n'
                    except ValueError:
                        response += f"Linha malformada: {line}\n"
                await ctx.send(response)
            else:
                await ctx.send("Nenhum registro encontrado.")
        except FileNotFoundError:
            await ctx.send("Nenhum registro encontrado.")

async def setup(bot):
    await bot.add_cog(Times(bot))

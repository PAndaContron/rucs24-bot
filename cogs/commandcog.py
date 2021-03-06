import discord
from discord.ext import commands
import json


class CommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("Admin")
    async def setcommand(self, ctx, name, *args):
        """Adds a custom command with the first word as command and rest as response"""

        # Retrieve commands, add command, dump new dict, send msg
        with open("jsondata/commands.json", "r") as f:
            commands = json.load(f)

        commands[name] = " ".join(args)

        with open("jsondata/commands.json", "w") as f:
            json.dump(commands, f)

        await ctx.send(f"Command {name} updated!")

    @commands.command()
    @commands.has_role("Admin")
    async def removecommand(self, ctx, name):
        """Removes a custom command with the given name"""

        # Get dict, remove given command, and write new dict
        with open("jsondata/commands.json", "r") as f:
            commands = json.load(f)

        try:
            commands.pop(name)
        except:
            await ctx.send("No command with that name!")
            return

        with open("jsondata/commands.json", "w") as f:
            json.dump(commands, f)

        await ctx.send(f"There is now no command for {name}")

    @commands.Cog.listener()
    async def on_message(self, msg):
        """Check for custom commands on every message"""

        # Get commands, if the message is in commands.keys() send the command
        with open("jsondata/commands.json", "r") as f:
            commands = json.load(f)

        if msg.content in commands.keys():
            await msg.channel.send(commands[msg.content])


def setup(bot):
    bot.add_cog(CommandCog(bot))

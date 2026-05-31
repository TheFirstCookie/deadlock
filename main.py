import logging
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_GUILD_ID = os.getenv("DISCORD_GUILD_ID")

if not DISCORD_TOKEN:
    raise SystemExit("Missing DISCORD_TOKEN environment variable.")

if DISCORD_GUILD_ID:
    try:
        GUILD_ID = int(DISCORD_GUILD_ID)
    except ValueError as exc:
        raise SystemExit("DISCORD_GUILD_ID must be a Discord server ID number.") from exc
else:
    GUILD_ID = None


class Client(commands.Bot):
    async def setup_hook(self):
        if GUILD_ID:
            guild = discord.Object(id=GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            logging.info("Synced %s command(s) to guild %s", len(synced), GUILD_ID)
        else:
            synced = await self.tree.sync()
            logging.info("Synced %s global command(s)", len(synced))

    async def on_ready(self):
        logging.info("Logged on as %s", self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('cookie'):
            await message.channel.send('buna ziua')

        await self.process_commands(message)


intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix='!', intents=intents)

characters = [
    'Abrams', 'Apollo', 'Bebop', 'Billy', 'Calico', 'Celeste', 'Doorman', 'Drifter',
    'Dynamo', 'Graves', 'Grey Talon', 'Haze', 'Holliday', 'Infernus', 'Ivy',
    'Kelvin', 'Lady Geist', 'Lash', 'McGinnis', 'Mina', 'Mirage', 'Mo & Krill',
    'Paige', 'Paradox', 'Pocket', 'Rem', 'Seven', 'Shiv', 'Silver', 'Sinclair',
    'Venator', 'Victor', 'Vindicta', 'Viscous', 'Vyper', 'Warden', 'Wraith',
    'Yamato'
]


@client.tree.command(name="random", description="Randomly chooses a character")
async def random_character(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(characters))


@client.tree.command(name="random-from-vc", description="Assigns a random character to everyone in your VC")
async def random_from_vc(interaction: discord.Interaction):
    if interaction.user.voice is None or interaction.user.voice.channel is None:
        await interaction.response.send_message(
            "You need to be in a voice channel to use this command!",
            ephemeral=True,
        )
        return

    voice_channel = interaction.user.voice.channel
    members = voice_channel.members

    if len(members) > len(characters):
        await interaction.response.send_message(
            f"There are {len(members)} people in the voice channel, but only "
            f"{len(characters)} characters to assign.",
            ephemeral=True,
        )
        return

    chosen_characters = random.sample(characters, len(members))

    response_lines = []
    for i, member in enumerate(members):
        response_lines.append(f"{member.display_name}: **{chosen_characters[i]}**")

    full_message = "\n".join(response_lines)
    await interaction.response.send_message(full_message)


client.run(DISCORD_TOKEN)

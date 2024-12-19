import discord
from discord import app_commands
from discord.ext import commands
import random
import string
from datetime import datetime

# Intents and bot setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Mission data storage
missions = {}

# Constants for mission grades
MISSION_XP = {
    "E": 100,
    "D": 250,
    "C": 500,
    "B": 1000,
    "A": 2800,
    "S": 3000,
    "S+": 3800,
    "SS": 4000
}

MISSION_REWARD = {
    "E": 35,
    "D": 40,
    "C": 58,
    "B": 60,
    "A": 85,
    "S": 100,
    "S+": 100,
    "SS": 100
}

# Helper function to generate random mission code
def generate_mission_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot {bot.user.name} is ready and connected!")

# Command group for mission management
class MissionCommands(app_commands.Group):
    def __init__(self):
        super().__init__(name="mission", description="Manage missions.")

    @app_commands.command(name="create", description="Create a new mission.")
    async def create(self, interaction: discord.Interaction, 
                     mission_grade: str, 
                     mission_member: str, 
                     monster_name: str = "", 
                     location: str = ""):  # Allow optional inputs
        if mission_grade not in MISSION_XP:
            await interaction.response.send_message(f"Invalid grade `{mission_grade}`. Choose from {', '.join(MISSION_XP.keys())}", ephemeral=True)
            return

        code = generate_mission_code()
        xp = MISSION_XP[mission_grade]
        reward = MISSION_REWARD[mission_grade]

        # Save mission details
        missions[code] = {
            "grade": mission_grade,
            "members": mission_member.split(),  # Split tags into a list
            "xp": xp,
            "reward": reward,
            "monster_name": monster_name,
            "location": location,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Format mission details
        mission_details = (
            f"# |»»»»MISSION CENTER««««|\n"
            f"# ===========================\n"
            f"Berhasil mendaftarkan hunter ke misi baru dengan Grade ""**{mission_grade}**""!\n\n"
            f"**Detail Misi:**\n"
            f"- **Code Mission:** {code}\n"
            f"- **Grade:** {mission_grade}\n"
            f"- **Monster/Alien/Robot Name:** {monster_name or '(kosong)'}\n"
            f"- **Location:** {location or '(kosong)'}\n"
            f"- **XP / Peserta:** {xp}\n"
            f"- **RYO Reward / Peserta:** {reward}\n"
            f"- **Member:** {', '.join(missions[code]['members'])}\n"
            f"- **Tanggal:** {missions[code]['date']}\n"
            f"# ===========================\n"
            f"# |»»»MISSION RUNNING«««|"
        )

        await interaction.response.send_message(mission_details)

    @app_commands.command(name="finish", description="Finish a mission.")
    async def finish(self, interaction: discord.Interaction, mission_code: str):
        if mission_code not in missions:
            await interaction.response.send_message(f"Mission code `{mission_code}` not found.", ephemeral=True)
            return

        mission = missions.pop(mission_code)
        grade = mission["grade"]
        xp = mission["xp"]
        reward = mission["reward"]
        members = mission["members"]

        # Format finish message
        finish_message = (
            f"# |»»»»MISSION CLEAR««««|\n"
            f"# ===========================\n"
            f"Misi dengan Code Mission **{mission_code}** telah selesai!\n\n"
            f"Setiap NeoAgent yang mengikuti misi tersebut mendapatkan **{reward} RYO** & **{xp} XP**!"
        )

        await interaction.response.send_message(finish_message)

    @app_commands.command(name="list", description="List all running missions.")
    async def list_missions(self, interaction: discord.Interaction):
        if not missions:
            await interaction.response.send_message("Tidak ada misi yang sedang berjalan saat ini.")
            return

        mission_list = "# |»»»MISSION LIST«««|\n# ===========================\n"
        for code, details in missions.items():
            mission_list += (
                f"- **Code Mission:** {code}\n"
                f"  **Grade:** {details['grade']}\n"
                f"  **XP / Peserta:** {details['xp']}\n"
                f"  **RYO Reward / Peserta:** {details['reward']}\n"
                f"  **Members:** {', '.join(details['members'])}\n"
                f"  **Tanggal:** {details['date']}\n"
                f"# ---------------------------\n"
            )

        await interaction.response.send_message(mission_list)

bot.tree.add_command(MissionCommands())

# Run the bot (replace 'YOUR_TOKEN_HERE' with your bot's token)
bot.run('MTMxOTE0NjQ1MDIwMjEzMjUyMA.GnzyUz.V69WHYULgHz3amuOe8TXAk46uE-2vru0E86SOw')
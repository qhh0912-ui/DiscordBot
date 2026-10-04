import discord
import json
import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime, timezone, timedelta
from discord.ext import tasks
join_times = {}
try:
    with open("join_times.json", "r") as f:
        join_times = json.load(f)
except FileNotFoundError:
    join_times = {}

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
@tasks.loop(hours=24)
async def check_members():
    now = datetime.now(timezone.utc)

    for member_id, joined_str in join_times.items():
        joined_time = datetime.fromisoformat(joined_str)

        if now - joined_time >= timedelta(days=30):
            member = discord.utils.get(client.get_all_members(), id=int(member_id))

            if member is None:
                continue

            old_role = discord.utils.get(member.guild.roles, name="中年龍")
            new_role = discord.utils.get(member.guild.roles, name="老龍")

            if old_role and new_role:
                await member.remove_roles(old_role)
                await member.add_roles(new_role)

        elif now - joined_time >= timedelta(days=10):
            member = discord.utils.get(client.get_all_members(), id=int(member_id))

            if member is None:
                continue

            old_role = discord.utils.get(member.guild.roles, name="幼龍")
            new_role = discord.utils.get(member.guild.roles, name="中年龍")

            if old_role and new_role:
                await member.remove_roles(old_role)
                await member.add_roles(new_role)                                                                              
@client.event
async def on_ready():
    print(f"恐龍戰士已上線！")
    if not check_members.is_running():
        check_members.start()    
@client.event
async def on_member_join(member):
    join_times[str(member.id)] = discord.utils.utcnow().isoformat()

    with open("join_times.json", "w") as f:
        json.dump(join_times, f)        
    print(f"{member.name} 加入了伺服器！")
    role = discord.utils.get(member.guild.roles, name="幼龍")
    await member.add_roles(role)            

client.run(os.getenv("DISCORD_TOKEN"))

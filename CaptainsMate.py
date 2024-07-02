import discord
from discord.ext import commands
import moment

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def send_message(user_id: int, message: str):
    await bot.send_message(user_id, message)

async def send_team_invite_message(user_id: int, team_id: int):
    invite_message = "You have been invited to join Team {}! Reply with 'Accept' or 'Decline' to respond.".format(team_id)
    await bot.send_message(user_id, invite_message)

async def notify_team_owner(user_id: int, team_id: int, response: str):
    team_owner_id = get_team_owner_id(team_id)
    if response == "Accept":
        notification_message = "{} has accepted the team invite!".format(user_id)
    else:
        notification_message = "{} has declined the team invite!".format(user_id)
    await bot.send_message(team_owner_id, notification_message)



# Initialize a dictionary to store user data
users = {}

# Initialize a dictionary to store team data
teams = {}

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='register')
async def register(ctx):
    user_id = ctx.author.id
    if user_id not in users:
        users[user_id] = {'teams': {}, 'available_times': []}
        await ctx.send('Registration successful!')
    else:
        await ctx.send('You are already registered!')

@bot.command(name='addteam')
async def add_team(ctx, team_name, division):
    user_id = ctx.author.id
    if user_id in users:
        if team_name not in users[user_id]['teams']:
            users[user_id]['teams'][team_name] = division
            await ctx.send(f'Team {team_name} added to {division} division!')
        else:
            await ctx.send('You already have a team with that name!')
    else:
        await ctx.send('You are not registered!')

@bot.command(name='listteams')
async def list_teams(ctx):
    user_id = ctx.author.id
    if user_id in users:
        teams_list = '\n'.join(f'Team {team_name} - {division}' for team_name, division in users[user_id]['teams'].items())
        await ctx.send(f'Your teams:\n{teams_list}')
    else:
        await ctx.send('You are not registered!')

@bot.command(name='listallteams')
async def list_all_teams(ctx):
    teams_list = '\n'.join(f'Team {team_name} - {division} (Owner: {owner.name})' for team_name, team_data in teams.items() for owner, division in team_data.items())
    await ctx.send(f'All teams:\n{teams_list}')

@bot.command(name='removeteam')
async def remove_team(ctx, team_name):
    user_id = ctx.author.id
    if user_id in users:
        if team_name in users[user_id]['teams']:
            del users[user_id]['teams'][team_name]
            await ctx.send(f'Team {team_name} removed!')
        else:
            await ctx.send('You do not have a team with that name!')
    else:
        await ctx.send('You are not registered!')

@bot.command(name='addtimeavailable')
async def add_time_available(ctx, day_of_week, start_time, end_time):
    user_id = ctx.author.id
    if user_id in users:
        users[user_id]['available_times'].append((day_of_week, start_time, end_time))
        await ctx.send('Time added to your available times!')
    else:
        await ctx.send('You are not registered!')

@bot.command(name='removetimeavailable')
async def remove_time_available(ctx, index):
    user_id = ctx.author.id
    if user_id in users:
        if index < len(users[user_id]['available_times']):
            del users[user_id]['available_times'][index]
            await ctx.send('Time removed from your available times!')
        else:
            await ctx.send('Invalid index!')
    else:
        await ctx.send('You are not registered!')

@bot.command(name='listmytimes')
async def list_my_times(ctx):
    user_id = ctx.author.id
    if user_id in users:
        times_list = '\n'.join(f'Index {i}: {day_of_week} {start_time}-{end_time}' for i, (day_of_week, start_time, end_time) in enumerate(users[user_id]['available_times']))
        await ctx.send(f'Your available times:\n{times_list}')
    else:
        await ctx.send('You are not registered!')

@bot.command(name='inviteteam')
async def invite_team(ctx, user_id_or_mention, team_name, division):
    user_id = ctx.author.id
    if user_id in users:
        if team_name in users[user_id]['teams']:
            team_owner = ctx.author.name
            await ctx.send(f'You have invited {user_id_or_mention} to join your team {team_name} in {division} division!')
        else:
            await ctx.send('You do not have a team with that name!')
    else:
        await ctx.send('You are not registered!')

@bot.command(name='removeteammember')
async def remove_team_member(ctx, user_id_or_mention, team_name):
    user_id = ctx.author.id
    if user_id in users:
        if team_name in users[user_id]['teams']:
            team_owner = ctx.author.name
            await ctx.send(f'You have removed {user_id_or_mention} from your team {team_name}!')
        else:
            await ctx.send('You do not have a team with that name!')
    else:
        await ctx.send('You are not registered!')

@bot.command(name='leaveteam')
async def leave_team(ctx, team_name):
    user_id = ctx.author.id
    if user_id in users:
        if team_name in users[user_id]['teams']:
            team_owner = ctx.author.name
            await ctx.send(f'You have left the team {team_name}!')
        else:
            await ctx.send('You are not part of that team!')
    else:
        await ctx.send('You are not registered!')

@bot.command(name='whencanteam')
async def when_can_team(ctx, team_name):
    if team_name in teams:
        team_members = teams[team_name]
        available_times = []
        for member, division in team_members.items():
            if member in users and 'available_times' in users[member]:
                available_times.extend(users[member]['available_times'])
        overlapping_times = moment.intersect(available_times)
        await ctx.send(f'The team {team_name} can play at the following times:\n{overlapping_times}')
    else:
        await ctx.send('Team not found!')

@bot.command(name='teamavailability')
async def team_availability(ctx, team_name):
    if team_name in teams:
        team_members = teams[team_name]
        available_times = []
        for member, division in team_members.items():
            if member in users and 'available_times' in users[member]:
                available_times.extend(users[member]['available_times'])
        await ctx.send(f'The team {team_name} members are available at the following times:\n{available_times}')
    else:
        await ctx.send('Team not found!')

# Run the bot
bot.run('TOKEN')

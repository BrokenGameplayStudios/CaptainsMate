# CaptainsMate.py
Captain's Mate is a versatile Discord bot designed to help captains with the challenging task of scheduling matches. It takes the stress out of planning and organizing, allowing captains to focus on leading their teams to victory.

## Installation
1. Clone the repository: `git clone https://github.com/BrokenGameplayStudios/CaptainsMate.git`
2. Create a virtual environment: `python -m venv env`
3. Activate the virtual environment: `.\env\Scripts\activate` (on Windows) or `source env/bin/activate` (on Linux/Mac)
4. Install the required packages: `pip install -r requirements.txt`
5. Create a Discord bot and obtain a token: https://discord.com/developers/applications
6. Update `CaptainsMate.py` with the token: `bot.run('YOUR_TOKEN_HERE')`
7. Run the application: `python CaptainsMate.py`

## Usage

To use CaptainsMate, simply invite the bot to your Discord server and use the available commands.

### Commands

| Command | Description |
| --- | --- |
| `!register` |	Registers a user |
| `!addteam` | Adds a team to the user's list of teams |
| `!listteams` | Lists the user's teams |
| `!listallteams` | Lists all teams |
| `!removeteam` |	Removes a team from the user's list of teams |
| `!addtimeavailable` |	Adds a time slot to the user's available times |
| `!removetimeavailable` | Removes a time slot from the user's available times |
| `!listmytimes` | Lists the user's available times |
| `!inviteteam`	| Invites a user to a team |
| `!removeteammember` | Removes a user from a team |
| `!leaveteam` |	Leaves a team |
| `!whencanteam` |	Lists the times when a team can play |
| `!teamavailability`	| Lists the available times of team members |

## Contributing

If you'd like to contribute to CaptainsMate, feel free to submit a pull request or open an issue on the GitHub repository.

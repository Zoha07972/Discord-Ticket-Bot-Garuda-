# Discord Ticket Bot — Garuda

A lightweight Discord ticketing bot written in Python. Garuda helps server staff manage support tickets by creating private ticket channels, assigning roles, and handling closures.

## Features

- Create private ticket channels via a command or reaction
- Automatic role-based access control for ticket channels
- Close and archive tickets
- Configurable category, role, and command prefix
- Built with discord.py (or nextcord/py-cord — adapt as needed)

## Requirements

- Python 3.10+
- discord.py (or compatible fork) — see `requirements.txt`

## Installation

1. Clone the repository:

   git clone https://github.com/Zoha07972/Discord-Ticket-Bot-Garuda-.git
   cd Discord-Ticket-Bot-Garuda-

2. Create and activate a virtual environment:

   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate

3. Install dependencies:

   pip install -r requirements.txt

## Configuration

The bot uses environment variables or a configuration file to store secrets and IDs. Create a `.env` file or set the following environment variables:

- DISCORD_TOKEN — your bot token
- GUILD_ID — (optional) the ID of the server to operate in
- TICKET_CATEGORY_ID — the category ID where ticket channels will be created
- MOD_ROLE_ID — role ID for moderators who can manage tickets
- PREFIX — command prefix (if the bot uses prefix commands)

Example `.env`:

DISCORD_TOKEN=your_bot_token_here
GUILD_ID=123456789012345678
TICKET_CATEGORY_ID=234567890123456789
MOD_ROLE_ID=345678901234567890
PREFIX=!

If your code uses a JSON/YAML config file, adapt these values accordingly.

## Usage

1. Start the bot:

   python bot.py

2. Common commands (example — adapt to your implementation):

- `!ticket` — open a new ticket
- `!close` — close the ticket and restrict access
- `!claim` — claim the ticket for a staff member

If your bot uses slash commands, register them with Discord and use `/ticket` etc.

## Deploying

- Docker (example):

  Create a Dockerfile and image, then run with environment variables set:

  docker build -t garuda-ticket-bot .
  docker run -d --env-file .env --name garuda garuda-ticket-bot

- Heroku / Railway / other: set the same environment variables in the service dashboard and deploy the repository.

## Contributing

Contributions are welcome. Please open issues for bugs or feature requests and submit pull requests for fixes/enhancements.

- Follow existing code style
- Add tests where appropriate
- Update README with any configuration or usage changes

## Troubleshooting

- Missing permissions: ensure the bot has Manage Channels, Manage Roles, Send Messages, View Channel, and Read Message History.
- Gateway intents: enable the required intents in the developer portal and in your bot code (members intent if you check member roles).

## License

Add a license file (e.g., MIT) if you want to open-source this project. If you already have one, update this section.

## Contact

Created by @Zoha07972. For support, open an issue in this repository.

# Discord Character Bot

A small Discord bot with slash commands for choosing a random character and assigning characters to everyone in your voice channel.

## Commands

- `/random` chooses one random character.
- `/random-from-vc` assigns a unique random character to each user in your current voice channel.
- Sending a message that starts with `cookie` makes the bot reply with `buna ziua`.

## Local Setup

1. Install Python 3.12 or newer.
2. Create and activate a virtual environment.
3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project folder:

   ```env
   DISCORD_TOKEN=your-token
   DISCORD_GUILD_ID=391706676685832195
   ```

5. Run the bot:

   ```powershell
   python main.py
   ```

Do not commit `.env` or your Discord token.

## Discord Setup

In the Discord Developer Portal:

- Regenerate the bot token before using this repo, because the old token was previously in source code.
- Enable the `Message Content Intent` if you want the `cookie` text reply to work.
- Invite the bot with the `bot` and `applications.commands` scopes.

## Deploy To Fly.io

This project includes a `Dockerfile` and `fly.toml`. Fly deploys Dockerfile apps from the project directory and uses `fly.toml` as the app configuration.

1. Install and log in to `flyctl`.
2. Edit `fly.toml` and change `app = "replace-me-discord-bot"` to a unique app name.
3. Create the Fly app without deploying yet:

   ```powershell
   fly launch --no-deploy
   ```

4. Store secrets on Fly:

   ```powershell
   fly secrets set DISCORD_TOKEN="your-new-discord-token"
   fly secrets set DISCORD_GUILD_ID="391706676685832195"
   ```

5. Deploy:

   ```powershell
   fly deploy
   ```

6. Check logs:

   ```powershell
   fly logs
   ```

Discord gateway bots should normally run as one active machine to avoid duplicate command handling. This config has no HTTP service, so Fly creates one running Machine for the process group and may create a stopped standby Machine on first deploy.

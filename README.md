# Furi-sama
A simple discord bot for viewing any given message with [Furigana](https://en.wikipedia.org/wiki/Furigana) added.

## How to set up
1. Install the required dependencies: `pip install -r requirements.txt`
2. Among others, this project depends on the `wkhtmltoimage` binary. Make sure you install it correctly.
2. Create a config file with the following contents:

```ini
[bot]
admins=
token=
# test_guild=
```
where:
* `admins` is a list of admins that are allowed to sync the app_commands with the discord API by pinging the bot and executing the `sync` command.
* `token` is your discord bot token.
* `test_guild` is the guild you're testing the bot in. If this is specified, the app_commands are only synced with that specific guild. If omitted, the app_commands are synced globally. See the discord API reference for more details.

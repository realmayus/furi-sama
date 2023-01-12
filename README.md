# Furi-sama
A simple discord bot for viewing any given message with [Furigana](https://en.wikipedia.org/wiki/Furigana) added.
If you have the option, please consider hosting your own instance of the bot as the image-generation is a resource-intensive task.
## Hosting your own instance
### Docker
You can use the Dockerfile in the repo to automatically install everything.
As the project depends on `wkhtmltoimage`, you will need to make sure the correct binary for your platform is being installed. The `Dockerfile` ships with a binary for **`amd64`-based systems**.
You can find other download URLs [here](https://wkhtmltopdf.org/downloads.html). Make sure to download the debain buster build for your platform.

First, you need to build the image. You can do that with the following command:
```shell
sudo docker build --tag furisama .
```
Create a local secrets folder with a file `config.ini` with the following contents:
```ini
[bot]
admins=
token=
```
where:
* `admins` is a comma-separated list of admins that are allowed to sync the app_commands with the discord API by pinging the bot and executing the `sync` command.
* `token` is your discord bot token.

Then, mount the secrets folder (we assume it's located at `$HOME/secrets` in this example) as a virtual volume and start the container with this command:
```shell
sudo docker run -v $HOME/secrets:/app/secrets:ro --name furisama furisama
```
### Manual setup
1. Install the required dependencies: `pip install -r requirements.txt`
2. Among others, this project depends on the `wkhtmltoimage` binary. Make sure you install it correctly.
2. Create a config file at `./secrets/` with the following contents:

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

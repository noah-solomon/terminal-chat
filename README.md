# TerminalChat

Simple terminal chat backend and CLI to send messages.

## CLI installation

`pip install TerminalChat` (Hosted on [PyPi](https://pypi.org/project/TerminalChat/))

## CLI Usage
Usage: `tchat [OPTIONS] COMMAND [ARGS]`

Commands:
- `tchat read`     Command to get unread messages, use `-a` or `--all` to get all messages.
- `tchat send`     Command to send a message. CLI walks through the steps.
- `tchat sign-up`  Command to sign up for the first time.

## Run backend locally (optional)

TerminalChat backend is hosted on Azure, so no need to run your own server (unless you want to).

1. Clone repo with `git clone git@github.com:noah-solomon/terminal-chat.git`
2. Enter backend directory with `cd terminal-chat/backend/src`

### With Docker
3. Create & run Docker container with `docker-compose up -d`

### Without Docker
3. Make a virtual environment with `python3 -m venv venv`
4. Activate your virtual environment with `source venv/bin/activate` (Mac)
5. Install requirements with `pip install requirements.txt`
6. Run server with `python3 app.py`


"""
Managing the server and it's database.
"""
from flask.ext.script import Manager, Shell, Server
from server import APP


MANAGER = Manager(APP)

# mangaer commands
MANAGER.add_command("runserver", Server())
MANAGER.add_command("shell", Shell(make_context={"app": APP}))


if __name__ == "__main__":
    MANAGER.run()

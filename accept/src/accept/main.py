import typer

from bot.bot import Bot
from bot.browser import start_browser
from bot.main import app as automation_app

app = typer.Typer()

app.add_typer(automation_app)


def main():
    app()

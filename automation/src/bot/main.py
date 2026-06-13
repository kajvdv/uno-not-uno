import typer

from bot.browser import start_browser

app = typer.Typer()

@app.command()
def startbrowser(port: int, user: str):
    driver = start_browser(port, user)
    while True:
        try:
            _ = driver.current_url
        except Exception:
            break


def main():
    app()
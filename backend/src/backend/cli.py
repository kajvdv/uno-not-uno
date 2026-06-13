import typer


app = typer.Typer()


@app.callback()
def callback():
    pass


@app.command("list")
def list_lobbies():
    print("hello")


def main():
    app()


if __name__ == "__main__":
    main()
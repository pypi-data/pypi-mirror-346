import typer


app = typer.Typer()


@app.callback()
def callback():
    """
    Curuba 
    """

@app.command()
def welcome():
    """
    Welcome
    """
    typer.echo("Welcome to curuba")

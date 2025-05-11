import typer


app = typer.Typer()


@app.callback()
def callback():
    """
    tpal 
    """


@app.command()
def welcome():
    """
    Welcome 
    """
    typer.echo("Welcome to tpal")

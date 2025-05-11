import typer


app = typer.Typer()


@app.callback()
def callback():
    """
    Claro 
    """


@app.command()
def welcome():
    """
    Welcome 
    """
    typer.echo("Welcome")

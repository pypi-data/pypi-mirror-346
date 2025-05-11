import typer


app = typer.Typer()


@app.callback()
def callback():
    """
    Paana tool 
    """


@app.command()
def welcome():
    """
    Welcome 
    """
    typer.echo("Welcome to the paana experience")


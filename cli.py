import os
import subprocess
import sys
import typer

app = typer.Typer(help="CLI para el proyecto FastAPI + GraphQL")

VENV_DIR = "venv"
PYTHON = sys.executable


@app.command()
def create_venv():
    """
    Crea un entorno virtual llamado 'venv'
    """
    if os.path.exists(VENV_DIR):
        typer.echo("✅ El entorno virtual ya existe.")
    else:
        typer.echo("⚙️  Creando entorno virtual...")
        subprocess.run([PYTHON, "-m", "venv", VENV_DIR])
        typer.echo("✅ Entorno virtual creado en './venv'")


# @app.command()
# def run():
#     """
#     Activa el entorno virtual y ejecuta Uvicorn
#     """
#     if not os.path.exists(VENV_DIR):
#         typer.echo("❌ El entorno virtual no existe. Ejecuta primero 'create-venv'.")
#         raise typer.Exit()

#     activate_script = (
#         os.path.join(VENV_DIR, "Scripts", "activate")
#         if os.name == "nt"
#         else os.path.join(VENV_DIR, "bin", "activate")
#     )

#     typer.echo("🚀 Activando entorno virtual y corriendo Uvicorn...")
#     shell_command = f"{activate_script} && uvicorn main:app --reload"

#     # Ejecutar en una nueva shell
#     subprocess.run(
#         shell_command, shell=True, executable="/bin/bash" if os.name != "nt" else None
#     )


@app.command()
def run():
    subprocess.run(["uvicorn", "app.api.main:app", "--reload"])


if __name__ == "__main__":
    app()

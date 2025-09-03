import pathlib
import subprocess
import argparse
import logging
import time
import os
import r2bac.settings as sg

logging.basicConfig(encoding="utf-8",level=logging.INFO,format="%(levelname)s : %(message)s")
ignore_dirs = ["libs"] # Les dossier qui sont ignoré lors de la compilation
app_dirs = sg.INSTALLED_APPS.copy()
app_dirs.append(sg.PROJECT_NAME.lower())

args = argparse.ArgumentParser(description="Compilateur de static django pour SCSS")
args.add_argument("source",type=str,help="Le dossier contenant toutes les applications django")
args.add_argument("-w","--watch",action='store_true',help="Ecouteur d'évenemment permettant de compilé à chaque modification d'un fichier dans un dossier source.")
args = args.parse_args()


def validate(path:pathlib.Path):
  if not path.is_dir():
    logging.error(f"Le répertoire {path.absolute()} n'as pas été trouvée. Vérifier que le chemin est valide et qu'il s'agit bien d'un dossier")
    exit(1)
  return path

source_dir:pathlib.Path = validate(pathlib.Path(args.source))


def compile_apps(apps:pathlib.Path):
  for app in apps.iterdir():
    if not app.is_dir():
      continue
    
    if not app.name in app_dirs:
      continue
    
    

    scss = pathlib.Path(app / "static" / app.name / "scss")
    scss.mkdir(parents=True,exist_ok=True)

    utils = pathlib.Path(source_dir / "r2bac/static/scss/utils/")
    subprocess.run(["cp","-ru",utils,pathlib.Path(scss)])
    
    css = pathlib.Path(app / "static" / app.name /"css")
    css.mkdir(parents=True,exist_ok=True)
    

    compile(scss,css)
    scss_public = pathlib.Path(app / "static" / "scss")
    if scss_public.is_dir():
      css_public = pathlib.Path(app / "static" / "css")
      css_public.mkdir(exist_ok=True)
      compile(scss_public,css_public)

files = {}
def compile(source:pathlib.Path,destination:pathlib.Path):
  for file in source.iterdir():
    if file.is_dir() and not file.name in ignore_dirs: # Récursivité dans les dossier
      compile(file.absolute(),pathlib.Path(destination / file.name).absolute())
    
    # Vérifie si le fichier est un .scss et que ce n'es pas un module '_'
    if not file.name.endswith(".scss") or file.name.startswith("_"):
      continue

    # Récupère la date de la dernière modification
    last_edit = os.path.getmtime(file)
    # Récupère la date de la dernière modification dans l'historique
    history_last_edit = files.get(file)
    if not history_last_edit is None and history_last_edit >= last_edit: # Vérifie si le fichier n'as pas subit de modification
      continue

    logging.debug(f"Dernière mise à jour du fichier : {last_edit}")
    logging.debug(f"Mise à jour dans l'histoirique : {history_last_edit}")
    
    files.update({file:last_edit})
    sortie = subprocess.run(["sass",file.absolute(),f"{pathlib.Path(destination.absolute() / file.stem)}.css","--no-source-map"],capture_output=True,text=True)
    if not sortie.stdout is None:
      logging.info(sortie.stdout if sortie.stdout != "" else f"Fichier {file} à été compilée avec succès")
    if sortie.stderr:
      logging.error(sortie.stderr)

  return None

def main():
  if args.watch:
    logging.info("Le Mode Watch à été activée")
    while True:
      try:
        time.sleep(0.5)
        compile_apps(source_dir)
      except KeyboardInterrupt:
        logging.info("Opération terminée")
        exit(0)
  else:
    compile_apps(source_dir)
  logging.info("Opération terminée")

if __name__ == "__main__":
  main()
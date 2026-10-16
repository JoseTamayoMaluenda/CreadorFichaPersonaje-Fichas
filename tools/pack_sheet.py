"""Package a character sheet, its backgrounds and a preview for the public catalogue."""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('sheet', type=Path)
parser.add_argument('images', type=Path)
parser.add_argument('--id', required=True)
parser.add_argument('--author', required=True)
parser.add_argument('--preview', type=Path, required=True)
parser.add_argument('--description', default='')
parser.add_argument('--version', type=int, default=1)
args = parser.parse_args()
if not re.fullmatch(r'[A-Za-z0-9_-]{1,100}', args.id):
    parser.error('El identificador solo puede contener letras, números, guiones y guiones bajos.')
root = Path(__file__).resolve().parent.parent
sheet = json.loads(args.sheet.read_text(encoding='utf-8-sig'))
images = set()
def collect(page):
    if page.get('backgroundImage'):
        images.add(page['backgroundImage'])
    images.update(g['backgroundImage'] for g in page.get('groups', []) if g.get('backgroundImage'))
    for child in page.get('extraPages', []):
        collect(child)
collect(sheet)
for name in images:
    if Path(name).name != name or not (args.images / name).is_file():
        parser.error('Falta una imagen o su nombre no es válido: ' + name)
(root / 'packages').mkdir(exist_ok=True)
(root / 'previews').mkdir(exist_ok=True)
package = root / 'packages' / (args.id + '.ficha')
with ZipFile(package, 'w', ZIP_DEFLATED) as bundle:
    bundle.writestr('manifest.json', json.dumps({'format': 'creador-ficha', 'version': 1, 'sheet': 'sheet.json'}))
    bundle.writestr('sheet.json', json.dumps(sheet, ensure_ascii=False))
    for image in sorted(images):
        bundle.write(args.images / image, 'images/' + image)
preview = root / 'previews' / (args.id + args.preview.suffix.lower())
if args.preview.resolve() != preview.resolve():
    shutil.copyfile(args.preview, preview)
index_path = root / 'catalog.json'
index = json.loads(index_path.read_text(encoding='utf-8-sig')) if index_path.exists() else {'format': 'creador-ficha-catalogue', 'version': 1, 'sheets': []}
entry = {'id': args.id, 'name': sheet['name'], 'author': args.author, 'gamebook': sheet.get('gamebook', ''),
         'description': args.description, 'version': args.version, 'package': package.relative_to(root).as_posix(),
         'thumbnail': preview.relative_to(root).as_posix(), 'sha256': hashlib.sha256(package.read_bytes()).hexdigest()}
index['sheets'] = [row for row in index['sheets'] if row['id'] != args.id] + [entry]
index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Ficha preparada:', entry['name'])

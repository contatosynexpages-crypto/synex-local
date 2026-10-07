# Reduz out/*@2x.png para 1080x1350 (formato do feed) e salva como out/<slug>.png
import glob, os
from PIL import Image
aqui = os.path.dirname(os.path.abspath(__file__))
for f in sorted(glob.glob(os.path.join(aqui, 'out', '*@2x.png'))):
    Image.open(f).convert('RGB').resize((1080, 1350), Image.LANCZOS).save(f.replace('@2x', ''), optimize=True)
    print('ok', os.path.basename(f).replace('@2x', ''))

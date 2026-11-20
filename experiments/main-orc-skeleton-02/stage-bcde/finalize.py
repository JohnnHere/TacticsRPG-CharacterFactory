from pathlib import Path
from PIL import Image,PngImagePlugin
import html,json
E=Path('experiments/main-orc-skeleton-02/stage-bcde')
# Text metadata only; assert decoded RGBA is unchanged after the write.
for folder in ['body-only','weapon-only','composite','evidence']:
 for p in (E/folder).glob('*.png'):
  im=Image.open(p);before=im.convert('RGBA').tobytes();meta=PngImagePlugin.PngInfo()
  text='Aseprite Lua composition/export of inherited Orc body and official Recruit Sword; no external raster retouch.'
  if folder=='evidence':text='Script-made inspection preview (nearest-neighbour 8x where indicated) of Aseprite Lua composition; no source-art change.'
  meta.add_text('Provenance',text);meta.add_text('ArtisticStatus','VISUAL_REVIEW_REQUIRED / PENDING_CREATOR');im.save(p,pnginfo=meta)
  assert Image.open(p).convert('RGBA').tobytes()==before
parts=['<!doctype html><meta charset="utf-8"><title>Experimento 02 — B/C/D/E</title><style>body{background:#242830;color:#eee;font:16px system-ui;margin:24px}section{margin:28px 0}figure{display:inline-block;margin:5px;vertical-align:top}img{image-rendering:pixelated;background:repeating-conic-gradient(#51565d 0 25%,#444950 0 50%) 0/16px 16px}figcaption{max-width:320px;font-size:13px}a{color:#9dd5ff}</style><h1>Experimento 02 — back_l / Sword</h1><p>VISUAL_REVIEW_REQUIRED · PENDING_CREATOR. <a href="report.md">Relatório</a> · <a href="attachment.json">Contrato de ligação</a></p><p>Autoria/composição programática no Aseprite sobre arte herdada. 00 e 13: arma montada somente para diagnóstico, sem alteração do intervalo de produção.</p>']
for i in [0,5,8,9,13]:
 parts.append(f'<section><h2>Quadro {i:02}</h2>')
 for n in ['body-only','weapon-only','composite']:
  parts.append(f'<figure><img width="256" height="256" src="{n}/{i:02}.png"><figcaption>{i:02} {n}: composto/exportado por Lua no Aseprite; corpo herdado sem retoque.</figcaption></figure>')
 parts.append('<div>')
 for n in ['body-only','weapon-only','composite']:
  parts.append(f'<figure><img width="320" height="320" src="evidence/{i:02}-{n}-hand-wrist-8x.png"><figcaption>{n}: mão/punho, recorte por script em 8×; pixels da composição Aseprite.</figcaption></figure>')
 parts.append('</div></section>')
(E/'review.html').write_text('\n'.join(parts),encoding='utf-8')

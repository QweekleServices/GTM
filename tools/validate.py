#!/usr/bin/env python3
"""
Validateur des modules GTM Qweekle.

Usage :  python tools/validate.py
Sortie :  code 0 si tout est valide, 1 sinon.

Verifie :
  1. Les 4 JSON sont valides, et les folders declares sont bien references.
  2. Le tag Consent Mode Default se declenche AVANT le tag CMP Update.
  3. Le tag CMP reste du JS valide dans l'etat livre (tous les blocs commentes).
  4. Aucun commentaire /* */ imbrique (JS ne les imbrique pas : le bloc se
     refermerait trop tot et le tag entier serait casse).
  5. Chaque bloc CMP reste du JS valide une fois decommente, en suivant
     exactement la procedure du README (retirer les /* et */ du bloc).
  6. Les extraits de code du README sont des copies exactes du JSON.
"""
import json, re, subprocess, sys, tempfile, textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULES = ['qweekle-1-base.json', 'qweekle-2-ga4.json',
           'qweekle-3-meta.json', 'qweekle-4-ads.json']
CMP_BLOCKS = ['AXEPTIO', 'DIDOMI', 'COOKIEBOT', 'COOKIEYES']

errors, checks = [], 0


def fail(msg):
    errors.append(msg)


def ok(msg):
    global checks
    checks += 1
    print(f'  OK   {msg}')


def node_check(js, label):
    """Verifie la syntaxe JS via node --check. Ignore si node absent."""
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False,
                                     encoding='utf-8') as fh:
        fh.write(js)
        path = fh.name
    try:
        r = subprocess.run(['node', '--check', path],
                           capture_output=True, text=True)
    except FileNotFoundError:
        print(f'  SKIP {label} (node introuvable)')
        return None
    finally:
        Path(path).unlink(missing_ok=True)
    if r.returncode != 0:
        first = (r.stderr.strip().split('\n') or [''])[:4]
        fail(f'{label} : JS invalide\n         ' + '\n         '.join(first))
        return False
    ok(label)
    return True


def cmp_tag_html():
    cv = json.loads((ROOT / 'qweekle-1-base.json').read_text(encoding='utf-8'))
    tag = next(t for t in cv['containerVersion']['tag']
               if 'CMP Update' in t['name'])
    return next(p for p in tag['parameter'] if p['key'] == 'html')['value']


def block_bounds(src, name):
    """Position du bloc CMP `name` : (debut du /*, debut du */).

    La banniere `// NOM` doit etre HORS du commentaire, sinon decommenter
    le bloc laisse les lignes `====` en code nu et casse tout le tag.
    """
    i = src.find('// ' + name)
    if i < 0:
        return None
    s = src.find('/*', i)
    e = src.find('*/', s) if s >= 0 else -1
    if s < 0 or e < 0:
        return None
    return s, e


def block_body(html, name):
    """Corps d'un bloc CMP, sans les delimiteurs de commentaire."""
    b = block_bounds(html, name)
    if b is None:
        return None
    s, e = b
    return textwrap.dedent(html[s + 2:e].strip('\n')).rstrip()


print('\n== 1. Structure des modules ==')
for m in MODULES:
    p = ROOT / m
    try:
        cv = json.loads(p.read_text(encoding='utf-8'))['containerVersion']
    except Exception as exc:
        fail(f'{m} : JSON illisible ({exc})')
        continue
    folders = {f['folderId']: f['name'] for f in cv.get('folder', [])}
    used = {e.get('parentFolderId')
            for k in ('tag', 'trigger', 'variable') for e in cv.get(k, [])}
    orphan = [f'{i} "{n}"' for i, n in folders.items() if i not in used]
    if orphan:
        fail(f'{m} : folder declare mais jamais utilise : {", ".join(orphan)}')
    else:
        ok(f'{m} ({len(cv.get("tag", []))} tags, {len(cv.get("trigger", []))} '
           f'triggers, {len(cv.get("variable", []))} variables)')

print('\n== 2. Ordre de declenchement du Consent Mode ==')
_cv = json.loads((ROOT / 'qweekle-1-base.json').read_text(encoding='utf-8'))
_tags = {t['name']: t for t in _cv['containerVersion']['tag']}


def _priority(tag):
    p = tag.get('priority')
    return int(p['value']) if isinstance(p, dict) else 0


_default = next((t for n, t in _tags.items() if n.endswith('Consent Mode - Default')), None)
_update = next((t for n, t in _tags.items() if 'CMP Update' in n), None)
if _default is None or _update is None:
    fail('tags Consent Mode Default / CMP Update introuvables')
else:
    pd, pu = _priority(_default), _priority(_update)
    if pd <= pu:
        fail(f'Consent Mode : Default (priorite {pd}) doit se declencher AVANT '
             f'CMP Update (priorite {pu}). Dans GTM la priorite la plus haute '
             'passe en premier : remonter celle du tag Default.')
    else:
        ok(f'Default (priorite {pd}) se declenche avant CMP Update ({pu})')

print('\n== 3. Tag CMP : etat livre ==')
html = cmp_tag_html()
js = html.replace('<script>', '').replace('</script>', '')
node_check(js, 'etat livre (tous les blocs commentes)')

active = re.sub(r'/\*.*?\*/', '', js, flags=re.S)
active = re.sub(r'^\s*//.*$', '', active, flags=re.M)
if 'qweekleUpdateConsent' not in active:
    fail('la fonction commune qweekleUpdateConsent() est commentee — '
         'elle doit rester active')
else:
    ok('la partie commune reste active')

print('\n== 4. Commentaires imbriques ==')
nested, i = [], 0
while (s := html.find('/*', i)) >= 0:
    e = html.find('*/', s + 2)
    if e < 0:
        fail('commentaire /* non ferme')
        break
    if html.find('/*', s + 2, e) >= 0:
        nested.append(html[:s].count('\n') + 1)
    i = e + 2
if nested:
    fail('commentaire /* */ imbrique ligne(s) ' + ', '.join(map(str, nested))
         + ' — le bloc se refermerait trop tot')
else:
    ok('aucun commentaire imbrique')

print('\n== 5. Procedure du README : decommenter un bloc ==')
for name in CMP_BLOCKS:
    b = block_bounds(js, name)
    if b is None:
        fail(f'{name} : banniere "// {name}" introuvable hors commentaire. '
             'Elle doit preceder le /* du bloc, sinon decommenter laisse '
             'les lignes "====" en code nu et casse tout le tag.')
        continue
    s, e = b
    node_check(js[:s] + js[s + 2:e] + js[e + 2:], f'{name} decommente')

print('\n== 6. Extraits README vs source JSON ==')
readme = (ROOT / 'README.md').read_text(encoding='utf-8')
sec = readme[readme.index('### 4.1 Consent Mode'):readme.index('### 4.2 Google Ads')]
fences = re.findall(r'```javascript\n(.*?)```', sec, re.S)
if len(fences) < 5:
    fail(f'section 4.1 : {len(fences)} blocs de code, 5 attendus '
         '(fonction commune + 4 CMP)')
else:
    for name, snippet in zip(CMP_BLOCKS, fences[1:]):
        body = block_body(html, name)
        if body is None:
            continue
        if snippet.rstrip() != body:
            fail(f'README section 4.1 : le bloc {name} a derive du JSON — '
                 'regenerer depuis qweekle-1-base.json')
        else:
            ok(f'README {name} identique au JSON')

print('\n' + '=' * 60)
if errors:
    print(f'ECHEC : {len(errors)} probleme(s)\n')
    for e in errors:
        print(f'  - {e}')
    sys.exit(1)
print(f'OK : {checks} verifications passees')

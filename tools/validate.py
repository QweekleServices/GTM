#!/usr/bin/env python3
"""
Validateur des modules GTM Qweekle.

Usage :  python tools/validate.py
Sortie :  code 0 si tout est valide, 1 sinon.

Verifie :
  1. Les 4 JSON sont valides, et les folders declares sont bien references.
  2. Le module Base ne contient aucun tag de consentement : le consentement
     (defaut et mises a jour) est gere par le modele GTM de la CMP, seul
     capable de poser les etats par defaut a temps.
  3. Les balises d'arrivee (GA4, Google Ads, Meta) se declenchent une fois
     par page sur des declencheurs conditionnes a l'etat du consentement
     (modele GTM Consent State), definis a l'identique dans chaque module
     et documentes dans le README.
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULES = ['qweekle-1-base.json', 'qweekle-2-ga4.json',
           'qweekle-3-meta.json', 'qweekle-4-ads.json']

errors, checks = [], 0


def fail(msg):
    errors.append(msg)


def ok(msg):
    global checks
    checks += 1
    print(f'  OK   {msg}')


def container(m):
    return json.loads((ROOT / m).read_text(encoding='utf-8'))['containerVersion']


print('\n== 1. Structure des modules ==')
for m in MODULES:
    try:
        cv = container(m)
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

print('\n== 2. Consentement gere par la CMP ==')
_consent_tags = [t['name'] for t in container('qweekle-1-base.json').get('tag', [])
                 if 'consent' in t['name'].lower()]
if _consent_tags:
    fail('module Base : tag(s) de consentement a retirer, le modele GTM de la '
         'CMP pose le consentement : ' + ', '.join(_consent_tags))
else:
    ok('module Base sans tag de consentement')

print('\n== 3. Balises d arrivee conditionnees au consentement ==')
# Une balise "Une fois par page" bloquee par le consentement est consideree
# comme deja declenchee par GTM : la condition de consentement doit donc etre
# portee par le declencheur (variables GTM Consent State), pas seulement par
# les parametres de consentement de la balise.
ARRIVAL = {
    'Qweekle - CE - Arrivee analytics accorde': ['analytics_storage'],
    'Qweekle - CE - Arrivee publicite accordee': ['ad_storage', 'ad_user_data'],
}
LANDING = {
    'qweekle-2-ga4.json': {
        '[GA4] Configuration': 'Qweekle - CE - Arrivee analytics accorde'},
    'qweekle-3-meta.json': {
        '[Meta] Pixel Base + PageView': 'Qweekle - CE - Arrivee publicite accordee'},
    'qweekle-4-ads.json': {
        '[Google Ads] Configuration': 'Qweekle - CE - Arrivee publicite accordee',
        '[Google Ads] Conversion Linker': 'Qweekle - CE - Arrivee publicite accordee'},
}
CONSENT_TEMPLATE = 'M6BW3'  # GTM Consent State (Ayudante), galerie
readme = (ROOT / 'README.md').read_text(encoding='utf-8')

definitions = {}
for m in MODULES:
    cv = container(m)
    trig = {t['name']: t for t in cv.get('trigger', [])}
    variables = {v['name']: v for v in cv.get('variable', [])}
    templates = {c.get('galleryReference', {}).get('galleryTemplateId')
                 for c in cv.get('customTemplate', [])}
    if m == 'qweekle-1-base.json':
        needed = set(ARRIVAL)
    else:
        needed = set(LANDING.get(m, {}).values())
    for name in sorted(needed):
        t = trig.get(name)
        if t is None:
            fail(f'{m} : declencheur "{name}" absent')
            continue
        definitions.setdefault(name, {})[m] = json.dumps(
            [t.get('customEventFilter'), t.get('filter')], sort_keys=True)
        tested = [p['value'] for f in t.get('filter', [])
                  for p in f['parameter'] if p['key'] == 'arg0']
        for consent_type in ARRIVAL[name]:
            var = f'Qweekle - CONSENT - {consent_type}'
            v = variables.get(var)
            params = {p['key']: p.get('value') for p in (v or {}).get('parameter', [])}
            if v is None or v['type'] != 'cvt_' + CONSENT_TEMPLATE:
                fail(f'{m} : variable "{var}" absente ou pas basee sur GTM Consent State')
            elif params.get('selectTarget') != 'any' or params.get('getType') != consent_type:
                fail(f'{m} : variable "{var}" mal parametree ({params})')
            elif '{{' + var + '}}' not in tested:
                fail(f'{m} : "{name}" ne teste pas {var}')
        if CONSENT_TEMPLATE not in templates:
            fail(f'{m} : modele GTM Consent State (galerie {CONSENT_TEMPLATE}) non embarque')
    for tag_name, trig_name in LANDING.get(m, {}).items():
        tag = next((t for t in cv.get('tag', []) if t['name'] == tag_name), None)
        if tag is None or trig_name not in trig:
            fail(f'{m} : tag {tag_name} ou declencheur {trig_name} introuvable')
            continue
        if tag.get('firingTriggerId') != [trig[trig_name]['triggerId']]:
            fail(f'{m} : {tag_name} doit se declencher uniquement sur "{trig_name}" '
                 '(All Pages le bloquerait definitivement pour un nouveau visiteur)')
        elif tag.get('tagFiringOption') != 'ONCE_PER_LOAD':
            fail(f'{m} : {tag_name} doit etre "Une fois par page" (ONCE_PER_LOAD)')
        else:
            ok(f'{m} : {tag_name} sur "{trig_name}", une fois par page')

for name, per_module in definitions.items():
    if len(set(per_module.values())) > 1:
        fail(f'"{name}" defini differemment selon les modules : {sorted(per_module)}')
        continue
    event_filter = json.loads(next(iter(per_module.values())))[0]
    regex = next((p['value'] for f in event_filter for p in f['parameter']
                  if p['key'] == 'arg1'), '')
    if not all(e in regex for e in ('gtm\\.js', 'cookie_consent_update')):
        fail(f'"{name}" doit ecouter gtm.js et cookie_consent_update')
    elif regex not in readme:
        fail(f'README : expression de "{name}" absente ou differente du JSON ({regex})')
    else:
        ok(f'"{name}" identique dans {len(per_module)} modules et le README')

print('\n' + '=' * 60)
if errors:
    print(f'ECHEC : {len(errors)} probleme(s)\n')
    for e in errors:
        print(f'  - {e}')
    sys.exit(1)
print(f'OK : {checks} verifications passees')

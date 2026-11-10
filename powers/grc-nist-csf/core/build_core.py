"""Convierte la exportación oficial del CPRT (csf-2.0-core-cprt.json) en CSV y Markdown legibles."""
import csv, json, collections
src = json.load(open('csf-2.0-core-cprt.json'))['response']['elements']
els, rel = src['elements'], src['relationships']
by_id = {e['element_identifier']: e for e in els}
withdrawn = {r['source_element_identifier']: by_id[r['dest_element_identifier']]['text']
             for r in rel if r['dest_element_identifier'].startswith('WR-')}
order = {e['element_identifier'][2:]: e['title'] for e in els if e['element_type'] == 'sort'}
key = lambda i: order.get(i, '99999')
funcs = sorted([e for e in els if e['element_type'] == 'function'], key=lambda e: key(e['element_identifier']))
cats = sorted([e for e in els if e['element_type'] == 'category' and e['element_identifier'] not in withdrawn], key=lambda e: key(e['element_identifier']))
subs = sorted([e for e in els if e['element_type'] == 'subcategory' and e['element_identifier'] not in withdrawn], key=lambda e: key(e['element_identifier']))
ex = collections.defaultdict(list)
for e in sorted((e for e in els if e['element_type'] == 'implementation_example'), key=lambda e: e['element_identifier']):
    ex[e['element_identifier'].rsplit('.', 1)[0]].append(e['text'])
cat_t = {c['element_identifier']: c for c in cats}
fun_t = {f['element_identifier']: f for f in funcs}

with open('csf-2.0-core.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['function', 'function_title', 'category', 'category_title', 'subcategory', 'subcategory_text', 'implementation_examples'])
    for s in subs:
        sid = s['element_identifier']; cid = sid.split('-')[0]; fid = cid.split('.')[0]
        w.writerow([fid, fun_t[fid]['title'], cid, cat_t[cid]['title'], sid, s['text'], ' | '.join(ex[sid])])

with open('withdrawn-v1.1.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['identifier_v1.1', 'title_or_text_v1.1', 'reason'])
    for i in sorted(withdrawn):
        w.writerow([i, by_id[i]['title'] or by_id[i]['text'], withdrawn[i]])

with open('csf-2.0-core.md', 'w') as f:
    f.write('# NIST CSF 2.0 Core (copia exportada)\n\n')
    f.write('Generado con `build_core.py` desde la exportación oficial del CPRT de NIST '
            '(`csf-2.0-core-cprt.json`). Textos en inglés, tal como los publica NIST. '
            'Fuente: <https://csrc.nist.gov/projects/cprt>\n\n')
    f.write(f'Funciones: {len(funcs)} · Categorías: {len(cats)} · Subcategorías vigentes: {len(subs)}\n\n')
    for fn in funcs:
        fid = fn['element_identifier']
        f.write(f"## {fid} {fn['title']}\n\n{fn['text']}\n\n")
        for c in (c for c in cats if c['element_identifier'].split('.')[0] == fid):
            cid = c['element_identifier']
            f.write(f"### {cid} {c['title']}\n\n{c['text']}\n\n")
            for s in (s for s in subs if s['element_identifier'].split('-')[0] == cid):
                sid = s['element_identifier']
                f.write(f"- **{sid}**: {s['text']}\n")
                for t in ex[sid]:
                    f.write(f"  - Ejemplo: {t}\n")
            f.write('\n')
print(len(funcs), len(cats), len(subs), len(withdrawn))

from pathlib import Path
import csv,json,math,hashlib
from datetime import date,timedelta
from collections import Counter
root=Path(__file__).resolve().parent.parent; p=root/'data'
def read(name):return list(csv.DictReader((p/name).open(encoding='utf-8-sig')))
raw=read('kobis_daily_top10.csv');derived=read('movie_daily_features.csv')
lookup={(r['movieCd'],date.fromisoformat(r['date'][:10])):r for r in raw}
assert len(lookup)==len(raw)==140
holidays={date(2026,9,24),date(2026,9,25),date(2026,9,26),date(2026,10,3),date(2026,10,5)}
computed={};verified=0
for r in raw:
    day=date.fromisoformat(r['date'][:10]);opened=date.fromisoformat(r['openDt'][:10]);key=(r['movieCd'],day)
    c={'eligible':False,'same_holiday':False}
    for lag,suffix in [(1,'dod'),(7,'wow')]:
        before=lookup.get((r['movieCd'],day-timedelta(days=lag)))
        if not before:continue
        fields={x:(float(r[x])/float(before[x])-1)*100 for x in ['audiCnt','scrnCnt','showCnt']}
        fields['audience_per_show']=(float(r['audiCnt'])/float(r['showCnt']))/(float(before['audiCnt'])/float(before['showCnt']))*100-100
        fields['rank_gain']=float(before['rank'])-float(r['rank'])
        got=next(g for g in derived if g['movieCd']==r['movieCd'] and g['date'][:10]==r['date'][:10])
        for field,value in fields.items():
            column='rank_gain_'+suffix if field=='rank_gain' else field+'_growth_'+suffix+'_pct'
            assert math.isclose(float(got[column]),value,abs_tol=1e-8), (key,column)
        verified+=1
        if lag==7:
            c.update(fields);c['eligible']=(day-opened).days>=7
            c['same_holiday']=(day in holidays)==(day-timedelta(days=7) in holidays)
    computed[key]=c
eligible={k:v for k,v in computed.items() if v['eligible']}
same={k:v for k,v in eligible.items() if v['same_holiday']}
sensitivity=read('candidate_sensitivity.csv')
for row in sensitivity:
    pool=same if row['scope']=='공휴일 여부 동일' else eligible
    threshold=float(row['threshold_pct_strictly_above']);rule=row['rule'];minimum=int(row['minimum_consecutive_days'])
    selected=set()
    for key,c in pool.items():
        if rule!='회당 관객' and c['audiCnt']<=threshold:continue
        if '회당 관객' in rule and c['audience_per_show']<=threshold:continue
        if '순위' in rule and c['rank_gain']<=0:continue
        selected.add(key)
    retained=set()
    for key in selected:
        code,day=key;length=1
        for direction in [-1,1]:
            offset=direction
            while (code,day+timedelta(days=offset)) in selected:
                length+=1;offset+=direction
        if length>=minimum:retained.add(key)
    assert len(retained)==int(row['selected_movie_days'])
    assert len({k[0] for k in retained})==int(row['selected_films'])
    assert len(pool)==int(row['eligible_rows'])
manifest=json.loads((p/'source_manifest.json').read_text(encoding='utf-8'))
assert all(hashlib.sha256((p/name).read_bytes()).hexdigest()==expected for name,expected in manifest['sha256'].items())
result={'raw_rows':len(raw),'films':len({r['movieCd'] for r in raw}),'lag_pair_checks':verified,
        'wow_pairs':sum('audiCnt' in v for v in computed.values()),'eligible_pairs':len(eligible),'holiday_same_pairs':len(same),
        'holiday_same_dates':dict(Counter(str(k[1]) for k in same)),
        'holiday_same_holiday_rows':sum(k[1] in holidays for k in same),
        'audience_positive':sum(v['audiCnt']>0 for v in eligible.values()),
        'efficiency_positive':sum(v['audience_per_show']>0 for v in eligible.values()),
        'sensitivity_checks':len(sensitivity),'hash_checks':len(manifest['sha256'])}
(root/'docs/검증_결과.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))

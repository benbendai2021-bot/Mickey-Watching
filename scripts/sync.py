#!/usr/bin/env python3
import json,datetime,pathlib,re,urllib.request
ROOT=pathlib.Path(__file__).resolve().parent.parent/'data'
def get(n):return json.loads((ROOT/n).read_text())
def put(n,obj):(ROOT/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
def fetch(url,payload=None):
 headers={'User-Agent':'Mozilla/5.0','Content-Type':'application/json','Referer':'https://leetcode.com/'}
 request=urllib.request.Request(url,data=json.dumps(payload).encode() if payload else None,headers=headers)
 with urllib.request.urlopen(request,timeout=30) as response:return json.load(response)
config=get('config.json');history=get('history.json');status=get('status.json')
warnings=[]
try:
 raw=fetch('https://raw.githubusercontent.com/krmanik/Anki-NeetCode/main/neetcode-150-list.json')
 topics=[]
 for name,entries in raw.items():
  problems=[]
  for title,item in entries.items():
   url=item.get('url','')
   slug=url.split('/problems/')[1].split('/')[0] if '/problems/' in url else re.sub('[^a-z0-9]+','-',title.lower()).strip('-')
   problems.append({'title':title,'slug':slug,'difficulty':item.get('difficulty','Unknown'),'url':url or 'https://leetcode.com/problems/'+slug+'/'})
  topics.append({'name':name,'problems':problems})
 if len(topics)!=18 or sum(len(t['problems']) for t in topics)!=150:raise ValueError('Unexpected topic/problem count')
 put('problems.json',{'topics':topics,'fetchedAt':datetime.datetime.now(datetime.timezone.utc).isoformat()})
except Exception as ex:warnings.append('Roadmap: '+str(ex)[:160])
try:
 query='query progress($username:String!){ matchedUser(username:$username){username submitStatsGlobal {acSubmissionNum{difficulty count}} submissionCalendar} recentAcSubmissionList(username:$username,limit:20){titleSlug timestamp}}'
 payload={'query':query,'variables':{'username':config['leetcodeUsername']}}
 data=fetch('https://leetcode.com/graphql/',payload)
 if data.get('errors'):raise ValueError(str(data['errors'])[:160])
 d=data['data'];user=d['matchedUser']
 if not user:raise ValueError('User unavailable')
 seen=set(history.get('seenAcceptedSlugs',[]))
 for x in d.get('recentAcSubmissionList') or []:
  if x.get('titleSlug'):seen.add(x['titleSlug'])
 history['seenAcceptedSlugs']=sorted(seen)
 status.update({'syncedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source':'leetcode-public-graphql','submissionCalendar':json.loads(user.get('submissionCalendar') or '{}'),'acceptedSlugs':sorted(seen),'allTimeSolved':{s['difficulty']:s['count'] for s in user['submitStatsGlobal']['acSubmissionNum']}})
except Exception as ex:warnings.append('LeetCode: '+str(ex)[:180])
road=get('problems.json');manual=get('manual.json')
valid={p['slug'] for t in road.get('topics',[]) for p in t['problems']}
completed=(set(history.get('seenAcceptedSlugs',[]))|set(manual.get('completedSlugs',[])))-set(manual.get('excludedSlugs',[]))
date=datetime.datetime.now(datetime.timezone.utc).date().isoformat()
history['snapshots']=[s for s in history.get('snapshots',[]) if s.get('date')!=date]+[{'date':date,'completed':len(valid & completed)}]
history['snapshots']=sorted(history['snapshots'],key=lambda x:x['date'])[-730:]
status['warnings']=warnings+['Public API only returns recent AC submissions. Older solved problems can be added to data/manual.json.']
put('history.json',history);put('status.json',status)
print('Synced. Warnings:',warnings)

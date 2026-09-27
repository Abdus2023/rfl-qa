"""Remediation-only execution recorder; never writes previous evidence."""
import datetime, json, os, pathlib, re, shlex, subprocess, sys, time
R=pathlib.Path(__file__).resolve().parents[2]; E=pathlib.Path(__file__).parent

def run(label,cmd,cwd=R,env=None,timeout=180):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat(); t=time.monotonic()
 try:
  p=subprocess.run(cmd,cwd=cwd,env={**os.environ,**(env or {})},capture_output=True,text=True,timeout=timeout)
  code,out,err=p.returncode,p.stdout,p.stderr
 except subprocess.TimeoutExpired as exc: code,out,err=124,str(exc.stdout or ''),str(exc.stderr or '')+'\nTIMEOUT'
 err=re.sub(r'https://[^\s\"]*[?&](?:signature|sig)=[^\s\"]*','[signed-download-URL-redacted]',err)
 rec=dict(label=label,command=cmd,cwd=str(cwd),environment_overrides=env or {},timestamp=start,duration_seconds=round(time.monotonic()-t,6),stdout=out,stderr=err,exit_code=code)
 with (E/'commands.log').open('a') as f:f.write(f'\n## {label}\n$ {shlex.join(cmd)}\n<STDOUT>\n{out}\n<STDERR>\n{err}\nexit_code={code}\n')
 with (E/'command-records.jsonl').open('a') as f:f.write(json.dumps(rec,sort_keys=True)+'\n')
 print(f'{label}: exit_code={code} duration={rec["duration_seconds"]}s')
 return rec
if __name__=='__main__':
 r=run(sys.argv[1],sys.argv[2:]);print(r['stdout'],end='');print(r['stderr'],end='',file=sys.stderr);sys.exit(r['exit_code'])

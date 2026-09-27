#!/usr/bin/env python3
"""Audit-only command recorder. Does not modify the qualification engine."""
import datetime, hashlib, json, os, pathlib, subprocess, sys, time, re
ROOT = pathlib.Path(__file__).resolve().parents[2]
AUDIT = pathlib.Path(__file__).resolve().parent

def run(label, command, cwd=ROOT, env=None, timeout=180):
    overrides = env or {}
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    before = time.monotonic()
    try:
        p = subprocess.run(command, cwd=cwd, env={**os.environ, **overrides},
                           capture_output=True, text=True, timeout=timeout)
        code, stdout, stderr = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as exc:
        code, stdout, stderr = 124, str(exc.stdout or ''), str(exc.stderr or '') + '\nAUDIT TIMEOUT'
    stderr = re.sub(r'https://[^\s\"]*[?&](?:signature|sig)=[^\s\"]*', '[signed-log-download-URL-redacted]', stderr)
    record = dict(label=label, command=command, cwd=str(cwd), env_overrides=overrides,
                  started_utc=started, duration_seconds=round(time.monotonic()-before, 6),
                  exit_code=code, stdout=stdout, stderr=stderr)
    raw = json.dumps(record, ensure_ascii=False, sort_keys=True)
    with (AUDIT/'commands.log').open('a') as f: f.write(raw+'\n')
    print(f'{label}: exit={code} duration={record["duration_seconds"]}s')
    return record

if __name__ == '__main__':
    label, *command = sys.argv[1:]
    r = run(label, command)
    print(r['stdout'], end=''); print(r['stderr'], end='', file=sys.stderr)
    sys.exit(r['exit_code'])

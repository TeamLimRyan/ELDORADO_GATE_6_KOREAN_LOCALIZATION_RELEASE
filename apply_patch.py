"""Apply the volume-specific Eldorado Gate Korean xdelta patch.

Copyright (c) 2026 TeamLimRyan. MIT license; see LICENSE-installer.txt.
"""
from pathlib import Path
import argparse,hashlib,json,os,shlex,shutil,subprocess,sys,tempfile

HERE=Path(__file__).resolve().parent
def sha(path):
 with Path(path).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def check(path,spec):
 path=Path(path)
 if not path.is_file():raise ValueError('파일이 없습니다: '+str(path))
 if path.stat().st_size!=spec['size'] or sha(path)!=spec['sha256']:raise ValueError('파일 크기 또는 SHA-256이 기준과 다릅니다: '+path.name)
 return path
def tool_path(request,name):
 choices=[request] if request else []
 if name=='xdelta3' and os.name=='nt':choices.append(str(HERE/'tools/xdelta3.exe'))
 choices.append(shutil.which(name))
 for p in choices:
  if p and Path(p).is_file():return str(Path(p).resolve())
 raise ValueError(name+' 실행 파일을 찾을 수 없습니다. README의 공식 다운로드 안내를 확인하세요.')
def read_gdi(path):
 lines=Path(path).read_text('utf-8-sig').splitlines()
 if not lines or lines[0].strip()!='3' or len([x for x in lines[1:] if x.strip()])!=3:raise ValueError('3트랙 원본 GDI가 필요합니다.')
 tracks=[];folder=Path(path).resolve().parent
 for line,want in zip([x for x in lines[1:] if x.strip()],[(1,0,4,2352),(2,450,0,2352),(3,45000,4,2352)]):
  parts=shlex.split(line)
  if len(parts)!=6 or tuple(map(int,parts[:4]))!=want or int(parts[5])!=0:raise ValueError('원본 GDI 트랙 구조가 다릅니다.')
  p=(folder/parts[4]).resolve()
  if not p.is_relative_to(folder):raise ValueError('GDI가 입력 폴더 밖의 파일을 참조합니다.')
  tracks.append(p)
 return tracks
def main():
 ap=argparse.ArgumentParser(description='엘도라도 게이트 한국어 xdelta 패치: 원본을 보존하고 새 GDI 폴더를 만듭니다.')
 ap.add_argument('--input',required=True,help='원본 .chd 또는 .gdi');ap.add_argument('--output',required=True,help='새 출력 폴더(기존 폴더 사용 불가)');ap.add_argument('--chdman',help='CHD 입력용 chdman 실행 파일');ap.add_argument('--xdelta3',help='xdelta3 실행 파일 경로');args=ap.parse_args()
 manifest=json.loads((HERE/'manifest.json').read_text('utf-8'));src=Path(args.input).expanduser().resolve();out=Path(args.output).expanduser().resolve()
 if not src.is_file():raise ValueError('원본 입력 파일이 없습니다.')
 if out.exists():raise ValueError('기존 출력 폴더를 덮어쓰지 않습니다. 새 폴더를 지정하세요.')
 if out==src or out==src.parent:raise ValueError('출력은 원본과 다른 새 폴더여야 합니다.')
 patch=check(HERE/manifest['patch']['name'],manifest['patch']);xd=tool_path(args.xdelta3,'xdelta3');out.parent.mkdir(parents=True,exist_ok=True)
 env=os.environ.copy();env.pop('XDELTA',None)
 with tempfile.TemporaryDirectory(prefix='eldorado-patch-',dir=out.parent) as temp:
  if src.suffix.lower()=='.chd':
   check(src,manifest['source_chd']);chdman=tool_path(args.chdman,'chdman');gdi=Path(temp)/'source.gdi';subprocess.run([chdman,'extractcd','-i',str(src),'-o',str(gdi)],check=True)
  elif src.suffix.lower()=='.gdi':gdi=src
  else:raise ValueError('입력은 .chd 또는 .gdi 파일이어야 합니다.')
  tracks=read_gdi(gdi)
  for p,spec in zip(tracks,manifest['source_tracks']):check(p,spec)
  out.mkdir();diagnostic=dict(version=manifest['version'],volume=manifest['volume'],input=str(src),output=str(out),status='IN_PROGRESS')
  try:
   for p,name in zip(tracks[:2],['disc01.bin','disc02.raw']):shutil.copyfile(p,out/name)
   partial=out/'disc03.bin.partial';subprocess.run([xd,'-d','-R','-D','-s',str(tracks[2]),str(patch),str(partial)],env=env,check=True)
   check(partial,manifest['target_files']['disc03.bin']);partial.replace(out/'disc03.bin');(out/'disc.gdi').write_bytes(manifest['gdi'].encode('ascii'))
   for name,spec in manifest['target_files'].items():check(out/name,spec)
   diagnostic['status']='PASS';print('완료: '+str(out/'disc.gdi'));print('출력 파일의 SHA-256이 배포 기준과 모두 일치합니다.')
  except Exception as exc:diagnostic.update(status='FAILED',error=str(exc));raise
  finally:(out/'diagnostics.json').write_text(json.dumps(diagnostic,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':
 try:main()
 except Exception as exc:print('오류: '+str(exc),file=sys.stderr);sys.exit(1)

"""Sprachaufnahmen transkribieren (faster-whisper, Sprache de, Wortzeitmarken):  python3 automatik/transkribieren.py aufnahmen aufnahmen/woerter_small.json
Dekodiert per ffmpeg selbst (die PyAV-Version im Container kennt metadata_errors nicht)."""
import json,sys,glob,os,subprocess
import numpy as np
from faster_whisper import WhisperModel
def lade(f):
    r=subprocess.run(['ffmpeg','-v','error','-i',f,'-ac','1','-ar','16000','-f','s16le','-'],capture_output=True,check=True)
    return np.frombuffer(r.stdout,np.int16).astype(np.float32)/32768
m=WhisperModel("small",device="cpu",compute_type="int8")
out={}
for f in sorted(glob.glob(sys.argv[1]+"/*.mp3")):
    segs,_=m.transcribe(lade(f),language="de",word_timestamps=True,beam_size=5)
    w=[[x.word.strip(),round(x.start,2),round(x.end,2),round(x.probability,2)] for s in segs for x in s.words]
    out[os.path.basename(f)]=w
    print(os.path.basename(f),"|"," ".join(x[0] for x in w),flush=True)
json.dump(out,open(sys.argv[2],"w"),ensure_ascii=False)

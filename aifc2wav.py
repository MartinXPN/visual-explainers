from pathlib import Path

from pydub import AudioSegment

video_dir = Path('~/Desktop/videos/012. BFS').expanduser()
aifc_files = list(video_dir.glob('*+.aifc'))
sorted_aifc_files = sorted(aifc_files, key=lambda path: float(path.stem.rstrip('+')))
print(*sorted_aifc_files, sep='\n')

for f in sorted_aifc_files:
    aifc_audio = AudioSegment.from_file(f, format='aiff')
    out_file = f.with_suffix('.out.wav')
    aifc_audio.export(out_file, format='wav')
    print(f'Exported {out_file}')

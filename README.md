python-rebuild-audio-file
===

Losslessly rebuild audio files.

Installation
---

```sh
pip install -U rebuild-audio-file
```

Command-line usage
---

```sh
raf existing.mp3 new.mp3
raf existing.flac new.flac
```

Programmatic usage
---

```python
from raf import rebuild_audio_file

rebuild_audio_file('existing.mp3', 'new.mp3')
rebuild_audio_file('existing.flac', 'new.flac')
```

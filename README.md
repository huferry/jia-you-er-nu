# 家有儿女 — Chinese Study Lessons

Printable lesson PDFs and MP3 clips built from the TV show *家有儿女 (Home with Kids)*.  
Each lesson covers ~12 consecutive dialogue lines: per-character pinyin with tone-colored boxes, English translation, HSK 3+ vocabulary table, and a hanzi-only practice page.

## Folder structure

```
家有儿女/
  source/
    家有儿女-S01E01.mp4                        source video (gitignored)
    家有儿女S01E01_subtitle_only.txt            OCR of burned-in subtitles
    家有儿女S01E01_transcript_audio.txt         Whisper audio transcript
  lessons/
    S01E01/
      <MM-SS>/                                 one folder per lesson, named by first-line timestamp
        家有儿女S01E01_build_lesson_<MMSS>.py   HTML generator script
        家有儿女S01E01_clip_<MM-SS>_lesson.html
        家有儿女S01E01_clip_<MM-SS>_lesson.pdf
        家有儿女S01E01_clip_<MM-SS>_lesson.mp3
```

## Lessons (S01E01)

| Timestamp | Topic |
|-----------|-------|
| 03:05 | 小雪 is coming — preparing the kids |
| 03:35 | More prep talk |
| 04:10 | Mosquito bite — *your blood is sweet* |
| 04:43 | Sibling banter |
| 05:09 | Dinnertime chaos |
| 05:40 | Waiting for 小雪 |
| 06:28 | More waiting |
| 07:01 | Food getting cold |
| 07:33 | Family anxiety |
| 08:05 | Still waiting |
| 08:31 | The hunger standoff |
| 09:23 | Water vs food — *that's what a stepmother would do* |
| 09:48 | No-bullying rules + sausage reward + 小雪 arrives |

## Creating a new lesson

Use the `video-lesson-pdf` skill in Claude Code:

```
/video-lesson-pdf S01E01
```

Provide a starting timestamp to begin from a specific point, or omit it to continue from the last lesson. The skill extracts dialogue, generates the PDF and MP3, and saves everything in a new `lessons/S01E01/<MM-SS>/` folder.

## Tone color convention

| Tone | Color |
|------|-------|
| 1st / neutral | no box |
| 2nd | blue `#0047d6` |
| 3rd | green `#0f8a1f` |
| 4th | red `#d21414` |

Coloring uses a **border box** around the hanzi character — not a background fill, which fades on a real printer.

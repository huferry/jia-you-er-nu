---
description: Build a printable Chinese-lesson PDF (+ matching MP3 snippet) from N consecutive dialogue lines of a video in this project, starting at a given timestamp — per-character pinyin with tone-colored boxes, English translation, an HSK3+ vocabulary page, a hanzi-only practice page, and a precisely-cut audio clip. Use when the user asks to "make a PDF/lesson" from a video clip, "create flashcards/vocab" for a scene, or asks for "the next N lines" as a PDF. Takes: video file, starting timestamp, number of lines (default 12).
allowed-tools: Bash, Read, Write, Edit
---

# video-lesson-pdf

Turn N consecutive lines of dialogue from a video into a study PDF (pinyin + translation +
HSK vocab + hanzi-only practice page) and a matching MP3 clip of just those lines. This is a
project-scoped skill — everything here is specific to the transcript files and conventions
already established in this project folder.

## Folder layout

```
家有儿女/
  .claude/skills/video-lesson-pdf/   this skill
  source/                            家有儿女.mp4, *_subtitle_only.txt, *_transcript_audio.txt
  lessons/<HH-MM>/                   one folder per lesson, named by first-line timestamp:
    家有儿女_build_lesson_<HHMM>.py    generator (writes the .html next to itself)
    家有儿女_clip_<HH-MM>_lesson.html / .pdf / .mp3
```

New lessons go in a new `lessons/<HH-MM>/` folder; copy the most recent build script as the
template (keep everything from `def tokenize` down, replace the data block above it).

## Inputs

- The season/episode of the video (e.g. `S01E01`, this means, use the file `家有儿女-S01E01.mp4`).
- A starting timestamp (e.g. `03:05.50`). (When not defined, it will continue from the last time stamp)
- Number of lines, default 12 unless the user says otherwise. (Default is 12 when not defined)

## Step 0 — Get the source lines

Prefer the already-generated transcripts in `source/` over re-running OCR/audio from
scratch:

- `*_subtitle_only.txt` — OCR of burned-in subtitles (see the [[subtitle-to-text]] skill,
  machine-wide, that produced it). This is the primary source for the actual on-screen
  wording.
- `*_transcript_audio.txt` — Whisper transcription of the audio, with `[subtitle: ...]` notes
  wherever it disagrees with the OCR. Use this to **cross-check and repair** OCR garbage, and
  for precise segment start/end timestamps (needed later for the MP3 cut — the subtitle file
  only gives line-start times).

If neither file exists yet for this video, generate the subtitle-only one first (that's the
other skill's job, not this one), then run/locate a Whisper pass over the audio for the
cross-check and timing data.

Pick N consecutive subtitle-only lines starting at/after the given timestamp. **Do not trust
the OCR text blindly** — for each line, check the corresponding audio-transcript line(s) in
the same time window:
- If OCR and audio agree (or differ only trivially), use the OCR wording — it's the literal
  on-screen text.
- If OCR is garbled (common on busy/bright backgrounds — see the subtitle-to-text skill's
  known limitations) but audio is clean, reconstruct the line from audio.
- Sometimes one garbled OCR line is actually *several* spoken lines merged — split it back
  out using the audio transcript's own line breaks and timestamps (this happened with a
  mock-poem recited in one breath, OCR'd as a single garbled line).
- It's fine, and expected, for translations to read as one continuous thought across
  consecutive short lines (dialogue is often split mid-sentence by subtitle timing).

## Step 1 — Build the sentence list

For each of the N lines: `(timestamp, hanzi_text, english_translation)`. Write natural,
accurate translations — not word-for-word — but keep them short enough to fit one line under
the hanzi.

## Step 2 — Per-character pinyin

Use `pypinyin` (`Style.TONE`, `heteronym=False`) per character. Two known correction passes
are required on top of the raw output:

1. **Heteronym overrides.** pypinyin's phrase-dict guesses wrong often enough to check by eye
   every time (e.g. 得 read as dé instead of děi in 必须得; 好 read as hào instead of hǎo in a
   second, repeated 做好). Key overrides by `(sentence_index, character_position_in_sentence)`,
   **not** by character alone — the same character can appear multiple times in one sentence
   needing different readings, and a per-character key silently mis-fixes the wrong occurrence.
2. **不-tone-sandhi.** 不 (bù, 4th tone) becomes 2nd tone (bú) when immediately followed by
   another 4th-tone syllable — this is well-defined regardless of word segmentation, so apply
   it automatically everywhere (scan the sentence, find 不, look at the tone of the next
   non-space character, retone if both are 4th). **Do not** attempt the other common sandhi
   rules (二 consecutive 3rd tones → first becomes 2nd; 一's tone shifting) — those need
   correct word-boundary segmentation to get right, and guessing wrong makes the material
   actively worse. Skip them unless the user explicitly asks, and say so if asked to "fix all
   the tones."

## Step 3 — HSK3+ vocabulary table

Pull out real content words (not single grammatical particles) that are HSK level 3 or above,
or idioms/four-character set phrases, or a notable grammar pattern. For each: the word, its
pinyin, and an **explanation that's more than a translation** — usage register, a common
collocation, a confusable near-synonym, or the grammar pattern it belongs to. A grammar
pattern like 一点…都没有 can go in the same table (mark its "level" column as `grammar`) even
though it's not a contiguous substring of the sentence text — just don't try to highlight it
in the sentence rows (see Step 4).

## Step 4 — Render to PDF (HTML → headless Chrome)

Build one HTML file, print it with headless Chrome, per page:

- **Pages 1-2 (or however many): full detail.** Per sentence: timestamp, then a row of
  character blocks (pinyin above, hanzi below), then the translation in italics below.
- **Tone coloring is a colored BOX (border) around each hanzi character, not a background
  fill** — background fills look fine on screen but print badly (user feedback: pale fills
  disappear/blur on a real printer). Use bold, saturated border colors: 2nd tone blue
  (`#0047d6`), 3rd tone green (`#0f8a1f`), 4th tone red (`#d21414`), 1st tone and neutral tone
  get no box. Same convention for the little swatches in the legend at the top.
- **Vocabulary table page**, forced onto its own page (`page-break-before: always` on its
  `<h2>`). Hanzi and pinyin in this table should render noticeably larger than the in-text
  pinyin/hanzi (readable at a glance): hanzi ~16pt, pinyin ~11.5pt.
- **Final "Text Only" page**: the same N lines, hanzi only — no pinyin, no translation, no
  tone-color boxes (plain black text). Hanzi should be the same large size as pages 1-2 (not
  shrunk). This page needs *much* tighter vertical spacing than the full-detail pages (no
  pinyin row, no translation line, smaller margins/border between lines) or 12 lines won't
  fit on one page — check the actual page count after rendering and tighten further if it
  spills onto an extra page.
- **Title**: `<Show/Video title> <first-line-timestamp> - <last-line-timestamp>`, e.g.
  `家有儿女 03:05.50 - 03:32.50`. Set both the `<title>` tag and the visible `<h1>`.
- **Font — critical, previously-broken:** use `"STHeiti", "Heiti SC", ...` for all hanzi, not
  `"PingFang SC"`. PingFang SC triggers a Chrome PDF font-subsetting bug where the *visible*
  render is correct but the embedded copyable text layer silently maps some characters to
  lookalike CJK Radical glyphs (e.g. 女 extracts as ⼥, 至 as ⾄, 心 as ⼼) — invisible on
  screen, but garbles anything copy-pasted from the PDF. **Always verify with
  `pdftotext file.pdf - | grep <a few known phrases from the text>`** after rendering, on
  every regenerate — this is silent and easy to reintroduce.

Render with:
```
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --no-pdf-header-footer --print-to-pdf="lessons/<HH-MM>/out.pdf" "file://$(pwd)/lessons/<HH-MM>/page.html"
```

## Step 5 — Matching MP3 snippet

Cut an audio clip covering exactly these N lines — but "precisely on the timestamps" means
the *actual spoken audio* of the first through last line, not a literal cut at the last
line's on-screen start time (that would chop off its audio mid-sentence).

- Use the Whisper transcript's segment `start`/`end` (not the subtitle line-start times) to
  find: the end time of the **last** line's speech, and, if available, a more precise start
  for the **first** line.
- Add a small pad: ~0.2s before the start, ~0.4s after the end, so words aren't clipped.
- Extract with ffmpeg directly from the video (it has real audio — see project history if a
  given `.mp4` initially doesn't):
  ```
  ffmpeg -nostdin -y -i source/video.mp4 -ss <start> -to <end> -vn -acodec libmp3lame -b:a 192k out.mp3
  ```

## Step 6 — Naming and delivery

Name the pair to match: `<video_basename>_clip_<HH-MM_of_first_line>_lesson.pdf` and the same
stem with `.mp3`. Save both (plus the .html and build script) in `lessons/<HH-MM>/`, and send both to
the user (`SendUserFile`, PDF with `display: "render"`, MP3 with `display: "attach"`).

## Iterating on an already-delivered PDF

The user will often ask for small global tweaks after seeing a draft (box vs. fill, bigger
vocab text, a new page, tone-sandhi fixes). Keep the HTML-generation script around per video
(don't regenerate from scratch each time) so these are quick, targeted edits — and **apply
each requested tweak to every PDF generated so far for this project**, not just the one just
discussed, since the user expects consistent formatting across the whole lesson series.

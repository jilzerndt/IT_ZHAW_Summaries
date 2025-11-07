# PROMPT: THEORY CONTENT EXTRACTION

Extract theoretical content from [SOURCE_FILE.pdf] and create LaTeX file(s) following layout_and_colours.sty.

SOURCE DESCRIPTION: [e.g., "Lecture 03 slides, Week 3, on Database Normalization"]

CRITICAL FILE NAMING:
- Use lecture/script naming: lecture01.tex, lecture02.tex, script_chapter03.tex
- For LONG lectures/scripts, split into multiple files for readability:
  - lecture02A.tex (first part)
  - lecture02B.tex (second part)
  - lecture02C.tex (if needed)
- Split when content exceeds ~800-1000 lines of LateX Code or covers multiple distinct major topics

---

CONTENT AND STYLE GUIDELINES, FORMATTING RULES: follow instructions in file 'misc_files/automatisation/reference_style_guide.txt'
-> FIRST fully understand that document before starting!!

---

CONTENT PRESERVATION:

- Extract ALL content from source - do NOT summarize yet
- Include all examples, figures, tables, and code snippets
- Maintain the logical flow and order from the source FOR NOW (Phase 2 will reorganize)
- Preserve all technical terminology exactly
- Include all mathematical derivations with steps
- For each visual element, create image TODO comment

---

FILE ORGANIZATION:

FILENAME PATTERNS:
- Lectures: lecture01.tex, lecture02A.tex, lecture02B.tex, lecture03.tex, ...
- Scripts: script_chapter01.tex, script_chapter02.tex, ...
- Textbooks: textbook_chapter01.tex, ...

SPLITTING GUIDELINES:
- Split long lectures (>15 pages) into parts: lectureXXA.tex, lectureXXB.tex
- Split at natural topic boundaries
- Each file should cover one major theme/topic cluster
- Maintain clear section breaks

FILE STRUCTURE:
- NO \documentclass or preamble in these files
- Start directly with \section{Topic Name}
- For split files, use logical section names:
  - lecture02A.tex: \section{Data Structures - Part 1}
  - lecture02B.tex: \section{Data Structures - Part 2}

---

IMAGE SUMMARY SECTION:

At the END of each file, include:

% ===== IMAGE SUMMARY =====
% Total images needed: [X]
% CRITICAL priority: [Y]
% IMPORTANT priority: [Z]
% SUPPLEMENTARY priority: [W]
%
% Quick extraction checklist:
% [ ] [Source.pdf, Slide/Page X] - [description] (PRIORITY)
% [ ] [Source.pdf, Slide/Page Y] - [description] (PRIORITY)
% [ ] [Source.pdf, Slide/Page Z] - [description] (PRIORITY)
% ...
% =====================

This checklist enables batch image extraction later!

---

VALIDATION BEFORE DELIVERY:

- [ ] VALDIATION CHECKLIST from 'misc_files/automatisation/reference_style_guide.txt'
- [ ] Filename follows lecture/script naming convention
- [ ] Long content appropriately split into multiple files
- [ ] Image summary section present at end

---

OUTPUT:

Deliver complete lectureXX.tex or lectureXXA.tex, lectureXXB.tex files ready for Phase 1.5 analysis.

If lecture is long, create multiple files with clear part indicators.
```

---

## WHEN TO SPLIT FILES

### Split when:
- Content exceeds ~800-1000 lines of LaTeX code (or Claude isn't able to handle in one file)
- Lecture covers multiple distinct major topics
- Natural break points exist (e.g., "Part 1: Theory" / "Part 2: Applications")
- File becomes difficult to navigate

### Keep together when:
- Content < ~800-1000 lines
- Single cohesive topic
- Topics tightly interconnected

### Example:
```
Lecture 02 (45 pages, covers: Arrays, Lists, Trees)
→ Split into:
   - lecture02A.tex: Arrays and Lists
   - lecture02B.tex: Trees and Tree Operations
```
---

**Note:** Phase 1A focuses ONLY on theory materials (lectures, scripts). Exercise materials are handled in Phase 1B.

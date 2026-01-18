# EXAMPLE WORKFLOW: Database Course Summary

## Scenario

You're taking a Database Systems course and need to create a LaTeX exam summary.

**Course materials**:
- 5 lecture PDFs (200 pages total)
- Exercise sheets with solutions (50 pages)
- 3 old exams (from 2022, 2023, 2024)
- Learning objectives document

**Exam info**:
- Written exam, 2 hours, closed book
- 40% theory (definitions, concepts), 60% practical problems
- Topics: SQL, Normalization, E-R diagrams, Transactions

**Timeline**: 2 weeks until exam

---

## Decision: Which Workflow?

### Quick Assessment

1. **Do I have LaTeX files already?** → No
2. **Do I have 3+ old exams?** → Yes (3 exams)
3. **Time until exam?** → 2 weeks (moderate)
4. **Confidence in prioritization?** → Medium (have old exams to guide)
5. **Need complete reference?** → No (just exam prep)

### Decision: Use Workflow 3 (Direct PDF → Summary)

**Why**: Have clear exam patterns from 3 old exams, don't need intermediate complete LaTeX, time-efficient for 2-week timeline.

---

## PHASE 1: PLANNING

### Step 1A: Scan All Sources

**Quick scan** (30 minutes reading through materials):

**Lecture PDFs**:
- Lecture 01-02: Database intro (20p), Relational model (30p)
- Lecture 03-04: SQL basics (40p), SQL advanced (40p)
- Lecture 05: Normalization (40p)
- Lecture 06: E-R modeling (25p)
- Lecture 07: Transactions (5p - very brief!)

**Exercises**:
- SQL queries: 15 problems (various difficulty)
- Normalization: 6 problems (2NF, 3NF)
- E-R diagrams: 4 problems
- Transaction concepts: 2 problems

**Old Exams Pattern**:
- Exam 2022: SQL (35%), Normalization (40%), E-R (15%), Transactions (10%)
- Exam 2023: SQL (40%), Normalization (35%), E-R (20%), Transactions (5%)
- Exam 2024: SQL (35%), Normalization (35%), E-R (25%), Transactions (5%)

### Step 1B: Prioritization Matrix

**Priority 1 (Must Include - Heavily Tested)**:
- **SQL Queries** (35-40% every exam)
  - Source: Lecture 03-04 (80 pages), Exercises (15 problems)
  - Coverage: SELECT, WHERE, JOIN types, subqueries, aggregation
  - KRs needed: 3 (complex queries, JOIN selection, GROUP BY)
  - Examples: 3 (easy, medium, hard)
  - Images: 6 (JOIN diagrams)

- **Normalization** (35-40% every exam)
  - Source: Lecture 05 (40 pages), Exercises (6 problems)
  - Coverage: FDs, 1NF/2NF/3NF, decomposition
  - KRs needed: 3 (identify FDs, normalize to 3NF, check BCNF)
  - Examples: 3 (easy, medium, hard)
  - Images: 4 (dependency diagrams)

- **E-R Diagrams** (15-25% every exam)
  - Source: Lecture 06 (25 pages), Exercises (4 problems)
  - Coverage: Entities, relationships, cardinality
  - KRs needed: 2 (create E-R, convert to tables)
  - Examples: 2 (medium, hard)
  - Images: 3 (notation, examples)

- **Relational Model** (prerequisite, indirectly tested)
  - Source: Lecture 01-02 (50 pages)
  - Coverage: Relations, keys, relational algebra basics
  - KRs needed: 1 (identify keys)
  - Examples: 1 (key identification)
  - Images: 2 (structure)

**Priority 2 (Should Include - Occasionally Tested)**:
- **Transactions** (5-10% each exam - brief)
  - Source: Lecture 07 (5 pages only!)
  - Coverage: ACID properties, isolation levels (basic)
  - KRs needed: 1 (explain ACID/isolation - brief)
  - Examples: 1 (simple scenario)
  - Images: 1 (ACID table)

**Priority 3 (Skip)**:
- **Database History** (Lecture 01, 20 pages) - never tested
- **Advanced Transactions** (not covered in lecture) - not in exam scope
- **Query Optimization** (mentioned but no exam questions) - skip

### Step 1C: Structure Proposal

**Proposed 5 Chapters**:

1. **Relational Model Foundations** (15%)
   - Topics: Relations, keys
   - ~120 lines
   - 1 KR, 1 example, 2 images

2. **SQL Fundamentals** (35%)
   - Topics: All SQL covered in exams
   - ~350 lines
   - 3 KRs, 3 examples, 6 images

3. **Database Normalization** (30%)
   - Topics: FDs, normal forms, decomposition
   - ~300 lines
   - 3 KRs, 3 examples, 4 images

4. **Database Design** (15%)
   - Topics: E-R diagrams, conversion
   - ~150 lines
   - 2 KRs, 2 examples, 3 images

5. **Transactions** (5%)
   - Topics: ACID, isolation (brief)
   - ~50 lines
   - 1 KR, 1 example, 1 image

**Total**: ~970 lines (~20-25 pages compiled)

**KRs**: 10 total
**Examples**: 11 total
**Images**: 16 total

### User Approval

**Present to self**:
> I've analyzed all materials and created this plan. SQL + Normalization get 65% of space (matching exam emphasis). Skipping database history (20 pages, never tested). Total: ~25 pages.
>
> **Approve?**

**Answer**: ✅ Approved (makes sense based on old exams)

---

## PHASE 2: FOCUSED EXTRACTION + SUMMARIZATION

### Chapter 1: Relational Model Foundations

**Extract from Lecture 01-02** (pages 20-50, skipping intro/history):

```latex
\section{Relational Model Foundations}

\mult{2}
\begin{definition}{Relation}\\
A table with rows (tuples) and columns (attributes). Each relation has a schema defining attribute names and domains.
\end{definition}

\begin{definition}{Tuple}\\
A single row in a relation, representing one instance or record. Contains values for each attribute.
\end{definition}
\multend

\begin{concept}{Keys}\\
% TODO: add image from lecture_01.pdf, page 25

\textbf{Primary Key}: Attribute(s) that uniquely identify each tuple. No nulls allowed.

\textbf{Foreign Key}: Attribute(s) referencing primary key of another relation. Enforces referential integrity.

\textbf{Candidate Key}: Any attribute set that could serve as primary key (unique, no nulls).
\end{concept}

\begin{KR}{How to Identify Primary/Candidate Keys}\\
\textbf{Given:} Relation with attributes and sample data

\textbf{Goal:} Identify all candidate keys and choose primary key

\textbf{Procedure:}
\begin{enumerate}
    \item \textbf{Find uniqueness}: For each attribute (or combination):
    \begin{itemize}
        \item Check if values are unique for all tuples
        \item If not unique alone, try combinations
    \end{itemize}
    \item \textbf{Check minimality}: For each unique set:
    \begin{itemize}
        \item Can any attribute be removed while maintaining uniqueness?
        \item Minimal unique sets are candidate keys
    \end{itemize}
    \item \textbf{Verify no nulls}: Candidate keys cannot contain null values
    \item \textbf{Choose primary key}: Select one candidate key based on:
    \begin{itemize}
        \item Smallest size (fewer attributes preferred)
        \item Stability (unlikely to change)
        \item Meaningfulness (often artificial ID)
    \end{itemize}
\end{enumerate}

\textbf{Common mistakes:}
\begin{itemize}
    \item Choosing non-minimal set → Must remove redundant attributes
    \item Missing composite keys → Sometimes need multiple attributes together
    \item Allowing nulls → Primary key cannot be null
\end{itemize}

\textbf{When to use:} "Identify keys", "what is the primary key", normalization setup
\end{KR}

\begin{example2}{Key Identification - Easy}\\
\textbf{Given:} Relation Students(StudentID, Name, Email, Major)

Sample data:
\begin{tabular}{|l|l|l|l|}
\hline
StudentID & Name & Email & Major \\
\hline
101 & Alice & alice@uni.edu & CS \\
102 & Bob & bob@uni.edu & Math \\
103 & Carol & carol@uni.edu & CS \\
\hline
\end{tabular}

\textbf{Find:} All candidate keys and primary key

\tcblower

\textbf{Solution:}
\begin{enumerate}
    \item \textbf{Check single attributes}:
    \begin{itemize}
        \item StudentID: Unique (101, 102, 103) ✓
        \item Name: Unique in sample, but not guaranteed → Not reliable
        \item Email: Unique ✓
        \item Major: Not unique (CS appears twice) ✗
    \end{itemize}
    \item \textbf{Candidate keys}: StudentID, Email
    \item \textbf{Choose primary key}: StudentID
    \begin{itemize}
        \item Reason: Artificial identifier, stable, designed for uniqueness
        \item Email could change (less stable)
    \end{itemize}
\end{enumerate}

\textbf{Answer:}
- Candidate keys: \{StudentID\}, \{Email\}
- Primary key: StudentID

\important{Key insight:} Artificial IDs (StudentID) usually best choice for primary key - stable and guaranteed unique by design.
\end{example2}

% ===== IMAGES =====
% Total: 2 images
% =====================
```

**Continue similarly for other chapters...**

### Chapter 2: SQL Fundamentals

**Extract from Lecture 03-04** (80 pages → ~350 lines):

```latex
\section{SQL Fundamentals}

% Group JOIN type definitions
\mult{2}
\begin{definition}{INNER JOIN}\\
Returns only rows with matching values in both tables. Non-matching rows excluded.
\end{definition}

\begin{definition}{LEFT JOIN}\\
Returns all rows from left table plus matches from right. Non-matching right rows appear as NULL.
\end{definition}
\multend

\mult{2}
\begin{definition}{RIGHT JOIN}\\
Returns all rows from right table plus matches from left. Non-matching left rows appear as NULL.
\end{definition}

\begin{definition}{FULL OUTER JOIN}\\
Returns all rows from both tables. Non-matching rows show NULL for missing side.
\end{definition}
\multend

% Comparison table
\begin{highlight}{JOIN Types Quick Reference}\\
\begin{tabular}{|l|p{4cm}|p{3cm}|}
\hline
\textbf{JOIN Type} & \textbf{Returns} & \textbf{Use When} \\
\hline
INNER & Only matches & Need matching data only \\
LEFT & All left + matches & Keep all left records \\
RIGHT & All right + matches & Keep all right records \\
FULL & All rows both sides & Need complete data \\
\hline
\end{tabular}
\end{highlight}

% TODO: add image from lecture_03.pdf, slide 15

\begin{KR}{How to Write Complex SQL Query}\\
\textbf{Given:} Multiple tables and data requirements

\textbf{Goal:} Write SELECT query to retrieve desired data

\textbf{Procedure:}
\begin{enumerate}
    \item \textbf{Identify tables}: List all tables containing needed data
    \item \textbf{Determine relationships}: Find foreign key connections
    \item \textbf{Choose JOIN types}:
    \begin{itemize}
        \item INNER: Only need matching data
        \item LEFT/RIGHT: Need all records from one side
        \item FULL: Need all records from both sides
    \end{itemize}
    \item \textbf{Write FROM and JOIN clauses}:
\begin{lstlisting}[language=SQL, style=base]
FROM table1
INNER JOIN table2 ON table1.fk_id = table2.pk_id
LEFT JOIN table3 ON table2.fk_id2 = table3.pk_id
\end{lstlisting}
    \item \textbf{Add WHERE}: Filter rows based on conditions
    \item \textbf{Add SELECT}: Specify columns to return
    \item \textbf{Add ORDER BY}: Sort results if needed
\end{enumerate}

\textbf{Common mistakes:}
\begin{itemize}
    \item Forgetting ON clause → Cartesian product (every row with every row)
    \item Wrong JOIN type → LEFT when need INNER loses unmatched rows
    \item Ambiguous columns → Use table.column when column name appears in multiple tables
    \item WHERE before JOIN → Apply WHERE after joining, not before
\end{itemize}

\textbf{When to use:} Need data from multiple tables, "join", "combine" tables
\end{KR}

\begin{example2}{Complex JOIN Query - Medium}\\
\textbf{Given:}
- Students(StudentID, Name)
- Enrollments(StudentID, CourseID)
- Courses(CourseID, CourseName)

\textbf{Task:} List all students and their enrolled courses. Include students with no enrollments.

\tcblower

\textbf{Solution:}

\textit{Strategy:} Need LEFT JOIN to keep all students even if not enrolled.

\begin{lstlisting}[language=SQL, style=base]
SELECT
    s.StudentID,
    s.Name,
    c.CourseName
FROM Students s
LEFT JOIN Enrollments e ON s.StudentID = e.StudentID
LEFT JOIN Courses c ON e.CourseID = c.CourseID
ORDER BY s.Name;
\end{lstlisting}

\textbf{Explanation:}
\begin{enumerate}
    \item Start with Students (need all students)
    \item LEFT JOIN Enrollments (keeps students with no enrollments)
    \item LEFT JOIN Courses (gets course names for enrollments)
    \item Result: All students listed, CourseNase NULL for unenrolled students
\end{enumerate}

\textbf{Answer:} Query returns all students with their courses (or NULL if not enrolled)

\important{Key technique:} Use LEFT JOIN to preserve all records from "main" table (Students) even when no matches in other tables.
\end{example2}

[Continue with 2 more examples: easy single JOIN, hard multi-JOIN with aggregation]

[Add 2 more KRs: How to Choose JOIN Type, How to Use GROUP BY with HAVING]

[Add 5 more images: JOIN result diagrams, subquery visualization, aggregation examples]

% ===== IMAGES =====
% Total: 6 images
% =====================
```

**Continue similarly for Chapter 3 (Normalization), Chapter 4 (E-R Diagrams), Chapter 5 (Transactions)...**

---

## Final Output

### File Structure Created

```
misc_files/automatisation/database_summary/
├── 01_relational_model.tex         (~120 lines)
├── 02_sql_fundamentals.tex         (~350 lines)
├── 03_normalization.tex            (~300 lines)
├── 04_database_design.tex          (~150 lines)
├── 05_transactions.tex             (~50 lines)
└── Database_Summary_Main.tex       (master document)
```

### Summary Creation Report

**Sources Processed**:
- Lecture 01-07 PDFs (200 pages)
- Exercises (50 pages)
- Old Exams (3 exams analyzed)

**Content Created**:
- **5 chapters**: Organized by exam importance
- **10 KRs**: Covering all tested problem types
- **11 examples**: Weighted toward SQL + Normalization
- **16 images**: Essential concepts only (TODO comments)

**Coverage**:
✅ All learning objectives covered
✅ All old exam topics covered
✅ All exercise problem types have KRs

**Estimated Output**: ~970 lines (~20-25 compiled pages)

**Content Skipped**: ~70 source pages (database history, extended intros, optimization details)

**Efficiency**: 200 source pages → 25 summary pages = 87.5% reduction while covering 100% of tested content

---

## Usage

### To Compile:

1. Place all .tex files in `content/` directory
2. Create `Database_Summary_Main.tex`:

```latex
\documentclass[a4paper, fontsize = 8pt, landscape]{scrartcl}
\usepackage{../../misc_files/LateX/layout_and_colours}
\makeatletter
\def\input@path{{content/}}
\makeatother
\graphicspath{{content/images/}}

\begin{document}
\begin{multicols}{2}
    \input{01_relational_model.tex}
    \raggedcolumns
    \pagebreak

    \input{02_sql_fundamentals.tex}
    \raggedcolumns
    \pagebreak

    \input{03_normalization.tex}
    \raggedcolumns
    \pagebreak

    \input{04_database_design.tex}
    \raggedcolumns
    \pagebreak

    \input{05_transactions.tex}
\end{multicols}
\end{document}
```

3. Compile: `pdflatex Database_Summary_Main.tex`
4. Result: Exam-ready summary PDF

### To Add Images:

1. Extract images from source PDFs based on TODO comments
2. Save with suggested filenames in `content/images/`
3. Uncomment `\includegraphics` lines in .tex files
4. Recompile

### Study Plan:

**Week 1 (10 days before exam)**:
- Day 1-2: Read entire summary (4-6 hours)
- Day 3-4: Master all 10 KRs (practice writing them)
- Day 5-6: Work through all 11 examples without looking at solutions
- Day 7: Review weak areas

**Week 2 (3 days before exam)**:
- Day 8: Practice with old exams using summary as reference
- Day 9: Memorize key formulas and recognition criteria
- Day 10: Final review of KRs and common mistakes

---

## Lessons Learned

### What Worked Well:

✅ Old exam analysis was CRITICAL - guided all prioritization decisions
✅ Skipping history/intro sections saved ~70 pages without losing exam content
✅ KR-first approach ensured all tested skills covered
✅ Organizing by importance (not lecture order) made studying efficient

### What Could Be Improved:

⚠️ Could have merged Chapter 1 into other chapters (small standalone chapter)
⚠️ Chapter 2 (SQL) is large - could split into SQL Basics + SQL Advanced
⚠️ More examples for E-R diagrams would be helpful (only 2)

### Time Investment:

- **Planning Phase 1**: 1 hour (scanning + prioritization + structure)
- **Extraction Phase 2**: 3.5 hours (focused extraction of 5 chapters)
- **Total**: 4.5 hours

**Compare to**:
- Reading all 200 source pages: ~25-30 hours
- Prompt 1 + Prompt 2 workflow: ~6-7 hours

**Efficiency**: Direct workflow saved ~2 hours vs. two-phase workflow, ~22 hours vs. reading everything.

---

## Success Metrics

**After using this summary**:
- Exam score: 92% ✅
- Topics covered: 100% of exam questions had corresponding KR ✅
- Time to review: 6 hours (vs. 30+ hours for all materials) ✅
- Confidence: High (knew exactly what to expect) ✅

**Student feedback**:
> "The KRs were exactly what I needed - every exam question matched one of the procedures. Organization by importance meant I studied the most-tested topics first. Would definitely use this workflow again!"

---

## Workflow Summary

### For Your Next Course:

1. **Gather materials** + old exams
2. **Analyze** old exam patterns (1 hour)
3. **Create prioritization matrix** (30 min)
4. **Get user approval** (your own or study partner)
5. **Execute focused extraction** (3-4 hours)
6. **Validate coverage** (check all KRs match problem types)
7. **Study efficiently** (KR-driven approach)

### Key Success Factors:

✅ Having 3+ old exams to identify patterns
✅ Ruthless prioritization (skip non-tested content)
✅ KR for every tested skill
✅ Examples matching exam difficulty
✅ Logical organization (not lecture order)

**Remember**: Quality > Quantity. 25 pages of focused, exam-relevant content beats 200 pages of complete coverage.

---

## Files Referenced

**Prompts**:
- misc_files/automatisation/prompt_direct_pdf_summary.txt

**Style guides**:
- misc_files/automatisation/reference_style_guide.txt
- misc_files/automatisation/specialty_programming.txt (for SQL code)

**KR templates**:
- misc_files/automatisation/kr_examples_library.txt

**Workflow guide**:
- misc_files/automatisation/workflow_guide.txt

**Quality target**:
- 4th_Semester/CT2/LateX/content/lecture_summary/*.tex

Good luck with your summaries! 📚✨

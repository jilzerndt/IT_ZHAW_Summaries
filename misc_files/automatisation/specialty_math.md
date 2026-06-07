# Specialty Prompt: Mathematics-Heavy Courses

## Purpose
Optimized workflow for courses with extensive mathematical content (Analysis, Linear Algebra, Differential Equations, Statistics, etc.) where formulas, proofs, and symbolic manipulation are central.

## When to Use
- Courses with >50% mathematical content
- When most exam questions involve calculations/proofs
- For theoretical mathematics or mathematical physics courses

---

## Enhanced Phase 1: Mathematical Content Extraction

```
Extract mathematical content from [SOURCE] and create LaTeX following the 
standard Phase 1 guidelines, with these MATHEMATICAL EXTENSIONS:

## Mathematical Environment Priority

### For Definitions:
Use enhanced mathematical formatting:
```latex
\begin{definition}{[Name]}\\
[Verbal definition]

\textbf{Formal:} [Mathematical formulation]

\textbf{Notation:} [Symbol explanation]
\end{definition}
```

Example:
```latex
\begin{definition}{Continuity}\\
A function is continuous at point $a$ if the limit equals the function value.

\textbf{Formal:} $\lim_{x \to a} f(x) = f(a)$

\textbf{Notation:} $f \in C^0$ means $f$ is continuous
\end{definition}
```

### For Theorems/Lemmas/Corollaries:
Include all components:
```latex
\begin{theorem}{[Name]}\\
\textbf{Statement:} [What the theorem says]

\textbf{Conditions:} [When it applies]
\begin{itemize}
    \item Prerequisite 1
    \item Prerequisite 2
\end{itemize}

\textbf{Conclusion:} [What you can conclude]

[Include proof ONLY if commonly tested]
\end{theorem}
```

### For Important Formulas:
Use highlight boxes:
```latex
\begin{highlight}{[Formula Category]}
\begin{itemize}
    \item $\displaystyle [formula 1]$ \quad [description/when to use]
    \item $\displaystyle [formula 2]$ \quad [description/when to use]
\end{itemize}
\end{highlight}
```

Or for single critical formulas:
```latex
\begin{iequation}
[important formula]
\end{iequation}
```

### For Derivations:
Use step-by-step aligned equations:
```latex
\begin{example2}{Deriving [Result]}\\
\begin{align*}
[starting expression] &= [step 1] && \text{[reason]} \\
&= [step 2] && \text{[reason]} \\
&= [final result] && \text{[conclusion]}
\end{align*}

\important{Key insight:} [What makes this work]
\end{example2}
```

## Mathematical Notation Standards

### Number Sets:
Use predefined commands (from layout_and_colours.sty):
- Natural numbers: `\N` → $\mathbb{N}$
- Integers: `\Z` → $\mathbb{Z}$
- Rationals: `\Q` → $\mathbb{Q}$
- Reals: `\R` → $\mathbb{R}$
- Complex: `\C` → $\mathbb{C}$

### Operators:
Prefer predefined operators:
```latex
% Correct ✅
\sin, \cos, \tan, \log, \ln, \exp
\lim_{x \to a}, \sum_{i=1}^{n}, \int_{a}^{b}, \prod_{i=1}^{n}

% Wrong ❌
sin, cos (renders as variables, not functions)
```

For custom operators, define them:
```latex
\DeclareMathOperator{\grad}{grad}
\DeclareMathOperator{\diam}{diam}
```

### Delimiters:
Use dynamic sizing:
```latex
% Good for short expressions
( a + b )
[ x, y ]

% Use \left \right for tall expressions
\left( \frac{a}{b} + \frac{c}{d} \right)
\left[ \sum_{i=1}^{n} x_i \right]
```

### Fractions:
```latex
% In display mode:
\frac{numerator}{denominator}

% In inline mode (more compact):
\tfrac{num}{den}  or  a/b
```

### Spacing in Formulas:
```latex
% Thin space: \,
% Medium space: \:
% Large space: \;
% Quad space: \quad
% Double quad: \qquad

Example: $f(x)\,dx$ vs $f(x)dx$ (second has no space)
```

## Enhanced KR Blocks for Mathematics

Create KRs for all procedural mathematics:

### Calculation Procedures:
```latex
\begin{KR}{How to [Compute/Calculate/Find] [X]}\\
\textbf{Given:} [What information you have]

\textbf{Goal:} [What you're solving for]

\textbf{Procedure:}
\begin{enumerate}
    \item [Step 1 with formula]: $[formula]$
    \item [Step 2]: If [condition], then [action]
    \item [Step 3]: Calculate [intermediate result]
    \item [Step 4]: [Final computation]
\end{enumerate}

\textbf{Verification:} [How to check your answer]

\textbf{Common mistakes:}
\begin{itemize}
    \item [Mistake 1]: [Why it's wrong]
    \item [Mistake 2]: [How to avoid it]
\end{itemize}
\end{KR}
```

### Proof Techniques:
```latex
\begin{KR}{Proving [Type of Statement]}\\
\textbf{Goal:} Show that [statement]

\textbf{Strategy:} [Which proof technique to use]

\textbf{Template:}
\begin{enumerate}
    \item Assume/Let [setup]
    \item [Key transformation or application of theorem]
    \item [Intermediate steps]
    \item Therefore [conclusion]
\end{enumerate}

\textbf{Watch out for:}
\begin{itemize}
    \item [Common logical gaps]
    \item [Cases to check separately]
\end{itemize}
\end{KR}
```

### Problem-Solving Strategies:
```latex
\begin{KR}{Solving [Problem Type]}\\
\textbf{Identify:} Recognize this problem type by [characteristics]

\textbf{Approach:}
\begin{enumerate}
    \item Simplify: [Reduction techniques]
    \item Apply: [Which theorem/formula]
    \item Manipulate: [Algebraic steps]
    \item Conclude: [Interpret result]
\end{enumerate}

\textbf{Alternative methods:}
\begin{itemize}
    \item Method B: [When to use, pros/cons]
    \item Method C: [When to use, pros/cons]
\end{itemize}
\end{KR}
```

## Example Structure for Math Courses

```latex
\begin{example2}{[Problem Type] - [Difficulty]}\\
\textbf{Given:} [All provided information with notation]

\textbf{Find:} [What needs to be calculated/proven]

\tcblower

\textbf{Solution:}

\textit{Strategy:} [Brief explanation of approach]

\begin{align*}
[step-by-step calculation with explanations]
\end{align*}

[If multiple steps, break into parts:]

\textit{Part 1: [Substep name]}
$$[calculation]$$

\textit{Part 2: [Substep name]}
$$[calculation]$$

\textbf{Answer:} [Clearly stated final result]

\important{Key technique:} [What makes this solution work / transferable skill]
\end{example2}
```

## Visual Aids for Mathematics

### For Geometric/Visual Concepts:
```latex
\\
\begin{center}
\begin{tikzpicture}
[your tikz code for diagram]
\end{tikzpicture}
\end{center}
\\
```

### For Function Plots:
```latex
\\
\begin{center}
\begin{tikzpicture}
\begin{axis}[
    xlabel=$x$,
    ylabel=$y$,
    grid=major
]
\addplot[blue, thick] {x^2};
\addplot[red, thick] {2*x};
\end{axis}
\end{tikzpicture}
\end{center}
\\
```

### For Comparison Tables:
```latex
\begin{center}
\begin{tabular}{|l|c|c|}
\hline
\textbf{Property} & \textbf{Method A} & \textbf{Method B} \\
\hline
Complexity & $O(n)$ & $O(n^2)$ \\
Accuracy & High & Medium \\
Use when & [condition] & [condition] \\
\hline
\end{tabular}
\end{center}
```

## Formula Sheet Organization

Create dedicated highlight blocks for formula collections:

```latex
\subsection{Formula Reference}

\begin{highlight}{Differentiation Rules}
\mult{2}
\textbf{Basic:}
\begin{itemize}
    \item $(x^n)' = nx^{n-1}$
    \item $(e^x)' = e^x$
    \item $(\ln x)' = \frac{1}{x}$
\end{itemize}

\textbf{Advanced:}
\begin{itemize}
    \item $(f \cdot g)' = f'g + fg'$
    \item $\left(\frac{f}{g}\right)' = \frac{f'g - fg'}{g^2}$
    \item $(f \circ g)' = f'(g) \cdot g'$
\end{itemize}
\multend
\end{highlight}

\begin{highlight}{Integration Rules}
[Similar structure for integrals]
\end{highlight}
```

## Special Considerations

### For Proof-Heavy Courses:
- Include proof sketches for important theorems
- Create KRs for common proof structures (induction, contradiction, etc.)
- Add "intuition" remarks to make proofs memorable

### For Calculation-Heavy Courses:
- Emphasize formula sheets and KRs
- Include many worked examples
- Note calculator/computational shortcuts

### For Abstract Mathematics:
- Focus on definitions and their implications
- Include counterexamples
- Provide visual/intuitive interpretations where possible

---

## Complete Example: Analysis Course Chapter

```latex
\section{Continuity and Limits}

\mult{2}
\begin{definition}{Limit}\\
$\displaystyle \lim_{x \to a} f(x) = L$ means $f(x)$ approaches $L$ as $x$ 
approaches $a$.

\textbf{Formal:} $\forall \epsilon > 0 \ \exists \delta > 0$ such that 
$0 < |x-a| < \delta \Rightarrow |f(x) - L| < \epsilon$
\end{definition}

\begin{concept}{Intuition}\\
The limit describes the behavior of $f$ near $a$, not necessarily at $a$.

\important{Key:} $f(a)$ need not even be defined!
\end{concept}
\multend

\begin{highlight}{Limit Laws}
If $\lim_{x \to a} f(x) = L$ and $\lim_{x \to a} g(x) = M$, then:
\begin{itemize}
    \item $\lim_{x \to a} [f(x) + g(x)] = L + M$
    \item $\lim_{x \to a} [f(x) \cdot g(x)] = L \cdot M$
    \item $\lim_{x \to a} \frac{f(x)}{g(x)} = \frac{L}{M}$ if $M \neq 0$
\end{itemize}
\end{highlight}

\begin{KR}{Computing Limits}\\
\textbf{Strategy selection:}
\begin{enumerate}
    \item \textbf{Direct substitution:} Try $f(a)$ first
    \item \textbf{If $\frac{0}{0}$ form:}
        \begin{itemize}
            \item Factor and cancel
            \item Rationalize (multiply by conjugate)
            \item L'Hôpital's rule: $\lim \frac{f}{g} = \lim \frac{f'}{g'}$
        \end{itemize}
    \item \textbf{If $\frac{\infty}{\infty}$ form:}
        \begin{itemize}
            \item Divide by highest power
            \item L'Hôpital's rule
        \end{itemize}
    \item \textbf{If $\infty - \infty$ form:}
        \begin{itemize}
            \item Combine fractions
            \item Rationalize
        \end{itemize}
\end{enumerate}

\textbf{Verification:} Check limiting behavior from left and right
\end{KR}

\begin{example2}{Indeterminate Form $\frac{0}{0}$}\\
\textbf{Find:} $\displaystyle \lim_{x \to 2} \frac{x^2 - 4}{x - 2}$

\tcblower

\textbf{Solution:}

\textit{Attempt direct substitution:}
$$\frac{2^2 - 4}{2 - 2} = \frac{0}{0} \quad \text{(indeterminate)}$$

\textit{Factor and simplify:}
\begin{align*}
\lim_{x \to 2} \frac{x^2 - 4}{x - 2} &= \lim_{x \to 2} \frac{(x-2)(x+2)}{x-2} \\
&= \lim_{x \to 2} (x + 2) && \text{(cancel for $x \neq 2$)} \\
&= 2 + 2 \\
&= 4
\end{align*}

\textbf{Answer:} $\displaystyle \lim_{x \to 2} \frac{x^2 - 4}{x - 2} = 4$

\important{Key technique:} Factor to cancel the problematic term. This only 
works because we're taking a limit (approaching but not equal to 2).
\end{example2}
```

---

## Time Optimization for Math Courses

Math content typically takes longer due to:
- Complex LaTeX notation
- Alignment of multi-step calculations
- Formula verification

**Strategies:**
1. Extract formulas in batches using highlight blocks
2. Create KR templates for common proof types
3. Use align* environments liberally for readability
4. Build a personal library of tikz templates for common diagrams

**Expected time per chapter:**
- Light math (30% calculations): Use standard workflow
- Medium math (50-70% calculations): +30% time for notation
- Heavy math (>70% calculations): +50% time, but saves massive manual TeXing time
```
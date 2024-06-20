# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath(''))


# -- Project information -----------------------------------------------------

project = 'SNP Labs'
copyright = '2022, stsh'
author = 'stsh'
master_doc = 'index'

# The full version, including alpha/beta/rc tags
release = ''

#LaTex




# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'myst_parser', # pip install myst-parser
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    #'sphinxcontrib.mermaid',# pip install sphinxcontrib-mermaid
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages'
]

myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

# -- Options for LaTeX output ---------------------------------------------
latex_engine = 'pdflatex'

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    'papersize': 'a4paper',
    'releasename':" ",
    # Sonny, Lenny, Glenn, Conny, Rejne, Bjarne and Bjornstrup
    # 'fncychap': '\\usepackage[Lenny]{fncychap}',
    'fncychap': '\\usepackage{fncychap}',
    'fontpkg': '\\usepackage{amsmath,amsfonts,amssymb,amsthm}',
    'figure_align':'htbp',
    # The font size ('10pt', '11pt' or '12pt').
    #
    'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    'preamble': r'''
        %% %% %% %% %% %% %% %% %% %% Meher %% %% %% %% %% %% %% %% %%
        %% %add number to subsubsection 2=subsection, 3=subsubsection
        %% % below subsubsection is not good idea.
        \setcounter{secnumdepth}{3}
        %
        %% %% Table of content upto 2=subsection, 3=subsubsection
        \setcounter{tocdepth}{2}
        \usepackage{amsmath,amsfonts,amssymb,amsthm}
        \usepackage{graphicx}
        %% % r educe spaces for Table of contents, figures and tables
        %% % i t is used "\addtocontents{toc}{\vskip -1.2cm}" etc. in the document
        \usepackage[notlot,nottoc,notlof]{}
        \usepackage{color}
        \usepackage{transparent}
        \usepackage{eso-pic}
        \usepackage{lipsum}
	\usepackage{lmodern}
        \usepackage{footnotebackref} %% link at the footnote to go to the place of footnote in the text
        %% spacing between line
        \usepackage{setspace}
        %% %% \onehalfspacing
        %% %% \doublespacing
        \singlespacing
        %% %% %% %% %% % d atetime
        \usepackage{datetime}
        \newdateformat{MonthYearFormat}{%
        \monthname[\THEMONTH], \THEYEAR}
        %% RO, LE will not work for 'oneside' layout.
        %% Change oneside to twoside in document class
        \usepackage{fancyhdr}
        \pagestyle{fancy}
        \fancyhf{}
        %% % Alternating Header for oneside
        \fancyhead[L]{\ifthenelse{\isodd{\value{page}}}{ \small \nouppercase{\leftmark} }{}}
        \fancyhead[R]{\ifthenelse{\isodd{\value{page}}}{}{ \small \nouppercase{\rightmark} }}
        %% % Alternating Header for two side
        %\fancyhead[RO]{\small \nouppercase{\rightmark}}
        %\fancyhead[LE]{\small \nouppercase{\leftmark}}
        %% for oneside: change footer at right side. If you want to use Left and right then use same as header defined above.
        %% %\fancyfoot[R]{\ifthenelse{\isodd{\value{page}}}{{\tiny } }{\href{http://pythondsp.readthedocs.io/en/latest/pythondsp/toc.html}{\tiny PythonDSP}}}
        %% % Alternating Footer for two side
        %\fancyfoot[RO, RE]{\scriptsize  ()}
        %% % page number
        \fancyfoot[CO, CE]{\thepage}
        \renewcommand{\headrulewidth}{0.5pt}
        \renewcommand{\footrulewidth}{0.5pt}
        
        \RequirePackage{tocbibind} %% % c omment this to remove page number for following
        \addto\captionsenglish{\renewcommand{\contentsname}{Table of contents}}
        \addto\captionsenglish{\renewcommand{\listfigurename}{List of figures}}
        \addto\captionsenglish{\renewcommand{\listtablename}{List of tables}}
        % \addto\captionsenglish{\renewcommand{\chaptername}{Chapter}}
        %% reduce spacing for itemize
        \usepackage{enumitem}
        \setlist{nosep}
        %% %% %% %% %% % Quote Styles at the top of chapter
        \usepackage{epigraph}
        \setlength{\epigraphwidth}{0.8\columnwidth}
        \newcommand{\chapterquote}[2]{\epigraphhead[60]{\epigraph{\textit{#1}}{\textbf {\textit{--#2}}}}}
        %% %% %% %% %% % Quote for all places except Chapter
        \newcommand{\sectionquote}[2]{{\quote{\textit{``#1''}}{\textbf {\textit{--#2}}}}}
        ''',
        
        'maketitle': r'''
        \pagenumbering{Roman} %% % to avoid page 1 conflict with actual page 1
        \begin{titlepage}
        \centering
        \vspace*{40mm} %% % * is used to give space from top
        \textbf{\Huge {SNP Laboratories}}
        \vspace{0mm}
        \begin{figure}[!h]
        \centering
        \includegraphics[scale=0.5]{en-zhaw-ines-rgb.png}
        \end{figure}
        \begin{figure}[!h]
        \centering
        \textbf{ welo, bazz, fisa, huno, grop, donn, scia }
        \end{figure}
        \vspace*{20mm}
        \vspace{20mm}
        
        \vspace*{0mm}
        \small Last updated : \MonthYearFormat\today
        %% \vfill adds at the bottom
        \vfill
        \small \textit{More documents are available at }{\href{https://github.zhaw.ch/SNP/snp-lab-code}{github.zhaw.ch}}
        \end{titlepage}
        \clearpage
        \pagenumbering{roman}
        \tableofcontents
        %% %\listoffigures
        %% %\listoftables
        \clearpage
        \pagenumbering{arabic}
        ''',


    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
    'sphinxsetup': \
        'hmargin={0.7in,0.7in}, vmargin={1in,1in}, \
        verbatimwithframe=true, \
        TitleColor={rgb}{0,0,0}, \
        HeaderFamily=\\rmfamily\\bfseries, \
        InnerLinkColor={rgb}{0,0,1}, \
        OuterLinkColor={rgb}{0,0,1}',
        'tableofcontents':' ',
}

latex_logo = 'en-zhaw-ines-rgb.png'
# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
# author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'main.tex', 'SNP Laboratories',
    '', 'report')
]


# ---------------------------------------------------

# Add any paths that contain templates here, relative to this directory.
templates_path = ['templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#
# today = ''
#
# Else, today_fmt is used as the format for a strftime call.
#
# today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# These patterns also affect html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The reST default role (used for this markup: `text`) to use for all
# documents.
#
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

highlight_options = {
  'default': {'stripall': True},
  'php': {'startinline': True},
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'
html_theme_path = ['_static']

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_theme_options = {
    'logo': 'logo.png',
    'logo_name' : 'true',
}

language = "en"
myst_html_meta = {
    "description lang=en": "metadata description",
    "description lang=fr": "description des métadonnées",
    "keywords": "Sphinx, MyST",
    "property=og:locale":  "en_US"
}

# About
`beam_me_up.py` is a simple Python script used to automatically convert a paper written in LaTeX directly to a Beamer slide deck (also in LaTeX). The script searches through raw LaTeX and extracts specific environments (i.e., figures, equations, etc.), placing each on its own slide in the Beamer slide deck.

# Dependencies
Install the [TexSoup package](https://texsoup.alvinwan.com/).

# How To Use
1. Paste the `beam_me_up.py` file in your paper's main directory.
2. Run `beam_me_up.py`. 
3. Wait a few seconds.
4. Open `slides/slides.tex` and compile it (e.g., using TeXstudio).

# Details
By default, `beam_me_up` assumes that users make use of several section files in their paper. For instance, the `main.tex` file of the paper may look something like this.
```
\documentclass[...]{...}
...
\input{math.tex}
\input{glossary.tex}

\begin{document}

\input{sec-introduction.tex}
\input{sec-system-model.tex}
\input{sec-contribution.tex}
\input{sec-results.tex}
\input{sec-conclusion.tex}

\end{document}
```
Here, `sec-*.tex` contains LaTeX for a given section (e.g., a System Model section) and exists in the same directory as `main.tex`. You can tailor `beam_me_up` to work with whatever convention you use. For instance, if you just use a single `main.tex` file, simply only have `beam_me_up` search through that single file.

By default, `beam_me_up` will search through all LaTeX files with the form `sec-*.tex`.
It will search for specific environments within each.
Currently, `beam_me_up` will search for the following LaTeX environments:
- `figure`, `figure*`
- `equation`, `equation*`
- `align`, `align*`
- `gather`, `gather*`
- `subequations`, `subequations*`
- `theorem`, `theorem*`
- `lemma`, `lemma*`
- `corollary`,`corollary*`
- `definition`,`definition*`

`beam_me_up` will create a `slides/` directory wherever it is being run and will place all of its output there.

For each `sec-*.tex` file, `beam_me_up` will extract each instance of these environments and place it verbatim on its own Beamer frame in a file `slides/sec-*.tex`.

`beam_me_up` will create a `slides/slides.tex` file, which it will populate as the main Beamer slide deck file. This file can be compiled to produce your PDF slide deck.

It is assumed that there exists `math.tex` and  `glossary.tex`, which `beam_me_up` will also copy into `slides/` and will include in the preamble of the `slides/slides.tex` Beamer file.

`beam_me_up` also copies several folders by default into `slides/`. For example, it will copy the `fig` directory to create `slides/fig`. This allows filenames to be preserved when compiling the slide deck from within the `slides/` directory and allows users to cut the `slides/` directory from their working directory and paste it elsewhere.

# Example Output
Example files output by `beam_me_up`.
```
slides/fig/
slides/plots/
slides/slides.tex
slides/sec-introduction.tex
slides/sec-system-model.tex
slides/sec-contribution.tex
slides/sec-results.tex
slides/sec-conclusion.tex
slides/math.tex
```

Example `slides/slides.tex` file (sections are output in alphabetical order).
```
\documentclass[aspectratio=1610,smaller]{beamer}

\usepackage{amsmath,amssymb,lmodern}
\usepackage[T1]{fontenc}
\usefonttheme[onlymath]{serif}
\usepackage[caption=false,font=footnotesize]{subfig}

\newcommand{\envalias}[2]{\newenvironment{#1}{\begin{#2}}{\end{#2}}}
\envalias{figure*}{figure}

\title{Title Here}
\subtitle{Subtitle Here}
\author{Author Here}
\institute{Institute Here}
\date{\today}

\input{math.tex}
\input{glossary.tex}

\begin{document} 

\maketitle

\input{sec-conclusion.tex}
\input{sec-contribution.tex}
\input{sec-introduction.tex}
\input{sec-results.tex}
\input{sec-system-model.tex}

\end{document}
```

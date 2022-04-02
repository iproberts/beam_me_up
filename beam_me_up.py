#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def readfile(filename):
  f = open(filename,'r')
  s = f.read()
  f.close()
  return s

def writefile(filename,s):
  f = open(filename,'w')
  f.write(s)
  f.close()
  return

def appendfile(filename,s,newline=True):
  if newline:
    s = '\n' + s + '\n'
  f = open(filename,'a')
  f.write(s)
  f.close()
  return

def create_beamer_frame(contents,title='\\insertsection'):
  s = "\\begin{frame}" + "{" + title + "}" + '\n' + contents + '\n' + "\\end{frame}"
  return s

def init_beamer_deck():
  s = "\\documentclass[aspectratio=1610,smaller]{beamer}" + '\n\n' + \
      "\\usepackage{amsmath,amssymb,lmodern}" + '\n' + \
      "\\usepackage[T1]{fontenc}" + '\n' + \
      "\\usefonttheme[onlymath]{serif}" + '\n' + \
      "\\usepackage[caption=false,font=footnotesize]{subfig}" + '\n\n' + \
      "\\newcommand{\\envalias}[2]{\\newenvironment{#1}{\\begin{#2}}{\\end{#2}}}" + '\n' + \
      "\\envalias{figure*}{figure}" + '\n\n' + \
      "\\title{Title Here}" + '\n' + \
      "\\subtitle{Subtitle Here}" + '\n' + \
      "\\author{Author Here}" + '\n' + \
      "\\institute{Institute Here}" + '\n' + \
      "\\date{\\today}" + '\n\n' + \
      "\\input{math.tex}" + '\n' + \
      "\\input{glossary.tex}" + '\n\n' + \
      "\\begin{document} " + '\n\n' + \
      "\\maketitle" + '\n\n'+ \
      "%\\begin{frame}{Outline}\\tableofcontents\\end{frame}" + '\n'
  return s

def end_beamer_deck():
  s = "\\end{document}"
  return s

def tex_to_beamer(tex_filename):
  filename = tex_filename
  beamer_filename = 'slides/' + filename
  tex = readfile(filename)
  
  # create section
  writefile(beamer_filename,'\\section{' + filename + '}\n')
  
  # parse LaTeX
  soup = TexSoup(tex)
  
  # environments to extract
  envs = ['figure','figure*','equation','equation*','align','align*','subequations','subequations*','gather','gather*','theorem','theorem*','definition','definition*','lemma','lemma*','corollary','corollary*']
  
  # extract each on its own slide
  for env in envs:
    gen = soup.find_all(env)
    
    s = []
    num_elem = soup.count(env)
    for i in range(num_elem):
      s.append(next(gen))
    
    for i in range(num_elem):
      frame = create_beamer_frame(str(s[i]))
      appendfile(beamer_filename,frame,newline=True)
    
  return

def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy(src, dst)
        # else: raise

# Main
from TexSoup import TexSoup
import glob, os
import shutil, errno

# Create slides directory
os.makedirs('slides',exist_ok=True)

# Copy directories if exist
direcs = ['fig','plots','tab','alg','bibtex']
for d in direcs:
  copyanything(d,'slides/'+d)

# Copy files if exist (e.g., macro files)
files = ['math.tex','glossary.tex']
for f in files:
  copyanything(f,'slides/'+f)

# Copy all .bib files
for f in glob.glob("*.bib"):
  copyanything(f,'slides/'+f)

# Create main deck file
filename_deck = 'slides/slides.tex'
s = init_beamer_deck() # preamble, start of main slide deck
writefile(filename_deck,s)

# Create each section
for file in sorted(glob.glob("sec-*.tex")):
    tex_to_beamer(file) # parse and write to frames
    s = "\\input{" + file + "}" # include in slides.tex
    appendfile(filename_deck,s,newline=True)

# Close main deck file
s = end_beamer_deck()
appendfile(filename_deck,s)

#!/bin/sh
python2 generate_page.py
cd cv
pdflatex seokhwan-cv.tex
pythontex --interpreter python:python2 seokhwan-cv.tex
pdflatex seokhwan-cv.tex
cd ..
git add index.html
git add cv/seokhwan-cv.pdf
git commit -m 'contents updated'
git push

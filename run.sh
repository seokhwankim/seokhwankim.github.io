#!/bin/sh
python generate_page.py
cd cv
pdflatex seokhwan-cv.tex
pythontex seokhwan-cv.tex
pdflatex seokhwan-cv.tex
cd ..
git add index.html
git add cv/seokhwan-cv.pdf
git commit -m 'contents updated'
git push

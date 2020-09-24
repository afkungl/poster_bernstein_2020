LATEXEXE=pdflatex
MV=mv
BIBTEXEXE=bibtex

handout.pdf:
	$(LATEXEXE) poster
	$(LATEXEXE) poster
	$(BIBTEXEXE) poster
	$(LATEXEXE) poster

cleanall: clean
	$(RM) main.pdf

clean:
	$(RM) *.toc *.nav *.out *.snm *.bak *.aux *.log *.bbl *.blg *.lof *.lot

.PHONY: main.pdf cleanall clean


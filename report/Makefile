.SUFFIXES:	.pdf .md

.md.pdf:
# add --listing for captions in listings...
	pandoc --resource-path=img $*.md -f markdown -o $*.pdf

IMGPATH=img

IMG = \
	$(IMGPATH)/q1_heatmap_0_120.png \
	$(IMGPATH)/q1_heatmap_26_120.png \


.PHONY: all clean mrproper

all: assignment.pdf

assignment.pdf: $(IMG)

clean:
	rm -fv *.aux *.bbl *.blg *.log *.out *.toc

mrproper: clean
	rm -fv *.pdf

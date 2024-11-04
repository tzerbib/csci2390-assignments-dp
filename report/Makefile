.SUFFIXES:	.pdf .md

IMGPATH=img

IMG = \
	$(IMGPATH)/age_music_heatmap_0_120.png \
	$(IMGPATH)/age_music_heatmap_26_120.png \
	$(IMGPATH)/age_color_heatmap_0_120.png \
	$(IMGPATH)/age_color_heatmap_26_120.png \
	$(IMGPATH)/laplace_pdf.png \


.PHONY: clean mrproper

assignment.pdf: assignment.md $(IMG)
	pandoc --listing --resource-path=img $*.md -f markdown -o $*.pdf

clean:
	rm -fv *.aux *.bbl *.blg *.log *.out *.toc

$(IMG): generate_results.py
	python3 generate_results.py


mrproper: clean
	rm -fv *.pdf

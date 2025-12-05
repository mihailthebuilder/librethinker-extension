unodit-code:
	python ../unodit/unodit.py -m 'sidebar_convert' -d 'C:\Users\mihai\projects\librethinker-extension\extension' -a 'LibreThinker' -p 1

unodit-files:
	python3 ../unodit/unodit.py -m 'sidebar_files' -d 'C:\Users\mihai\projects\librethinker-extension\extension' -a 'LibreThinker' -p 1

unodit-zip:
	python3 ../unodit/unodit.py -m 'sidebar_oxt' -d 'C:\Users\mihai\projects\librethinker-extension\extension' -a 'LibreThinker' -p 1
	mkdir -p dist
	mv "extension/LibreThinker''.oxt" dist/LibreThinker.oxt

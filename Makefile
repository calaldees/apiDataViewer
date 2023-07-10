run: cache_tools.py
	python3 main.py

pdb:
	python3 -m pdb -c continue main.py

cache_tools.py:
	curl https://raw.githubusercontent.com/calaldees/libs/master/python3/calaldees/cache_tools.py -O


clear:
	rm -rf __*
run: cache_tools.py
	python3 extract.py

cache_tools.py:
	curl https://raw.githubusercontent.com/calaldees/libs/master/python3/calaldees/cache_tools.py -O

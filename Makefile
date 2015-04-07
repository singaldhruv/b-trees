all: tree.py
	python tree.py >stats.out

clean:
	rm -rf data/

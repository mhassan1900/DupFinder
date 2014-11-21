

all: gui

gui:
	python dup_gui.py 


cmdline:
	python DuplicateFinder.py ".."

clean:
	rm *.pyc

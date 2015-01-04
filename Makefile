

all: 
	@echo "Choose from following targets <gui|install|uninstall|cmdline|clean" 

gui:
	python dup_gui.py 

install:
	python2.7 ./setup.py install --user

uninstall:
	pip uninstall dupfinder_wx 

cmdline:
	python DuplicateFinder.py ".."

clean:
	find . -name '*.pyc' -exec rm -rf {} \;
	/bin/rm -rf  ./dist ./build ./src/*.egg*




project=dupfinder
save_lint=n

all: 
	@echo "Choose from following targets <lint|install|uninstall||clean" 

lint:
	cd src && pylint --rcfile ../.pylintrc $(project) -f colorized  --files-output=$(save_lint) 

install:
	python2.7 ./setup.py install --user

uninstall:
	pip uninstall $(project)

clean:
	find . -name '*.pyc' -exec rm -rf {} \;
	find . -name '*.egg*' -exec rm -rf {} \;
	/bin/rm -rf  ./dist ./build 




project=dupfinder
save_lint=n
pylintrc=.pylintrc

all: 
	@echo "Choose from following targets lint|install|uninstall|clean" 

lint:
	# cd src && pylint --rcfile ../.pylintrc $(project) -f colorized  --output $(save_lint) 
	cd src && pylint --rcfile ../$(pylintrc) $(project) -f colorized  

install:
	# python ./setup.py install --user
	python ./setup.py install 

uninstall:
	pip uninstall $(project)

clean:
	find . -name '*.pyc' -exec rm -rf {} \;
	find . -name '*.egg*' -exec rm -rf {} \;
	/bin/rm -rf  ./dist ./build 


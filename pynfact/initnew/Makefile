# Makefile :: Py'nFact
#
# Modify this file to your convenience

BIN = python ./pynfact/cli.py
PORT = 4000 # test port when serving on local machine.


all:
	make build
#	make upload

build:
	${BIN} build

serve:
	${BIN} serve ${PORT}

test:
	make build
	make serve

#upload:
#	rsync -e 'ssh' -a _build/ http://your.site.com/
#	@echo "Done."


.PHONY: docs

docs: docs/index.html

docs/index.html: $(shell find src -name "*.py")
	python3 -m robot.libdoc src/AkamaiLibrary docs/index.html

DOCS=docs

.PHONY: docs tests


docs:
	cd $(DOCS) && $(MAKE) clean && $(MAKE) html
		
docs-online:
	ghp-import -np $(DOCS)/_build/html

python-hosted:
	python setup.py upload_docs --upload-dir=docs/_build/html
	
tests:
# 	py.test tests

install:
	python setup.py install

pypi:
	python setup.py sdist upload
	
binstar:

	
# sdist:
# 	python setup.py sdist
	
final:
	$(MAKE) tests
	$(MAKE) docs
	$(MAKE) docs-online
	$(MAKE) python-hosted
	$(MAKE) pypi
	$(MAKE) binstar
	

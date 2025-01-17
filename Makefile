# Makefile for maintainer tasks

PACKAGE=sokoban

po/$(PACKAGE).pot: po/$(PACKAGE).pot.in
	sed -e s/VERSION/$$(grep version pyproject.toml | grep -o "[0-9.]\+")/ < $^ > $@

update-pot:
	$(MAKE) po/$(PACKAGE).pot
	find $(PACKAGE) -name "*.py" | xargs xgettext --add-comments=TRANSLATORS --from-code=utf-8 --default-domain=$(PACKAGE) --output=po/$(PACKAGE).pot.in

update-po:
	for po in po/*.po; do [ -e "$$po" ] || continue; msgmerge --update $$po po/$(PACKAGE).pot; done

compile-po:
	for po in po/*.po; do [ -e "$$po" ] || continue; mo=$(PACKAGE)/locale/$$(basename $${po%.po})/LC_MESSAGES/$(PACKAGE).mo; mkdir -p $$(dirname $$mo); msgfmt --output-file=$$mo $$po; done

update-pofiles:
	$(MAKE) update-pot
	$(MAKE) po/$(PACKAGE).pot
	$(MAKE) update-po
	$(MAKE) compile-po

build:
	$(MAKE) update-pofiles
	python -m build

dist:
	git diff --exit-code && \
	rm -rf ./dist && \
	mkdir dist && \
	$(MAKE) build

test:
	tox

release:
	make test
	make dist
	twine upload dist/* && \
	git tag v$$(grep version pyproject.toml | grep -o "[0-9.]\+") && \
	git push --tags

loc:
	cloc --exclude-content="ptext module" $(PACKAGE)/*.py

.PHONY: dist build

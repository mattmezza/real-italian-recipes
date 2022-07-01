.PHONY: dev build release deploy

tw=npx tailwindcss -i ./src/style.css -o ./src/public/style.css
serve=npx five-server
check_defined = \
    $(strip $(foreach 1,$1, \
        $(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
    $(if $(value $1),, \
      $(error Undefined $1$(if $2, ($2))))


init:
	brew install zip
	brew install gh
dev:
	$(tw) --watch & $(serve)
build:
	$(tw)
release: build
	@:$(call check_defined, v, The version number e.g. 1.0.0 - specify like this 'make release v=1.0.0')
	git tag v$(v)
	git push origin v$(v)
	cd src/public && zip -r v$(v).zip .
	gh release create v$(v) 'src/public/v$(v).zip#Real Italian Recipes v$(v)' --generate-notes
	rm -f src/public/v$(v).zip
deploy: release
	git branch -f gh-pages
	git checkout gh-pages
	git reset --hard origin/main
	find . -maxdepth 1 ! -name src ! -name .git -exec rm -r {} ';'
	cp -r src/public/* .
	rm -r src
	echo 'realitalianrecipes.com' > CNAME
	git add -A .
	git commit -a -m 'gh-pages update'
	git push origin gh-pages --force
	git checkout main

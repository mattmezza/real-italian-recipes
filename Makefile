tw=npx tailwindcss -i ./src/style.css -o ./src/public/style.css
serve=npx five-server

dev:
	$(tw) --watch & $(serve)
build:
	$(tw)
deploy: build
	git branch -f gh-pages
	git checkout gh-pages
	git reset --hard origin/main
	find . -maxdepth 1 ! -name src -delete
	cp -r src/public/* .
	rm -r src
	echo 'realitalianrecipes.com' > CNAME
	git add -A .
	git commit -a -m 'gh-pages update'
	git push origin gh-pages --force
	git checkout main

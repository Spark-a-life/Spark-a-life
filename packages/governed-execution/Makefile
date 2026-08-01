.PHONY: demo test check serve keygen clean docker-build docker-demo

demo:
	npm run demo

test:
	npm test

check:
	npm run check

serve:
	npm run serve

keygen:
	npm run keygen

clean:
	npm run clean

docker-build:
	docker build -t wisegen-ape-governed-execution:1.0.0 .

docker-demo:
	docker compose run --rm control-plane npm run demo

EXT_NAME:=com.github.cacciaresi-ulauncher-asana
EXT_DIR:=$(shell pwd)

.PHONY: help lint format link unlink deps dev
.DEFAULT_TARGET: help

help: ## Show help menu
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

lint: ## Run Pylint
	@find . -iname "*.py" | xargs pylint

format: ## Format code using yapf
	@yapf --in-place --recursive .

link: ## Symlink the project source directory with Ulauncher extensions dir.
	ln -s ${EXT_DIR} ~/.local/share/ulauncher/extensions/${EXT_NAME}

unlink: ## Unlink extension from Ulauncher
	@rm -r ~/.local/share/ulauncher/extensions/${EXT_NAME}

deps: ## Install Python Dependencies
	pip3 install -r requirements.txt

dev: ## Runs Ulauncher on development mode
	ulauncher --no-extensions --dev -v

debug: ## Runs the extension in debug mode
	VERBOSE=1 ULAUNCHER_WS_API=ws://127.0.0.1:5054/com.github.cacciaresi-ulauncher-asana PYTHONPATH=/usr/lib/python3/dist-packages /usr/bin/python3 ~/.local/share/ulauncher/extensions/com.github.cacciaresi-ulauncher-asana/main.py

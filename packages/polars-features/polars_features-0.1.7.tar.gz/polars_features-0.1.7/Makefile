.PHONY: build publish release setup

setup:
	@command -v maturin >/dev/null 2>&1 || { echo "Installing maturin..."; pip install maturin; }

build: setup
	maturin build

publish: build
	maturin publish

release: setup
	@echo "Select the type of release (patch, minor, major):"
	@read release_type; \
	if [ "$$release_type" = "patch" ] || [ "$$release_type" = "minor" ] || [ "$$release_type" = "major" ]; then \
		poetry version $$release_type; \
		git add pyproject.toml; \
		git commit -m "Bump version to $$(poetry version -s)"; \
		echo ""; \
		echo "Note: If git push fails due to large files, you may need to set up Git LFS:"; \
		echo "1. Install Git LFS: https://git-lfs.github.com"; \
		echo "2. Run: git lfs install"; \
		echo "3. Track large files: git lfs track \"*.rlib\" \"dist/*.tar.gz\""; \
		echo "4. Try the release process again"; \
		echo ""; \
		if git push --set-upstream origin main || git push; then \
			maturin build && maturin publish; \
		else \
			echo "Git push failed. Please fix the issues above and try again."; \
			exit 1; \
		fi \
	else \
		echo "Invalid release type: $$release_type"; \
		echo "Please use patch, minor, or major."; \
		exit 1; \
	fi

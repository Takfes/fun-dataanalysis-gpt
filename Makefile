.DEFAULT_GOAL := help

.PHONY: help
help:
	@uv run python -c "import re; \
	[[print(f'\033[36m{m[0]:<20}\033[0m {m[1]}') for m in re.findall(r'^([a-zA-Z_-]+):.*?## (.*)$$', open(makefile).read(), re.M)] for makefile in ('$(MAKEFILE_LIST)').strip().split()]"

.PHONY: install
install: ## Install the virtual environment and install the pre-commit hooks
	@echo "🚀 Creating virtual environment using uv"
	@uv sync
	@uv run pre-commit install

.PHONY: check
check: ## Run code quality tools.
	@echo "🚀 Checking lock file consistency with 'pyproject.toml'"
	@uv lock --locked
	@echo "🚀 Linting code: Running pre-commit"
	@uv run pre-commit run -a
	@echo "🚀 Static type checking: Running mypy"
	@uv run mypy
	@echo "🚀 Checking for obsolete dependencies: Running deptry"
	@uv run deptry .

.PHONY: app
app: ## Run the application
	@echo "🚀 Running the application"
	@uv run streamlit run app/app.py

.PHONY: test
test: ## Test the code with pytest
	@echo "🚀 Testing code: Running pytest"
	@uv run python -m pytest --cov --cov-config=pyproject.toml --cov-report=xml

.PHONY: build
build: clean-build ## Build wheel file
	@echo "🚀 Creating wheel file"
	@uvx --from build pyproject-build --installer uv

.PHONY: clean-build
clean-build: ## Clean build artifacts
	@echo "🚀 Removing build artifacts"
	@uv run python -c "import shutil; import os; shutil.rmtree('dist') if os.path.exists('dist') else None"

.PHONY: docs-test
docs-test: ## Test if documentation can be built without warnings or errors
	@uv run mkdocs build -s

.PHONY: docs
docs: ## Build and serve the documentation
	@uv run mkdocs serve

.PHONY: clean-data
clean-data: ## Clean up the data directory
	@echo "🚀 Cleaning up the data directory..."
	rm -rf ./data/*
	@echo "✅ Data directory is clean."

.PHONY: get-amazon-data
get-amazon-data: ## Download, unzip, and clean up the Amazon dataset
	@echo "🚀 Downloading Amazon dataset from Kaggle..."
	kaggle datasets download sujalsuthar/amazon-delivery-dataset -p ./data/amazon
	@echo "📦 Unzipping the Amazon dataset..."
	unzip -o ./data/amazon/amazon-delivery-dataset.zip -d ./data/amazon
	@echo "🧹 Cleaning up ZIP files..."
	rm ./data/amazon/amazon-delivery-dataset.zip
	@echo "🔄 Renaming extracted CSV file..."
	mv ./data/amazon/*.csv ./data/amazon/amazon.csv
	@echo "✅ amazon dataset is ready in ./data/amazon/amazon.csv"

.PHONY: get-zomato-data
get-zomato-data: ## Download, unzip, and clean up the Zomato dataset
	@echo "🚀 Downloading Zomato dataset from Kaggle..."
	kaggle datasets download saurabhbadole/zomato-delivery-operations-analytics-dataset -p ./data/zomato
	@echo "📦 Unzipping the Zomato dataset..."
	unzip -o ./data/zomato/zomato-delivery-operations-analytics-dataset.zip -d ./data/zomato
	@echo "🧹 Cleaning up ZIP files..."
	rm ./data/zomato/zomato-delivery-operations-analytics-dataset.zip
	@echo "🔄 Renaming extracted CSV file..."
	mv ./data/zomato/*.csv ./data/zomato/zomato.csv
	@echo "✅ zomato dataset is ready in ./data/zomato/zomato.csv"

.PHONY: load-amazon-data
load-amazon-data: ## Load the amazon dataset into the database
	@echo "🚀 Loading amazon dataset into the database..."
	@uv run python scripts/load_to_duckdb.py --data amazon
	@echo "✅ amazon dataset is loaded into the database."

.PHONY: load-zomato-data
load-zomato-data: ## Load the zomato dataset into the database
	@echo "🚀 Loading zomato dataset into the database..."
	@uv run python scripts/load_to_duckdb.py --data zomato
	@echo "✅ zomato dataset is loaded into the database."

.PHONY: get-load-amazon-data
get-load-amazon-data: get-amazon-data load-amazon-data ## Download, unzip, and load the amazon dataset into the database

.PHONY: get-load-zomato-data
get-load-zomato-data: get-zomato-data load-zomato-data ## Download, unzip, and load the zomato dataset into the database

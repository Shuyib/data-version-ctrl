# .DEFAULT_GOAL tells make which target to run when no target is specified
.DEFAULT_GOAL := all

# .PHONY tells make that these targets do not represent actual files
.PHONY: all install clean

# run all commands
all: install create_dirs

# Specify python location in virtual environment
# Specify pip location in virtual environment
ORIGINAL_PY_VERSION := $(shell python3 --version)
PYTHON := .venv/bin/python3
PIP := .venv/bin/pip3
DOCKER_CONTAINER_NAME := ML_workflow:v0.0.0
DATA_DIR := data/
OUTPUT_DIR := output/
MODEL_OUTPUT_DIR := model_output/


venv/bin/activate: requirements.txt
	# create virtual environment
	python3 -m venv .venv
	# make command executable
	chmod +x .venv/bin/activate
	# activate virtual environment
	. .venv/bin/activate

activate:
	# activate virtual environment
	# run . .venv/bin/activate manually if it doesn't work
	. .venv/bin/activate

install: venv/bin/activate requirements.txt # prerequisite
	# install commands
	# This is step 1: install the virtual environment
	# Py version using py 3.10 from envname
	@echo "Python version: $(ORIGINAL_PY_VERSION)"
	@echo "Installing virtual environment"
	@echo "This is step 1: install the virtual environment"
	$(PIP) --no-cache-dir install --upgrade pip &&\
		$(PIP) --no-cache-dir install -r requirements.txt

docstring: activate
	# format docstring
	pyment -w -o numpydoc *.py
  
format: activate 
	# format code
	black *.py

clean:
	@echo "Cleaning up"
	# clean directory of cache
	rm -rf __pycache__ &&\
	rm -rf utils/__pycache__ &&\
	rm -rf testing/__pycache__ &&\
	rm -rf .pytest_cache &&\
	rm -rf .venv
	rm -rf db

lint: activate install format
	# flake8 or #pylint
	pylint --disable=R,C --errors-only *.py utils/*.py testing/*.py

# Make sure the directories have been created
create_dirs:
	@echo "Creating directories"
	@echo "This is step 2: create directories"
	mkdir -p -v $(DATA_DIR)
	mkdir -p -v $(OUTPUT_DIR)
	mkdir -p -v $(MODEL_OUTPUT_DIR)
	@echo "Directories created"
	@echo "remember to follow these steps https://www.kaggle.com/discussions/general/74235"

import_data: create_dirs
	@echo "Importing data from Kaggle"
	@echo "This is step 3: import data"
	@echo "The data folder has a new dataset"
	@echo "Your task Can you accurately predict insurance costs? Regression problem"
	# make sure script is executable
	chmod +x import_data.sh
	# run script
	./import_data.sh

clean_data: import_data data/original_data/insurance.csv
	@echo "Cleaning data"
	@echo "This is step 4: clean data"
	@echo "The data folder has a cleaned dataset in data/transform"
	$(PYTHON) cleandata.py load_data --file_path data/original_data/insurance.csv
	$(PYTHON) cleandata.py summary --file_path data/original_data/insurance.csv
	$(PYTHON) cleandata.py check_missing --file_path data/original_data/insurance.csv
	$(PYTHON) cleandata.py check_duplicate --file_path data/original_data/insurance.csv
	$(PYTHON) cleandata.py encode_data --file_path data/original_data/insurance.csv --version 000
	@echo "Data cleaned"

eda: clean_data
	@echo "Performing EDA"
	@echo "This is step 5: EDA"
	@echo "The output folder has an EDA report in output/eda"
	$(PYTHON) eda.py --input data/transform/insurance_000.parquet --output output/eda_combined_plots.png

split_data: eda
	@echo "Splitting data"
	@echo "This is step 6: split data"
	@echo "The output folder has a split dataset in data/transform/validation"
	@echo "For train test split"
	$(PYTHON) split_data.py --data data/transform/insurance_000.parquet --strategy train_test_split --test_size 0.2
	@echo "For kfold split"
	#$(PYTHON) split_data.py --data data/transform/insurance_000.parquet --strategy kfold --test_size 0.2 --n_splits 5

evaluate_model: split_data
	@echo "Evaluating model"
	@echo "This is step 7: evaluate model"
	@echo "The output folder has a model evaluation in output/model_evaluation"
	#$(PYTHON) evaluate_model.py --data data/transform/validation/insurance_000_train.parquet --model_name linear_regression --model_output model_output/linear_regression_000.pkl
	#$(PYTHON) evaluate_model.py --data data/transform/validation/insurance_000_train.parquet --model_name random_forest --model_output model_output/random_forest_000.pkl
	#$(PYTHON) evaluate_model.py --data data/transform/validation/insurance_000_train.parquet --model_name xgboost --model_output model_output/xgboost_000.pkl
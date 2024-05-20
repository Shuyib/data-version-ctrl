# .DEFAULT_GOAL tells make which target to run when no target is specified
.DEFAULT_GOAL := all

# .PHONY tells make that these targets do not represent actual files
.PHONY: all install clean format lint create_dirs activate_venv import_data clean_data eda split_data evaluate_model

# run all commands
all: 
	dvc repro

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

activate_venv:
	# activate virtual environment
	# run . .venv/bin/activate manually if it doesn't work
	@echo "Activating virtual environment"
	dvc repro activate_venv


install: venv/bin/activate requirements.txt # prerequisite
	# install commands
	# This is step 1: install the virtual environment
	# Py version using py 3.10 from envname
	@echo "Python version: $(ORIGINAL_PY_VERSION)"
	@echo "Installing virtual environment"
	@echo "This is step 1: install the virtual environment"
	$(PIP) --no-cache-dir install --upgrade pip &&\
		$(PIP) --no-cache-dir install -r requirements.txt
docstring: 
	# format docstring
	pyment -w -o numpydoc *.py
  
format: 
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
	rm -rf data
	rm -rf output
	rm -rf model_output
	

lint: activate install format
	# flake8 or #pylint
	pylint --disable=R,C --errors-only *.py utils/*.py testing/*.py

init:
	@echo "Initializing DVC"
	dvc init

# Make sure the directories have been created
create_dirs:
	@echo "Creating directories"
	@echo "This is step 2: create directories"
	dvc repro create_dirs

import_data: 
	@echo "Importing data from Kaggle"
	@echo "This is step 3: import data"
	@echo "The data folder has a new dataset"
	@echo "Your task Can you accurately predict insurance costs? Regression problem"
	dvc repro import_data

clean_data: import_data data/original_data/insurance.csv
	@echo "Cleaning data"
	@echo "This is step 4: clean data"
	@echo "The data folder has a cleaned dataset in data/transform"
	dvc repro clean_data

eda:
	@echo "Performing EDA"
	@echo "This is step 5: EDA"
	@echo "The output folder has an EDA report in output/eda"
	dvc repro eda
	
split_data: 
	@echo "Splitting data"
	@echo "This is step 6: split data"
	@echo "The output folder has a split dataset in data/transform/validation"
	@echo "For train test split"
	dvc repro split_data
evaluate_model: 
	@echo "Evaluating model"
	@echo "This is step 7: evaluate model"
	@echo "The output folder has a model evaluation in output/model_evaluation"
	dvc repro evaluate_model

compare_metrics:
	@echo "Comparing metrics"
	@echo "This is step 8: compare metrics"
	@echo "The output folder has a model evaluation in output/model_evaluation"
	dvc metrics diff

hyperparam_diff:
	@echo "Comparing hyperparameters"
	@echo "This is step 9: compare hyperparameters"
	@echo "The output folder has a model evaluation in output/model_evaluation"
	dvc params diff


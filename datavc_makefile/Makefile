# ====================
# Environment Settings
# ====================
SHELL := /bin/bash
.DEFAULT_GOAL := all

# Python settings
PYTHON := .venv/bin/python3
PIP := .venv/bin/pip3
ORIGINAL_PY_VERSION := $(shell python3 --version)

# Docker settings 
DOCKER_CONTAINER_NAME := ml_regression_workflow:v0.0.0
CONTAINER_INSTANCE_NAME=ml_regression_workflow
#ENV_VARS := -e KAGGLE_USERNAME=$(KAGGLE_USERNAME) -e KAGGLE_KEY=$(KAGGLE_KEY)

# Directory paths
DATA_DIR := data/
OUTPUT_DIR := output/
MODEL_OUTPUT_DIR := model_output/

# Declare phony targets
.PHONY: all clean help install format lint create_dirs \
        import_data clean_data eda split_data evaluate_model \
        docker_build docker_run docker_clean

# ====================
# Virtual Environment
# ====================
venv/bin/activate: requirements.txt
	# create virtual environment
	python3 -m venv .venv
	# make command executable
	chmod +x .venv/bin/activate
	# activate virtual environment
	. .venv/bin/activate

install: requirements.txt # prerequisite
	# install commands
	# This is step 1: install the virtual environment
	# Py version using py 3.10 from envname
	@echo "Python version: $(ORIGINAL_PY_VERSION)"
	@echo "Installing virtual environment"
	@echo "This is step 1: install the virtual environment"
	pip --no-cache-dir install --upgrade pip &&\
		pip --no-cache-dir install -r requirements.txt


# ====================
# Docker Commands  
# ====================
docker_build: requirements.txt Dockerfile
	@echo "Building docker image"
	sudo docker build --platform linux/amd64 -t $(DOCKER_CONTAINER_NAME) .

docker_run: docker_build
	@echo "Running docker container"
	sudo docker run --platform linux/amd64 \
		-e USERNAME=$(USERNAME) \
		-e PHONE_NUMBER=$(PHONE_NUMBER) \
		-e AT_API_KEY=$(AT_API_KEY) \
		-it --rm \
		--name $(CONTAINER_INSTANCE_NAME) \
		$(DOCKER_CONTAINER_NAME)

docker_clean:
	@echo "Cleaning up docker"
    docker rmi $(DOCKER_CONTAINER_NAME)

# ====================
# Development Tools
# ====================
format: 
	# format code
	black *.py

lint: install format
	# flake8 or #pylint
	pylint --disable=R,C --errors-only *.py utils/*.py testing/*.py

docstring: 
	# format docstring
	pyment -w -o numpydoc *.py

# ====================
# Data Pipeline
# ====================
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
	# chmod +x import_data.sh
	# run script
	./import_data.sh

clean_data: import_data data/original_data/insurance.csv
	@echo "Cleaning data"
	@echo "This is step 4: clean data"
	@echo "The data folder has a cleaned dataset in data/transform"
	python cleandata.py load_data --file_path data/original_data/insurance.csv
	python cleandata.py summary --file_path data/original_data/insurance.csv
	python cleandata.py check_missing --file_path data/original_data/insurance.csv
	python cleandata.py check_duplicate --file_path data/original_data/insurance.csv
	python cleandata.py encode_data --file_path data/original_data/insurance.csv --version 000
	@echo "Data cleaned"

eda: clean_data
	@echo "Performing EDA"
	@echo "This is step 5: EDA"
	@echo "The output folder has an EDA report in output/eda"
	python eda.py --input data/transform/insurance_000.parquet --output output/eda_combined_plots.png

split_data: eda
	@echo "Splitting data"
	@echo "This is step 6: split data"
	@echo "The output folder has a split dataset in data/transform/validation"
	@echo "For train test split"
	python split_data.py --data data/transform/insurance_000.parquet --strategy train_test_split --test_size 0.2
	@echo "For kfold split"
	python split_data.py --data data/transform/insurance_000.parquet --strategy kfold --test_size 0.2 --n_splits 5

evaluate_model: split_data
	@echo "Evaluating model"
	@echo "This is step 7: evaluate model"
	@echo "The output folder has a model evaluation in output/model_evaluation"
	python evaluate.py --criterion squared_error --min_samples_leaf 10 --max_leaf_nodes 5 --degree 3

completed_process:
	@echo "Notification of the completed_process"
	@echo "This is the final step: completed_process"
	python send_sms.py $(USERNAME) $(PHONE_NUMBER) "Model evaluation is complete."

# ====================
# Main Targets
# ====================
all: create_dirs install import_data clean_data eda split_data evaluate_model completed_process

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

help:
	@echo "Makefile for the data version control project"
	@echo "Usage:"
	@echo "make install"
	@echo "       install the virtual environment"
	@echo "make format"
	@echo "       format the code"
	@echo "make lint"
	@echo "       lint the code"
	@echo "make docstring"
	@echo "       format the docstring"
	@echo "make create_dirs"
	@echo "       create directories"
	@echo "make import_data"
	@echo "       import data from Kaggle"
	@echo "make clean_data"
	@echo "       clean data"
	@echo "make eda"
	@echo "       perform EDA"
	@echo "make split_data"
	@echo "       split data"
	@echo "make evaluate_model"
	@echo "       evaluate model"
	@echo "make all"
	@echo "       run all steps"
	@echo "make clean"
	@echo "       clean up"
	@echo "make help"
	@echo "       show help"
	@echo "make docker_build"
	@echo "       build docker image"
	@echo "make docker_run"
	@echo "       run docker container"
	@echo "make docker_clean"
	@echo "       clean up docker"
	@echo "make completed_process"
	@echo "       send a notification of the completed process"
	# ====================
	# Makefile for the data version control project
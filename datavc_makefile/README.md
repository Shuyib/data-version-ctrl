# datavc_makefile
This folder uses a Makefile only to help to help manage machine learning workflows.

> For more information check out more prose here <https://github.com/Shuyib/data-version-ctrl/blob/main/datavc_full/README.md>



## Folder structure    

Rather similar to the previous project.     

.    
├── Dockerfile            # Helps create the workflow with Docker (needs fixing)    
├── Makefile              # Commands to manage the project lifecycle     
├── README.md             # This file, providing an overview of the project    
├── activate_venv.sh      # Script to activate the virtual environment (optional)    
├── cleandata.py          # Script to load, clean, and preprocess the data    
├── eda.py                # Script for exploratory data analysis    
├── evaluate.py           # Script to evaluate machine learning models    
├── import_data.sh        # Script to import data from Kaggle   
├── send_sms.py           # Script to send a text message with Africa's Talking API        
├── params.yaml           # File to store and manage hyperparameters    
├── requirements.txt      # Python package requirements    
└── split_data.py         # Script to split data into training and testing sets    

## Setup

> You need a kaggle account to use the kaggle API. Please handle the resultant `kaggle.json` with care. Don't add it to the repository. You can enforce that by adding it .gitingore file and .dockerignore file.    

To set up the project, follow these steps:

Ensure you have a virtual environment running. You can create and activate a new virtual environment using the following commands:

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```
Install the required Python packages by running:    

```bash
make install
```

This command will install all the dependencies listed in requirements.txt in your virtual environment.

> Note: The project was originally developed using Python 3.12.

## Running the Project

After setting up the virtual environment and installing the dependencies, you can run the project using the following commands:

```bash
make all
```
Or step by step

```bash
make create_dirs 
make install 
make activate_venv 
make import_data 
make clean_data 
make eda 
make split_data 
make evaluate_model
```

## Things you can try   

* Add logging instead of using print statements.    
* Try fixing the Dockerfile   
* Do you think there's a missing step? Add it?

### DataKind Dublin 

## Volunteer Ireland 2015

# Volunteer Information Project


---


## Development:

### Git clone the repo to your workspace.

e.g. in Mac OSX terminal:

        workspace$ git clone [GITHUB_PATH]
        workspace$ cd vi2015


   
### Setup a virtual environment for Python libraries
    
Using Anaconda distro, 

1. create a new virtual environment, installing packages from requirements file
    

        conda create -n vi2015 --file requirements_conda
        source activate vi2015



2. OPTIONAL install packages only available on binstar 
    

        (manual commands are shown in file requirements_binstar)



3. OPTIONAL install remaining packages pip:


        pip install -r requirements_pip
    


### Install local data (not stored in the repo)

Data is currently held separately, ask DataKind Dublin leaders where
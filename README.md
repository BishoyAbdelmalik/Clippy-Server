# Clippy

The server (desktop application) for clippy the clipboard and remote control application.

## Setup ##

### Method 1 (python enviroment) ###



Run the command below to create the python enviroment.

```shell 
python3 -m venv enviroment
```
#### Activate the python enviroment ####

For powershell users:

To activate the enviroment run:

```pwsh
.\enviroment\Scripts\Activate.ps1
```


For CMD users:

To activate the enviroment run:

```
enviroment\Scripts\activate.bat
```

Note: you should see the enviroment name in your shell prompt when activated
#### Install the project's dependencies ####

After activating the python enviroment run: 

```shell
python -m pip install -r requirements.txt
```
Now its all set you can [run the program](#run-the-application).


To deactive the enviroment just type:
```
deactivate
```


### Method 2 (run directly) ###

Make sure python3 and pip installed.

Run the command below to install dependencies
```shell
python3 -m pip install -r requirements.txt
```
Now you can [run the program](#method-2-run-directly-1).


## Run the application ##

### Method 1 (python enviroment) ###
Activate the python enviroment then run.
```shell 
python server.py
```


### Method 2 (run directly) ###
Run the command below.
```shell 
python3 server.py
```


## Documentation ##

### Build ###
Make sure you have all the `requirements.txt` dependencies up to date
(especially `sphinx` and `recommonmark`).

#### HTML ####
Run
```bash
make html
```
and the HTML documentation will be generated in `_build/`

#### LaTeX ####
TODO...



# Mums and Dads Portal (MaD)

## Contributing to the project

To start contributing you first need to fork this repository. It is not possible to clone and commit changes to the main
repository. If you dont feel confident with using git then 
[find out more here.](https://gist.github.com/Chaser324/ce0505fbed06b947d962#file-github-forking-md)

## Setting up virtual environment (Recommended)

Virtual environment is where all libraries used in this project will be installed. It is not required to use one but its
generally good practice to use one to avoid issues when different projects use different library versions. 
[Find out more here.](https://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/)

### PyCharm

If you are using PyCharm there is no need to do this manually. 
[Find out more here.](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html)

### Command Line

```
pip install virtualenv
virtualenv .env
source .env/Scripts/activate
```

## Installing dependencies

```
pip install -r requirements.txt
```

## Running the server

```
./manage.py runserver 8000
```

## Project Specification

### Goals

- Automatic assignment of children and parents
- Remove bias when assigning
- Children should be assigned ASAP after registration so that they can ask their parents for advice

### Features:

- Distinct pages for child and parent signup
- Parents can select a partner
  - The second person receives an email invitation to confirm and fill in details
- Both people have to fill in basic information
- Should parents be forced to log in using college details?
  - If not then should it be possible to change information after submission? 
    - Generate some access link with unique id to access profile
- Assign all unregistered children after deadline
- Email notifications after child/parent assignment

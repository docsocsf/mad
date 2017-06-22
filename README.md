# Mums and Dads Portal (MaD)

## Contributing to the project

To start contributing you first need to fork this repository. It is not possible to clone and commit changes to the main
repository. If you dont feel confident with using git then 
[find out more here.](https://gist.github.com/Chaser324/ce0505fbed06b947d962#file-github-forking-md)

If you don't know what to start working on then have a look at the [Issues](https://github.com/docsocsf/mad/issues) tab 
in the repository and have a got at solving one of the tasks. If you have any questions feel free to contact any of the 
[frequent contributors](https://github.com/docsocsf/mad/graphs/contributors) or ask in our slack, we are here to help 
you get started.

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


## Creating required database

Execute this operation every time you pull updates from the repository. This command updates your database to reflect
the changes made.

```
python manage.py migrate
```

## Setting up local config

Secret and local information should not be uploaded to git that is why you should NEVER commit config.py. Instead make a
copy of sampleconfig.py and save it as config.py. Make changes if need be.

## Running the server

```
./manage.py runserver 8000
```

## Testing

Before submitting a pull request run all tests to make sure you have not broken any functionality. To run tests use
the following command.

```
./test.sh
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

### Project Overview
You will develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

### Getting ready

#### Prerequisites
  * [Python3](https://www.python.org/)
  * [Vagrant](https://www.vagrantup.com/)
  * [VirtualBox](https://www.virtualbox.org/)

#### Setup Project
  1. Install Vagrant and VirtualBox
  2. Download or clone the [fullstack-nanodegree-vm](https://github.com/sh4rkfx/udacity-fsnd/tree/master/3/vm) repository.
  3. Move the project folder's contents inside of the `vm/vagrant` directory.

#### Launching the Virtual Machine
  1. Open up a command line/secure shell/terminal

  2. Navigate into the VM's vagrant folder:

  ```
    $ cd path/to/../vm/vagrant
  ```
  3. Launch the Virtual Machine:

  ```
    $ vagrant up
  ```
  4. Then login using a secure shell:

  ```
    $ vagrant ssh
  ```
  5. Navigate to the project folder:
  ```
    $ cd /vagrant/project_2
  ```

#### Installing all requirements
  ```
    $ pip install -r requirements.txt
  ```

#### Setting up the database
  ```
    $ python run.py --setup
  ```

#### Run the application
  1. Run the script
  ```
    $ python run.py
  ```
  2. Open a browser and visit http://localhost:8000

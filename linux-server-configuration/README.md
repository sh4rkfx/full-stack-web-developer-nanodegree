# Linux Server Configuration

## Project Overview

You will take a baseline installation of a Linux server and prepare it to host your web applications. You will secure your server from a number of attack vectors, install and configure a database server, and deploy one of your existing web applications onto it.

## Get your server
URL: http://ec2-35-169-56-175.compute-1.amazonaws.com
IP: 35.169.56.175
Port: 2200

## Connect to your instance
1. Launch an Amazon EC2 instance using an Ubuntu Linux template
2. Move the private key file into the folder ~/.ssh (where ~ is your environment's home directory). So if you downloaded the file to the Downloads folder, just execute the following command in your terminal:
```bash
mv ~/Downloads/server_config.pem ~/.ssh/
```
3. Open your terminal and type in
```bash
chmod 400 ~/.ssh/server_config.pem
```
4. To connect using SSH and your private key:
```bash
ssh -i "~/.ssh/server_config.pem" ubuntu@ec2-35-169-56-175.compute-1.amazonaws.com
```

## Secure your server
### Update all currently installed packages
```bash
apt-get update
apt-get upgrade
reboot
```

### Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123)
```bash
ufw status
ufw default deny incoming
ufw default allow outgoing
ufw allow 2200/tcp
ufw allow http
ufw allow ntp
ufw enable
ufw status
```

### Change the SSH port from 22 to 2200
1. Open the config file
```bash
nano /etc/ssh/sshd_config
```
2. Change line 'Port 22' to 'Port 2200' and save the file
3. Restart SSH
```bash
service ssh restart
```
4. Now to connect, use:
```bash
ssh -i "~/.ssh/server_config.pem" ubuntu@ec2-35-169-56-175.compute-1.amazonaws.com -p 2200
```

## Give grader access
1. Create user „grader“ and set up a password
```bash
adduser grader
```    
2. Give grader the permission to sudo
```bash
adduser grader sudo
```
3. Switch to the newly created user
```bash
sudo su - grader
```
4. Create the .ssh folder and limit access to this directory to grader
```bash
mkdir .ssh && chmod 700 .ssh
```
5. Create the `authorized_keys` file inside of .ssh and limit access to grader
```bash
touch .ssh/authorized_keys && chmod 600 .ssh/authorized_keys
```
6. Create a new key pair in the Amazon EC2 console
```
NETWORK & SECURITY > Key Pairs > Create Key Pair
```
7. Download the key pair (grader.pem)
8. Open another console and move the key pair to your preferred folder (e.g. "~/.ssh/")
```bash
mv ~/Downloads/grader.pem ~/.ssh/
```
9. Limit access to your user account
```bash
chmod 400 ~/.ssh/grader.pem
```
10. Run the ssh-keygen tool
```bash
ssh-keygen -y
```
11. Enter the path of your key pair and the name of your key pair itself
```
~/.ssh/grader.pem
```
12. Copy the returned public key
13. Switch back to the connection to your Amazon EC2 instance and open the authorized_keys file
```bash
nano ~/.ssh/authorized_keys
```
14. Paste your copied public key information and save the file
15. To connect the user "grader" you can now run
```bash
ssh -i "~/.ssh/grader.pem" grader@ec2-35-169-56-175.compute-1.amazonaws.com -p 2200
```

## Prepare to deploy your project
### Configure the local timezone to UTC
1. Run the timezone configuration tool
```bash
dpkg-reconfigure tzdata
```
2. Select
```
None of the above
```
3. Select
```
UTC
```
4. To check the timezone
```bash
date
```

### Reconfigure locales (to get rid of possible Perl warnings)
1. Open the locales file
```bash
nano /etc/default/locale
```
2. Paste the following then save the file:
```
LANGUAGE=en_US.UTF-8
LC_ALL=en_US.UTF-8
LANG=en_US.UTF-8
LC_TYPE=en_US.UTF-8
```
3. Reconfigure the locales
```bash
dpkg-reconfigure locales
```
### Set up application environment
1. Install Python 3 (if not already present)
```bash
apt-get install python3
```
2. Install the Python packet manager
```bash
apt-get install python3-pip
```
3. Update pip to the current version
```bash
pip install --upgrade pip
```

## Deploy the Item Catalog project

### Install git, clone and setup your Catalog App project (from your GitHub repository from earlier in the Nanodegree program) so that it functions correctly when visiting your server’s IP address in a browser. Remember to set this up appropriately so that your .git directory is not publicly accessible via a browser!

1. Get git (if not already installed)
```bash
apt-get install git
```
2. Clone the repository
```bash
git clone https://github.com/sh4rkfx/udacity-fsnd.git
```
3. Create folder www/html (if not already present)
```bash
mkdir /var/www && mkdir /var/www/html
```
4. Move project to the just created folder
```bash
mv udacity-fsnd/5/project /var/www/html/
```
5. Delete everything else from the repository
```bash
rm -rf udacity-fsnd
```

### Install application requirements
```bash
pip3 install -r /var/www/html/project/requirements.txt
```

### Update Google application domain
on: https://console.developers.google.com

to: http://ec2-35-169-56-175.compute-1.amazonaws.com/login/authorized

#### Set up database and get application configured
```bash
python3 /var/www/html/project/run.py --setup
```

### Run the application
```bash
python3 /var/www/html/project/run.py
```

## References
[How To Create a Sudo User on Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-create-a-sudo-user-on-ubuntu-quickstart)

[How do I add new user accounts with SSH access to my Amazon EC2 Linux instance?](https://aws.amazon.com/premiumsupport/knowledge-center/new-user-accounts-linux-instance/)

[How can I close a terminal without killing the command running in it?](https://unix.stackexchange.com/a/4006)

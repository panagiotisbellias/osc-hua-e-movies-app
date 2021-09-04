# e-movies-app
E-Movies App, a Django project in the context of HUA DIT course 'Basic DevOps Concepts and Tools'

## Run project locally
### Clone and run project locally
```bash
git clone https://github.com/panagiotisbellias/e-movies-app 
python3 -m venv myvenv
source myvenv/bin/activate
pip install -r requirements.txt
cd movies_app
cp movies_app/.env.example movies_app/.env
```
edit movies_app/.env file to define
```vim
SECRET_KEY='test123'
DATABASE_URL=sqlite:///./db.sqlite3
ALLOWED_HOSTS=localhost
```

If you want to run it with PostgreSQL Database visit the [link](https://www.youtube.com/watch?v=RAFZleZYxsc) and change DATABASE_URL above as:
```bash
DATABASE_URL=postgresql://<DB-USERNAME>:<DB-PASSWORD>@localhost/<DB-NAME>
``` 
after you have created a database using [pgAdmin](https://www.youtube.com/watch?v=1wvDVBjNDys)

### Database migration
```bash
python manage.py makemigrations && python manage.py migrate
```

### Run development server
```bash
python manage.py runserver
```

### Alternatively, run gunicorn application server
```bash
gunicorn --bind 0.0.0.0:8000 movies_app.wsgi:application
```

## Deploy django project to a VM (Virtual Machine)

We are going to need 4 VMs. One for the jenkins server and one for each execution environment (ansible, docker and kubernetes)

* [Create VM in Gcloud](https://cloud.google.com/compute/docs/instances/create-start-instance)
* [Create VM in Azure Portal](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/quick-create-portal)
* [SSH Access to VMs](https://help.skytap.com/connect-to-a-linux-vm-with-ssh.html)
* [SSH Automation](https://linuxize.com/post/using-the-ssh-config-file/)
* [Reserve Static IP in Gcloud](https://cloud.google.com/compute/docs/ip-addresses/reserve-static-external-ip-address)
* [Reserve Static IP in Azure](https://azure.microsoft.com/en-au/resources/videos/azure-friday-how-to-reserve-a-public-ip-range-in-azure-using-public-ip-prefix/)

### CI/CD tool configuration (Jenkins Server)

### Deployment with pure Ansible

In order to be able to use Ansible for automation, there is the [ansible-movie-project](https://github.com/panagiotisbellias/ansible-movie-code.git). There is installation and usage guide.

* [More Details](https://github.com/panagiotisbellias/ansible-movie-code/blob/main/README.md)

### Deployment with Docker and docker-compose using Ansible

### Deployment using Kubernetes and a few things from Ansible

## Creating Domain Names
### DNS Zone

### A and CNAME records

## Installing SSL Certificates
### in pure Ansible environment

### in Docker environment

### in Kubernetes environment

# Extra things for exploration
* [Using Visual Studio Code with WSL](https://code.visualstudio.com/docs/remote/wsl)
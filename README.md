# e-movies-app
E-Movies App, a Django project in the context of HUA DIT course 'Basic DevOps Concepts and Tools'

## Run project locally
### Clone and initialize project
```bash
git clone https://github.com/panagiotisbellias/e-movies-app 
python3 -m venv myvenv
source myvenv/bin/activate
pip install -r requirements.txt
cd movies_app
cp movies_app/.env.example movies_app/.env
```
Edit movies_app/.env file to define
```vim
SECRET_KEY='test123'
DATABASE_URL=sqlite:///./db.sqlite3
ALLOWED_HOSTS=localhost
```

If you want to run it with PostgreSQL Database visit the [link](https://www.youtube.com/watch?v=RAFZleZYxsc) and change DATABASE_URL above as:
```vim
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

* [Install Jenkins](https://www.jenkins.io/doc/book/installing/linux/)

Make sure service is running
```bash
sudo systemctl status jenkins
netstat -anlp | grep 8080 # needs package net-tools
```

#### Step 1: Configure Shell
Go to Dashboard / Manage Jenkins / Configure System / Shell / Shell Executable and type '/bin/bash'

#### Step 2: Add webhooks both to django and ansible repositories
[Dublicate](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/creating-a-repository-on-github/duplicating-a-repository) repositories for easier configuration.

* [Add Webhooks - see until Step 4](https://www.blazemeter.com/blog/how-to-integrate-your-github-repository-to-your-jenkins-project)

#### Step 3: Add the credentials needed

* [Add SSH keys & SSH Agent plugin](https://plugins.jenkins.io/ssh-agent/) with id 'ssh-ansible-vm' to access ansible-vm, and 'ssh-docker-vm' to access docker-vm
* [Add Secret Texts](https://www.jenkins.io/doc/book/using/using-credentials/) for every environmental variable we need to define in our projects during deployment, like below

```vim
# ID                What is the value?
psql-user           a username you choose for the db user
psql-pass           a password you choose for the db user
psql-db             a name you choose for your database - must be aligned with the db-urls below
django-key          the django secret key - can be a random string
ansible-db-url      'postgresql://<db-user-name>:<db-user-password>@localhost/<db-name>'
ansible-hosts       the domain name for your ansible vm
docker-db-url       'postgresql://<db-user-name>:<db-user-password>@db/<db-name>'
docker-hosts        the domain name for your docker vm
docker-image        the docker image as it is named in Dockerhub (e.g. belpanos/django-movies)
docker-user         your username for Dockerhub
docker-pass         your password for Dockerhub
k8s-db-url          postgresql://<db-user-name>:<db-user-password>@pg-cluster-ip/<db-name> # NO QUOTES TO AVOID PROBLEMS
k8s-hosts           the domain name for your k8s vm
```

#### Create Jobs
* [Create Freestyle project for Ansible code](https://www.guru99.com/create-builds-jenkins-freestyle-project.html)
* [More for Ansible](https://github.com/panagiotisbellias/ansible-movie-code/blob/main/README.md)
* [Create Pipeline project](https://www.jenkins.io/doc/pipeline/tour/hello-world/)
* [Add Webhooks to both jobs - see until Step 9](https://www.blazemeter.com/blog/how-to-integrate-your-github-repository-to-your-jenkins-project)

In the django job the pipeline will be the [Jenkinsfile](Jenkinsfile)

##### Build stage
Takes the code from the git repository
##### Test stage
Activates a virtual environment, installs the requirements, copies the .env.example to use it as .env with some demo values for testing and executes the tests.py file so the application can be tested before goes on production.
NOTE: connect to your jenkins vm and do the below line so the test stage can run
```bash
<username>@<vm-name>:~$ sudo apt-get install libpcap-dev libpq-dev
```
##### Ansible Deployment
Ansible connects to the ansible-vm through ssh agent and the ssh key we define there and runs a playbook for postgres database configuration and django site configuration passing the sensitive parameters from secret texts.

##### Docker Deployment
Ansible connects to the docker-vm through ssh and runs a playbook that it will define the sensitive parameters and will use docker-compose module to do docker-compose up the containers according to [docker-compose.yml](docker-compose.yml)

##### Preparing k8s Deployment
Here, to deploy our app we need a docker image updated. So we build the image according to [nonroot.Dockerfile](nonroot.Dockerfile), we are logging in Dockerhub and push the image there to be public available.

##### Kubernetes Deployment
After we have [configure connection](https://github.com/panagiotisbellias/e-movies-app#connect-kubernetes-cluster-with-local-pc-orand-jenkins-server) between jenkins user and our k8s cluster, we update secrets and configmaps using also some Ansible to populate ~/.env values and create all the needed entities such as persistent volume claims, deployments, cluster IPs, ingress, services.

Secrets and ConfigMaps could be just prepared from earlier. This is applied to the https ingress, we will see later in [SSL configuration](https://github.com/panagiotisbellias/e-movies-app#in-kubernetes-environment)

### Deployment with pure Ansible
In order to be able to use Ansible for automation, there is the [ansible-movie-project](https://github.com/panagiotisbellias/ansible-movie-code.git). There is installation and usage guide.

* [More Details](https://github.com/panagiotisbellias/ansible-movie-code/blob/main/README.md)

### Deployment with Docker and docker-compose using Ansible
In order to deploy our project in Docker environment, we use again the [ansible-movie-project](https://github.com/panagiotisbellias/ansible-movie-code.git) where we use a playbook that uses an Ansible role to run the application with docker-compose according to the [docker-compose.yml](docker-compose.yml). In that file, we have defined three services, the postgres container with its volume in order to be able to store data, the django container for our app taking environmental variables from local .env file (it's ready when we run the playbook from jenkins-server where the sensitive values from environmental variables are parametric). The django container is built according to the [nonroot.Dockerfile](nonroot.Dockerfile) as a nonroot process for safety reasons. Also, the nginx container is defined to start so as to have a web server in front of django container and to be able to pass SSL certificates for HTTPS environment. For the HTTPS part we will talk about [later](https://github.com/panagiotisbellias/e-movies-app#in-docker-environment).

* [More Info Here](https://github.com/panagiotisbellias/ansible-movie-code/blob/main/README.md)

### Deployment using Kubernetes and a few things from Ansible
In order to deploy our project in Kubernetes cluster, we first need to connect to that VM so as to configure a better connection between local PC or jenkins server and deployment vm's:

* [installing microk8s](https://ubuntu.com/tutorials/install-a-local-kubernetes-with-microk8s#2-deploying-microk8s)
* Do this trick to write less in terminal
```bash
echo "alias k='microk8s.kubectl' " >> ~/.profile
```
The permanent alias will be applied only if you reconnect to your VM.

#### Cluster Configuration & Enable Addons
```bash
sudo usermod -a -G microk8s <your-username>
sudo chown -f -R <your-username> ~/.kube
microk8s enable dns dashboard storage ingress
microk8s status
```

#### Connect Kubernetes Cluster with Local PC or/and Jenkins server
```bash
# VM's terminal
k config view --raw > kube-config
cat kube-config

# Local terminal
mkdir ~/.kube
scp <vm-name>:/home/<vm-username>/kube-config ~/.kube/config
```
Edit ~/.kube/config to replace the 127.0.0.1 with the VM's public ip and the certificate line in clusters section with the below line (not used this way in a real production environment)
```bash
insecure-skip-tls-verify: true
```

* Don't forget to add a firewall rule for the port specified in the ~/.kube/config file
With
```bash
kubectl get pods
```
you can ensure that the connection is established.

If you use CI/CD tool and mostly Jenkins do the following (for better deployment fork the repository to be able to change code where needed):
```bash
# Jenkins terminal
sudo su
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
su jenkins
cd

# Local terminal
scp ~/.kube/config <jenkins-vm-name>:/tmp/config

# Jenkins terminal
mkdir -p .kube
cp /tmp/config ~/.kube/
```
With
```bash
kubectl get pods
```
you can ensure that the connection is established.

#### Kubernetes Entities
Either manually or via jenkins server using Jenkinsfile and secret texts the following will do the trick! The code is located in [k8s](k8s) folder. (The .yaml files)

* Don't forget to have a docker image in DockerHub with the project because the deployment entity for django uses it. You can follow the logic located in Jenkinsfile in the 'Preparing k8s Deployment' stage. You must have docker installed in your local machine (or jenkins server)

* [Docker Image](https://hub.docker.com/repository/docker/belpanos/django-movies)

```bash
# Persistent Volume Claim
kubectl apply -f db/postgres-pvc.yaml

# Secret (for the postgresql database)
kubectl create secret generic pg-user \
--from-literal=PGUSER=<put user name here> \
--from-literal=PGPASSWORD=<put password here>

# Config Map (for .env variables)
vim movies_app/movies_app/.env # change to the correct values
kubectl create configmap django-config --from-env-file=movies_app/movies_app/.env

# Deployments
kubectl apply -f db/postgres-deployment.yaml
kubectl apply -f django/django-deployment.yaml

# Services (Cluster IPs)
kubectl apply -f db/postgres-clip.yaml
kubectl apply -f django/django-clip.yaml

# Ingress (For just HTTP - Edit file changing host to your own dns name)
kubectl apply -f django/django-ingress.yaml

# For possible errors with init-containers & migrations do this
kubectl get pods # to see the full name of django pod (e.g. django-r4nd0m-str1n0)
kubectl exec -it <pod name> bash # to apply migrations manually inside pod

# Now inside the container's bash shell
python manage.py makemigrations && python manage.py migrate ## to migrate database
python manage.py createsuperuser # and answer the prompts in case you want to have an admin present
exit # or press ctrl-D to exit container's bash
```

## Creating Domain Names
* [Go here](https://www.cloudns.net/) to make a free account.

### DNS Zone
* [Go here](https://www.cloudns.net/wiki/article/29/) to make a DNS zone with a general name and a fixed ending. Each VM later will have one more word in front of the DNS zone as you will see.

### A and CNAME records
* [Make A records](https://www.cloudns.net/wiki/article/10/) for your VMs.

* [Make CNAME records](https://www.cloudns.net/wiki/article/13/) when you will need to verify your domain names at the SSL installation.

## Installing SSL Certificates

* [Take SSL certificates from here](https://zerossl.com/) for each VM you have, making an account or more when free certificates are over. (Usually 3 certificates per account)

Make Account / New Certificate / Enter your domain name (A record) / 90-Day Certificate / Verify Domain / DNS (CNAME)

Now, follow the steps and add the CNAME record the instructions tell you. When done press 'verify domain'.

Choose Server Format: NGINX / Install Certificate / Download .zip file

[General Installation Instructions](https://help.zerossl.com/hc/en-us/articles/360058295894-Installing-SSL-Certificate-on-NGINX) which are described better below for each execution environment.

### in Jenkins VM

Let's assume that we have done the wanted concatenation and now we have the certificate.crt and the private.key files. These files should be moved in the cloned [ansible-movie-code](https://github.com/panagiotisbellias/ansible-movie-code.git) project under the path 'files/certs/jenkins' inside that folder. In case you have repo duplicated and push code the .gitignore protects these files from become visible.

So now we run from our local PC (where we have already set ssh connection between Ansible and Jenkins) the related playbook.
```bash
ansible-playbook -l <group-name with jenkins-vm> playbooks/jenkins-config.yml
```

### in pure Ansible environment

Now we want the certificate files for ansible-vm to be located under 'files/certs/django' inside that folder.
So we can run the related playbook.
```bash
ansible-playbook -l <group-name with ansible-vm> playbooks/ansible-https.yml
```

### in Docker environment

Here we need to do the work manually. So,

#### Step 1: Connect to VM and install docker

* Connect to docker-vm via SSH.
* Install Docker and docker-compose if they aren't already installed.

#### Step 2: Configure Django project and it's files

* Clone the django project and go inside the root folder.
* Edit the docker-compose.yml and uncomment commented lines.
* Copy the .env.example to .env
* Make directory 'certs' under 'assets/nginx' both locally and in VM.
* Edit 'assets/nginx/nginx.http.config' & uncomment 1st, 3rd and 4th commented line.

### Step 3: Pass certificates in project's folder

* Save locally the certificate in the 'assets/nginx/certs' folder and do the concatenation if it hasn't been done already.
* Copy them in the VM going in 'assets/nginx/certs' folder and using scp like below:
```bash
scp certificate.crt docker-vm:/home/<username>/e-movies-app/assets/nginx/certs/server.crt
scp private.key docker-vm:/home/azureuser/e-movies-app/assets/nginx/certs/server.key
```

### Step 4: Run docker-compose

* Run
```bash
docker-compose up --build
docker-compose down
```
to apply the changes. Before scaling down the containers go and check what you have done in **https://DNS-A-RECORD-FOR-DOCKER-VM/**

### in Kubernetes environment

After you have certificates for k8s-vm too (you can use same local folder as before if docker https configuration was successful) make sure you have access to your kubernetes cluster.

NOTE: No concatenation needed here. We want the 3 files that [ZeroSSL](https://zerossl.com/) gave us.

Make a secret and apply the https ingress controller we have in .yaml file in [k8s folder](k8s) (Edit [file](k8s/django/django-https-ingress.yaml) changing host to your own dns name):
```bash
kubectl create secret generic tls-secret \
--from-file=tls.crt=certificate.crt \
--from-file=tls.key=private.key \
--from-file=ca.crt=ca_bundle.crt

cd k8s
kubectl apply -f django/django-https-ingress.yaml
```

Go and check what you have done in **https://DNS-A-RECORD-FOR-K8S-VM/**

# Extra things for exploration
* [Using Visual Studio Code with WSL](https://code.visualstudio.com/docs/remote/wsl)
* [Install Docker](https://dev.to/semirteskeredzic/docker-docker-compose-on-ubuntu-20-04-server-4h3k)
* [k9s tool - handle kubernetes clusters](https://github.com/derailed/k9s)
* [Static files in Kubernetes - whitenoise](http://whitenoise.evans.io/en/stable/)
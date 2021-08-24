pipeline {
    agent any

    environment { 
        //PSQL_USER = credentials('PSQL_USER')
        PSQL_PASSWD = credentials('PSQL_PASSWD')
        PSQL_DATABASE = credentials('PSQL_DATABASE')
        SECRET_KEY = credentials('SECRET_KEY')
        ANS_DB_URL = credentials('ANS_DATABASE_URL')
        ANS_HOSTS = credentials('ANS_ALLOWED_HOSTS')
        DOCK_DB_URL = credentials('DOCK_DATABASE_URL')
        DOCK_HOSTS = credentials('DOCK_ALLOWED_HOSTS')
        K8S_DATABASE_URL = credentials('K8S_DATABASE_URL')
        K8S_HOSTS = credentials('K8S_ALLOWED_HOSTS')
        EMAIL_USER = credentials('EMAIL_USER')
        EMAIL_PASSWD = credentials('EMAIL_PASSWD')
    }

    stages {
        stage('Build') {
            steps {
                // Get some code from a GitHub repository
                git branch: 'main', url: 'https://github.com/panagiotisbellias/e-movies-app.git'
            }
        }
        
        stage('Test') {
            steps {
                sh '''
                    python3 -m venv myvenv
                    source myvenv/bin/activate
                    pip install -r requirements.txt

                    cd movies_app
                    cp movies_app/.env.example movies_app/.env
                    ./manage.py test
                '''
            }
        }

        stage('Ansible Deployment') {
            steps {
                sshagent (credentials: ['ssh-azure']) {

                sh '''
                    cd ~/workspace/ansible-movie-code
                    ansible-playbook -l gcloud_ansible playbooks/postgres-install.yml \
                    -e PSQL_USER=$PSQL_USER \
                    -e PSQL_PASSWD=$PSQL_PASSWD \
                    -e PSQL_DB=$PSQL_DATABASE

                    ansible-playbook -l gcloud_ansible playbooks/django-install.yml\
                    -e SECRET_KEY=$SECRET_KEY \
                    -e DATABASE_URL=$ANS_DB_URL \
                    -e ALLOWED_HOSTS=$ANS_HOSTS \
                    -e EMAIL_USER=$EMAIL_USER \
                    -e EMAIL_PASSWD=$EMAIL_PASSWD \
                    -e DEBUG=$DEBUG
                    '''
                }
            }
        }

        stage('Docker Deployment') {
            steps {
                sshagent (credentials: ['ssh-azure']) {
                    sh '''
                        cd ~/workspace/ansible-movie-code
                        ansible-playbook -l azure_docker playbooks/django-docker.yml \
                        -e SECRET_KEY=$SECRET_KEY \
                        -e DATABASE_URL=$DOCK_DB_URL \
                        -e ALLOWED_HOSTS=$DOCK_HOSTS \
                        -e EMAIL_USER=$EMAIL_USER \
                        -e EMAIL_PASSWD=$EMAIL_PASSWD \
                        -e DEBUG=$DEBUG
                    '''
                }
            }
        }

        stage('Preparing k8s Deployment') {
            environment {
                IMAGE='belpanos/django-movies'
                DOCKER_USERNAME='belpanos'
                DOCKER_PASSWORD=credentials('docker-passwd')
            }
            
            steps {
                sh '''
                    echo $BUILD_ID
                    COMMIT_ID=$(git rev-parse --short HEAD)
                    echo $COMMIT_ID
                    TAG=$COMMIT_ID-$BUILD_ID
                    docker build -t $IMAGE -t $IMAGE:$TAG -f nonroot.Dockerfile .
                    docker login -u="$DOCKER_USERNAME" -p="$DOCKER_PASSWORD"
                    docker push $IMAGE --all-tags
                '''
            }
        }

        stage('Kubernetes Deployment') {
            steps {
                sh '''
                    kubectl config use-context microk8s

                    kubectl delete secret/pg-user
                    kubectl create secret generic pg-user \
                    --from-literal=PGUSERNAME=$PSQL_USER
                    --from-literal=PGPASSWORD=$PSQL_PASSWD
                    --from-literal=PGDATABASE=$PSQL_DATABASE
                    
                    cd ~/workspace/ansible-movie-code
                    ansible-playbook playbooks/django-populate-env.yml \
                    -e SECRET_KEY=$SECRET_KEY \
                    -e DATABASE_URL=$K8S_DATABASE_URL \
                    -e ALLOWED_HOSTS=$K8S_HOSTS \
                    -e EMAIL_USER=$EMAIL_USER \
                    -e EMAIL_PASSWD=$EMAIL_PASSWD \
                    -e DEBUG=$DEBUG
                    kubectl delete configMaps/django-config
                    kubectl create configmap django-config --from-env-file=movies_app/movies_app/.env
                    
                    cd k8s
                    kubectl apply -f db/postgres-pvc.yaml
                    kubectl apply -f db/postgres-deployment.yaml
                    kubectl apply -f db/postgres-clip.yaml
                    kubectl apply -f django/django-deployment.yaml
                    kubectl apply -f django/django-clip.yaml
                    kubectl apply -f django/django-ingress.yaml
                '''
            }
        }

    }
}
pipeline {
    agent any

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
                    ansible-playbook -l test playbooks/postgres-install.yml
                    ansible-playbook -l test playbooks/django-install.yml
                    '''
                }
            }
        }

        stage('Docker Deployment') {
            steps {
                sshagent (credentials: ['ssh-azure']) {
                    sh '''
                        cd ~/workspace/ansible-movie-code
                        ansible-playbook -l test playbooks/django-docker.yml
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
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

        stage('Docker Image Getting Ready') {
            steps {
                sh '''
                    docker build -t belpanos/django-movies -f nonroot.Dockerfile .
                '''
            }
        }

        stage('Kubernetes Deployment') {
            steps {
                sh '''
                    kubectl get pods
                '''
            }
        }

    }
}
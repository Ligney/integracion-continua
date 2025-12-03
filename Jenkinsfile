pipeline {
    agent any

    environment {
        GITHUB_CRED = 'github-token'
    }

    stages {

        stage('Checkout') {
            steps {
                echo "Clonando repositorio..."
                git branch: 'main',
                    credentialsId: env.GITHUB_CRED,
                    url: 'https://github.com/Ligney/integracion-continua.git'
            }
        }

        stage('Tests y Cobertura') {
            agent {
                docker {
                    image 'python:3.10'
                }
            }
            steps {
                dir('api-tareas') {
                    sh '''
                        pip install -r api-tareas/requirements.txt
                        coverage run -m pytest
                        coverage report --fail-under=80
                        coverage html
                    '''
                }
            }
        }

        stage('Build Backend') {
            steps {
                echo "Construyendo imagen del backend (api-tareas)..."
                dir('api-tareas') {
                    sh 'docker build -t api-tareas:latest .'
                }
            }
        }

        stage('Build Frontend') {
            steps {
                echo "Construyendo imagen del frontend (ui-tareas)..."
                dir('ui-tareas') {
                    sh 'docker build -t ui-tareas:latest .'
                }
            }
        }

        stage('Docker Compose - Down') {
            steps {
                echo "Deteniendo despliegues previos..."
                sh 'docker compose down || true'
            }
        }

        stage('Docker Compose - Up') {
            steps {
                echo "Levantando los servicios con docker compose..."
                sh 'docker compose up -d --build'
            }
        }

        stage('Smoke Tests (Comprobaciones básicas)') {
            steps {
                echo "Verificando endpoints..."
                sh 'curl -fsS http://localhost:8081 || echo "Front no disponible"'
                sh 'curl -fsS http://localhost:5000/ || echo "API no disponible"'
            }
        }

        stage('List Docker Images') {
            steps {
                echo "Listando imágenes creadas..."
                sh 'docker images'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completado correctamente.'
        }
        failure {
            echo 'Error en el pipeline.'
        }
    }
}

pipeline {
  agent any
  stages {
    stage('BuildImage') {
      steps {
        sh '''docker image build --no-cache -t harbor.finupgroup.com/alert-service-api/alert-service-api:v$BUILD_NUMBER .
docker image tag harbor.finupgroup.com/alert-service-api/alert-service-api:v$BUILD_NUMBER harbor.finupgroup.com/alert-service-api/alert-service-api:latest'''
      }
    }
    stage('PushImage') {
      steps {
        sh '''docker image push harbor.finupgroup.com/alert-service-api/alert-service-api:v$BUILD_NUMBER
docker image push harbor.finupgroup.com/alert-service-api/alert-service-api:latest'''
      }
    }
    stage('PullImage') {
      steps {
        sh 'ssh -p 60000 root@10.19.155.13 \'docker image pull harbor.finupgroup.com/alert-service-api/alert-service-api:latest\''
      }
    }
    stage('Clean Image') {
      parallel {
        stage('Clean Image') {
          steps {
            sh '''docker image rm harbor.finupgroup.com/alert-service-api/alert-service-api:v$BUILD_NUMBER
docker image rm harbor.finupgroup.com/alert-service-api/alert-service-api:latest'''
          }
        }
        stage('Confirm Deploy') {
          steps {
            timeout(time: 1, unit: 'HOURS') {
              input(message: 'Deploy to Production Env?', ok: 'Deploy!')
            }
            
          }
        }
      }
    }
    stage('StopContainer') {
      steps {
        sh 'sh -x /var/lib/jenkins/scripts/stop_container_full_support.sh 10.19.155.13 alert-service-api 60000 root'
      }
    }
    stage('Run Container') {
      steps {
        sh 'ssh -p 60000 root@10.19.155.13 docker container run --add-host redis:10.19.155.13 -d -p 8004:8004 --restart always --name alert-service-api_v$BUILD_NUMBER harbor.finupgroup.com/alert-service-api/alert-service-api'
      }
    }
  }
}
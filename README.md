#Development
============

04.06.2023
syncing repositories

# Flask_app
project- build an web app based on flask and python
- app.py uses postgres
- app-no-db.py doesn't use postgres
 
 -Dockerfile is for testing and Deployment is for pruductions stage
 
# Jenkins
- use Jenkinsfile-Docker to see automation with docker
- use Jenkinsfile.k8s to deploy your project on rancher cluster (or any k8 cluster)
- Jenkinsfile deploy the app on amazon (uses anssible and sh scripts)
- Set up shared library if you want to use custom command like colored logs (Library(Logs-OPT))

# Slack
- to setup notification to slack from jenkins you need to download the slack notifications plugin and set it up in system
  you need to use the token of the slack app (either custom or Jenkis CI)
  use slackSend commands or just turn on in your job slack notifications
- to use slash commands in slack or any special features you need to make an app in slack api.
    download ngrok on your machine hosting jenkins and generic webhood plugin in jenkins
    use command ngrok http 8080 (exposes jenkins to be public)
    check the webhook trigger box in a jenkins job, add post parameter+expression, add token
    use the JENKINS_URL as the ip you get when exposing the 8080 port with ngrok
    define slash commands in jenkins app
- 
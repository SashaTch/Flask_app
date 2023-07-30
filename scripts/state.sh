#!/bin/bash

#arguments
stage=$1 #cicd stage
state=$2 #stop/run
tag=$3   #ec2 tag
value=$4 #ec2 values to said tag
ssh_key=$5 #ssh key path

id=$(aws ec2 describe-instances --filters "Name=tag:$3,Values=$4" --query "Reservations[*].Instances[*].InstanceId" --output text)
ip=$(aws ec2 describe-instances --filters "Name=tag:$3,Values=$4" --query "Reservations[*].Instances[*].PublicIpAddress" --output text)

case "$stage" in
        state)
                #change_ec2_state
                if [ $2 = "stop" ]; then
                        aws ec2 stop-instances --instance-ids $id
                elif [ $2 = "run" ]; then
                        aws ec2 start-instances --instance-ids $id
                else
                        echo "invalid input"
                        exit 1
                fi
                ;;
        deploy)
                #deploy
                scp -i $ssh_key /var/lib/jenkins/workspace/Project/app.tar.gz ec2-user@$ip:~
                ssh -i $ssh_key ec2-user@$ip "tar -xzf app.tar.gz && cd Flask_app && tmux new-session -d -s gunicorn_session 'nohup gunicorn -b 0.0.0.0:5000 flask_app:app'"
                #ssh -i $ssh_key ec2-user@$ip temux attach-session -t gunicorn_session #reatach the gunicorn terminal session to view logs
                ;;
        deploy_docker)
                #deploy using docker
                echo "BUILD_NUMBER is ${BUILD_NUMBER}"
                ssh -i $ssh_key ec2-user@$ip "docker pull sashatchern/flask:v${BUILD_NUMBER}"
                ssh -i $ssh_key ec2-user@$ip "docker run -d -p 5000:5000 sashatchern/flask:v${BUILD_NUMBER} > container_id.txt"
                ;;
        test)
                #tests
                curl $ip:5000
                ssh -i $ssh_key ec2-user@$ip "docker stop \$(cat /home/ec2-user/container_id.txt)"
                ssh -i $ssh_key ec2-user@$ip "sudo rm -f /home/ec2-user/container_id.txt"
                ;;
        *)
                echo "invalid input for stage, please use state/deploy/test."
                exit 1
                ;;
esac


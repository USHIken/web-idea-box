IDEA_DIR=`pwd`
echo "IDEA_PATH=\"${IDEA_DIR}/local.yml\"
alias idea-compose=\"docker-compose -f \$IDEA_PATH\"
alias idea-manage=\"docker-compose -f \$IDEA_PATH run django python manage.py\"
alias idea-bash=\"docker-compose -f \$IDEA_PATH run django /bin/bash\"
alias idea-logs=\"docker-compose -f \$IDEA_PATH logs -f --tail=100\"" >> ~/.bash_profile
source ~/.bash_profile
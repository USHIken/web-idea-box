# 引数チェックとUsageの出力
if [ -n $1 ]; then
    echo ""
    echo "docker-compose -f local.yml 〜を楽にするaliasを作成します。"
    echo ""
    echo "使い方:"
    echo "    aliasのprefixを第1引数に指定します。"
    echo "    $ sh alias.sh project"
    echo ""
    echo "登録されるalias例:"
    echo "    $ project-compose up -d"
    echo "    $ project-logs django"
    echo "    $ project-manage showmigrations"
    echo ""
    exit
fi

ALIAS_PREFIX=$1
IDEA_DIR=`pwd`
echo "IDEA_PATH=\"${IDEA_DIR}/local.yml\"
alias ${ALIAS_PREFIX}-compose=\"docker-compose -f \$IDEA_PATH\"
alias ${ALIAS_PREFIX}-manage=\"docker-compose -f \$IDEA_PATH run django python manage.py\"
alias ${ALIAS_PREFIX}-bash=\"docker-compose -f \$IDEA_PATH run django /bin/bash\"
alias ${ALIAS_PREFIX}-logs=\"docker-compose -f \$IDEA_PATH logs -f --tail=100\"" >> ~/.bash_profile
source ~/.bash_profile
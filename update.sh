#!/usr/bin/env bash

PREFIX=$(cd "$(dirname "$0")"; pwd)
cd $PREFIX

source ~/.bashrc

source $PREFIX/ssl_config/dns.sh

~/.acme.sh/acme.sh --renew -d $HOST --force --log

sync() {
    git add -u && git commit -m 'UPDATE HTTPS CERTIFICATE' ;
    local branch=`git branch 2> /dev/null | sed -e '/^[^*]/d' |awk -F' ' '{print $2}'`
    git pull $1 $branch && git push $1 $branch;
}


$PREFIX/merge.py ~/.acme.sh/ $HOST $PREFIX $DP_Id $DP_Key

sync origin
sync gitee

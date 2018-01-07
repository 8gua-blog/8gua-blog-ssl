#!/usr/bin/env bash

PREFIX=$(cd "$(dirname "$0")"; pwd)
cd $PREFIX

source private/dnspod_config.sh

 ~/.acme.sh/acme.sh --issue --dns dns_dp -d $HOST  -d www.$HOST --force





sync() {
    git add -u && git commit -m 'UPDATE HTTPS CERTIFICATE' ;
    local branch=`git branch 2> /dev/null | sed -e '/^[^*]/d' |awk -F' ' '{print $2}'`
    git pull origin $branch && git push origin $branch;
}


$PREFIX/merge.py ~/.acme.sh/ $HOST $PREFIX

sync

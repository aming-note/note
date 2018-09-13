#!/bin/bash

file=./dns.list
if [ -f ./err.list ];then
	rm -f ./err.list
fi
systemctl restart nscd
function check(){
	http_code=`curl -Is $1 | head -n 1 | awk '{print $2}'`
	if [ -n "$http_code" ];then
		if [ $http_code = 200 ];then
			echo -e "$1	\033[34m$http_code\033[0m"
			echo "-----------------------"
		else
			echo -e "$1	\033[31m$http_code\033[0m"
			echo $i >>./err.list
			echo "-----------------------"
		fi
	else
		echo -e "$1	\033[31mError\033[0m"
		echo $i >>./err.list
		echo "-----------------------"
	fi
}

if [ -f $file ];then
	echo "域名		HTTP响应码"
	for i in `cat $file`;do
		check $i
	done
fi
curl -s myip.ipip.net
if [ -f ./err.list ];then
	echo "==============================="
	echo -e "\033[36m错误域名:\033[0m"
	for s in `cat ./err.list`;do
		echo -e "\033[31m$s\033[0m"
	done
	rm -f ./err.list
fi

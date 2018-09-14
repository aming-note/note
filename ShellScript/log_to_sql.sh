#!/bin/bash

log_file="/usr/local/nginx/logs/bet.log"

err_line=0
function get_new_log(){
	kg=0
	file=`cat $log_file`
	cut=`cat /home/linshi 2>/dev/null`
	for i in $file;do
		if [ -f /home/linshi ];then
			if [ "$cut" = "`tail -n 1 $log_file`" ];then
				break
			fi
			if [ $kg = "1" ];then
				send_mysql $i
				echo $i > /home/linshi
			fi
			if [ "$cut" = "$i" ];then
				kg=1
			fi
		else
			for a in $file;do
				send_mysql $a
				echo $a >/home/linshi
			done
		fi
	done
}

function send_mysql(){
	check=`echo $1 | awk -F ',' '{print $6}' | wc -c`
	if [ $check -ge 2 ];then
		remote_addr=`echo $1 | awk -F ',' '{print $1}'`
		time_local=`echo $1 | awk -F ',' '{print $2}'`
		request_time=`echo $1 | awk -F ',' '{print $3}'`
		http_referer=`echo $1 | awk -F ',' '{print $4}'`
		http_cookie=`echo $1 | awk -F ',' '{print $5}'`
		request_body=`echo $1 | awk -F ',' '{print $6}'`
		mysql -ubet_user -p'123456' -h 192.168.1.84 -e "INSERT INTO test.bet_log(
		remote_addr,time_local,request_time,http_referer,http_cookie,request_body) VALUES(
		$remote_addr,$time_local,$request_time,$http_referer,$http_cookie,$request_body)"
	else
		err_line=`expr $err_line + 1`
	fi
}


get_new_log
if [ $err_line -gt 0 ];then
	now_date=`date '+%Y-%m-%d_%H:%M:%S'`
	mysql -ubet_user -p'123456' -h 192.168.1.84 -e "INSERT INTO test.bet_log(time_local,info) VALUES('$now_date','Log_Code_Error_$err_line')"
fi

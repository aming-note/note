#!/bin/bash
function bak_log() {
	date=`date +%Y-%m-%d_%H:%M`
	pid_file=/usr/local/nginx/logs/nginx.pid
	error_log_name=error_$date.log
	access_log_name=access_$date.log
	mv /usr/local/nginx/logs/error.log /home/log_bak/$error_log_name
	mv /usr/local/nginx/logs/access.log /home/log_bak/$access_log_name
	kill -USR1 `cat $pid_file`
	echo "Backup Secuessfull"
}

function clear_log() {
	log_count=`ls -lh /home/log_bak | grep $1 | wc -l`
	delete_line=`expr $log_count - 15`
	if [ $delete_line -ge 1 ];then
		ls -lh /home/log_bak/ | grep $1 | head -n $delete_line | awk '{print $9}' >>./linshi
		for s in `cat ./linshi`;do
			echo "Delete For $s"
			rm -f /home/log_bak/$s
		done
		rm -f ./linshi
	else
		echo "No Have Many Log Files"
	fi
}
echo "=============================="
bak_log
echo "=============================="
clear_log access
echo "=============================="
clear_log error

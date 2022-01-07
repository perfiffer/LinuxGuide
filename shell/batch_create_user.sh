#!/bin/bash

#method 1
#function echo_color() {
#    if [ $1 == 'green' ];then
#        echo -e "\033[32;40m$2\033[0m"
#    elif [ $1 == 'red' ];then
#        echo -e "\033[31;40m$2\033[0m"
#    fi
#}

#method 2
function echo_color() {
    case $1 in 
        green)
            echo -e "\033[32;40m$2\033[0m"
            ;;
        red)
            echo -e "\033[31;40m$2\033[0m"
            ;;
	*)
	    echo "[Usage]: echo_color [color] [text]"
    esac
}

DATE=$(date +%F_%T)
USER_FILE=user.txt
if [ -s $USER_FILE ];then
   mv $USER_FILE ${USER_FILE}-${DATE}.bak
   echo_color green "$USER_FILE exist,raname ${USER_FILE}-${DATE}.bak"
fi
echo -e "User\tPassword" >> $USER_FILE
echo "-----------------" >> $USER_FILE
for USER in user{1..2};do
   if ! id $USER &> /dev/null; then
      PASS=$(echo $RANDOM | md5sum | cut -c 1-8)
      useradd $USER
      echo $PASS | passwd --stdin $USER &> /dev/null
      echo -e "$USER\t$PASS" >> $USER_FILE
      echo "$USER User create successful."
   else
      echo_color red "$USER User already exists."
   fi
done

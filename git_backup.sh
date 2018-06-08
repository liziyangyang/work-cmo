#!/bin/bash

/opt/gitlab/bin/gitlab-rake gitlab:backup:create

backup_dir=/var/opt/gitlab/backups

new_file=$(ls -t /var/opt/gitlab/backups |head -n1)
echo $new_file

scp -r $backup_dir/$new_file root@172.16.1.32:/vms/git_backup/186

echo 'finish scp $file'

#only keep latest 7 files

max_file_number=7

chmod 700 $backup_dir

file_number=$(ls $backup_dir | wc -l)
echo $file_number

while [ $file_number -gt $max_file_number ];do
    echo 'file_number $file_number'
    file=$(ls $backup_dir -t|tail -n1)
    echo 'start to delete $file'
    rm -rf  $backup_dir/$file
    file_number=$(ls $backup_dir | wc -l)
done

echo 'finish delete'

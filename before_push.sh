#run before push to avoid conflict
#process:
#1: ./before_push.sh
#2: git add .
#3: git commit -m "..."
#4: git push

#hint: maybe you need to run "chmod 777 before_push.sh" before run this shell

#delete all pyc file in this project
find . -name "*.pyc" -type f -print -exec rm -rf {} \;

#Cancels all changes to the database
git checkout -- db.sqlite3
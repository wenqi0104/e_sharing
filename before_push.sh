#run before push to avoid conflict

#delete all pyc file in this project
find . -name "*.pyc" -type f -print -exec rm -rf {} \;

#Cancels all changes to the database
git checkout -- db.sqlite3
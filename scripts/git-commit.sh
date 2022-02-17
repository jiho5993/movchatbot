# ./scripts/git-commit.sh check
# ./scripts/git-commit.sh push "msg"

if [ "$1" = "check" ]
then
    python manage.py check --deploy
    pip3 freeze > requirements.txt
elif [ "$1" = "push" ]
then
    git add .
    git commit -m "$2"
    git push origin main
fi
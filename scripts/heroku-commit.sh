if [ $1 == "config" ]
then
    heroku config:set '"'"$2"'"'
fi

git push heroku main
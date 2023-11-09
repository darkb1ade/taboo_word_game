# taboo_word_game

# Deploy using `heroku`
## Setting
```commandline
heroku create
heroku container:push web --app ${YOUR_APP_NAME}
```
## Release
### 1. From docker image
**docker authentication**
```commandline
heroku auth:token
docker login --username=_ --password=${YOUR_TOKEN} registry.heroku.com
```
or 
```commandline
heroku container:login
```
**push docker image**
```commandline
docker build -t registry.heroku.com/${YOUR_APP_NAME}/web .
docker push registry.heroku.com/${YOUR_APP_NAME}/web
```

### 2. From Dockerfile
```commandline
 heroku container:push web
 heroku container:release web
 heroku open
```
---
## Check dashboard
[here](https://dashboard.heroku.com/apps)
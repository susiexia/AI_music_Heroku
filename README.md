# AI_music_Heroku

Deployed app about Music Classification with CNN models.

Link: <https://ai-music-web.herokuapp.com/>

## Source Code 

All source codes from ETL data pipeline, loading to PostgreSQL to training CNN models are in this github repository:

[AI_Music_Repo](https://github.com/susiexia/AI_Music)

### How to deploy to your own heroku web

1. Clone and move to a folder without git

2. Create a new Heroku app.
Official instruction here: <https://devcenter.heroku.com/articles/getting-started-with-python>

3. Make connection to heroku remote github.

`$ heroku git:remote -a <your new app name>`

4. Add *heroku-buildpack-apt* [Reference](https://elements.heroku.com/buildpacks/heroku/heroku-buildpack-apt)

`$ heroku buildpacks:add --index 2 heroku-community/apt`




5. Add code and push to remote heroku repository


`git add .`
`git commit -m""`
`git push heroku master`

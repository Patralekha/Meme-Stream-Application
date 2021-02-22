xmeme_frontend folder contains files that are responsible for the frontend of the app.The ajax calls in the index.js file include calls to the publicly deployed backend on heroku.Includes html,css and javascript files.The php file was included in order to deploy the frontend to heroku.


xmeme is a django application containing the backend of the meme stream application using django rest framework.
xmeme_backend that contains the model for the meme stream aplication in models.py,the views in views.py and serializer classes in serializers.py to map objects to json and vice versa.The urls.py contain various url endpoints
including swagger endpoint.


Other files include:manage.py to run django development server and bash scripts(install.sh,server_run.sh, sleep.sh and test_server.sh) to automate installation of python3,pip,django,packages specified in requirements.txt,to set up postgres database , run django development server and execute curl commands.
# Meme-Stream-Application

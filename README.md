# TREE INVENTORY SYSTEM (TIS)

>**Used:** \
Python 3.9.10, Django 3.2.7, BeautifulSoap 4.10.0, requests 2.26.0, Bootstrap 5, Django Rest Framework 3.12.4, SQLite3, JQuery 3.6.0, JavaScript


### __Distinctiveness and Complexity:__
__________________________________
The project meets the requirements because it is not similar to other projects in the course, it has an advanced view with form sets and several other forms sent asynchronously (ajax), it contains several models linked by realities and a django command that scrapes tree species from some web page. All views are only accessible to logged in users. The complexity of the project also lies in a dynamically changing table with sets of forms depending on the stage/status of the created inventory.

### __File contents__
__________________________
1. **requirements.txt** - all required packages, for example: djangorestframework, pillow, requests
2. **.flake8** - settings flake8, Flake8 is not required package
3. **README.md** - description project
4. **.gitignore** - file for github, files that are to be ignored by the version control system
5. **project** (directory) - contains settings for the project, defined the URLs, an example *.env* file called *.env.template*
6. **static** (directory) - js and css files and *tree_photos* directory:
    - **app.css** - base style app, simple styling
    - **timeline.css** - style for inventory timeline

    ![timeline photo](https://github.com/me50/andree0/blob/web50/projects/2020/x/capstone/static/screenshots/timeline.png)
    
    - **status.js** - contains ajax requests for update inventory status, add tree photos, add tree comments, loading tree comments, also includes update display and render table with trees or offcanvas items, includes helper functions get cookie and other
    - **style_form.js** - includes basic form styling changes, show and hide password and insert bootstrap icons
    - **style_list.js** - contains style for the nav items and alert messages
    - **update_inventory.js** - sets the basic style for the inventory update form and activates it
    - **tree_photos** (directory) - directory for storing images of trees related to the model in the database
    - **screenshots** (directory) - directory to store the images used in the README.md file for visualization of the description
7. **TIS_app** (directory) - views, forms, models, page templates and everything that makes up this application:
    - **managemant/commands/loadbasicspecies.py** - command scraping basic tree species found in Poland, uses BeautifulSoup and requests libraries
    - **migrations** (directory) - contains migration files for the database
    - **templates** (directory) - contains page templates divided into two directories, for registration and login *(resgistration)*, and the rest *(TIS_app)*
    - **admin.py** - registering models in the django admin panel
    - **context_processors.py** - contains meta data that is available in all views
    - **forms.py** - contains predefined django forms and their configurations
    - **models.py** - contains structure and definitions of models mapped to objects in database
    - **permissions.py** - includes definitions of custom permissions
    - **serializers.py** - data serializers for rest views
    - **validators.py** - conatins password validator
    - **views.py** - contains all views, the first part contains rest views and the second part class generic django views, proper separator comment was used


### __Launching the app__
___________________________

#### __Locally__

1. Run command `cp .env.template .env` in *project* directory
2. Run command `pip install -r requirements.txt` in your enviroment
3. Run command `python manage.py makemigrations`
4. Run command `python manage.py migrate`
5. Run command `python manage.py loadbasicspecies`
6. Go to <http://127.0.0.1:8000/> in your browser

#### __With Docker__


If you do not have docker installed, see how to do it at <https://docs.docker.com/get-docker/> and <https://docs.docker.com/compose/install/>.
1. Run command `docker-compose up`
2. Run command `docker-compose exec web ./manage.py makemigrations`
3. Run command `docker-compose exec web ./manage.py migrate`
4. Run command `docker-compose exec web ./manage.py loadbasicspecies`. \
    If the command was executed correctly, the message `Added basic tree species to db` will appear.
5. Go to <http://0.0.0.0:8000/> in your browser



### TODO:
_______
1. View to edit personal data and settings of app (for example: pagination) or two views, one for edit data and second for settings.
2. Dynamic loading comments to tree, reverse infinity scroll.
3. Button closing inventory.
4. Filters to list of inventories and trees.
5. Re-inventory. Another inventory of the same location. The `Tree.exists` field is displayed in the form. Adding history of inventory in specify location.
6. Dashboard extension (more statistics and data).
7. Take photos of tree directly into the app.
8. Map with inventory locations.
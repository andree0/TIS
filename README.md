# TREE INVENTORY SYSTEM (TIS)

>**Used:** \
Python 3.9.10, Django 3.2.7, BeautifulSoap 4.10.0, requests 2.26.0, Bootstrap 5, Django Rest Framework 3.12.4, SQLite3, JQuery 3.6.0, JavaScript


### __Distinctiveness and Complexity:__
__________________________________
The project meets the requirements because it is not similar to other projects in the course, it has an advanced view with form sets and several other forms sent asynchronously (ajax), it contains several models linked by realities and a django command that scrapes tree species from some web page. All views are only accessible to logged in users. The complexity of the project also lies in a dynamically changing table with sets of forms depending on the stage/status of the created inventory.

This application is aimed at landscape architects and dendrologists, as well as anyone performing green space inventories.
The application contains several basic views: user registration, user login, main view for non-logged in, main view for logged in, inventory creation, list of inventories created by the user, inventory deletion confirmation view, inventory details with a list of trees, view of adding a tree to the inventory and its circumference, gallery with photos of trees.

The most complex view is the inventory details view *(class __UpdateInventoryView__ in views.py)*. It contains many elements that are dynamically changed using JS. When you click on the button to edit the inventory, the code from the *update_inventory.js* file is run. Fields appear filled with the current values, which can be changed and saved by clicking the __*Save*__ button. Saving the inventory is already done on the django view side.
Under the inventory name there is a description and under it a __*timeline*__ indicating the current status of the inventory, on the sides there are buttons to change the status, which is updated via an ajax query. Changing the inventory status changes many things on the page, including the number of columns in the tree table. In the __*status.js*__ file there is a __*updateInventoryStatus*__ function which is responsible for the ajax query that updates the status, its call will also run the __*updateStyleDisplayStatus*__ function which is responsible for the dynamic changes on the page caused by the status change, it is also called when the view is loaded. The camera icon causes a hidden canvas to slide out from the left side with a form for adding photos. The photo icon is a link to the gallery. Clicking on the message icon will bring up a hidden canvas on the left with a form for leaving comments, remarks for that tree. When the inventory status is __*Inventory*__, the tree table on the page shows the information collected when the tree was measured. When the status is changed to __*Valorization*__, several cells in the table are hidden and two columns with one form for each tree (sets of forms) appear. When the status is __*Tree management*__, the cells with forms for valorization are locked and a column with forms for deciding what to do with the tree appears. The __*status.js*__ file is responsible for dynamic table changes. It is also responsible for sending ajax requests for adding photos or comments via hidden canvases, as well as loading those comments.
There is also a button on this view that takes you to the add tree view, which displays the number of all trees added to the inventory.


Ajax requests are sent to Django Rest Framework views defined in the __*views.py*__ file.

The __*style_list.js*__ file is responsible for the delicate border around the tab for the current page (*All Your Inventories*, *Start New Inventory*).

The __*style_form.js*__ file is responsible for setting the base appearance of all forms, the eye icon in forms with a password field, for hiding and showing the password in forms when the eye icon is clicked, for adding and removing the tree circumference field in the add tree form.

I'm most happy that I learned some work with django form sets and sending images with ajax requests. Although I know that my code is far from perfect and doesn't handle too many errors. There is still a lot to do and a lot to improve in this project, that's why I included a [TODO](#todo)
 section.

### __Table of contents__
__________________________
1. **requirements.txt** - all required packages, for example: djangorestframework, pillow, requests
2. **.flake8** - settings flake8, Flake8 is not required package, this is a package for static code analysis
3. **README.md** - description project
4. **.gitignore** - file for github, files that are to be ignored by the version control system
5. **project** (directory) - contains settings for the project (settings.py), defined the URLs (urls.py), an example *.env* file called *.env.template*, *.env.template* contains example SECRET_KEY variable for django project
6. **static** (directory) - js and css files and *tree_photos* directory *(operation of individual files is also described in the text above)*:
    - **app.css** - base style app, simple styling
    - **timeline.css** - style for inventory timeline with inventory status

    ![timeline photo](https://github.com/me50/andree0/blob/web50/projects/2020/x/capstone/static/screenshots/timeline.png)
    
    - **status.js** - contains ajax requests for update inventory status, add tree photos, add tree comments, loading tree comments, also includes update display and render table with trees or offcanvas items, includes helper functions get cookie and other
    - **style_form.js** - includes basic form styling changes, show and hide password and insert bootstrap icons
    - **style_list.js** - contains style for the nav items and alert messages
    - **update_inventory.js** - sets the basic style for the inventory update form and activates it
    - **tree_photos** (directory) - directory for storing images of trees related to the model in the database
    - **screenshots** (directory) - directory to store the images used in the README.md file for visualization of the description
7. **TIS_app** (directory) - views, forms, models, page templates and everything that makes up this application:
    - **managemant/commands/loadbasicspecies.py** - command scraping basic tree species found in Poland, uses BeautifulSoup and requests libraries, this is an helper command to quickly add data to the database
    - **migrations** (directory) - contains migration files for the database
    - **templates** (directory) - contains page templates divided into two directories, for registration and login *(resgistration)*, and the rest *(TIS_app)* which are application view templates, in TIS_app directory there is a *base.html* file from which other templates are inherited, there are also additional templates which are inserted into other ones *(pagination.html, messages.html, login_info.html)*
    - **admin.py** - registering models in the django admin panel
    - **context_processors.py** - contains meta data that is available in all views, my personal data and links to social media
    - **forms.py** - contains predefined django forms and their configurations, forms used in views
    - **models.py** - contains structure and definitions of models mapped to objects in database, contains 8 models defined by me which are connected with each other by relations
    - **permissions.py** - includes definitions of custom permissions (class IsOwnerOrReadOnly and IsOwnerInventoryForObj)
    - **serializers.py** - data serializers for rest views
    - **validators.py** - conatins password validator
    - **views.py** - contains all views, the first part contains rest views and the second part class generic django views, proper separator comment was used

8. **Dockerfile** - A file that defines the container, what image it is based on, what port is exposed, a command to install dependencies
9. **docker-compose** -service configuration in a container and the command to start the service


### __Launching the app__
___________________________

#### __Locally__

Run the following commands in the terminal at the level of the directory where the manage.py file is located with the exception of the first command which runs in the *project* directory.

You can use python3 instead of python.

1. Run command `cp .env.template .env`
2. Run command `pip install -r requirements.lock.txt` in your enviroment
3. Run command `python manage.py makemigrations`
4. Run command `python manage.py migrate`
5. Run command `python manage.py loadbasicspecies`
6. Go to <http://127.0.0.1:8000/> in your browser

#### __With Docker__


If you do not have docker installed, see how to do it at <https://docs.docker.com/get-docker/> and <https://docs.docker.com/compose/install/>.

Run the following commands in a terminal at the directory level where the __*docker-compose.yml*__ file is located.
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
9. Generation of documents for public institutions, requests for tree removal or intervention.

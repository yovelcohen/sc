# **Base SCR Django App**

Base Django App to server all SCR Products


-----------

Configurations
-----------

```bash
pip install coockiecutter

cookiecutter <url>
```

This will run the cookie cutter CLI and config your project

In the project directory you'll find a py_charm_settings.py file, if you are using pycharm as your IDE you can import
this settings:

File -> Manage IDE Settings -> Import Settings

This configurations include some small additions, Mainly it reconfigures Pycharm python console to be able to run Django
code, So, Querysets, Models and all you can import from Django.

It also has the base test settings configurations which allows use of the Pycharm Debugger in testing


-----------

Django:
-----------

cd into the created Project.

In there you'll find 3 installed apps:
    
* users:
    - contains the base user model (email based) and it's manager
    - urls.py file already created and a Login Serializer
    
* api:
    - contains Account and GeoLocation models.
    - also contain two sample implementation of the abstract scr models
    - serializers
    - views divided into files, and an implemented version of the graphs/csv exporter view
    - admin configured
    - apps importing the signals file already
    - example test file
  
* account management api:
  - this app is exposed to SalesForce and Zoura, (API Key based auth)
  - Accounts and Other Entities (sites,farms,readers...) are being posted to our app via SF.
  - it also manages the usage reports construction and sending billing to Zoura
  

-----------

Additional:
-----------
_**the common dir**:_
  
contains constant and utilities
  - Constants
  - utilities
  - dates utilities and constant
  - admin utilities
  - docs 
  - abstracted objects:
    - exceptions
    - custom management command
    - managers
    - models (site,scores,groups...)
    - views (just mixins with small scr configurations)
    - test:
      check it out for info, it explains how to debug django code using 
      pycharm's debugger, which is extremely recommended
      

Additional info:

  - comes with django-silk debugger preinstalled and configured.


  - the cookiecutter script also exports environment variables such as Auth Tokens (zoura and data platform), 
    it also sets a silk env var which is used to activate the django-silk debugger 
    on local env.
    

  - creates an Heorku Procfile configured by your chosen cookie cutter configs ("add_the_migrate_command_to_pipeline",
    "async_or_sync_deployment") and runtime.txt file.
    
  
  - creates BitBucket Pipeline.yml file 
  

  - if "add_file_logger" is set to true, the application will create a log file
    
    
  - the data package:
    this package configures a small ETLs pipeline Infrastructure.
    
    It has Base classes for Extractor,Transformer and Loader.
    It provides a Factory module for each part in the pipeline, all the implementation
    classes should be registered there and a Runner class which should support all scenarios.
    
    You can check out the Zoura implementation for example

    It also contains the Resources file which contains all the necessary functions to get auth tokens and URLS
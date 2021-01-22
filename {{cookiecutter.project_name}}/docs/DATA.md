## **The Data Module**

This module contains ETLs pipelines infrastructure.

_****Extractors:****_

extractors are responsible for getting the data from the resource (db, api, file...), and organize it in a way that's
easy to edit and enhance

_****Transformers:****_

transformers are responsible for modifying and manipulating the data to the desired outputs

_****Loaders:****_

loaders are responsible for getting the transformed data, validate it and load it to the end source (DB, Static Files
Storage,further in code ETLs...)

_****Factory:****_

This dir contains the factories for all the ETLs processes. Every factory should register it's implemented classes.

check out the Zoura in the ETLs Flows for more

It also contains the Resources file, this file contains all the URLs of third parties and reads the token from env vars
automatically.

And Lastly, deployment to cloud helpers, currently only for GCP
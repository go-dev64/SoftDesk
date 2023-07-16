# OCR PROJET 10
Créez une API sécurisée RESTful en utilisant Django REST.

## Scénario
SoftDesk, une société d'édition de logiciels de développement et de collaboration, a décidé de publier une application permettant de remonter et suivre des problèmes techniques (issue tracking system). Cette solution s’adresse à des entreprises clientes, en B2B.

SoftDesk a mis en place une nouvelle équipe chargée de ce projet, et vous avez été embauché comme ingénieur logiciel (back-end) pour créer un back-end performant et sécurisé, devant servir les applications sur toutes les plateformes.

<center>

![Logo de SoftDesk](image.png)


</center>





# Projet : Application Web SoftDesk
1. [Général / Présentation](#Général)
2. [Technologies](#technologies)
3. [Installation](#installation)
4. [Fonctionnement](#fonctionnement)
5. [License](#licence)


## <a id = Général>Général / Présentation</a>
***
Cette application a pour but le suivi des problèmes pour les trois plateformes (site web, app Android et IOS).

L'application permet essentiellement aux utilsateurs de créer des projets, d'ajouter des utilisateurs à des porjets spécifiques, de créer des problèmes au sein des projets et d'attribuer des libellés à ces problèmes en fonction de leurs priorités, de balises/Tags, etc.

Les principales fonctionnalités de l'application sont données dans la documentation Postman ci-dessous:

https://documenter.getpostman.com/view/25793951/2s946bDFFv


## <a id = technologies>Technologies</a>
***

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)  ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)  ![Python](https://img.shields.io/badge/python_3.10-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)     ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

L'application est developpée sous le framework Django et Django restframework.

Elle utilse les languages suivant:



* [Python](https://www.python.org/downloads/release/python-31012/) : Version 3.10
* Type Base de donnée : Sqlite



## <a id = installation>Installation</a>
***
> **Installation** > Python doit etre instalé sur votre machine.
***
### *Telecharger ou cloner les fichiers du repository GITHUB dans le dossier de votre choix, puis deplacer vous dans le dossier "SotDesk"*.
***
Toutes les opérations suivantes seront exécutées dans ce répertoire "SotDesk".

### _**Création environnement Virtuel**_

Por créer un environnement virtuel, taper dans votre terminal les commandes suivantes : 


> Sous Windows:
> ````commandline
> py -m venv env 
>````

> Sous Unix/Mac:
>````commandline
>python3 -m venv env
>````

### _**Activation environnement Virtuel**_

Pour activer ce dernier, taper les instructions suivantes toujours dans votre terminal :

> Sous Windows:
> ````commandline
> env\scripts\activate
>````

> Sous Unix/Mac:
>````commandline
>source env/bin/activate
>````

Votre terminal affichera la ligne de commande comme ci-dessous, confirmant l'activation de l'environnement virtuel :

````
(venv) PS C:\xxx\xxxx\xxxx\SoftDesk>
````


###  **_Installation des packages_**

Taper dans votre terminal les commandes suivantes : 

> Sous Windows:
> ````commandline
> py -m pip install -r requirements.txt
>````

> Sous Unix/Mac:
>````commandline
>python3 -m pip install -r requirements.txt
>````


Cette commande permet l'installation de tous les packages nécessaire au fonctionnement de l'application.

### **_Variable d'environnement_**

Ce projet utilise des variables d'environnement afin de stocker notamment les données sensible tels que la secret key django.

Vous trouverez dans le dossier _SoftDesk/config/.env.example_ un exemple de configuration de variables d'environnement utilisée pour ce projet.


## <a id= fonctionnement>Fonctionnement</a>

###  **_Lancement de l'API_**

Le lancement de l'API s'effectue avec la commande suivante dans le terminal :

> ````commandline
> py manage.py runserver
>````

Le terminal affichera :

>````commandline
>Watching for file changes with StatReloader
>Performing system checks...
>
>System check identified no issues (0 silenced).
>'date et heure'
>Django version 4.2.3, using settings 'config.settings'
>Starting development server at http://127.0.0.1:8000/ 
>Quit the server with CTRL-BREAK.


Ensuite taper l'adresse suivante dans votre navigateur:

> ````commandline
> http://127.0.0.1:8000/
>````

ou  

> ````commandline
> localhost:8000/
>````

## Endpoint
Vous trouverez le descriptif des différentes fonctionnalités de l'API dans la documentation ci-dessous:

https://documenter.getpostman.com/view/25793951/2s946bDFFv

***
## <a id = licence>Licence</a>


* [Licence ouverte](https://www.etalab.gouv.fr/wp-content/uploads/2017/04/ETALAB-Licence-Ouverte-v2.0.pdf) : Version 2.0
***

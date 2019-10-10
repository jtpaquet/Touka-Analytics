Touka Analytics
===================

Table of Contents
-------------
1. [Introduction](#introduction)
2. [Setup](#setup)
3. [Analytics](#analytics)
4. [Archives](#archives)
5. [Chatbot](#chatbot)
6. [Database](#database)
7. [Figures](#figure)
8. [LocalDB](#localDB)
9. [Text to speech](#text-to-speech)
10. [Utils](#utils)
11. [Changelog](#changelog)

Introduction
-------------


Touka Analytics is a platform that 


Setup
-------------


Analytics
-------------

``touka_analytics.py`` génère des statistiques sur les membres de Toukas.
``recherche_mot.py`` génère des statistiques sur les mots dits dans la conversation.


Archives
-------------

``vieux_touka.json`` est le document utilisé pour produire les figures dans (#figure).


Chatbot
-------------


bruh


Database
-------------

bruh


Figures
-------------

bruh


LocalDB
-------------


bruh



Text to speech
-------------

bruh



Utils
-------------

`utils/run_tensorboard.py` is easy to use wrapper starting Tensorboard with model folder

`utils/pairing_testing_outputs.py` - joins model/output_dev file with data/tst2012.form file and prints result to a console allowing easy check if things are going ok during training. The console will consist of input phrase, inference output frame, and separator.

`utils/prepare_for_deployment` - copies only necessary files for inference. [See more below](#deploying-chatbotmodel)



Changelog
---------

### Master
- 

### v0.2
- 

### v0.1
- 

----------
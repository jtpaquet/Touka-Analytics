Touka Analytics
===================

Table of Contents
-------------
1. [Introduction](#introduction)
2. [Setup](#setup)
3. [Analytics] (#analytics)
4. [Archives] (#archives)
5. [Chatbot] (#chatbot)
6. [Database] (#database)
7. [Figures] (#figure)
8. [LocalDB] (#localDB)
9. [Text to speech] (#text-to-speech)
10. [Utils](#utils)
11. [Changelog](#changelog)

Introduction
-------------

Description

Touka Analytics is a platform that 


Setup
-------------

Steps to setup project for your needs:
It is *highly* recommended that you use Python 3.6+. Python 3.4 and 3.5 is likely to work in Linux, but you will eventually hit encoding errors with 3.5 or lower in a Windows environment.

If you want to use exactly what's in tutorial made by Sentdex, use v0.1 tag. There are multiple changes after last part of tutorial.

 1. ```$ git clone --recursive https://github.com/daniel-kukiela/nmt-chatbot```  
    (or)  
    ```$ git clone --branch v0.1 --recursive https://github.com/daniel-kukiela/nmt-chatbot.git``` (for a version featured in Sentdex tutorial)
 2. ```$ cd nmt-chatbot```
 3. ```$ pip install -r requirements.txt``` TensorFlow-GPU is one of the requirements. You also need CUDA Toolkit 8.0 and cuDNN 6.1. (Windows tutorial: https://www.youtube.com/watch?v=r7-WPbx8VuY  Linux tutorial: https://pythonprogramming.net/how-to-cuda-gpu-tensorflow-deep-learning-tutorial/)
 4. ```$ cd setup```
 5. (optional) edit settings.py to your liking. These are a decent starting point for ~4GB of VRAM, you should first start by trying to raise vocab if you can. 
 6. (optional) Edit text files containing rules in the setup directory.
 7. Place training data inside "new_data" folder (train.(from|to), tst2013.(from|to), tst2013(from|to)). We have provided some sample data for those who just want to do a quick test drive.
 8. ```$ python prepare_data.py``` ...Run setup/prepare_data.py - a new folder called "data" will be created with prepared training data
 9. ```$ cd ../```
 10. ```$ python train.py``` Begin training

Version 0.3 introduces epoch-based training including custom (epoch-based as well) decaying scheme - refer to `preprocessing['epochs']` in `setup/settings.py` for more detailed explanation and example (enabled by default).



Analytics
---------

bruh


Archives
--------

bruh


Chatbot
-------


bruh


Database
--------

bruh


Figures
-------

bruh


LocalDB
-------


bruh



Text to speech
--------------

bruh



Utils
-----

`utils/run_tensorboard.py` is easy to use wrapper starting Tensorboard with model folder

`utils/pairing_testing_outputs.py` - joins model/output_dev file with data/tst2012.form file and prints result to a console allowing easy check if things are going ok during training. The console will consist of input phrase, inference output frame, and separator.

`utils/prepare_for_deployment` - copies only necessary files for inference. [See more below](#deploying-chatbotmodel)



Changelog
---------

### Master
- New response scoring engine (work in progress, suggestions and code improvements are welcome)
- Showing score modifiers in 'live' inference mode
- Fixed 'learning bpe' stage of 'prepare_data' speed issue (it's multiple times faster now)
- Improved 'prepare training set' stage of 'prepare_data' speed (should run about 1/3rd faster)
- Fixed model paths - pathhs are relative now, so model can be easily moved between different paths or even machines
- Fixed info about importing project as a module
- Updated README
- Added changelog
- Added table of contents
- Added passing checkpoint name as a parameter for inference
- Added deployment script
- Added ability to cache some `prepare_data` common steps for multiple script run
- Added epoch-based training
- Added custom decaying scheme (epoch-based)
- Added ability to return own evaluation values (will be plotted in TensorBoard)
- Updated `NMT` fork (fixed `train_ppl` graph, added evaluation outputs saved to a separate files, added ability to pass custom evaluation callback function)
- Merged latest `NMT` changes into our fork
- Various fixes and other small improvements

### v0.2
- BPE/WPM-like tokenizer
- Updated NMT
- Enabled NMT's SMP detokenizer with our embedded BPE/WPM-like tokenizer
- Fixed issue with paths on Linux and MacOS machines
- Improved pair testing utility
- Fixed command for tag cloning
- Various fixes and other small improvements, improved readme file

### v0.1
- Initial commit, code for tutorial: https://pythonprogramming.net/chatbot-deep-learning-python-tensorflow/

----------
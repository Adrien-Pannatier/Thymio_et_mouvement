# Thymio Mouvement Organique

Welcome to the user guide for the Choreography Management Software: **TMO**, a tool designed for playing, recording, and editing choreographies seamlessly. This software an intuitive interface to interact with the various modules that make up the system.

# Thymio Movement Organique

1. [Overview](#overview)
   - [Modular Development](#modular-development)
2. [Getting Started](#getting-started)
   - [Installation](#installation)
     - [Requirements](#requirements)
     - [Install Python](#install-python)
     - [Install Thymio Suite](#install-thymio-suite)
     - [Install Software Environment](#install-the-software-environment)
   - [Launch the Software](#launch-the-software)
   - [Usage](#usage)
3. [Usage](#usage)
   - [Play Mode](#play-mode)
   - [Record Mode](#record-mode)
   - [Info Mode](#info-mode)
   - [Editor Mode](#editor-mode)
4. [FAQ](#faq)

## Overview

TMO comprises several modules, each designed to cater to specific functionalities. The user interface is developed using the Python library customtkinter, a refined variant of the tkinter library with enhanced aesthetic properties.

### Modular Development

To ensure robust testing and systematic integration, the development process was divided into four distinct modules:

1.  **Play module:**
    -   Connects to the Thymio robot, enabling users to play different choreographies and sequences effortlessly.
2.  **Record module:**
    -   Allows users to record choreographies using the Mimyo controller, capturing creative sequences with ease.
4.  **Info module:**
    -   Displays essential information about choreographies and sequences, offering insights to enhance user experience.
5.  **Editor module:**
    -   Stores and manages different choreographies and sequences, empowering users to trim, create, and customize choreographies. This module also facilitates the creation of sequences and allows users to add responses to sensor events, providing a comprehensive editing experience.

## Getting Started

This user guide is designed to walk you through the functionalities of each module, offering step-by-step instructions and insights to help you make the most of our Choreography Management Software. Whether you're a seasoned user or a newcomer, this guide will assist you in navigating the software effectively.
## Installation
### Requirements
TMO uses a Thymio robot by Mobsya [**https://www.thymio.org/**] to display the choreography and a Mimyo controller to record the choreographies. Both these elements are required to play and record choreographies. However the software can be launched without these for editing purposes. They also can be connected once the software has been launched.
### Install Python

Before using TMO, you'll need to install Python.

-   [**Here is a link to the Python downloads page.**](https://www.python.org/downloads)
-   [**Here is a helpful guide to installing Python on various operating systems.**](https://wiki.python.org/moin/BeginnersGuide/Download)

_Later in this guide, you will use the Package Installer for Python (pip), which may require you to add Python to your system PATH._
-   To run Tkinter Designer from the source code, follow the instructions below.

### Install Thymio suite
To program Thymio, you must first [**download and install the software**](https://thymio.org/program/), then connect your robot (turn it on, then connect it via cable or wireless dongle). Thymio suite must be openned to allow TMO to recognise the Thymio robots connected to the computer.
    
### Install the software environment
1.	Download the source files for TMO by downloading it manually or using GIT.
	
        `git clone https://github.com/Adrien-Pannatier/Thymio_et_mouvement.git`

3.  Change your working directory to the app folder.
        
        `cd ...TMO/app/`
        
4.  Install the necessary dependencies by running
        
        `pip install -r requirements.txt`
	   -   In the event that pip doesn't work, also try the following commands:
            -   `pip3 install -r requirements.txt`
            -   `python -m pip install -r requirements.txt`
            -   `python3 -m pip install -r requirements.txt`
            -   If this still doesn't work, ensure that Python is added to the PATH.
    
    This will install all requirements needed for TMO to work corectly.
## Launch the software
First you'll need to open Thymio suite and select one of the programming options.
To launch TMO you'll need to open a terminal and enter:
`python -m app`

That's It! You can now use the TMO software on your computer.
    
## Usage

### Play mode

![Play mode](https://github.com/Adrien-Pannatier/Thymio_et_mouvement/blob/main/app/Readme_assets/play_gui.png?raw=true)The play mode allows you to play choreographies and sequences. You can select what you want to play on the left and modify the playing options:

 - Speed factor: between 0.1 and 9.9, scales the playing speed. 
 (**⚠** the Thymio robot has a maximal speed, speed instructions over this speed will be set at the maximal speed)
 - Nbr repetition: the number of times the choreography/sequence must repeat
 - Loop: check to repeat the choreography indefinitely
 - Play/Pause/Stop: Buttons to control the playing choreography/sequence

### Record mode
![Record mode](https://github.com/Adrien-Pannatier/Thymio_et_mouvement/blob/main/app/Readme_assets/record_mode_gui.png?raw=true)The record mode allows you to record new choreographies. On the left you can write down the choreography name and the description of the choreography. 
- The option "⚙" button allows the modification of the calibration constants by hand.
- The "calib" button allows the calibration of the mouse by using the Mimyo controller
- The record "◉" button allows to record a new choreography. The choreography is approximately 20 seconds long.
### Info mode
![Info mode](https://github.com/Adrien-Pannatier/Thymio_et_mouvement/blob/main/app/Readme_assets/info_mode_gui.png?raw=true)The info mode displays useful information about choreographies and sequences. You can select wich choreography/sequence you want informations about in the leften lists.
### Editor mode
The editor mode features 4 different submodules. We will here cover what they can do.

#### Manage mode
![manage mode](https://github.com/Adrien-Pannatier/Thymio_et_mouvement/blob/main/app/Readme_assets/editor_GUI_manage.png?raw=true)
This is the manage mode, here you can manage choreographies and sequences. you can do the following:

 - Delete button "🗑":  delete a choreography/sequence
 - Rename button "✎": rename a choreography/sequence
 - Trim button "✂": trim a choreography
 - Copy button "🗒️": copy a choreography/sequence

#### Create sequence mode
![Create sequence](https://github.com/Adrien-Pannatier/Thymio_et_mouvement/blob/main/app/Readme_assets/editor_GUI_seqcreator.png?raw=true)
This is the create sequence mode, here you can create sequences. You can see the choreographies you can add to the sequence on the left. You can also add a description and a name to the sequence. To create the sequence, you need to click on the button 'create sequence' at the bottom of the screen. The sequence order is the order of the choreographies by number. For example, if you want to create a sequence with the choreographies 1, 2 and 3, you need to enter 1-2-3 in the input dialog.

#### Create random choreography
![Create random choreography](https://github.com/Adrien-Pannatier/Thymio_et_mouvement/blob/main/app/Readme_assets/editor_GUI_randchor.png?raw=true)
This mode allow you to create random choreographies by specifying the speed range, the length, the timestep size and decide wether the motors should start with the same speed or not.

#### Set emotions modes
![Set emotions mode](https://github.com/Adrien-Pannatier/Thymio_et_mouvement/blob/main/app/Readme_assets/editor_GUI_emotions.png?raw=true)
This modules allows you to add emotions to the robot. Emotions are reactions to sesor triggering. The two emotions provided with the program are "fear" and "curiosity". "fear" makes the robot flee if it detects something. "curiosity" on the opposite, attracts the robot to the detected object.

## FAQ
aefs


# GUI for Arduino LED Strip


![image](https://github.com/IceyFL/GUI-for-Arduino-LED-Strip/assets/82657910/42585fd4-38b8-431d-bba3-b27e22bf1fbb)
This is a simple project i have made in my free time

This was designed specifically for my arduino so you may need to mess around with a few things to get it to work properly with your LED Lights.
When you run the app it will automatically minimize to the windows system tray. To change any of the colors you should open the system tray right click on the App Icon and then click show. This will allow you to choose color1 and color2 for your LED effect.

The Project is currently setup for an Arduino UNO.


# Setup


1. You should start by either running the setup.bat file or opening a command prompt instance in the directory you have downloaded this to and running ```pip install -r requirements.txt```

2. Next you will want to setup a jsonblob at https://jsonblob.com with a color1 string and a color2 string

3. In the python code you should add the jsonblobid and the com port of your arduino

4. Run the file

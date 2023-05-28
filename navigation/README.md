# Drone Navigation Usage

## Hardware Requirements
- Raspberry Pi 3/4
- Pixhawk 4

## How-to

1. Update the packages lists :
    ```
    sudo apt-get update
    ```

2. Install the following packages :
    ```
    sudo apt-get install python3-dev python3-opencv python3-wxgtk4.0 python3-pip python3-matplotlib python3-lxml python3-pygame
    ```

3. Install Python dependencies :
    ```
    pip3 install PyYAML mavproxy --user
    sudo pip install pymavlink
    sudo pip install mavproxy
    sudo pip install dronekit
    ```

4. Make sure you have enabled Serial Port on your RPi (check RPi documentation).

## Test setup

- Check if drone is ready to use by running the following command in RPi terminal :

    ```
    mavproxy.py --master=/dev/ttyS0 --baudrate 921600 --aircraft MyDrone
    ```

    As soon as you run this you will get all drone parameters.

- Place the drone in a flyable zone and run   command :

    ```
    python simple_take_off.py --connect /dev/ttyS0
    ```

    Now you will see that drone will take off and after reaching 15m altitude it will stop and then land.

## TODO
- Work-In-Progress
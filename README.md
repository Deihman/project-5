# UOCIS322 - Project 5 #
Brevet time calculator with MongoDB!

Author:     Calvin Stewart

Contact:    clownvant@icloud.com
        or
            cstewar2@uoregon.edu

## Overview

### Display is not working!

This is a python AJAX-based calculator that takes the distance of a 200km, 300km, 400km, 600km, or 1000km brevet, the brevet's start time, and the distance of a checkpoint and calculates the open and close times of the checkpoint.

The JQuery watches for the user to exit the form, then takes their input and displays the open and close times in the form `YYYY-MM-DDTH:mm`.

This version of the calculator adds `Submit` and `Display` buttons that are supposed to store and fetch the input data from a Mongo database. `Submit` is supposed to clear out the input fields, and `Display` is supposed to refill the input fields with the previously stored data.

## How to run



To connect to the calculator, open up your browser and go to `localhost:5001`, replacing `5001` with your port. Play around with it as much as you want, and let me know if you find any issues.


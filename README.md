[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/OcE5Fe4c)

## Task 1 - Exploring Hyperparameters

The hyperparameter "Scale factor for number of conv filters" has been explored and certain configurations have been tested. A few plots and models have been generated and uploaded.

See [01-hyperparameters/REAME.md](https://github.com/UT-ITT/assignment-05-cnn-Brotdev/blob/main/01-hyperparameters/README.md)

## Task 2 - Gathering a Dataset

New pictures have been taken and annoated according to the HaGRID specifications. A confusion matrix has been generated using a slightly modified notebook from task 1.

## Task 3 - Gesture-based Media Controls

Using the slightly modified notebook from task 1 and AR_Game.py from exercise 04, the media controler has been implemented according to the specifications.
The applications detects whether a hand is present in the bottom right corner and trys to predict the current hand pose.
To prevent accidentially triggering an input, the input is debounced (using a cooldown) and visualized as such.


The following **Controls** have been implemented:<br>
`Like`:     Increase Volume<br>
`Dislike`:  Decrease Volume<br>
`Fist`:     Start/Pause media<br>
`Stop`:     Stop media<br>
`Q`: Exit application

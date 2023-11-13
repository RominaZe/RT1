Python Robotics Simulator
================================

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).
Some of the arenas and the exercises have been modified for the Research Track I course

Installing and running
----------------------

The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Pygame, unfortunately, can be tricky (though [not impossible](http://askubuntu.com/q/312767)) to install in virtual environments. If you are using `pip`, you might try `pip install hg+https://bitbucket.org/pygame/pygame`, or you could use your operating system's package manager. Windows users could use [Portable Python](http://portablepython.com/). PyPyBox2D and PyYAML are more forgiving, and should install just fine using `pip` or `easy_install`.

## Troubleshooting

When running `python run.py <file>`, you may be presented with an error: `ImportError: No module named 'robot'`. This may be due to a conflict between sr.tools and sr.robot. To resolve, symlink simulator/sr/robot to the location of sr.tools.

On Ubuntu, this can be accomplished by:
* Find the location of srtools: `pip show sr.tools`
* Get the location. In my case this was `/usr/local/lib/python2.7/dist-packages`
* Create symlink: `ln -s path/to/simulator/sr/robot /usr/local/lib/python2.7/dist-packages/sr/`

To run one or more scripts in the simulator, use `run.py`, passing it the file names. 

```bash
$ python2 run.py assignment.py
```

Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).
https://studentrobotics.org/docs/programming/sr/

 Flowchart
 ---------------------
![image](https://github.com/RominaZe/RT1/assets/146995126/f124557d-1581-402d-a782-0b5c5904b492)


Marker Aggregation Robot
------------
The objective of this project is to create a robot that can collect tokens from a designated area and consolidate them into a single point. The robot will follow these steps:

1. **Navigate to the Center**: The robot will autonomously move to the central location within the arena.
2. **Observe Markers**: Once positioned at the center, the robot will scan the surroundings to detect markers present in the specified area.
3. **Token Collection Strategy**:
	* The robot will initially pick up the first marker it encounters.
	* It will then release this marker at the central point.
	* Subsequently, the robot will collect the remaining markers and position them adjacent to the first one.

By following this process, the robot will effectively aggregate all the markers into a single consolidated point. 

**Note that the coordinates used for release are approximate (based on my PC)**

### Search Token ###
The `primo_token` function analyzes the area using the `R.see()` method of the robot, adding observed tokens to a list. It then checks if any new tokens are present and appends their values to the list


### First Token Function ###
The function `primo_token` is designed to handle tokens when they are the first one. 

1. **Calculate Distance and Angle**: Determine the distance and angle to the target token that we want to reach.
2. **Retrieve the Target Token**: Obtain the relevant token based on the calculated parameters.
3. **Check for Unseen Tokens**: Verify if there are other tokens that were not observed during the previous check.
4. **Release Captured Token**: Release the grabbed token next to the initially captured token in a certain point.

### Other Tokens Function ###
The function `take_token` is designed to handle tokens when they are not the first one encountered. It follows a series of steps to process the tokens effectively:

1. **Calculate Distance and Angle**: Determine the distance and angle to the target token that we want to reach.
2. **Retrieve the Target Token**: Obtain the relevant token based on the calculated parameters.
3. **Check for Unseen Tokens**: Verify if there are other tokens that were not observed during the previous check.
4. **Release Captured Token**: Release the grabbed token next to the initially captured token.
   

### Gathering Function ###
The function `get_together` is designed to handle tokens when they are not the first one encountered. It follows a series of steps to process the tokens effectively:

1. **Calculate Distance and Angle**: Determine the distance and angle to the target token that we want to reach.
2. **Retrieve the Target Token**: Obtain the relevant token based on the calculated parameters.
3. **Check for Unseen Tokens**: Verify if there are other tokens that were not observed during the previous check.
4. **Release Captured Token**: Release the grabbed token next to the initially captured token.

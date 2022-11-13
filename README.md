# Cook-It-Off
An interactive narrative game which involves **automatic commentary generation**.
This project is a work in progress for our [CSC 582 Computer Models of Interactive Narrative](https://www.engineeringonline.ncsu.edu/course/csc-582-computer-models-of-interactive-narrative/) class.

# Premise
<p align="center">
  <img src="https://user-images.githubusercontent.com/24948340/201385087-fa9dc94c-00c4-4710-8fdf-8d0117811ca6.png" alt="3D render of an omelette in a pan, disney artstation style" width="250"/>
  <br>
  <i>Omelette in a pan, using <a href="https://labs.openai.com/">Dall-E</a></i>
</p>

_Join me in an adventure, as I teach you how to cook an omelette with the lovely music of Johann Strauss II playing in the air._

_- Gordo Ramo, Michelin star chef_

# Install
This game requires `flask`. To install flask,
```bash
python3 -m pip install flask
```

To run the game, use
```bash
flask --app server --debug run
```

The game should be running on your localhost.

# License
This project uses code from Pattern's codebase to implement the logic of changing tenses (see [`inflect.py`](https://github.com/pncnmnp/Cook-It-Off/blob/master/inflect.py)). Pattern's code is [licensed under BSD 3-Clause](https://github.com/clips/pattern/blob/master/LICENSE.txt).


# Contributors
* Bonnie Chhatrala (bschhatr@ncsu.edu)
* Brian Davis (bbdavis4@ncsu.edu)
* Omar Kalam (okalam@ncsu.edu)
* Parth Parikh (pmparikh@ncsu.edu)

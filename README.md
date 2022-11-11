# Cook-It-Off
An interactive narrative game which involves automatic dialogue generation.
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
This game requires `nltk` and `pattern`. To install nltk,
```bash
python3 -m pip install nltk
```

There are [some issues with installing pattern on python 3.7 and above](https://github.com/clips/pattern/pull/250). We recommend using a 2019 fork,
```bash
python3 -m pip install git+https://github.com/uob-vil/pattern.git
```

To run the game, use
```bash
flask --app server --debug run
```

The game should be running on your localhost.

# Contributors
* Bonnie Chhatrala (bschhatr@ncsu.edu)
* Brian Davis (bbdavis4@ncsu.edu)
* Omar Kalam (okalam@ncsu.edu)
* Parth Parikh (pmparikh@ncsu.edu)

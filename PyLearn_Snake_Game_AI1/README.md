# Snake Game manual and AI
Hi, the snake game developed by python.

This project inclode two type of game, manual and artificial intellgent. The manual version is in main.py and AI in main_ai.py.

This is version one and at this version of game, you have to eat fruit, as you know!

The apple has one score and pear has two score but eating the shit decrease one score.

You can move snake by navigation keys.

![_game](https://user-images.githubusercontent.com/43343453/212552592-6534d978-54cc-4375-80e6-c00213e006b0.png)

You will lose if:

1- your score decrease to zero by eating shit.

![_gameover_cross](https://user-images.githubusercontent.com/43343453/212552425-6cf4f964-3461-42fc-9d88-fea9ba7904c3.png)

2- your snake collision with itself.

![_gameover_cross](https://user-images.githubusercontent.com/43343453/212552595-1131549e-acaa-4f32-bfbd-4a0f0e540455.png)

3- your snake collision with edge of the game.

![_gameover_out](https://user-images.githubusercontent.com/43343453/212552610-8ce649da-83b5-4c8b-ae25-afbf66861fe3.png)


## Artificial Intelligent

Algorithm: The snake check if the path to pear is free, else check if the path to apple is free, else continues on its way. For check the path, algorithm create rectangle from snake head to target, if path is free this rectangle is blue else is red. Rectangle plot if self.debug is true.
If in next step snake collision fance, snake change direction to pear and if in next step snake collision itself, snake change direction to free space.

                
https://user-images.githubusercontent.com/43343453/213138070-76172ba2-77bd-41f4-b91b-4d18e8021d30.mp4




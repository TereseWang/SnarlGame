README for milestone10:

after downloading all the files, use command "cd" to get
into the folder p10-exec.

run the command to run snarlGen executable:

-- ./dist/snarlGen

you can add the following conditions after the command above,
functions are the same as requirement in m10 description:

 --rooms INT

 --min [ROWS,COLS]
 --max [ROWS,COLS]
 !! there cannot be any space between rows and cols!!

 --json
specifying that a preview of the level should be rendered
 to the screen.

 --render
 specifying that a preview of the level should be rendered
  to the screen.

  You will be able to see the whole map printed in terminal.

Also when you tries to run snarlServer and snarlClient, please do it with python3 snarlClient4.py, some unknown issue happened with the exec and can't be solved. Also when you are rendering the map with snarlGen, please wait a little bit in khoury machine (less than 10 second probably) and also minimize your font size by control&-, since the rendering happens using terminal string , it will looks to cramp together unless you minimize the font size and enlarge the window for the terminal 
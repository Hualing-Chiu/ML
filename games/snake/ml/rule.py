"""
The template of the script for playing the game in the ml mode
"""

# from posix import ST_NOATIME


from typing import ChainMap


class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.pre_command = 0
        pass

    def update(self, scene_info):
        global command
        # global pre_command
        command = 0
        # pre_command=0
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] == "GAME_OVER":
            return "RESET"

        snake_head = scene_info["snake_head"]
        food = scene_info["food"]
        # snake_body = scene_info["snake_body"]
        if len(scene_info["snake_body"]) <= 100:
            if snake_head[1] > 10 and snake_head[1] < 290:
                if snake_head[0]%20 == 10 and snake_head[1] != 10:
                    command = "UP"
                elif snake_head[0]%20 == 0 and snake_head[1] != 290:
                    command = "DOWN"
            # if snake_head[1]+10 == 290 and self.pre_command != "UP":
            #     command = "DOWN"
            elif snake_head[1] == 290 and self.pre_command == "DOWN":
                command = "RIGHT"
            elif snake_head[1] == 290 and self.pre_command == "RIGHT":
                command = "UP"
            # elif snake_head[1]-10 == 0:
            #     command = "UP"
            elif snake_head[1] == 10 and snake_head[0] != 290 and self.pre_command == "UP":
                command = "RIGHT"
            elif snake_head[1] == 10 and self.pre_command == "RIGHT":
                command = "DOWN"
            elif snake_head[0] == 290 and snake_head[1] != 0:
                command = "UP"
            elif snake_head[1] ==0 and snake_head[0] != 0:
                command = "LEFT"
            # elif snake_head[0]-10 == 0 and snake_head[1] == 0:
            #     command = "LEFT"
            elif snake_head[0] == 0 and self.pre_command == "LEFT":
                command = "DOWN"
        elif len(scene_info["snake_body"]) > 100:
            command = "RIGHT"
        print(len(scene_info["snake_body"]))
        # if snake_head[0] == food[0] and snake_head[1]==0:
        #     command = "DOWN"
        # elif snake_head[1] == 290 and snake_head[0] != 290 and snake_head[0] != 0 and snake_head[0] < food[0]:
        #     command = "RIGHT"
        # elif snake_head[1] == 290 and snake_head[0] != 0 and snake_head[0] != 290 and snake_head[0] > food[0] :
        #     command = "LEFT"
        # elif snake_head[1] == 290 and (snake_head[0] == 290 or snake_head[0] == 0):
        #     command = "UP"
        # elif snake_head[1] == 0:
        #     if snake_head[0] != 290:
        #         command = "RIGHT"
        #     elif snake_head[0] != 0:
        #         command = "LEFT"
        # print(scene_info["snake_body"])

        self.pre_command = command
        return command

    def reset(self):
        """
        Reset the status if needed
        """
        pass

# 手動模式:python MLGame.py -m snake
# python MLGame.py -i rule.py snake

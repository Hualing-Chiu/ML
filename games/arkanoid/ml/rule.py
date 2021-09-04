"""
The template of the main script of the machine learning process
"""
import random
import os.path
import pickle

class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        # with open(os.path.join(os.path.dirname(__file__),'model.pickle'),'rb') as f:
        #     self.model=pickle.load(f)
        self.ball_served = False
        self.preX=0
        self.preY=0
        # self.final_X=0
    def update(self, scene_info):
        global command
        global final_X
        global X1
        global Y1
        global m
        global n
        X1=0
        Y1=0
        final_X=0
        m=0
        n=0
        """
        Generate the command according to the received `scene_info`.
        """
        # Make the caller to invoke `reset()` for the next round.
        if (scene_info["status"] == "GAME_OVER" or
            scene_info["status"] == "GAME_PASS"):
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            rand=random.randint(0,9)
            if rand<5:
                command = "SERVE_TO_LEFT"
            else:
                command = "SERVE_TO_RIGHT"
            # command="SERVE_TO_LEFT"
        else:
            # 算斜率
            X1=scene_info["ball"][0]-self.preX
            Y1=scene_info["ball"][1]-self.preY
            if X1!=0:
                m=Y1/X1
            
            if X1>0:
                final_X=scene_info["ball"][0]+(400-(scene_info["ball"][1]))*abs(m)
            else:
                final_X=scene_info["ball"][0]-(400-(scene_info["ball"][1]))*abs(m)
            # if X1<0 and scene_info["ball"][0]==50:
            #     if final_X<50 and final_X>=-150:
            #         final_X=final_X*(-1)+50
            #     elif final_X<-150 and final_X>=-350:
            #         final_X=200-(final_X*(-1)+50)
            # elif X1>0 and scene_info["ball"][0]==145:
            #     if final_X>=150 and final_X<300:
            #         final_X=150-(final_X-150) 
            # else:
            if final_X>=200 and final_X<400:
                final_X=200-(final_X-200)
            elif final_X>=400 and final_X<600:
                final_X=200-(final_X-400)
            elif final_X<0 and final_X>=-200:
                final_X=final_X*(-1)
            elif final_X<-200 and final_X>=-400:
                final_X=200-(final_X*(-1)-200)
            elif final_X<-400 and final_X>=-600:
                final_X=200-(final_X*(-1)-400)
            # print(scene_info["bricks"])
            # print(m)

            if scene_info["ball"][1]<250:
                if scene_info["platform"][0]<70:
                    command="MOVE_RIGHT"
                elif scene_info["platform"][0]>80:
                    command="MOVE_LEFT"
                else:
                    command="NONE"
            else:
                if scene_info["platform"][0]+20<final_X:
                    command="MOVE_RIGHT"
                elif scene_info["platform"][0]+10>final_X:
                    command="MOVE_LEFT"
                else:
                    command="NONE"
        self.preX=scene_info["ball"][0]
        self.preY=scene_info["ball"][1]
        return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False

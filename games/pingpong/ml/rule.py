"""
The template of the script for the machine learning process in game pingpong
"""
import random
class MLPlay:
    def __init__(self, side):
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        self.ball_served = False
        self.side = side
        self.preX=0
        self.preY=0
        self.blockX1=0
        self.blockX2=0
        self.final_X1=0
        self.final_X2=0
        self.ball_X1=0
        self.ball_X2=0

    def update(self, scene_info):
        global X
        global Y
        global command
        global m
        global flag
        X=0
        Y=0
        m=0
        command=0
        flag=0
        """
        Generate the command according to the received scene information
        """
        # X=scene_info["ball"][0]-self.preX
        # Y=scene_info["ball"][1]-self.preY
        # if scene_info["ball_speed"][0]:
        #     m=scene_info["ball_speed"][1]/scene_info["ball_speed"][0]
        if scene_info["status"] != "GAME_ALIVE":
            print(scene_info["ball_speed"])
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            rand=random.randint(0,1)
            if rand==0:
                return "SERVE_TO_LEFT"
            else:
                return "SERVE_TO_RIGHT"
            # return "SERVE_TO_LEFT"
        else:
            if scene_info["ball_speed"][1] != 0:
                global up_2P
                global down_1P
                if scene_info["ball"][1] == 80:
                        up_2P = scene_info["ball"][0]
                if scene_info["ball"][1] == 415:
                        down_1P = scene_info["ball"][0]
                if self.side=="1P":                
                    if scene_info["ball"][1]>240 : #球還在障礙物底下
                        if scene_info["ball"][1]==415:
                            # self.catchX1=scene_info["ball"][0] #紀錄板子接到球的x
                            if scene_info["ball_speed"][0] > 0:
                                self.blockX1=scene_info["ball"][0] + abs((260-415)/scene_info["ball_speed"][1]*scene_info["ball_speed"][0]) #撞到障礙物底部
                                flag=1
                            elif scene_info["ball_speed"][0] < 0:
                                self.blockX1=scene_info["ball"][0] - abs((260-415)/scene_info["ball_speed"][1]*scene_info["ball_speed"][0]) #撞到障礙物底部
                                flag=2

                        if self.blockX1 > 195: # 撞到右側牆壁
                            self.blockX1 = 195-(self.blockX1-195)
                            flag=2
                        elif self.blockX1 < 0: # 撞到左側牆壁
                            self.blockX1 = self.blockX1*(-1)
                            flag=1
                        # print(self.blockX1)
                        if flag==1 :
                            self.final_X1=self.blockX1+abs((415-260)/scene_info["ball_speed"][1]*scene_info["ball_speed"][0])
                        elif flag==2:
                            self.final_X1=self.blockX1-abs((415-260)/scene_info["ball_speed"][1]*scene_info["ball_speed"][0])
                        
                        if self.final_X1>200 and self.final_X1<400:
                            self.final_X1=200-(self.final_X1-200)
                        elif self.final_X1>=400 and self.final_X1<600:
                            self.final_X1=self.final_X1-400
                        elif self.final_X1<0 and self.final_X1>=-200:
                            self.final_X1=self.final_X1*(-1)
                        elif self.final_X1>=-400 and self.final_X1<-200:
                            self.final_X1=self.final_X1-(-400)

                        if scene_info["platform_1P"][0]+15>self.final_X1:
                            command="MOVE_LEFT"
                        elif scene_info["platform_1P"][0]+30<self.final_X1:
                            command="MOVE_RIGHT" 
                        else:
                            command="NONE" 
                    
                    # part 2 預設撞到磚塊側邊
                    if scene_info["ball_speed"][1] > 0 and scene_info["ball"][1]<240:
                        if scene_info["ball_speed"][0] > 0 :
                            self.final_X1=(scene_info["ball"][0])+abs((415-(scene_info["ball"][1]))/scene_info["ball_speed"][1]*scene_info["ball_speed"][0])
                            flag=1
                        elif scene_info["ball_speed"][0] < 0:
                            self.final_X1=(scene_info["ball"][0])-abs((415-(scene_info["ball"][1]))/scene_info["ball_speed"][1]*scene_info["ball_speed"][0])   
                            flag=2

                        if self.final_X1>200 and self.final_X1<=400:
                            self.final_X1=200-(self.final_X1-200)
                        elif self.final_X1>400 and self.final_X1<=600:
                            self.final_X1=self.final_X1-400
                        elif self.final_X1<0 and self.final_X1>=-200:
                            self.final_X1=self.final_X1*(-1)
                        elif self.final_X1>=-400 and self.final_X1<-200:
                            self.final_X1=self.final_X1-(-400)
                            # print(self.final_X1)
                        # print(up_2P)
                        self.final_X1=(self.final_X1 + up_2P)/2

                        if scene_info["platform_1P"][0]+15>self.final_X1:
                            command="MOVE_LEFT"
                        elif scene_info["platform_1P"][0]+30<self.final_X1:
                            command="MOVE_RIGHT" 
                        else:
                            command="NONE" 

                        # print("final_X1",self.final_X1)
                    if scene_info["ball_speed"][1] < 0:
                        if scene_info["ball"][1]<260:
                            # print(1)
                            if scene_info["platform_1P"][0]<95:
                                command="MOVE_RIGHT"
                            elif scene_info["platform_1P"][0]>105:
                                command="MOVE_LEFT"
                            else:
                                command="NONE"
                    # 修正
                    if scene_info["ball"][1]>=260 and scene_info["ball_speed"][1] > 0:
                        if scene_info["ball_speed"][0] > 0 :
                            self.ball_X1=scene_info["ball"][0]+abs((415-scene_info["ball"][1])/scene_info["ball_speed"][1]*scene_info["ball_speed"][0])
                        elif scene_info["ball_speed"][0] < 0:
                            self.ball_X1=scene_info["ball"][0]-abs((415-scene_info["ball"][1])/scene_info["ball_speed"][1]*scene_info["ball_speed"][0])
                        
                        if self.ball_X1>200 and self.ball_X1<400:
                            self.ball_X1=200-(self.ball_X1-200)
                        elif self.ball_X1>=400 and self.ball_X1<600:
                            self.ball_X1=self.ball_X1-400
                        elif self.ball_X1<0 and self.ball_X1>=-200:
                            self.ball_X1=self.ball_X1*(-1)
                        elif self.ball_X1>=-400 and self.ball_X1<-200:
                            self.ball_X1=self.ball_X1-(-400)

                        self.final_X1 = self.ball_X1
                            
                        if scene_info["platform_1P"][0]+15>self.final_X1:
                            command="MOVE_LEFT"
                        elif scene_info["platform_1P"][0]+30<self.final_X1:
                            command="MOVE_RIGHT" 
                        else:
                            command="NONE" 
                elif self.side=="2P":
                    if scene_info["ball"][1]<260 :
                        if scene_info["ball"][1]==80:
                        # self.catchX2=scene_info["ball"][0] #紀錄板子接到球的x
                            if scene_info["ball_speed"][0] > 0:
                                self.blockX2=scene_info["ball"][0] + abs((235-80)/scene_info["ball_speed"][1]*scene_info["ball_speed"][0]) #撞到障礙物底部
                                flag=1
                            elif scene_info["ball_speed"][0] < 0:
                                self.blockX2=scene_info["ball"][0] - abs((235-80)/scene_info["ball_speed"][1]*scene_info["ball_speed"][0]) #撞到障礙物底部
                                flag=2
                        if self.blockX2 > 195: # 撞到右側牆壁
                            self.blockX2 = 195-(self.blockX2-195)
                            flag=2
                        elif self.blockX2 < 0: # 撞到左側牆壁
                            self.blockX2 = self.blockX2*(-1)
                            flag=1

                        if flag==1:
                            self.final_X2=self.blockX2+abs((235-80)/scene_info["ball_speed"][1]*scene_info["ball_speed"][0])
                        elif flag==2:
                            self.final_X2=self.blockX2-abs((235-80)/scene_info["ball_speed"][1]*scene_info["ball_speed"][0])
                        
                        if self.final_X2>200 and self.final_X2<400:
                            self.final_X2=200-(self.final_X2-200)
                        elif self.final_X2>=400 and self.final_X2<600:
                            self.final_X2=self.final_X2-400
                        elif self.final_X2<0 and self.final_X2>=-200:
                            self.final_X2=self.final_X2*(-1)
                        elif self.final_X2>=-400 and self.final_X2<-200:
                            self.final_X2=self.final_X2-(-400)

                        if scene_info["platform_2P"][0]+15>self.final_X2:
                            command="MOVE_LEFT"
                        elif scene_info["platform_2P"][0]+30<self.final_X2:
                            command="MOVE_RIGHT"  
                        else:
                            command="NONE"
                        
                    if scene_info["ball_speed"][1] < 0 and scene_info["ball"][1]>=240:
                        if scene_info["ball_speed"][0] > 0:
                            self.final_X2=scene_info["ball"][0]+abs(((scene_info["ball"][1])-80)/scene_info["ball_speed"][1]*scene_info["ball_speed"][0])
                        elif scene_info["ball_speed"][0] < 0:
                            self.final_X2=scene_info["ball"][0]-abs(((scene_info["ball"][1])-80)/scene_info["ball_speed"][1]*scene_info["ball_speed"][0])

                        if self.final_X2>200 and self.final_X2<400:
                            self.final_X2=200-(self.final_X2-200)
                        elif self.final_X2>=400 and self.final_X2<600:
                            self.final_X2=self.final_X2-400
                        elif self.final_X2<0 and self.final_X2>=-200:
                            self.final_X2=self.final_X2*(-1)
                        elif self.final_X2>=-400 and self.final_X2<-200:
                            self.final_X2=self.final_X2-(-400)
                            # print(self.final_X1)

                        self.final_X2=(self.final_X2 + down_1P)/2

                        if scene_info["platform_2P"][0]+15>self.final_X2:
                            command="MOVE_LEFT"
                        elif scene_info["platform_2P"][0]+30<self.final_X2:
                            command="MOVE_RIGHT"  
                        else:
                            command="NONE"

                    if scene_info["ball_speed"][1] > 0:
                        if scene_info["ball"][1]>240:
                            if scene_info["platform_2P"][0]<95:
                                command="MOVE_RIGHT"
                            elif scene_info["platform_2P"][0]>105:
                                command="MOVE_LEFT"
                            else:
                                command="NONE"
                    # 修正
                    if scene_info["ball"][1]<=240 and scene_info["ball_speed"][1] < 0:
                        if scene_info["ball_speed"][0] > 0:
                            self.ball_X2=scene_info["ball"][0]+abs((scene_info["ball"][1]-80)/scene_info["ball_speed"][1]*scene_info["ball_speed"][0])
                        elif scene_info["ball_speed"][0] < 0:
                            self.ball_X2=scene_info["ball"][0]-abs((scene_info["ball"][1]-80)/scene_info["ball_speed"][1]*scene_info["ball_speed"][0])
                        
                        if self.ball_X2>200 and self.ball_X2<400:
                            self.ball_X2=200-(self.ball_X2-200)
                        elif self.ball_X2>=400 and self.ball_X2<600:
                            self.ball_X2=self.ball_X2-400
                        elif self.ball_X2<0 and self.ball_X2>=-200:
                            self.ball_X2=self.ball_X2*(-1)
                        elif self.ball_X2>=-400 and self.ball_X2<-200:
                            self.ball_X2=self.ball_X2-(-400)

                        self.final_X2=self.ball_X2
                
                        if scene_info["platform_2P"][0]+15>self.final_X2:
                            command="MOVE_LEFT"
                        elif scene_info["platform_2P"][0]+30<self.final_X2:
                            command="MOVE_RIGHT"  
                        else:
                            command="NONE"       
                return command

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False

# python MLGame.py -i ml_play_template.py pingpong HARD 3
# python MLGame.py -i ml_play_template.py -f 100 -r pingpong HARD 3
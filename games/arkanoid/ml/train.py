import os
import pickle
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

X_all = np.array([[0, 0, 0, 0 ,0 ,0]])
y_all = np.array([])
# 列出 pickle 檔
dir_path = './log/'
files = os.listdir(dir_path)

for file in files:
    file_path = dir_path + file
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    scene_info = data['ml']['scene_info']
    command = data['ml']['command']

    Ball_x = []
    Ball_y = []
    Ball_speed_x = []
    Ball_speed_y = []
    Direction = []
    Platform = []
    Command = []

    print(scene_info[1:-2])
    for i, s in enumerate(scene_info[1:-2]):
        Ball_x.append(s['ball'][0])
        Ball_y.append(s['ball'][1])
        Platform.append(s['platform'][0])
        Ball_speed_x.append(scene_info[i+2]["ball"][0] - scene_info[i+1]["ball"][0])
        Ball_speed_y.append(scene_info[i+2]["ball"][1] - scene_info[i+1]["ball"][1])
        if Ball_speed_x[-1] > 0:
            if Ball_speed_y[-1] > 0:
                # 右下
                Direction.append(0)
            else:
                # 右上
                Direction.append(1)
        else:
            if Ball_speed_y[-1] > 0:
                # 左下
                Direction.append(2)
            else:
                # 左上
                Direction.append(3)
                
    for c in command[1:-2]:
        if c == "NONE":
            Command.append(0)
        elif c == "MOVE_LEFT":
            Command.append(-1)
        elif c == "MOVE_RIGHT":
            Command.append(1)
    numpy_data = np.array([Ball_x, Ball_y, Ball_speed_x, Ball_speed_y, Direction, Platform])
    X = np.transpose(numpy_data) 
    y = command
    scene_info = data['ml']['scene_info']
    command = data['ml']['command']

    k = range(1, len(scene_info)-1)

    ball_x = np.array([scene_info[i]['ball'][0] for i in k])
    ball_y = np.array([scene_info[i]['ball'][1] for i in k])
    ball_speed_x = np.array([scene_info[i+1]['ball'][0] - scene_info[i]['ball'][0] for i in k])
    ball_speed_y = np.array([scene_info[i+1]['ball'][1] - scene_info[i]['ball'][1] for i in k])
    direction = np.where(np.vstack((ball_speed_x, ball_speed_y)) > 0, [[1],[0]], [[2],[3]]).sum(axis=0)  # x y: ++1, +-4, -+2, --3
    platform = np.array([scene_info[i]['platform'][0] for i in k])
    target = np.where(np.array(command) == 'NONE', 0,
                    np.where(np.array(command) == 'MOVE_LEFT', -1, 1))[1:-1]  # [0] SERVE_TO_RIGHT, [1897] None
    X = np.hstack((ball_x.reshape(-1, 1),
               ball_y.reshape(-1, 1),
               ball_speed_x.reshape(-1, 1),
               ball_speed_y.reshape(-1, 1),
               direction.reshape(-1, 1),
               platform.reshape(-1, 1)))
    y = target
    
    X_all = np.concatenate((X_all, X))
    y_all = np.append(y_all, y)

X_all = np.delete(X_all, 0, axis=0)

model = KNeighborsClassifier(n_neighbors=3)
print(model.fit(X_all, y_all))
print(model.score(X_all, y_all))
with open('my_model.pickle', 'wb') as f:
    pickle.dump(model, f)
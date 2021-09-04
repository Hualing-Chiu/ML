import os
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import datasets
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# X_all = np.array([[0, 0, 0, 0 ,0 ,0]])
# y_all = np.array([])
# 列出 pickle 檔
dir_path = './log/'
files = os.listdir(dir_path)
for file in files:
    file_path = dir_path + file
    with open(file_path, 'rb') as f:
        data = pickle.load(f)
    scene_info=data['ml']['scene_info']
    command=data['ml']['command']

    snake_X = []
    snake_Y = []
    food_X = []
    food_Y = []
    Command = []

    # print(scene_info[1:-2])
    k = range(0, len(scene_info))

    snake_X = np.array([scene_info[i]['snake_head'][0] for i in k])
    snake_Y = np.array([scene_info[i]['snake_head'][1] for i in k])
    # food_X = np.array([scene_info[i]['food'][0] for i in k])
    # food_Y = np.array([scene_info[i]['food'][1] for i in k])
    # for s in enumerate(scene_info[1:-2]):
    #     snake_X.append(s['snake_head'][0])
    #     snake_Y.append(s['snake_head'][1])
    #     food_X.append(s['food'][0])
    #     food_Y.append(s['food'][1])

    for c in command:
        if c == "LEFT":
            Command.append(0)
        elif c == "RIGHT":
            Command.append(1)
        elif c == "UP":
            Command.append(2)
        elif c == "DOWN":
            Command.append(3)
        else:
            Command.append(4)
    numpy_data = np.array([snake_X,snake_Y])
    X = np.transpose(numpy_data) 
    y = Command
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3)
# rfc=RandomForestClassifier(n_estimators=100,n_jobs = -1,random_state =50, min_samples_leaf = 10)
rfc=RandomForestClassifier(n_estimators=5)

print(rfc.fit(X_test,y_test))
print(rfc.score(X_test,y_test))
with open('my_model.pickle', 'wb') as f:
    pickle.dump(rfc, f)
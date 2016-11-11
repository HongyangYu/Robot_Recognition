import os

path = '/home/henry/Desktop/RobotLearning/Recognition/test1'
files = os.listdir(path)
fh = open('testing.csv','w')
for eachfile in files:
    if not eachfile.startswith('image'):
        continue
    else:
        filename = os.path.join(path,eachfile)
        fh.write(filename+'\n')
fh.close()

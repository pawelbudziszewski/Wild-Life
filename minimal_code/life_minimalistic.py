from cv2 import*;from numpy import*;W=random.rand(800,999)<.8
while waitKey(1)<0:N=filter2D(W*1.,-1,ones((3,3)))-W;W=(N==3)|(W==1)&(N==2);imshow('',W*1.)
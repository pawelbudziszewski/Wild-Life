from cv2 import*;from numpy import*;W=eye(800,999)
while waitKey(1)<0:N=filter2D(W,6,ones((3,3)))-W;W=((N==3)|(W==1)&(N==2))*1.;imshow('',W)
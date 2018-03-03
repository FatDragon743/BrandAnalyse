# -*- coding:utf-8 -*-  
'''
Created on 2018年3月1日

@author: Administrator
'''
import operator
import math
def handle_lines(lines,width,height):
    kh = []#横线
    ks = []#竖线
    i = 0
#     print lines[0]
    ks,kh=get_hs(lines,width)
    ks,kh=get_marge(ks,kh)
    ks,kh=extend_line(ks,kh,width,height)
    ks,kh=cut_line(ks,kh,width)
    return ks,kh
def get_hs(lines,width):
    kh = []#横线
    ks = []#竖线
    for line in lines:
        for x1,y1,x2,y2 in line:
            L = (x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)
            if L < (width/16)*(width/16):
                continue
            #if the length of the line <width/16 abandon
            k1 = (x1-x2)*(x1-x2)
            k2 = (y1-y2)*(y1-y2)
            tmp =[x1,y1,x2,y2]
            # 区分横线还是竖线
            if k1<0.5:
                ks.append(tmp)  
            elif k2<0.5:  
                kh.append(tmp)
    return ks,kh
def get_marge(ks,kh):
    #合并横线
    for i in range(len(ks)):
        for j in range(i+1,len(ks)):
                L = (ks[j][0]-ks[i][0])*(ks[j][0]-ks[i][0])
                if (L < 100):
                    ll = ks[i][1],ks[j][1],ks[i][3],ks[j][3]
                    _min = min(ll)
                    _max = max(ll)
                    tmp = [ks[i][0],_min,ks[i][0],_max]
                    ks[i]=[0,0,0,0]
                    ks[j]=tmp  
    #合并竖线
    for i in range(len(kh)):
        for j in range(i+1,len(kh)):
                L = (kh[j][1]-kh[i][1])*(kh[j][1]-kh[i][1])
                if (L < 100):
                    ll = kh[i][0],kh[j][0],kh[i][2],kh[j][2]
                    _min = min(ll)
                    _max = max(ll)
                    tmp = [_min,kh[i][1],_max,kh[i][3]]
                    kh[i]=[0,0,0,0]
                    kh[j]=tmp  
#     sorted(kh,key = operator.itemgetter(0),reverse=True)
    return ks,kh
def extend_line(ks,kh,width,height):
    new_ks = []
    new_kh=[[0,0,width,0],[0,height,width,height]]
    for x1,y1,x2,y2 in kh:
        L = (x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)
        if L<=(width/8)*(width/8):
            continue
        tmp =[x1,y1,x2,y2]
        if x1<width/4:
            tmp[0]=0
        if x2>width/4*3:
            tmp[2]=width
        if math.fabs(x1-width/2)<width/4:
            tmp[0] = width/2
        if math.fabs(x2-width/2)<width/4:
            tmp[2] = width/2
        new_kh.append(tmp)
    new_kh.sort(cmp=None, key=operator.itemgetter(1))
    for x1,y1,x2,y2 in ks:
        L = (x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)
        if L<=(height/2)*(height/2)*0.2:
            continue
        _min = 0
        _max = height
        for i in range(len(new_kh)-1):
            y11=new_kh[i][1]
            y111=new_kh[i+1][1]
            if y11<y1:
                _min =y11
            if y11<y2:
                _max =y111
        new_ks.append([x1,_min,x2,_max])
    return new_ks,new_kh
def cut_line(ks,kh,width):
    _min = ks[0][1]
    _max = ks[0][3]
    new_kh = []
    for x1,y1,x2,y2 in kh:
        if y1 > _min and y1 < _max:
            new_kh.append([x1,y1,width/2,y2])
            new_kh.append([width/2,y1,x2,y2])
        else:
            new_kh.append([x1,y1,x2,y2])
    return ks,new_kh
            
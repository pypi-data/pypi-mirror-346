"""
upd 2025.5.5: 背景无需是黑色，可设置背景颜色
"""
import cv2
from imageio import *
import numpy as np
def spin(im,v,t,fn,ctr=(0,0),fps=30,col=(0,0,0)):
    """
    旋转
    :param im: 图像
    :param v: 速度(°/s)
    :param t: 时间
    :param fn: 文件名
    :param ctr: 旋转中心
    :param fps: fps
    :param col: 背景颜色，默认为黑色
    :return:
    """
    l=[]
    l.append(cv2.cvtColor(im,cv2.COLOR_BGR2RGB))
    a,b=im.shape[:2]
    for i in range(0,t*fps):
        mat=cv2.getRotationMatrix2D(ctr,v*t*i/(t*fps),1)
        rotimg=cv2.warpAffine(im,mat,(b,a),borderMode=cv2.BORDER_CONSTANT,borderValue=col)
        l.append(cv2.cvtColor(rotimg,cv2.COLOR_BGR2RGB))
    if fn.endswith('.gif'):
        mimwrite(fn,list(reversed(l)), duration=1000/fps)
    else:
        mimwrite(fn, list(reversed(l)), fps=fps)
def enlarge(im,t,fn,ctr=(0,0),fps=30,col=(0,0,0)):
    """
    放大
    :param im: 图像
    :param t: 时间
    :param ctr: 放大中心
    :param fn: 文件名
    :param fps: fps
    :param col: 背景颜色，默认为黑色
    :return:
    """
    l=[]
    a,b=im.shape[:2]
    for i in range(0,t*fps):
        mat=cv2.getRotationMatrix2D(ctr,0,1/(t*fps)*(i+1))
        rotimg=cv2.warpAffine(im,mat,(b,a),borderMode=cv2.BORDER_CONSTANT,borderValue=col)
        l.append(cv2.cvtColor(rotimg,cv2.COLOR_BGR2RGB))
    l.append(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
    if fn.endswith('.gif'):
        mimwrite(fn,l, duration=1000/fps)
    else:
        mimwrite(fn, l, fps=fps)
def enlarge_spin(im,v,t,fn,ctr=(0,0),fps=30,col=(0,0,0)):
    """
    放大+旋转
    :param im: 图像
    :param v: 速度(°/s)
    :param t: 时间
    :param ctr: 放大中心
    :param fn: 文件名
    :param fps: fps
    :param col: 背景颜色，默认为黑色
    :return:
    """
    l=[]
    a,b=im.shape[:2]
    for i in range(0,t*fps):
        mat=cv2.getRotationMatrix2D(ctr,v*t*(1-i/(t*fps)),1/(t*fps)*(i+1))
        rotimg=cv2.warpAffine(im,mat,(b,a),borderMode=cv2.BORDER_CONSTANT,borderValue=col)
        l.append(cv2.cvtColor(rotimg,cv2.COLOR_BGR2RGB))
    l.append(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
    if fn.endswith('.gif'):
        mimwrite(fn,l, duration=1000/fps)
    else:
        mimwrite(fn, l, fps=fps)
def translate(im,vx,vy,t,fn,fps=30,col=(0,0,0)):
    """
    平移
    :param im: 图像
    :param vx: 水平速度(px/s)
    :param vy: 垂直速度(px/s)
    :param t: 时间
    :param fn: 文件名
    :param fps: fps
    :param col: 背景颜色，默认为黑色
    :return:
    """
    l=[]
    l.append(cv2.cvtColor(im,cv2.COLOR_BGR2RGB))
    a,b=im.shape[:2]
    for i in range(0,t*fps):
        mat=np.float32([[1,0,vx*i/(t*fps)],[0,1,vy*i/(t*fps)]])
        rotimg=cv2.warpAffine(im,mat,(b,a),borderMode=cv2.BORDER_CONSTANT,borderValue=col)
        l.append(cv2.cvtColor(rotimg,cv2.COLOR_BGR2RGB))
    if fn.endswith('.gif'):
        mimwrite(fn,list(reversed(l)), duration=1000/fps)
    else:
        mimwrite(fn, list(reversed(l)), fps=fps)
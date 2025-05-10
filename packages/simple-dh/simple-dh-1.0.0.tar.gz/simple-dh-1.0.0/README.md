```shell
pip install simple-dh
```

```py
from dh import *
img=cv2.imread('testimg.png')
mx,my=img.shape[0],img.shape[1]
mx//=2
my//=2
spin(img,30,2,'result.mp4',col=(255,255,255))
enlarge(img,2,'result2.mp4',(my,mx),col=(255,255,255))
enlarge_spin(img,30,2,'result3.mp4',(my,mx),col=(255,255,255))
translate(img,110,250,2,'result4.mp4',col=(255,255,255))
spin(img,30,2,'result.gif',col=(255,255,255))
enlarge(img,2,'result2.gif',(my,mx),col=(255,255,255))
enlarge_spin(img,30,2,'result3.gif',(my,mx),col=(255,255,255))
translate(img,110,250,2,'result4.gif',col=(255,255,255))
```
# simple_dh
 简易动画制作器


需要的库：[opencv-python](https://pypi.org/project/opencv-python)，[imageio](https://pypi.org/project/imageio)

目前支持如下动画，详细简介请看注释：
* 旋转
* 放大
* 放大旋转
* 平移

效果：

[![result.gif](https://i.postimg.cc/qgfSC9JM/result.gif)](https://postimg.cc/0KfcTXKL)

[![result2.gif](https://i.postimg.cc/x1QjwZv2/result2.gif)](https://postimg.cc/TpkXmCN7)

[![result3.gif](https://i.postimg.cc/WbGTw7Qf/result3.gif)](https://postimg.cc/XpYRV9Nw)

[![result4.gif](https://i.postimg.cc/tTnHZd3k/result4.gif)](https://postimg.cc/r0TH7rYR)

Simple Animation Maker

Required libraries: [opencv-python](https://pypi.org/project/opencv-python)，[imageio](https://pypi.org/project/imageio)

Currently, these types of animation are supported. Please refer to the comments for a detailed introduction:
* Spin
* Enlarge
* Enlarge and spin
* Translate

Effect:

[![result.gif](https://i.postimg.cc/qgfSC9JM/result.gif)](https://postimg.cc/0KfcTXKL)

[![result2.gif](https://i.postimg.cc/x1QjwZv2/result2.gif)](https://postimg.cc/TpkXmCN7)

[![result3.gif](https://i.postimg.cc/WbGTw7Qf/result3.gif)](https://postimg.cc/XpYRV9Nw)

[![result4.gif](https://i.postimg.cc/tTnHZd3k/result4.gif)](https://postimg.cc/r0TH7rYR)

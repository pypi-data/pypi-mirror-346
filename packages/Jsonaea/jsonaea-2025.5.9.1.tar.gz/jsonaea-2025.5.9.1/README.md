***Jsonaea*** *script by* ***Begloon.***  

# 简介
**Jsonaea**为可将Arcaea游戏中铺面文件（``x.aff``）转换为json文件 / 字典，亦可将json文件 / 字典转换回铺面文件的实用库。  
其理论上可读取并转换aff文件中的任何语句（目前除注释外），并无损地将其互相转换。  
此库使用``Python``编写。  
此库还有一个``Tools``附加库，内含多种不必要但减少代码量的实用函数。

## 快速使用
在github本项目上直接下载后手动安装。   
在 [本页面](https://github.com/321bug/Jsonaea/tree/main/dist) 下载最新版本的两个打包中任意一个  
然后在终端中输入命令：
```
pip install 下载的文件本地路径  
```

---
在py文件中导入库：  
```python
import jsonaea
```
---
使用load函数生成字典：
```python
load(arcPath)
```
``arcPath``: Arcaea铺面文件导入路径  
此函数将返回一个字典。

---
使用createJson函数生成json文件
```python
createJson(dict,JsonPath)
```
`dict`:创建json文件的字典
`JsonPath`:创建json文件的路径
此函数不返回值，会创建一个json文件。

---
导出生成的json文件 / 字典为``.aff``文件：
```python
output(arcJson,arcPath)
```
``arcJson``: 提供的json文件（字典）  
``arcPath``: Arcaea铺面文件导出路径  
此函数不返回值，会创建一个``.aff``文件。

### 示例
jsonaea库使用的具体示例，以下代码可将铺面中的arc全部转化为蛇：  
```python
import tkinter as tk
from tkinter import filedialog
from jsonaea import *

#生成铺面导入窗口
root = tk.Tk()
root.withdraw () 
arcPath = filedialog.askopenfilename () 

#导入铺面
arc = load(arcPath)
#设置Tools库全局变量
Tools.arcJson = arc
#检索所有黑线事件
searchedEvent = Tools.searchEventSubject({"type":"arc","IsSkyline": True})
#并将其全部转化为蛇
for se in searchedEvent:
    Tools.changeEvent(se,{"IsSkyline":False})
#导出铺面
output(arc,"./noSkyline.aff")
#导出处理完的Json文件
createJson(arc, "./this.json")
input("已完成")
```

# json文件 / 字典格式
```json
{
  "META":{},
  "Camera":[],
  "Scenecontrol":[],
  "TimingList":[
    {
      "tags":[],
      "notes":[],
      "timing":[],
    }
  ]
}
```
- META字典：  
  存储铺面文件头，如:
  ```json
  "AudioOffset": 0,
  "TimingPointDensityFactor":2
  ```
- Camera列表：  
  存储铺面摄像头信息，如：
  ```json
  "time": 0,
  "transverse": 0.0,
  "bottomzoom": 0.0,
  "linezoom": 0.0,
  "steadyangle": 0.0,
  "topzoom": 0.0,
  "angle": 0.0,
  "easing": "reset",
  "lastingtime": 1
  ```
  详见 [ARCAEA中文维基](https://wiki.arcaea.cn/) 中对谱面格式的介绍  
  多个字典以列表形式存储

- Scenecontrol列表：
  存储铺面Scenecontrol事件信息，如：
  ```json
  "time": 0,
  "type": "arcahvdistort",
  "param": [
    1.25,
    0
  ]
  ```
  其中``"param"``项在没有参数时不会生成，详见 [ARCAEA中文维基](https://wiki.arcaea.cn/) 中对谱面格式的介绍  
  多个字典以列表形式存储
- TimingList列表：
  存储无timinggroup与timinggroup组的事件  
  在该列表中无timinggroup的下标为0，timinggroup组的下标≥1（如果铺面中无timinggroup组，则该列表中只有下标为零的字典）  
  多个字典以列表形式存储，字典中存有key为``"tags"``,``"notes"``与``"timing"``的三个列表  
  当在该列表中下标为0的字典中（即无timinggroup的事件），``"tags"``中无参数。
  - tags
    在aff文件``timinggroup(){};``中小括号中的标识，一般用于对timinggroup中的事件达成特殊效果（如noinput）  
    字典格式如：
      ```json
      "noinput",
      "anglex200"
      ```
      
  - notes  
    note事件，分为``tap``、``hold``、``arc``三个类型，由key值``"type"``区分  
    其中``tap``的字典格式如：
    ```json
    "type": "tap",
    "time": 0,
    "track": 1
    ```
    其中track指轨道，目前无法读取track为小数的tap事件  
    
    其中``hold``的字典格式如：
    ```json
    "type": "hold",
    "startTime": 0,
    "endTime": 1000,
    "track": 3
    ```
    其中track指轨道，目前无法读取track为小数的hold事件  
   
    其中``arc``的字典格式如：
    ```json
    "type": "arc",
    "startTime": 0,
    "endTime": 1000,
    "startPos": [
      0.5,
      1.0
    ],
    "endPos": [
      1.0,
      1.0
    ],
    "arcType": "si",
    "color": "blue",
    "hitsound": "none",
    "IsSkyline": true
    ```
    其中``"startPos"``与``"endPos"``列表中下标为0的参数时坐标x,下标为1的为坐标y  
    ``"arcType"``是指该arc的滑动方式  
    ``"hitsound"``为该arc上arctap的打击音，如果有填以铺面的相对路径，如果没有填none  
    ``"IsSkyline"``为该arc是否为黑线，反之为蛇  
    如果该arc上有arctap，那么将在下方添加键值对，如：  
    ```json
    "arctap": [
       200,
       600
    ]
    ```
    列表中存储着该arc上所有arctap的时间，其范围在startTime与endTime之间  
    
  - timing
    控制铺面的bpm（流速）与beat（小节线）
    其格式如：
    ```json
    "time": 0,
    "BPM": 191.0,
    "metreInfo": 4.0
    ```
    其中``"metreInfo"``是指表示每多少个四分拍为一小节，并出现一条小节线  
    多个字典以列表形式存储  
    
  对以上任何信息如有困惑，详见 [ARCAEA中文维基](https://wiki.arcaea.cn/) 中对谱面格式的介绍。  

# 特别声明
**本项目只对Arcaea铺面文件进行解读，关于Arcaea铺面使用与更改的最终解释权归Arcaea版权方lowiro所有。**  
**任何通过通过本项目对游戏内铺面的改写与本项目无关，一切责任归使用者所有。**  
**本项目版权归程序编写者Begloon(321bug)所有。**

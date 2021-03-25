# rubik-color-recognition
> **魔方颜色识别**

- A simple demo for class e-me system
  > 机电控制实验项目文档

- The code is only for image processing, GUI and machanic operating parts are created by my parterner Siyi Liu using unity
  > 此程序仅进行颜色识别，操作界面以及手爪控制由小组同学刘思一利用unity完成。

- This program reads image file named "Screenshot_.png" then split nine blocks and generate a json file to give out the colors of each block by numbers in the table below.
  > 该程序从根目录中读取`Screenshot_.png`，将魔方的九个色块进行分割并对颜色进行识别，生成包含又各色块颜色数据的json文件，颜色-数字对应表在下方给出。

- This python code can only run properly in specific circumstances, or the RGB data will differ from those in train.txt.
  > 程序只能在特定环境下使用，因为在不同环境下获得的RGB数值会有所不同，与`train.txt`中的训练数据会有较大出入。

- `Ctrl+C` to kill the program, for now.
  > 目前程序第一版仅支持`Ctrl+C`退出。

- The color-number corresponding relation table is shown below.
  > 颜色-数字对应表如下：

|num|color|颜色|
|---|-----|----|
|1|blue|蓝色|
|2|green|绿色|
|3|red|红色|
|4|orange|橙色|
|5|white|白色|
|6|yellow|黄色|

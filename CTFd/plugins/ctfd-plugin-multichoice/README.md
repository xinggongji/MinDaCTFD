# ctfd-plugin-multichoice

 CTFd多选题插件

## 使用方法

1. 克隆仓库到`CTFd/CTFd/plugin`目录下
2. 在页面中创建multichoice挑战
3. 在options中输入选项，以'#'分割，例如`a#b#c#d`
4. 在Flags中创建静态flag，按照**选项顺序**设置答案，中间以`,`分割。例如`a,b,c`，`b,d`
5. 依然可以使用CTFd中的正则flag功能

## 注意

本插件仅在3.4版本以上测试过！
选择题应在`update`页面中Max Attempts设置最大答题次数，防止暴力作答！

## 使用截图

![](https://s2.loli.net/2022/03/15/k9dFRLPpBnSoJCV.png)

# ncurses<a name="ZH-CN_TOPIC_0000001106844024"></a>

- [简介](#section11660541593)
- [目录结构](#section367519246426)
- [编译构建](#section137768191623)
- [许可证](#section126611612164217)

## 简介<a name="section11660541593"></a>

ncurses是一个编写文本界面（TUI）的接口库。是一个用于控制终端屏幕输出和输入的库，可以用于创建交互式的命令行界面,它提供了一系列函数来控制终端的光标位置、颜色、文本输出等。使用 ncurses 库需要先初始化，然后使用各种函数来控制终端的输出和输入。它的主要接口和功能包括
- initscr(): 初始化curses模式，返回一个指向标准屏幕指针。
- endwin(): 退出curses模式，恢复终端的正常状态。
- addch(): 在当前光标位置添加一个字符，并更新光标位置。
- addstr()：在当前光标位置添加一个字符串，并更新光标位置。
- getch(): 从键盘获取一个字符，并返回其ASCII码或键值。
- move(): 移动光标到指定的行和列位置。
- refresh(): 将虚拟屏幕上的内容复制到物理屏幕上，并刷新显示。
- clear(): 清除虚拟屏幕上的内容，并将光标移动到左上角。


在Openharonmy引入后，在lldb构建中开启编译可选依赖选项LLDB_ENABLE_CURSES，lldb.so会依赖ncurses编译生成的动态库ncurses.so，最终实现lldb调试器命令行调试时自动补齐和gui功能。
## 目录结构<a name="section367519246426"></a>
```
- COPYING                           版权文件
- OAT.xml                           OAT.xml过滤配置文件
- README.OpenSource                 项目README.OpenSource文件
- README.md                         英文说明
- README_zh.md                      中文说明
- backport-CVE-2022-29458.patch     CVE修复补丁 
- ncurses-6.3.tar.gz                ncurses6.3源码压缩tar包
- ncurses-xxx.patch                 上游更新补丁列表
- ncurses.spec                      上游更新记录说明
- ncurses.yaml                      yaml文件
```
## 编译与安装<a name="section137768191623"></a>

### 单项目模式运行<a name="section1771013213818"></a>

```
- ./configure：用于配置软件的脚本，会根据系统环境检测和设置一些变量，生成对应的Makefile和一些头文件。其中运行configure脚本的时候指定一些参数来改变配置选项，如--prefix指定安装目录，--libdir指定库文件目录，--bindir指定可执行文件目录。
- make: 用于安装ncurses软件，根据Makefile中的规则执行一系列的操作，编译源代码，运行测试，检查外部依赖等。
- make install: 将编译好的ncurses.so文件安装到配置时指定的目录中。
```



## ncurses使用文档
官方文档  https://invisible-island.net/ncurses/ncurses.html


## 许可证<a name="section126611612164217"></a>

本项目遵从MIT许可证。

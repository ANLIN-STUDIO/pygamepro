# pygamepro
若您意于利用pygame编写各种可视化图形程序，
    但却烦恼于一些你要使用碰巧pygame没有的功能，那就来看看吧！

当pygame没有输入框，没有动画，没有视频等一系列美化图形或实用的函数时，
那就让我来为大家创建吧！

利用pygamepro，它可以使您更好的使用pygame！

## pygamepro.Font()
烦于创建文字并输出在窗口上？
那就使用"pygamepro.Font()"函数，快速创建文字！
再利用"show()"函数，它就即将可以显示在你的窗口上了！
甚至您想用一行代码来“整活”，或许"pygamepro.Font().show()"是个不错的选择！

## pygamepro.Button()
如何不用几十行代码写出一个pygame上真正的按钮？
不妨试试"pygamepro.Button()"。
您还可以将"hd()"函数放在while循环中，
    来使鼠标移动到这个按钮上，按钮就变色，
    也许别人的按钮都是这样(^_^) 。
在默认情况下，若您的(文字长度×文字大小)＞按钮宽度时，
    它会自动将按钮增宽，所以如果您不确定这个按钮上的文字有多少，
    也许将rect_size设为[0, 高度]会更加美观。

## pygamepro.window.Input_rect()
没错，就是输入框！
你还在对pygame没有输入框而感到恐惧吗？pygamepro来帮你。
继承"pygamepro.Button()"，没错，能用在按钮上的，它也能用！
单击输入框为选中状态，才可以进行输入。
单击除输入框的其他地方，就会失去焦点，则不能输入。

### 您可以在Github上找到ANLIN-3344的账户，pygamepro将持续更新！

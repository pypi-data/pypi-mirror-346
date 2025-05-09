# PythonTool使用说明

`PythonTool`依赖库：`manim`

*发现任何bug或问题，请反馈到[我的邮箱](malito:tommy1008@dingtalk.com)，谢谢！

## `ManimTool`：$\text{Manim}$相关工具

了解更多详情，请前往$\text{Manim}$官网：[manim.community](https://www.manim.community)

```renpy
ChineseMathTex(*texts, color=WHITE, font="SimSun", font_size=DEFAULT_FONT_SIZE, tex_to_color_map={})
```

创建中文数学公式，在此函数的公式部分直接写入中文即可，无需包裹`\text{}`，返回`MathTex()`。

其余用法与$\text{Manim}$原版`MathTex()`相同。

```renpy
YellowCircle(dot1, dot2)
```

创建以`dot1`为圆心，`dot1`到`dot2`的距离为半径的黄色圆，返回`Circle()`。

`dot1`和`dot2`均为$\text{Manim}$中的位置`[x,y,z]`。

```renpy
YellowLine(start, end)
```

创建以`start`开始，到`end`结束的黄色线，返回`Line()`。

用法与$\text{Manim}$原版`Line()`相同。

```renpy
LabelDot(dot_label, dot_pos, label_pos=DOWN, buff=0.1)
```

创建一个带有名字的点，返回带有点和名字的`VGroup()`。

`dot_label`：点的名字，字符串。

`dot_pos`：点的位置，$\text{Manim}$中的位置`[x,y,z]`。

`label_pos`：点的名字相对于点的位置，$\text{Manim}$中的八个方向。

`buff`：点的名字与点的间距，数值。

```renpy
MathTexLine(start, end, mathtex, color=WHITE, font_size=DEFAULT_FONT_SIZE, direction=UP, buff=0.5):
```

创建以`start`开始，到`end`结束的线，但可以标注文字、公式等，返回带有线和标注内容的`VGroup()`。

`start`和`end`用法与$\text{Manim}$原版`Line()`相同。

`mathtex`、`color`、`font_size`用法与$\text{Manim}$原版`MathTex()`相同，不过`mathtex`只能是单个字符串。

`direction`：标注内容相对于线的位置，$\text{Manim}$中的八个方向。

`buff`：标注内容与线的间距，数值。

```renpy
MathTexBrace(start, end, mathtex, color=WHITE, font_size=DEFAULT_FONT_SIZE, direction=UP, buff=0.5)
```

创建一个从`start`开始，`end`结束的大括号，并且可以在大括号上标注文字、公式等，返回带有大括号和标注内容的`VGroup()`。

用法与`MathTexLine()`相同。

```renpy
MathTexDoublearrow(start, end, mathtex, color=WHITE, font_size=DEFAULT_FONT_SIZE, direction=UP, buff=0.5)
```

创建一个从`start`开始，`end`结束的双箭头线，并且可以在双箭头上标注文字、公式等，返回带有双箭头线和标注内容的`VGroup()`。

用法与`MathTexLine()`相同。

```renpy
CircleInt(circle1, circle2)
```

寻找两个圆的两个交点并返回$\text{Manim}$位置，如果没有交点会返回`None`。

`circle1`和`circle2`均为$\text{Manim}$中的`Circle()`类型。

```renpy
LineCircleInt(line, circle)
```

寻找一条线和一个圆的一个或两个交点并返回$\text{Manim}$位置，如果没有交点会返回`None`。

`line`：$\text{Manim}$中的`Line()`类型。

`circle`：$\text{Manim}$中的`Circle()`类型。

```renpy
LineInt(line1: Line, line2: Line) -> Optional[Tuple[float, float]]
```

寻找两条线的一个交点并返回$\text{Manim}$位置，如果没有交点会返回`None`。

`line1`和`line2`均为$\text{Manim}$中的`Line()`类型。

```renpy
ExtendLine(line: Line, extend_distance: float) -> Line:_point)
```

将一条线延长`extend_distance`的距离，返回延长后的`Line()`。





`line`：$\text{Manim}$中的`Line()`类型。

`extend_distance`：要延长的距离，数值。

## `SortTool`：排序相关工具

参数`arr`为列表，`reverse=False`为升序排序，`reverse=True`为降序排序，返回排序后的列表。

```renpy
bubsort(arr, reverse=False)
```

冒泡排序。

```renpy
inssort(arr, reverse=False)
```

插入排序。

```renpy
selsort(arr, reverse=False)
```

选择排序。

```renpy
quicksort(arr, reverse=False)
```

快速排序。

```renpy
mergesort(arr, reverse=False)
```

归并排序。

```renpy
heapsort(arr, reverse=False)
```

堆排序。

```renpy
shellsort(arr, reverse=False)
```

希尔排序。

```renpy
cousort(arr, reverse=False)
```

计数排序。

```renpy
bucsort(arr, reverse=False)
```

桶排序。

```renpy
radsort(arr, reverse=False)
```

基数排序。

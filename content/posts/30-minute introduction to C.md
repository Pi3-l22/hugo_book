---
title: 30分钟入门C语言 
date: 2024-10-29
lastmod: 2024-10-29
author: Robot
avatar: https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Smilies/Robot.png
authorlink: https://blog.pi3.fun
cover: https://cdn.jsdelivr.net/gh/Pi3-l22/pico_rep/img/c.jpg
images:
  - https://cdn.jsdelivr.net/gh/Pi3-l22/pico_rep/img/cpp.jpg
categories:
  - C
tags:
  - tag1
  - tag2
# nolastmod: true
# draft: false
---

<!--more-->

### C语言 30分钟入门教程

欢迎进入C语言的世界！C语言作为编程语言之母，有着强大的表现力和丰富的应用场景。本教程将带你快速入门C语言的基础知识，并以简洁易懂的方式介绍一些常见语法、基本的代码结构和一些实用的例子。

<img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Smilies/Partying%20Face.png" alt="Partying Face" width="25" height="25" />

---

#### 1. 环境设置

1. **选择编译器**：推荐使用GCC（Linux/macOS）或MinGW（Windows）作为编译器。
2. **选择编辑器**：推荐使用VS Code、CLion等现代编辑器。
3. **编译&运行**：编写完代码后，可以通过命令行编译和运行代码：
   ```bash
   gcc hello.c -o hello   // 编译
   ./hello                // 运行
   ```

#### 2. 第一个C程序

我们从经典的 "Hello, World!" 程序开始。这是C语言中的第一个入门程序：

```c
#include <stdio.h>  // 包含标准输入输出库

int main() {
    printf("Hello, World!\n");  // 输出 "Hello, World!" 并换行
    return 0;  // 返回0表示程序成功结束
}
```

##### 解析：
- `#include <stdio.h>`：这是C语言中的标准输入输出库，用于执行输入输出操作。
- `int main()`：`main`函数是程序的入口，程序总是从这里开始执行。
- `printf()`：`printf`函数用于打印文本到屏幕。
- `return 0;`：结束`main`函数，返回0表示程序成功执行。

#### 3. 数据类型和变量

在C语言中，数据类型定义了变量能存储的数据类型。例如：
- `int`：整数类型
- `float`：单精度浮点数
- `double`：双精度浮点数
- `char`：字符类型

##### 代码示例：

```c
#include <stdio.h>

int main() {
    int age = 20;           // 整型变量
    float height = 1.75;    // 浮点型变量
    char initial = 'A';     // 字符变量

    printf("年龄：%d\n", age);
    printf("身高：%.2f\n", height);
    printf("姓名首字母：%c\n", initial);

    return 0;
}
```

##### 解析：
- `%d`、`%f`和`%c`是格式说明符，用于指定输出类型。
- `%.2f`控制输出的小数点后两位。

#### 4. 输入与输出

C语言中可以使用`scanf`函数接收用户输入。

```c
#include <stdio.h>

int main() {
    int age;
    printf("请输入你的年龄：");
    scanf("%d", &age);  // 使用 &age 传递变量地址
    printf("你的年龄是：%d\n", age);

    return 0;
}
```

##### 解析：
- `scanf`使用`&`获取变量的内存地址，以便将用户输入的值存储到变量中。

#### 5. 条件语句和循环语句

- **if-else**条件语句用于判断条件是否成立。
- **while**和**for**循环语句用于执行重复操作。

##### 代码示例：简单的猜数字游戏

```c
#include <stdio.h>
#include <stdlib.h>  // 包含随机数函数库
#include <time.h>    // 包含时间库

int main() {
    srand(time(0));  // 初始化随机数种子
    int secret = rand() % 100 + 1;  // 生成1到100之间的随机数
    int guess;

    printf("猜一个1到100之间的数字：\n");

    while (1) {
        printf("请输入你的猜测：");
        scanf("%d", &guess);

        if (guess < secret) {
            printf("太小了！\n");
        } else if (guess > secret) {
            printf("太大了！\n");
        } else {
            printf("恭喜你，猜对了！\n");
            break;  // 退出循环
        }
    }

    return 0;
}
```

##### 解析：
- `rand()`：生成一个随机数。
- `while(1)`：无限循环直到用户猜对。
- `break`：猜对时跳出循环。

#### 6. 数组

数组用于存储同一类型的一组数据。

```c
#include <stdio.h>

int main() {
    int scores[5] = {95, 88, 76, 90, 82};  // 初始化一个包含5个整数的数组

    for (int i = 0; i < 5; i++) {
        printf("成绩 %d: %d\n", i+1, scores[i]);
    }

    return 0;
}
```

##### 解析：
- 数组下标从0开始。
- 使用`for`循环逐个访问数组元素。

#### 7. 函数

函数可以将代码模块化，方便重用和组织。

##### 代码示例：实现两个数相加的函数

```c
#include <stdio.h>

int add(int a, int b) {
    return a + b;  // 返回两个整数的和
}

int main() {
    int result = add(3, 5);  // 调用add函数
    printf("3 + 5 = %d\n", result);

    return 0;
}
```

##### 解析：
- `int add(int a, int b)`：定义一个返回`int`类型的函数，接收两个参数。
- 在`main`函数中调用`add`函数并输出结果。

#### 8. 指针（简单介绍）

指针是C语言中的一种特殊数据类型，用于存储变量的地址。

```c
#include <stdio.h>

int main() {
    int num = 10;
    int *p = &num;  // 定义指针并存储num的地址

    printf("num的值为：%d\n", num);
    printf("num的地址为：%p\n", p);
    printf("通过指针访问num的值：%d\n", *p);

    return 0;
}
```

##### 解析：
- `&`符号用于获取变量地址，`*`符号用于访问指针指向的值。
- `p`是一个指向`num`的指针，通过`*p`访问`num`的值。

---

### 总结

恭喜你完成了C语言的入门课程！在30分钟内，我们了解了C语言的基本语法、数据类型、条件语句、循环、数组、函数和简单的指针概念。C语言是现代编程的基础，理解这些基础概念对进一步学习非常重要。

### 练习

1. **练习1**：创建一个小程序，计算两个浮点数的乘积。
2. **练习2**：编写一个程序，判断一个输入数字是奇数还是偶数。
3. **练习3**：扩展上面的“猜数字游戏”代码，添加猜测次数限制。

### 练习 1：计算两个浮点数的乘积

#### 代码

```c
#include <stdio.h>

int main() {
    float num1, num2, product;

    printf("请输入第一个浮点数：");
    scanf("%f", &num1);  // 输入第一个浮点数
    printf("请输入第二个浮点数：");
    scanf("%f", &num2);  // 输入第二个浮点数

    product = num1 * num2;  // 计算乘积

    printf("两个浮点数的乘积为：%.2f\n", product);  // 输出结果，保留两位小数

    return 0;
}
```

#### 解析
1. **变量声明**：声明了三个`float`类型的变量——`num1`、`num2`用于存储用户输入的浮点数，`product`用于存储计算的乘积。
2. **输入部分**：`scanf`使用`%f`格式符读取浮点数，并将用户输入的值分别存入`num1`和`num2`。
3. **计算部分**：将两个数相乘并将结果赋值给`product`。
4. **输出部分**：`printf`使用`%.2f`格式符输出结果，保留两位小数。

---

### 练习 2：判断一个数字是奇数还是偶数

#### 代码

```c
#include <stdio.h>

int main() {
    int number;

    printf("请输入一个整数：");
    scanf("%d", &number);  // 输入一个整数

    if (number % 2 == 0) {
        printf("%d 是偶数。\n", number);  // 如果能被2整除，说明是偶数
    } else {
        printf("%d 是奇数。\n", number);  // 否则就是奇数
    }

    return 0;
}
```

#### 解析
1. **输入部分**：使用`scanf`读取用户输入的整数并存储在`number`变量中。
2. **条件判断**：
   - `if (number % 2 == 0)`：使用取模操作符`%`判断`number`是否能被2整除。若条件成立，则说明`number`为偶数。
   - `else`部分：如果条件不成立，则`number`为奇数。
3. **输出结果**：根据条件判断结果输出对应的信息。

---

### 练习 3：猜数字游戏（带猜测次数限制）

#### 代码

```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    srand(time(0));  // 初始化随机数种子
    int secret = rand() % 100 + 1;  // 生成1到100之间的随机数
    int guess, attempts = 5;  // 初始化尝试次数为5次

    printf("猜一个1到100之间的数字（你有%d次机会）：\n", attempts);

    while (attempts > 0) {
        printf("请输入你的猜测：");
        scanf("%d", &guess);

        if (guess < secret) {
            printf("太小了！\n");
        } else if (guess > secret) {
            printf("太大了！\n");
        } else {
            printf("恭喜你，猜对了！\n");
            break;  // 退出循环
        }

        attempts--;  // 每猜一次，次数减1
        if (attempts > 0) {
            printf("你还有%d次机会。\n", attempts);
        } else {
            printf("很遗憾，机会用完了！正确答案是：%d\n", secret);
        }
    }

    return 0;
}
```

#### 解析
1. **随机数生成**：
   - `srand(time(0))`：初始化随机数种子，以确保每次运行时生成不同的随机数。
   - `secret = rand() % 100 + 1`：生成一个1到100之间的随机数，并存储在`secret`变量中。
2. **猜测次数控制**：
   - `attempts = 5`：将尝试次数初始化为5。
   - 每次猜测后，使用`attempts--`减少一次剩余尝试次数。
3. **循环结构**：
   - `while (attempts > 0)`：使用循环让用户反复猜测，直到猜对或尝试次数耗尽。
   - 若用户猜对（`guess == secret`），则输出成功信息并`break`退出循环。
   - 若尝试次数耗尽，则输出正确答案，并结束游戏。
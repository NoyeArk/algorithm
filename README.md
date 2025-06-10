# 机试学习

记录算法问题的学习路线，提高机试学习效率，持续提升机试代码能力。

## 1 知识点概览

![](algorithm/image/knowledge.png)

| Type | Knowledge | 
| - | ------- |
| 基础算法 | [双指针](algorithm/基础算法/双指针.md)、[差分](algorithm/基础算法/差分.md)、[滑动窗口](algorithm/基础算法/滑动窗口.md)、[二分](algorithm/基础算法/二分算法.md)、[贪心](algorithm/基础算法/贪心.md)|
| 数据结构 | [线段树](algorithm/数据结构/树形数据结构/线段树.md) 、[单调栈](algorithm/数据结构/基础数据结构/单调栈.md)、[堆](algorithm/数据结构/基础数据结构/堆.md)、[Trie树](algorithm/数据结构/树形数据结构/Trie树.md)|
| 动态规划 | [动态规划](algorithm/动态规划/README.md) |

---

## 2 数据范围分析

根据数据范围的复杂度和算法内容，ACM或笔试题的时间限制一般为1~2秒。

在这种情况下，C++代码中的操作次数控制在 $10^7~10^8$ 为最佳。下面给出在不同数据范围下，代码的时间复杂度和算法该如何选择：

| Data Range  | Time Complexity | Common Algorithm |
| -------  | --------  | -------- |
| $n≤30$   | 指数级别   | dfs+剪枝，状态压缩dp|
| $n≤10^2$  | $O(n^3)$  | floyd，dp，高斯消元|
| $n≤10^3$ | $O(n^2)$、 $O(n²logn)$ | dp，二分，朴素版Dijkstra、朴素版Prim、Bellman-Ford|
| $n≤10^4$  | $O(n∗\sqrt{n})$ | 块状链表、分块、莫队 |
| $n≤10^5$  | $O(nlogn)$ | 各种sort，线段树、树状数组、set/map、heap、拓扑排序、dijkstra+heap、prim+heap、Kruskal、spfa、求凸包、求半平面交、二分、CDQ分治、整体二分、后缀数组、树链剖分、动态树 |
| $n≤10^6$  | 常数较小的 $O(nlogn)$ | 单调队列、 hash、双指针扫描、BFS、并查集，kmp、AC自动机 |
| $n≤10^7$  | $O(n)$ | 双指针扫描、kmp、AC自动机、线性筛素数 |
| $n≤10^9$  | $O(\sqrt{n})$ | 判断质数 |
| $n≤10^{18}$  | $O(logn)$ | 最大公约数，快速幂，数位DP |
| $n≤10^{1000}$  | $O((logn)²)$ | 高精度加减乘除 |
| $n≤10^{100000}$  | $O(logk×loglogk)$ | $k$ 表示位数，高精度加减、FFT/NTT |

---

## 3 刷题记录

| ID | 平台 | 题单名称 | 状态 | 完成时间 |
|--| ---- | ------ | ----  | ------ |
|1|[Acwing](acwing/Readme.md)|[算法基础课](acwing/1-算法基础课/)| Ongoing | |
|2|[Acwing](acwing/Readme.md)|[蓝桥杯每日一题](acwing/2-蓝桥杯每日一题/)| Ongoing | |
|3|[Acwing](acwing/Readme.md)|[算法竞赛进阶指南](acwing/3-算法竞赛进阶指南/)| Ongoing | |
|5|[Leetcode](leetcode/Readme.md)|[Leetcode热题100](leetcode/2-热题100/)| Over | 2024.07.27 |
|6|[Leetcode](leetcode/Readme.md)|[动态规划（基础版）](leetcode/3-动态规划（基础版）/)| Over | 2024.10.08 |
|7|[Leetcode](leetcode/Readme.md)|[「新」动计划·编程入门](leetcode/6-「新」动计划%20·%20编程入门/)| Over | 2024.07.23 |
|8|[Leetcode](leetcode/Readme.md)|[面试经典150题](leetcode/7-面试经典%20150%20题/)| Ongoing |  |
|9|[Leetcode](leetcode/Readme.md)|[119经典题变种挑战](leetcode/8-119经典题变种挑战/)| Ongoing |  |
|10|[Leetcode](leetcode/Readme.md)|[30天Pandas挑战](leetcode/9-30%20天%20Pandas%20挑战/)| Over | 2024.11.27 |
|11|[Nowcoder](nowcoder/Readme.md)|[笔试必刷TOP101](nowcoder/笔试必刷TOP101/)| Ongoing |  |
|12|[Nowcoder](nowcoder/)|[输入输出练习](nowcoder/输入输出练习/)| Ongoing |  |
|13|[Leetcode](leetcode/Readme.md)|[高频 SQL 50 题（基础版）](leetcode/10-高频%20SQL%2050%20题（基础版）/)| Ongoing | |

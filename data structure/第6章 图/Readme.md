# 1 图的存储

图的存储结构至少要保存两类信息：	

1. 顶点的数据
2. 顶点间的关系

如何表示顶点间的关系？

## 1.1 邻接矩阵
图的邻接矩阵(Adjacency Matrix) 存储方式是用两个数组来表示图。一个一维数组存储图中顶点信息，一个二维数组(称为邻接矩阵)存储图中的边或弧的信息。

设图 G 有 n 个顶点，则邻接矩阵 A 是一个n ∗ n的方阵，定义为:

![alt text](https://img-blog.csdnimg.cn/20210301095908432.png#pic_center)

下图是一个无向图和它的邻接矩阵：

![alt text](https://img-blog.csdnimg.cn/202103011006555.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1JlYWxfRm9vbF8=,size_16,color_FFFFFF,t_70#pic_center)

可以看出：
1. 无向图的邻接矩阵一定是一个对称矩阵(即从矩阵的左上角到右下角的主对角线为轴，右上角的元与左下角相对应的元全都是相等的)。 因此，在实际存储邻接矩阵时只需存储上(或下)三角矩阵的元素。
2. 对于无向图，邻接矩阵的第i行(或第i列)非零元素(或非∞元素)的个数正好是第i个顶点的度。
3. 有向图中：
   	-  顶点 $ V_{i} $ 的出度是A中第 i 行元素之和
   	-  顶点 $ V_{i} $ 的入度是A中第 i 列元素之和

   
**邻接矩阵存储适用于稠密图。**

## 1.2 邻接表

当一个图为稀疏图时（边数相对顶点较少），使用邻接矩阵法显然要浪费大量的存储空间，如下图所示：

![alt text](https://img-blog.csdnimg.cn/20210301113238489.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1JlYWxfRm9vbF8=,size_16,color_FFFFFF,t_70#pic_center)

而图的邻接表法结合了顺序存储和链式存储方法，大大减少了这种不必要的浪费。

邻接表类似于树的孩子表示法，如果能把图中任一个顶点的所有邻接点都表示出来，也就可以表示图。

实现：为图中每个顶点建立一个单链表，第i个单链表中的结点表示依附于顶点Vi的边（有向图中指以Vi为尾的弧）。

```C++
// 图的邻接表存储
int h[N], e[N], ne[N], idx;
void add(int a, int b)
{
	e[idx] = b, ne[idx] = h[a], h[a] = idx ++;
}
```

无向图的邻接表的实例如下图所示：

![alt text](https://img-blog.csdnimg.cn/20210301165232511.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1JlYWxfRm9vbF8=,size_16,color_FFFFFF,t_70#pic_center)

### 1.2.1 邻接表表示的特点
1. 无向图中顶点Vi的度为第i个单链表中的结点数
2. 有向图中
   1. 顶点Vi的出度为第i个单链表中的结点个数
   2. 顶点Vi的入度为整个单链表中邻接点域值是i的结点个数
3. 逆邻接表：有向图中对每个结点建立以Vi为头的弧的单链表

## 1.3 十字链表

十字链表是**有向图**的一种链式存储结构。

对于有向图来说，邻接表是有缺陷的。关心了出度问题，想了解入度就必须要遍历整个图才能知道，反之，逆邻接表解决了入度却不了解出度的情况。有没有可能把邻接表与逆邻接表结合起来呢?答案是肯定的，就是把它们整合在一起。这就是我们现在要介绍的有向图的一种存储方法：十字链表(Orthogonal List)。

重新定义顶点表结点结构如下表所示。

![alt text](https://img-blog.csdnimg.cn/20210301175445875.png#pic_center)

其中 $ firstin $ 表示入边表头指针，指向该顶点的入边表中第一个结点，$ firstout $ 表示出边表头指针，指向该顶点的出边表中的第一个结点。

重新定义的边表结点结构如下表所示。

![alt text](https://img-blog.csdnimg.cn/20210301175546226.png#pic_center)

其中$tailvex$是指弧起点在顶点表的下标，$headvex$ 是指弧终点在顶点表中的下标， $ headlink $ 是指入边表指针域，指向终点相同的下一条边，$ taillink $ 是指边表指针域，指向起点相同的下一条边。如果是网，还可以再增加一个 $ weight $ 域来存储权值。

**举例如下：**

![alt text](https://img-blog.csdnimg.cn/20210301180237656.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1JlYWxfRm9vbF8=,size_16,color_FFFFFF,t_70#pic_center)

十字链表的好处就是因为把邻接表和逆邻接表整合在了一起，这样既容易找到以$ V_{i} $为尾的弧，也容易找到以$ V_{i} $为头的弧，因而容易求得顶点的出度和入度。

而且它除了结构复杂一点外，其实创建图算法的时间复杂度是和邻接表相同的，因此，在有向图的应用中，十字链表是非常好的数据结构模型。

```C++
#include<iostream>
using namespace std;

const int maxNum = 100;
typedef struct arcNode {    //弧结点类型
	int tail;				//弧尾下标
	int head;				//弧头下标
	struct arcNode*hlink;	//指针，指向同弧头的弧
	struct arcNode*tlink;	//指针，指向同弧尾的弧
}arcNode;

typedef struct vexNode
{
	char data;				//指点数据
	arcNode *firstIn;		//指针，指向第一个入弧
	arcNode *firstout;		//指针，指向第一个出弧
};

typedef struct {
	vexNode vex[maxNum];
	int vexnum, edgenum;	//顶点数量，边数量
}OLGraph;

OLGraph g;

int LocateVex(char c)
{
	for (int i = 0; i < g.vexnum; i++)
	{
		if (g.vex[i].data == c)
		{
			return i;
		}
	}
	return -1;
}

void insertedge(char a, char b)
{
	int ai = LocateVex(a);
	int bi = LocateVex(b);
	arcNode* an = new arcNode;  // 生成一条新弧
	an->tlink = g.vex[ai].firstout;		
	an->head = bi;						//由ai->bi
	an->tail = ai;
	g.vex[ai].firstout = an;			//顶点第一个出弧更新，头插入
	an->hlink = NULL;
	if (g.vex[bi].firstIn == NULL)
	{
		g.vex[bi].firstIn = an;
	}
	else 
	{
		arcNode* curArc = g.vex[bi].firstIn;		//找到最后一个入弧,尾插入
		while (curArc->hlink != NULL)
		{
			curArc = curArc->hlink;
		}
		curArc->hlink = an;
	}
}

void CreateOLGraph() {
	cout << "请输入顶点数量和边数：" << endl;
	cin >> g.vexnum >> g.edgenum;
	cout << "输入对应的顶点:" << endl;
	for (int i = 0; i < g.vexnum; i++)
	{
		cin >> g.vex[i].data;
		g.vex[i].firstIn = NULL; 
		g.vex[i].firstout = NULL;
	}
	cout << "输入要插入的边" << endl;
	int m = g.edgenum;
	while (m > 0)
	{
		char a, b;
		cin >> a >> b;
		insertedge(a, b);
		m--;
	}
}
void GetOLVexDu() {			//获得十字链表中某一个点的入度和出度
	for (int i = 0; i < g.vexnum; i++)
	{
		vexNode n = g.vex[i];
		cout << n.data << "的出度有" << " : ";
		arcNode* outArc = n.firstout;
		while (outArc != NULL)
		{
			cout << outArc->head << " ";
			outArc = outArc->tlink;
		}
		cout << endl;
		cout << n.data << "的入度有" << " : ";
		arcNode* inArc = n.firstIn;
		while (inArc != NULL)
		{
			cout << inArc->tail << " ";
			inArc = inArc->hlink;
		}
		cout << endl;
	}
}

int main()
{
	CreateOLGraph();
	GetOLVexDu();
	return 0;
}
```

## 1.4 邻接多重表

邻接多重表是**无向图**的另一种链式存储结构。

在邻接表中，容易求得顶点和边的各种信息，但在邻接表中求两个顶点之间是否存在边而对边执行删除等操作时，需要分别在两个顶点的边表中遍历，效率较低。

比如下图中，若要删除左图的（v~0~, v~2~）这条边，需要对邻接表结构中右边表的阴影两个结点进行删除操作，显然这是比较烦琐的。

![alt text](https://img-blog.csdnimg.cn/20210301182203109.png#pic_center)

重新定义的边表结点结构如下表所示。

![alt text](https://img-blog.csdnimg.cn/20210301183315496.png#pic_center)

其中 ivex 和 jvex 是与某条边依附的两个顶点在顶点表中下标。ilink 指向依附顶点 ivex 的下一条边，jlink 指向依附顶点 jvex 的下一条边。这就是邻接多重表结构。

每个顶点也用一一个结点表示，它由如下所示的两个域组成。

![alt text](https://img-blog.csdnimg.cn/20210301183423578.png#pic_center)

其中，data 域存储该顶点的相关信息，firstedge 域指示第一条依附于该顶点的边。

**举例如下：**

![alt text](https://img-blog.csdnimg.cn/20210301185220315.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1JlYWxfRm9vbF8=,size_16,color_FFFFFF,t_70#pic_center)

---
# 2 图的遍历
图的遍历（Traversing Graph）：从图中某一个顶点出发，访问图中的其余顶点，且使每个顶点仅被访问一次。

主要有深度优先搜索和广度优先搜索，它们对无向图和有向图都适用。
- 深度优先搜索类似于树的先根遍历
- 广度优先搜索类似于树的层次遍历

## 2.1 DFS
从图的某一顶点$V_{0}$出发，访问此顶点；然后依次从$V_{0}$的未被访问的邻接点出发，深度优先遍历图，直至图中所有和$V_{0}$相通的顶点都被访问到；

若此时图中尚有顶点未被访问，则另选图中一个未被访问的顶点作起点，重复上述过程，直至图中所有顶点都被访问为止。

### 2.1.1 DFS代码模板

```C++
bool st[N];
void dfs(int u)
{
    st[u] = true;  // st[u] 表示点u已经被遍历过

    for (int i = h[u]; i != -1; i = ne[i])
    {
        int j = e[i];
        if (!st[j]) dfs(j);
    }
}
```

![alt text](https://img-blog.csdnimg.cn/20210302110631863.png#pic_center)

- 对于同一个图，基于邻接矩阵的遍历得到的DFS序列和BFS序列是唯一的
- 基于邻接表遍历所得到的DFS序列和BFS序列是不唯一的

###　2.1.2 性能分析
- **空间复杂度**：递归算法，需要使用递归栈，空间复杂度为O(V)，V为顶点数
- **时间复杂度**：遍历过程实际上是查找每个点的临界点的过程
	- 邻接矩阵：查找每个顶点的邻接点需要时间为O(|V|)，总时间复杂度为O(|V²|)
	- 邻接表：查找每个顶点的邻接点需要时间为O(|E|)，总时间复杂度为O(|V|+|E|)

## 2.2 BFS

从图的某一顶点$V_{0}$出发，访问此顶点后，依次访问$V_{0}$的各个未曾访问过的邻接点；然后分别从这些邻接点出发，广度优先遍历图，直至图中所有已被访问的顶点的邻接点都被访问到；

若此时图中尚有顶点未被访问，则另选图中一个未被访问的顶点作起点，重复上述过程，直至图中所有顶点都被访问为止。

### 2.2.1 BFS代码模板

```C++
void bfs()
{
	queue<int> q;
	st[1] = true;  // 表示1号点已经被遍历过
	q.push(1);

	while (q.size())
	{
		int t = q.front();
		q.pop();

		for (int i = h[t]; i != -1; i = ne[i])
		{
			int j = e[i];
			if (!st[j])
			{
				st[j] = true;  // 表示点j已经被遍历过
				q.push(j);
			}
		}
	}
}
```

![alt text](https://hackr.io/blog/media/architecture-of-bfs.png)

###　2.2.1 性能分析
- **空间复杂度**：无论使用什么存储方式，BFS都需要借助一个辅助队列Q，因此最坏情况下，空间复杂度为O(|V|)
- **时间复杂度**：分析同DFS
  - 邻接矩阵：O(|V|²)
  - 邻接表：O(|V|+|E|)
---

# 3 最小生成树
**生成树**：所有顶点均由边连接在一起，但不存在回路的图。

一个图可以有许多棵不同的生成树，所有生成树具有以下共同特点：

1. 生成树的顶点个数与图的顶点个数相同
2. 生成树是图的极小连通子图
3. 一个有n个顶点的连通图的生成树有n-1条边
4. 生成树中任意两个顶点间的路径是唯一的
5. 在生成树中再加一条边必然形成回路

含n个顶点n-1条边的图不一定是生成树。

## 3.1 普利姆（Prim）算法

### 3.1.1 算法思想

- 初始令$U=\{u_{0}\}，(u_{0}∈V), TE=ɸ$；
- 在所有u∈U，v∈V-U的边(u,v)∈E中，找一条代价最小的边($u_{0}$，$v_{0}$)；
- 将($u_{0}$，$v_{0}$)并入集合TE，同时$v_{0}$并入U；
- 重复上述操作直至U=V为止，则T=(V,{TE})为N的最小生成树；

### 3.1.2 算法过程

![alt text](https://img-blog.csdnimg.cn/3e8389add71f4f4f8ff01d977bda755d.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ0Njg1NTg0,size_16,color_FFFFFF,t_70)

### 3.1.3 代码实现
```C++
#include <iostream>
#include <cstring>
using namespace std;

const int N = 510;
int n, m;
int dist[N];
int g[N][N];
bool st[N];

int prim()
{
	memset(dist, 0x3f, sizeof dist);
	dist[1] = 0;
	int res = 0;
	for (int i = 1; i <= n; i ++)
	{
		int t = -1;
		for (int j = 1; j <= n; j ++)
			if (!st[j] && (t == -1 || dist[t] > dist[j]))
				t = j;
		st[t] = true;
		res += dist[t];
		// 这个一定要加，防止溢出
		if (res > 0x3f3f3f3f / 2) return 0x3f3f3f3f;
		for (int j = 1; j <= n; j ++)
			dist[j] = min(dist[j], g[t][j]);
	}
	return res;
}

int main()
{
	memset(g, 0x3f, sizeof g);
	cin >> n >> m;
	while (m --)
	{
		int a, b, c; cin >> a >> b >> c;
		g[a][b] = g[b][a] = min(g[a][b], c);
	}
	int ans = prim();
	if (ans > 0x3f3f3f3f / 2) cout << "impossible";
	else cout << ans;
	return 0;
}
```

### 3.1.4 性能分析

- **空间复杂度**：使用一个dist数组用于记录距离，O(|V|)
- **时间复杂度**：两重循环，O(|V|²)，不依赖于E，**适合求解边稠密图的最小生成树**

## 3.2 克鲁斯卡尔（Kruskal）算法

### 3.2.1 算法思想

按边权选择合适的边来构造最小生成树。

- 初始状态为只有n个顶点而无边的非连通图T=(V,{ɸ})，每个顶点自成一个连通分量；
- 在E中选取代价最小的边，若该边依附的顶点落在T中不同的连通分量上，则将此边加入到T中；否则，舍去此边，选取下一条代价最小的边依此类推，直至T中所有顶点都在同一连通分量上为止；

### 3.2.2 算法过程

![alt text](https://img-blog.csdnimg.cn/2020052116522528.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQ2NDIzMTY2,size_16,color_FFFFFF,t_70)

### 3.2.3 代码实现

```C++
#include <iostream>
#include <algorithm>
using namespace std;

const int N = 200010;
struct Edge
{
	int a, b, w;
}edges[N];
int n, m;
int pre[N];

bool cmp(Edge& x, Edge& y)
{
	return x.w < y.w;
}

int find(int x)
{
	return pre[x] = (pre[x] == x ? x : find(pre[x]));
}

int Kruskal()
{
	int res = 0, cnt = 0;
	for (int i = 1; i <= m; i ++)
	{
		auto e = edges[i];
		int a = find(e.a), b = find(e.b);

		if (a == b) continue;
		pre[a] = b;
		res += e.w, cnt ++;
	}
	return cnt < n - 1 ? 0x3f3f3f3f : res;
}

int main()
{
	cin >> n >> m;
	// 初始化并查集
	for (int i = 1; i <= n; i ++) pre[i] = i;

	for (int i = 1; i <= m; i ++) 
		cin >> edges[i].a >> edges[i].b >> edges[i].w;

	sort(edges + 1, edges + 1 + m, cmp);

	int ans = Kruskal();
	if (ans == 0x3f3f3f3f) cout << "impossible";
	else cout << ans;

	return 0;
}
```

### 3.2.4 性能分析

- **空间复杂度**：使用一个dist数组用于记录距离，O(|V|)
- **时间复杂度**：通常采用堆来存放边的集合，选择边权最小的边需要O(log|E|)的时间，同时遍历每条边，时间复杂度为O(|E|log|E|)，**适用于求解边稀疏而顶点较多的图**

### 3.2.5 具体应用

- n个城市间建立通信联络网

---
# 4 最短路径

带权有向图G的最短路径问题一般可分为两类：

1. 单源最短路
2. 每对顶点间的最短路径

## 4.1 Dijkstra算法

解决单源最短路径问题的一个常用算法是Dijkstra算法，它是由E.W\.Dijkstra提出的一种按路径长度递增的次序产生到各顶点最短路径的贪心算法。

### 4.1.1 算法思想

首先，在这些最短路径中，长度最短的这条路径上必定只有一条弧，且它的权值是从源点出发的所有弧上权的最小值。

其次，第二条长度次短的最短路径只可能有两种情况：

1. 或者只含一条从源点出发的弧且小于其它从源点出发的弧上的权值；&#x20;

2. 或者是一条只经过已求得最短路径的顶点的路径。

依次类推，按迪杰斯特拉算法先后求得的每一条最短路径必定只有两种情况，或者是由源点直接到达终点，或者是只经过已经求得最短路径的顶点到达终点。

### 4.1.2 求最短路径步骤&#xD;

1. 初始化：令 S={V0}，T={其余顶点}，dist\[]的初始值$dist[i]=arcs[0][i], i=1,2,...,n-1$。
2. 从顶点集合V-S中选出$v_{j}$，满足$dist[j]= \min \{dist[i]|vi\in V-S\}$，$v_{j}$就是当前求得的一条从$v_{0}$出发的最短路径的终点，令$S=S\bigcup{j}$。
3. 对T中顶点的距离值进行修改：若加进W作中间顶点，从V0到Vi的距离值比不加W的路径要短，则修改此距离值。
4. 重复上述步骤，直到S中包含所有顶点，即S=V为止。

![](img/image_SD_1cEKC7Q.png)

### 4.1.3 代码实现

```c++
#include <iostream>
#include <cstring>
using namespace std;

// 稠密图，采用邻接矩阵存储
const int N = 510;
int n, m;
int g[N][N], dist[N];
bool st[N];

int dijkstra()
{
    memset(dist, 0x3f, sizeof dist);
    dist[1] = 0;
    for (int i = 1; i <= n; i ++)
    {
        int t = -1;
        for (int j = 1; j <= n; j ++)
            if (!st[j] && (t == -1 || dist[t] > dist[j])) 
                t = j;
        st[t] = true;
        // 更新到其他点的距离
        for (int j = 1; j <= n; j ++)
            dist[j] = min(dist[j], dist[t] + g[t][j]);
    }
    return dist[n] == 0x3f3f3f3f ? -1 : dist[n];
}

int main()
{
    cin >> n >> m;
    memset(g, 0x3f, sizeof g);
    while (m --)
    {
        int a, b, c; cin >> a >> b >> c;
        g[a][b] = min(g[a][b], c);
    }
    cout << dijkstra();
    return 0;
}
```

### 4.1.4 性能分析

- **时间复杂度**：O(n²)
- **空间复杂度**：O(n)

Dijkstra算法是基于贪心策略，当边上带有负值时，该算法并不适用，会进入死循环。

## 4.2 Floyd算法

如何求每一对顶点之间的最短路径？

1. 每次以一个顶点为源点，重复执行Dijkstra算法n次：T(n)=O(n³)。

2. 弗洛伊德(Floyd)算法


**算法思想**：逐个顶点试探法。

### 4.2.1 求最短路径步骤&#xA;

1. 初始时设置一个n阶方阵，令其对角线元素为0，若存在弧\<Vi,Vj>，则对应元素为权值；否则为∞。
2. 逐步试着在原直接路径中增加中间顶点，若加入中间点后路径变短，则修改之；否则维持原值。
3. 所有顶点试探完毕，算法结束。

![](img/image_MH2j8EZWlF.png)

![](img/image_Wjqn9qnUvo.png)

### 4.2.2 代码实现

```c++
#include <iostream>
#include <cstring>
using namespace std;

const int N = 210;
int dist[N][N];
int n, m, q;

void floyd()
{
    for (int k = 1; k <= n; k ++)
        for (int i = 1; i <= n; i ++)
            for (int j = 1; j <= n; j ++)
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]);
}

int main()
{
    cin >> n >> m >> q;
    
    for (int i = 1; i <= n; i ++)
        for (int j = 1; j <= n; j ++)
            if (i == j) dist[i][j] = 0;
            else dist[i][j] = 0x3f3f3f3f;

    while (m --)
    {
        int a, b, c; cin >> a >> b >> c;
        dist[a][b] = min(dist[a][b], c);
    }
    floyd();
    while (q --)
    {
        int x, y; cin >> x >> y;
        if (dist[x][y] > 0x3f3f3f3f / 2) cout << "impossible" << endl;
        else cout << dist[x][y] << endl;
    }
    return 0;
}
```

### 4.2.3 性能分析

- **时间复杂度**：O(n³)，不过由于其代码很紧凑，且不包含其他复杂的数据结构，因此隐含的常数系数是很小的。
- **空间复杂度**：O(n²)

Floyd算法允许图中有带负权值的边，但不允许有包含带负权值的边组成的回路。

---
# 5 拓扑排序

**AOV网**：用顶点表示活动，用弧表示活动间优先关系的有向图称为顶点表示活动的网（Activity On Vertex network），简称AOV网。
- 若<$v_{i}$, $v_{j}$>是图中有向边，则$v_{i}$是$v_{j}$的直接前驱；$v_{j}$是$v_{i}$的直接后继
- AOV网中不允许有回路，这意味着某项活动以自己为先决条件

**拓扑排序**：把AOV网络中各顶点按照它们相互之间的优先关系排列成一个线性序列的过程叫拓扑排序。

## 5.1 算法思想

- 在有向图中选一个没有前驱的顶点且输出之；
- 从图中删除该顶点和所有以它为尾的弧；
- 重复上述两步，直至全部顶点均已输出；或者当图中不存在无前驱的顶点为止。

## 5.2 算法过程

![alt text](https://pica.zhimg.com/v2-def95e93dd0e7eba3144c688c550e612_1440w.jpg?source=172ae18b)

## 5.3 代码实现

```C++
#include <iostream>
#include <cstring>
using namespace std;

const int N = 100010;
int n, m;
int d[N];
int q[N], hh, tt = -1;
int h[N], e[N], ne[N], idx;

bool top_sort()
{
	for (int i = 1; i <= n; i ++)
		if (!d[i]) q[++ tt] = i;
	while (hh <= tt)
	{
		int t = q[hh ++];
		for (int i = h[t]; i != -1; i = ne[i])
		{
			int j = e[i];
			if (-- d[j] == 0)
				q[++ tt] = j;
		}
	}
	return tt == n - 1;
}

int main()
{
	memset(h, -1, sizeof h);
	cin >> n >> m;
	while (m --)
	{
		int a, b; cin >> a >> b;
		d[b] ++;
		e[idx] = b, ne[idx] = h[a], h[a] = idx ++;
	}

	if (top_sort())
		for (int i = 0; i <= tt; i ++)	cout << q[i] << " ";
	else cout << -1;
	return 0;
}
```

## 5.4 性能分析

- **空间复杂度**：使用一个辅助队列Q，O(|V|)
- **时间复杂度**：从队列中取出每个点的同时还要遍历从它出发的边，所以时间复杂度为O(|V|+|E|)

## 5.5 逆拓扑排序

与上述拓扑排序过程相反，先输出出度为0的点，然后删除所有以该顶点为终点的有向边，直到当前AVO网为空。

### 5.5.1 具体应用

- 学生选修课程问题

---
# 6 关键路径

**AOE网（Activity On Edge）**：边表示活动的网。AOE网是一个带权的有向无环图，其中顶点表示事件，弧表示活动，权表示活动持续时间。
- 在AOE网中仅有一个入度为0的顶点，称为**开始结点（源点）**，表示整个工程的开始；
- 仅存在一个出度为0的顶点，称为**结束顶点（汇点）**，表示整个工程的结束；

**路径长度**：路径上各活动持续时间之和。

**关键路径**：路径长度最长的路径。

完成整个工程的最短时间就是关键路径的长度，即关键路径上各活动花费开销的总和。因为关键活动影响整个工程的时间，因此只要找到关键活动，就找到了关键路径。

## 6.1 相关变量

### 6.1.1 $V_{e}$：事件$V_{j}$的最早发生时间$V_{e}(j)$

源点的最早发生时间为0，其余任一顶点$V_{j}$的最早发生时间，等于从源点出发沿着各条路径达到$V_{j}$时每条路径上权的累加和的最大值。

$$
	Ve(j) = \max (Ve(i) + Weight(<i ,j>))
$$

### 6.1.2 $V_{l}$：事件$V_{j}$的最迟发生时间$V_{l}(j)$

汇点的最迟发生时间$V_{l}[n]$等于汇点的最早发生时间$V_{e}[n]$。其余任一顶点$V_{i}$的最迟发生时间等于从汇点的最迟发生时间中减去从顶点$V_{i}$出发沿着各条路径达到汇点时，每条路径上权的累加和的最大值。

$$
	V_l(i) = \min \{V_l(j) - Weight(<i ,j>)\}
$$

在计算$V_{l}(k)$时，按从后向前的顺序进行，可以在逆拓扑排序的基础上计算。

### 6.1.3 $e_{i}$：活动$a_{i}$的最早开始时间

即该事件的起点的最早发生时间。

### 6.1.4 $l_{i}$：活动$a_{i}$的最迟开始时间

该活动弧的终点所表示的事件的最迟发生事件与该活动所需事件之差。

### 6.1.5 时间余量

时间余量是指一个活动的最迟开始时间和最早开始时间的差额。其中余量为0的活动为关键活动。

## 6.2 算法思想

求关键路径的算法步骤如下：

1. 从源点出发，令ve(源点) = 0，按拓扑有序求其余顶点的最早发生时间ve()。
2. 从汇点出发，令vl(汇点) = ve(汇点)，按逆拓扑有序求其余顶点的最迟发生时间vl()。
3. 根据各顶点的ve()值求所有弧的最早开始时间e()。
4. 根据各顶点的vl()值求所有弧的最早开始时间l()。
5. 求AOE网中所有活动的差额d()，找出所有d() = 0的活动构成关键路径。

### 6.2.1 注意

- **关键路径上的所有活动都是关键活动，可以通过加快关键活动来缩短整个工程的工期**，但是不能任意缩短关键活动，因为缩短到一定程度，该关键活动就可能变成非关键活动。
- **网中的关键路径并不唯一**。对于含有多条关键路径的网中，只有加快那些包括在所有关键路径上的关键活动才能达到缩短工期的目的。

## 6.3 算法过程

![alt text](https://img-blog.csdnimg.cn/20200610180344442.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NjA3Mjc3MQ==,size_16,color_FFFFFF,t_70)

## 6.4 代码实现

```C++
#include <iostream>
#include <cstring>
using namespace std;

const int N = 100010;
int n, m;
int h[N], inverse_h[N], e[N], ne[N], w[N], idx;

int in_d[N], out_d[N];
int q[N], hh, tt = -1;

void add(int list[], int a, int b, int c)
{
	e[idx] = b, ne[idx] = list[a], w[idx] = c, list[a] = idx ++;
}

int ve[N];  // 顶点的最早发生时间
// 按照拓扑排序求解所有顶点的最早发生时间
void top_sort()
{
	hh = 0, tt = -1;
	for (int i = 1; i <= n; i ++)
		if (!in_d[i]) q[++ tt] = i;
	while (hh <= tt)
	{
		auto t = q[hh ++];
		for (int i = h[t]; i != -1; i = ne[i])
		{
			int j = e[i];
			ve[j] = max(ve[j], ve[t] + w[i]);
			if (-- in_d[j] == 0) q[++ tt] = j;
		}
	}
	for (int i = 1; i <= n; i ++)
		printf("ver:%d ve:%d\n", i, ve[i]);
}

int vl[N];  // 求顶点的最迟发生时间
void inverse_top()
{
	memset(vl, 0x3f, sizeof vl);
	hh = 0, tt = -1;
	for (int i = 1; i <= n; i ++)
		if (!out_d[i]) q[++ tt] = i;
	vl[q[hh]] = ve[q[hh]];
	while (hh <= tt)
	{
		auto t = q[hh ++];
		for (int i = inverse_h[t]; i != -1; i = ne[i])
		{
			int j = e[i];
			vl[j] = min(vl[j], vl[t] - w[i]);
			if (-- out_d[j] == 0) q[++ tt] = j;
		}
	}
	for (int i = 1; i <= n; i ++)
		printf("ver:%d vl:%d\n", i, vl[i]);
}

int ee[N];  // 得到每个边的最早开始时间
void get_e()
{
	hh = 0, tt = -1;
	q[++ tt] = 1;
	while (hh <= tt)
	{
		auto t = q[hh ++];
		for (int i = h[t]; i != -1; i = ne[i])
			ee[i] = ve[t];
	}
	for (int i = 1; i <= n; i ++)
		printf("ver:%d vl:%d\n", i, vl[i]);
}

int main()
{
	memset(h, -1, sizeof h);
	memset(inverse_h, -1, sizeof inverse_h);
	cin >> n >> m;
	while (m --)
	{
		int a, b, c; cin >> a >> b >> c;
		add(h, a, b, c); add(inverse_h, b, a, c);
		out_d[a] ++, in_d[b] ++;
	}

	top_sort();
	cout << "--------" << endl;
	inverse_top();
	cout << "--------" << endl;
	get_e();

	return 0;
}
```
<!-- ![alt text] -->
/**
 * @file 单调栈.cpp
 * @author horiki
 * @version 0.1
 * @date 2024-05-03
 * @copyright Copyright (c) 2024
 * 
 * @brief 
 * 
 */

#include <iostream>
using namespace std;

const int N = 100010;
int stk[N], tt;

int main()
{
    int n; cin >> n;
    for (int i = 1; i <= n; i ++)
    {
        int x; cin >> x;
        while (tt && stk[tt] >= x) tt --;
        if (tt) cout << stk[tt] << " ";
        else cout << -1 << " ";
        stk[++ tt] = x;
    }

    return 0;
}
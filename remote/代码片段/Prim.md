
```c++
#include<iostream>
#include<vector>
#include <climits>
 
using namespace std;
int main() {
    int v, e;
    int x, y, k;
    cin >> v >> e;
    // 填一个默认最大值，题目描述val最大为10000
    vector<vector<int>> grid(v + 1, vector<int>(v + 1, 10001));
    while (e--) {
        cin >> x >> y >> k;
        // 因为是双向图，所以两个方向都要填上
        grid[x][y] = k;
        grid[y][x] = k;
 
    }
     
    // 所有节点到最小生成树的最小距离
    vector<int> minDist(v + 1, 10001);
 
    // 这个节点是否在树里
    vector<bool> isInTree(v + 1, false);
     
    for(int i = 1 ; i < v ; i++){
        int cur = -1;
        int minVal = INT_MAX;
         
        // 最小的节点
        for(int j = 1; j <= v ; j++){
            if(!isInTree[j] && minDist[j] < minVal){
                cur = j;
                minVal = minDist[j];
            }
        }
         
        isInTree[cur] = true;
         
        for(int j = 1 ; j <= v; j++){
            if(!isInTree[j] && grid[cur][j] < minDist[j]){
                minDist[j] = grid[cur][j];
            }
        }
         
         
    }
     
    int result = 0;
    for (int i = 2; i <= v; i++) { // 不计第一个顶点，因为统计的是边的权值，v个节点有 v-1条边
        result += minDist[i];
    }
    cout << result << endl;
     
     
}
```
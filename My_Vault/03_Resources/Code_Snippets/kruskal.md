```c++
#include<iostream>
#include<vector>
#include <climits>
#include <algorithm>

using namespace std;

struct Edge{
    int l,r,val;
};

int n = 10001;
vector<int> father(n, -1);

void init(){
    for(int i= 0 ;i < n ; i++){
        father[i] = i;
    }
}

int find(int u){
    return u == father[u] ? u : father[u] = find(father[u]); 
}

void uni(int x, int y){
    int father_x = find(x);
    int father_y = find(y);
    
    if(father_x == father_y) return;
    father[father_x] = father_y;
}




int main() {
    int v, e;
    int x, y, k;
    cin >> v >> e;
    
    vector<Edge> edges;
    int result = 0;
    while (e--) {
        cin >> x >> y >>k;
        edges.push_back({x,y,k});
    }
    
    sort(edges.begin(), edges.end(), [](const Edge& x, const Edge &y){
        return x.val < y.val;
    });
    
    init();
    
    for(Edge edge : edges){
        int father_left = find(edge.l);
        int father_right = find(edge.r);
        
        if(father_right == father_left) continue;
        
        result += edge.val;
        uni(father_left, father_right);
    }
    
    cout << result << endl;
    return 0;
    
    
}
```
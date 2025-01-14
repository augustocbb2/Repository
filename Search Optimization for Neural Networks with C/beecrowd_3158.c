/* 
Author: Augusto Bastos
Master's Class: Project and Analysis of Algorithms
Date: 5/14/23, 9:23:52 PM

1. Problem Description:
Livrolândia is a country that values reading. In this city, there is a universal rule: every city in the country must have access to libraries. All presidents who passed through Livrolândia managed to maintain this rule.

Roci is the current president and made a point of maintaining all libraries in the country, as well as the good quality of roads between cities so that cities without libraries can gain access to neighboring cities that do.

Unfortunately, Roci is very unlucky, and early in his tenure, a tornado destroyed all libraries and obstructed all roads in Livroland. Now, the president will have to come up with a plan to rebuild the country, following his universal rule and at the lowest possible cost for the works.

Livrolândia has N cities numbered 1 to N. The cities are connected by M two-way roads. A city has access to a library if:

- The city itself has a library.
- It is possible to travel from this city to a city that contains a library.

The cost to repair a road is E tolkiens (tolkiens is the currency of Livroland), and the cost to build a library is B tolkiens.

Given the map of Livrolândia and the costs of repair and construction, write a program that returns the minimum cost to rebuild the country, following the universal rule, and thus save Roci.

2. Input:
The first line of the input contains an integer T indicating the number of possible maps.
The second line of the input contains 4 integers: N, M, B, and E, representing the number of cities, the number of roads, the cost to build a library, and the cost to build a road, respectively.
Then there are M lines indicating the blocked roads, each of which has two integers X and Y, indicating that there is a road that connects city X to city Y.

Limits:
1 <= T <= 10
1 <= N <= 10^5
0 <= M <= min(10^5, (N * (N-1)) / 2)
1 <= B, E <= 10^5
1 <= X, Y <= N

3. Output:
For each possible map, indicate the minimum cost to rebuild the country.

Code Description:

The code solves the problem of rebuilding the country of Livrolândia after a disaster. It determines the minimum cost required to rebuild the country while following the rule that every city must have access to a library.

The minCost function calculates the minimum cost by using a breadth-first search (BFS) algorithm. It traverses the graph representing the cities and roads and checks the number of libraries needed and the cost of repairing roads. If the cost of building a library is less than or equal to the cost of repairing a road, then it is more cost-effective to build a library in each city. Otherwise, it uses BFS to visit a limited number of neighboring cities from each city, simulating the construction of roads between cities. The cost is calculated based on the number of components (connected groups of cities) and the cost of repairing roads.

The solve function reads the input, constructs the graph, and calls the minCost function for each possible map. It outputs the minimum cost to rebuild the country.

Overall, the code efficiently solves the problem by considering the cost trade-offs between building libraries and repairing roads, and by using BFS to determine the minimum cost.
*/

#include <iostream>
#include <vector>
#include <queue>
#include <cmath>
using namespace std;

long long int min(long long int a, long long int b) {
    return a < b ? a : b;
}

long long int minCost(long long int n, long long int m, long long int b, long long int e, vector<vector<long long int>>& graph) {
    if (b <= e) {
        return n * b;
    }
    queue<long long int> q;
    vector<bool> visited(n + 1, false);
    long long int cost = 0;
    long long int components = 0;
    for (long long int i = 1; i <= n; i++) {
        if (visited[i]) {
            continue;
        }
        visited[i] = true;
        components++;
        q.push(i);
        while (!q.empty()) {
            long long int u = q.front();
            q.pop();
            
            // Visit up to ceil(b/e) nodes from u
            long long int limit = min(b, graph[u].size());
            for (long long int v : graph[u]) {
                if (!visited[v] && limit > 0) {
                    visited[v] = true;
                    q.push(v);
                    cost += e;
                    limit--;
                }
            }
        }
    }
    cost += b * components;
    return cost;
}

void solve() {
    long long int T;
    cin >> T;
    while (T--) {
        long long int N, M, B, E;
        cin >> N >> M >> B >> E;
        vector<vector<long long int>> graph(N + 1);
        for (long long int i = 0; i < M; i++) {
            long long int X, Y;
            cin >> X >> Y;
            graph[X].push_back(Y);
            graph[Y].push_back(X);
        }
        cout << minCost(N, M, B, E, graph) << endl;
    }
}

int main() {
    solve();
}

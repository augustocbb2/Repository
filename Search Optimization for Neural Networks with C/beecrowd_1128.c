/* 
Author: Augusto Bastos
Master's Class: Project and Analysis of Algorithms
Date: 5/1/23, 12:45:27 PM

Problem:
1. Description:
In a certain city, there are N intersections connected by one-way and two-way streets. It is a modern city, and several of the streets have tunnels or overpasses. Evidently, it must be possible to travel between any two intersections. More precisely, given two intersections V and W, it must be possible to travel from V to W and from W to V.

Your task is to write a program that reads a description of the city street system and determines whether the requirement of connectedness is satisfied or not.

2. Input:
The input contains several test cases. The first line of a test case contains two integers N and M, separated by a space, indicating the number of intersections (2 ≤ N ≤ 2000) and the number of streets (2 ≤ M ≤ N(N−1)/2). The next M lines describe the city street system, with each line describing one street. A street description consists of three integers V, W, and P, separated by a blank space, where V and W are distinct identifiers for intersections (1 ≤ V, W ≤ N, V ≠ W), and P can be 1 or 2. If P = 1, the street is one-way, and traffic goes from V to W. If P = 2, then the street is two-way and links V and W. A pair of intersections is connected by at most one street.

The last test case is followed by a line that contains only two zero numbers separated by a blank space.

3. Output:
For each test case, your program should print a single line containing an integer G, where G is equal to one if the condition of connectedness is satisfied, and G is zero otherwise.

Solution Description:
This code solves the problem of determining whether a given city's street system satisfies the requirement of connectedness. It takes as input a description of the city's street system, consisting of the number of intersections, the number of streets, and the details of each street (intersections, whether it is a one-way or two-way street).

The code uses a depth-first search (DFS) algorithm to check if all intersections can be reached from any other intersection. It initializes an adjacency matrix g to represent the connectivity between intersections. The dfs function performs a DFS traversal starting from a given intersection and marks visited intersections in the vis array.

The main function reads the input test cases, constructs the adjacency matrix, and then performs the DFS traversal for each intersection. If any intersection is not visited during the DFS traversal, it sets the flag variable to true, indicating that the requirement of connectedness is not satisfied. Otherwise, if all intersections are visited, the flag remains false, indicating that the connectedness condition is satisfied.

Finally, the code prints the output, where 0 is printed if the condition of connectedness is not satisfied, and 1 is printed if the condition is satisfied.


*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define true 1
#define false 0
#define MAXSIZE 2000

int vis[MAXSIZE];
int g[MAXSIZE][MAXSIZE];

int n;
void dfs(int);


void dfs(int u)
{
    int i;
    vis[u] = true;

    for (i = 1; i <= n; ++i)
        if (g[u][i])
            if (!vis[i])
                dfs(i);
}


int main(int argc, char **argv)
{
    int m, u, v, p, i, j;

    while (scanf("%d %d", &n, &m), m && n)
    {
        memset(g, 0, sizeof(g));
        
        for (i = 0; i < m; ++i)
        {
            scanf("%d %d %d", &u, &v, &p);
            if (p == 1)
                g[u][v] = true;
            else
                g[u][v] = g[v][u] = true;
        }   

        int flag = false;
        for (i = 1; i <= n; ++i)
        {
            memset(vis, 0, sizeof(vis));
            dfs(i);
            flag = false;
            for (j = 1; j < n && !flag; ++j)
                if (!vis[j])
                    flag = true;
            if (flag)
                break;
        }

        printf("%d\n", flag ? 0 : 1);
    }

    return 0;
}

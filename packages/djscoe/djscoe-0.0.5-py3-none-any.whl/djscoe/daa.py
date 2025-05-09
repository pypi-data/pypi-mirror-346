insertion_sort = '''
#include <stdio.h>
#include <time.h>
#include <stdlib.h> 

void insertionSort(int arr[], int n) {
    int i, key, j;
    for (i = 1; i < n; i++) {
        key = arr[i];
        j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = key;
    }
}

void printArray(int arr[], int size) {
    int i;
    for (i = 0; i < size; i++)
        printf("%d ", arr[i]);
    printf("\\n");
}

int main() {
    int arr[100000], n, i;
    int choice;
    printf("Enter the number of elements: ");
    scanf("%d", &n);

    printf("Choices  : ");
    printf("\\n(1). Best Case : ");
    printf("\\n(2). Average Case : ");
    printf("\\n(3). Worst Case : ");

    printf("\\nEnter Choice : ");
    scanf("%d", &choice);

    switch(choice){
        case 1 :  
            printf("\\nBest Case");
            for (i = 0; i < n; i++)
                arr[i] =  i;
            break;
        case 2 :
            printf("\\nAverage Case");
            for (i = 0; i < n; i++)
                arr[i] = rand();
            break;
        case 3 :
            printf("\\nWorst Case");
            for (i = n; i >= 0 ; i--)
                arr[n - i] =  i;
            break;
        default:
            break;
    }

    clock_t pre_sort_seconds;
     
    pre_sort_seconds = clock();

    insertionSort(arr, n);

    clock_t post_sort_seconds;
     
    post_sort_seconds = clock();

    clock_t timetaken = post_sort_seconds-pre_sort_seconds;
    printf("\\nTime Taken %ld",timetaken);

    return 0;
}

'''

selection_sort = '''
#include<stdio.h>
#include<conio.h>
#include <time.h>
#include <stdlib.h>
 
void printArray(int a[], int n){
    int i;
    for(i = 0; i < n; i++){
        printf("%d ", a[i]);
    }
    printf("\\n");
}

void selectionSort(int a[], int n){
    int i, j, minIndex, temp;
    for(i = 0; i < n-1; i++){
        minIndex = i;
        for(j = i+1; j < n; j++){
            if(a[j] < a[minIndex]){
                minIndex = j;
            }
        }
        temp = a[i];
        a[i] = a[minIndex];
        a[minIndex] = temp;
    }
}

int main()
{
    int arr[100000], n, i;
    int choice;
    printf("Enter the number of elements: ");
    scanf("%d", &n);

    printf("Choices  : ");
    printf("\\n(1). Best Case : ");
    printf("\\n(2). Average Case : ");
    printf("\\n(3). Worst Case : ");

    printf("\\nEnter Choice : ");
    scanf("%d", &choice);

    switch(choice){
        case 1 :  
            printf("\\nBest Case");
            for (i = 0; i < n; i++)
                arr[i] =  i;
            break;
        case 2 :
            printf("\\nAverage Case");
            for (i = 0; i < n; i++)
                arr[i] = rand();
            break;
        case 3 :
            printf("\\nWorst Case");
            for (i = n; i >= 0 ; i--)
                arr[n - i] =  i;
            break;
        default:
            break;
    }

    clock_t pre_sort_seconds;
     
    pre_sort_seconds = clock();

    selectionSort(arr, n);

    clock_t post_sort_seconds;
     
    post_sort_seconds = clock();

    clock_t timetaken = post_sort_seconds-pre_sort_seconds;
    printf("\\nTime Taken %ld",timetaken);

    return 0;
}
'''

merge_sort = '''
#include <stdio.h>
#include <conio.h>
#include <time.h>
#include <stdlib.h>

void merge(int arr[], int l, int m, int r) {
    int i, j, k;
    int n1 = m - l + 1;
    int n2 = r - m;

    int L[n1], R[n2];

    for (i = 0; i < n1; i++)
        L[i] = arr[l + i];
    for (j = 0; j < n2; j++)
        R[j] = arr[m + 1 + j];

    i = 0;
    j = 0;
    k = l;

    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        } else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }

    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }

    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }
}

void mergeSort(int arr[], int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;

        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);

        merge(arr, l, m, r);
    }
}

void printArray(int A[], int size) {
    int i;
    for (i = 0; i < size; i++)
        printf("%d ", A[i]);
    printf("\\n");
}

int main() {
    int arr[100000], n, i;
    int choice;
    printf("Enter the number of elements: ");
    scanf("%d", &n);

    printf("Choices  : ");
    printf("\\n(1). Best Case : ");
    printf("\\n(2). Average Case : ");
    printf("\\n(3). Worst Case : ");

    printf("\\nEnter Choice : ");
    scanf("%d", &choice);

    switch(choice){
        case 1 :  
            printf("\\nBest Case");
            for (i = 0; i < n; i++)
                arr[i] =  i;
            break;
        case 2 :
            printf("\\nAverage Case");
            for (i = 0; i < n; i++)
                arr[i] = rand();
            break;
        case 3 :
            printf("\\nWorst Case");
            for (i = n; i >= 0 ; i--)
                arr[n - i] =  i;
            break;
        default:
            break;
    }

    clock_t pre_sort_seconds;
     
    pre_sort_seconds = clock();

    mergeSort(arr, 0, n - 1);

    clock_t post_sort_seconds;
     
    post_sort_seconds = clock();

    clock_t timetaken = post_sort_seconds-pre_sort_seconds;
    printf("\\nTime Taken %ld",timetaken);

    return 0;

    
}

'''

quick_sort = '''
#include<stdio.h>
#include<conio.h>
#include <time.h>
#include <stdlib.h>
 
void printArray(int arr[], int size) {
    for (int i = 0; i < size; i++)
        printf("%d ", arr[i]);
    printf("\\n");
}

void swap(int* a, int* b) {
    int t = *a;
    *a = *b;
    *b = t;
}

int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = (low - 1);

    for (int j = low; j <= high - 1; j++) {
        if (arr[j] < pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[high]);
    return (i + 1);
}

void quickSort(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);

        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

int main()
{
    int arr[100000], n, i;
    int choice;
    printf("Enter the number of elements: ");
    scanf("%d", &n);

    printf("Choices  : ");
    printf("\\n(1). Best Case : ");
    printf("\\n(2). Average Case : ");
    printf("\\n(3). Worst Case : ");

    printf("\\nEnter Choice : ");
    scanf("%d", &choice);

    switch(choice){
        case 1 :  
            printf("\\nBest Case");
            for (i = 0; i < n; i++)
                arr[i] =  i;
            break;
        case 2 :
            printf("\\nAverage Case");
            for (i = 0; i < n; i++)
                arr[i] = rand();
            break;
        case 3 :
            printf("\\nWorst Case");
            for (i = n; i >= 0 ; i--)
                arr[n - i] =  i;
            break;
        default:
            break;
    }

    clock_t pre_sort_seconds;
     
    pre_sort_seconds = clock();

    quickSort(arr, 0, n - 1);

    clock_t post_sort_seconds;
     
    post_sort_seconds = clock();

    clock_t timetaken = post_sort_seconds-pre_sort_seconds;
    printf("\\nTime Taken %ld",timetaken);

    return 0;
}
'''

binary_search = '''
#include <stdio.h>
#include <conio.h>

int binarySearch(int arr[], int n, int data) {
    int left = 0;
    int right = n - 1;

    while (left <= right) {
        int mid = left + (right - left) / 2;

        if (arr[mid] == data) {
            return mid; 
        } else if (arr[mid] < data) {
            left = mid + 1; 
        } else {
            right = mid - 1; 
        }
    }

    return -1; 
}

int main() {
    int arr[10], n, i, data;

    printf("Enter the number of elements: ");
    scanf("%d", &n);

    printf("Enter the elements (in ascending order):\\n");
    for (i = 0; i < n; i++)
        scanf("%d", &arr[i]);

    printf("Enter the element to be searched: ");
    scanf("%d", &data);

    int result = binarySearch(arr, n, data);

    if (result != -1)
        printf("%d found at position %d\\n", data, result + 1);
    else
        printf("%d not found\\n", data);

    return 0;
}

'''

min_max = '''
#include<stdio.h>
#include<stdlib.h>

int a[100], min, max;

void MinMax(int low, int high) {
	int mid, min1, max1;
	if (low == high) {
		max = min = a[low];
	}
	else if (low == high - 1) {
		if (a[low] < a[high]) {
			min = a[low];
			max = a[high];
		}
		else {
			min = a[high];
			max = a[low];
		}
	}
	else {
		mid = (low + high) / 2;
		MinMax(low, mid);
		min1 = min;
		max1 = max;
		MinMax(mid + 1, high);
		if (max1 > max)
			max = max1;
		if (min1 < min)
			min = min1;
	}
}

int main() {
	int i;
    int n;
    printf("Enter the number of elements: ");
    scanf("%d", &n);
	for (i = 0; i < n; i++)
    {
        printf("Enter element %d : ", i + 1);
		scanf("%d", &a[i]);
    }    
	MinMax(0, n - 1);
	printf("Min: %d, Max: %d", min, max);
	return 0;
}
'''

prims='''
#include <stdio.h>
#include <conio.h>
#include <limits.h>

#define NODES 9
#define INF INT_MAX

int mst[NODES];
int adj[NODES][NODES] = {

	{0, 4, 0, 0, 0, 0, 0, 8, 0},
	{4, 0, 8, 0, 0, 0, 0, 11, 0},
	{0, 8, 0, 7, 0, 4, 0, 0, 2},
	{0, 0, 7, 0, 9, 14, 0, 0, 0},
	{0, 0, 0, 9, 0, 10, 0, 0, 0},
	{0, 0, 4, 14, 10, 0, 2, 0, 0},
	{0, 0, 0, 0, 0, 2, 0, 1, 6},
	{8, 11, 0, 0, 0, 0, 1, 0, 7},
	{0, 0, 2, 0, 0, 0, 6, 7, 0}
};

struct Vertices {
	int dist;
	int parent;
	int visited;
} V[NODES];

struct Graph {
	char nodes[NODES];
	int adjMatrix[NODES][NODES];
} G;

int extractMin() {
	int min = INF;
	int minIndex = -1;
	for (int i = 0; i < NODES; i++) {
		if (!V[i].visited && V[i].dist < min) {
			min = V[i].dist;
			minIndex = i;
		}
	}
	return minIndex;
}


void Prims(int start) {
	for (int i = 0; i < NODES; i++) {
		V[i].dist = INF;
		V[i].parent = -1;
		V[i].visited = 0;
	}
	V[start].dist = 0;
	for (int i = 0; i < NODES; i++) {
		int u = extractMin();
		V[u].visited = 1;
		for (int v = 0; v < NODES; v++) {
			if (G.adjMatrix[u][v] && !V[v].visited && V[v].dist > G.adjMatrix[u][v]) {
				V[v].parent = u;
				V[v].dist = G.adjMatrix[u][v];
			}
		}
	}
	for (int i = 0; i < NODES; i++) {
		mst[i] = V[i].parent;
	}
}

int main() {
	int totalCost = 0;
	for (int i = 0; i < NODES; i++) {
		for (int j = 0; j < NODES; j++) {
			G.adjMatrix[i][j] = adj[i][j];
		}
	}
	for (int i = 0; i < NODES; i++) {
		G.nodes[i] = 'a' + i;
	}
	Prims(0);
	printf("Minimum Spanning Tree: \\n");
	for (int i = 0; i < NODES; i++) {
		if (mst[i] != -1) {
			printf("%c - %c: %d\\n", G.nodes[mst[i]], G.nodes[i], G.adjMatrix[i][mst[i]]);
			totalCost += G.adjMatrix[i][mst[i]];
		}
	}
	printf("Total Cost: %d\\n", totalCost);
	return 0;
}
'''

kruskal='''
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

#define NODES 9
#define INF INT_MAX

int adj[NODES][NODES] = {

	{0, 4, 0, 0, 0, 0, 0, 8, 0},
	{4, 0, 8, 0, 0, 0, 0, 11, 0},
	{0, 8, 0, 7, 0, 4, 0, 0, 2},
	{0, 0, 7, 0, 9, 14, 0, 0, 0},
	{0, 0, 0, 9, 0, 10, 0, 0, 0},
	{0, 0, 4, 14, 10, 0, 2, 0, 0},
	{0, 0, 0, 0, 0, 2, 0, 1, 6},
	{8, 11, 0, 0, 0, 0, 1, 0, 7},
	{0, 0, 2, 0, 0, 0, 6, 7, 0}
};

struct Edge {
    int src, dest, weight;
};

int parent[NODES];

int find(int i) {
    while (parent[i] != i)
        i = parent[i];
    return i;
}

void unionOp(int i, int j) {
    int a = find(i);
    int b = find(j);
    parent[a] = b;
}

int compare(const void *a, const void *b) {
    struct Edge* edge1 = (struct Edge*)a;
    struct Edge* edge2 = (struct Edge*)b;
    return edge1->weight - edge2->weight;
}

void Kruskal(struct Edge edges[], int totalEdges) {
    int edgeCount = 0;
    int totalCost = 0;

    qsort(edges, totalEdges, sizeof(struct Edge), compare);

    for (int i = 0; i < NODES; i++)
        parent[i] = i;

    printf("Minimum Spanning Tree: \\n");

    for (int i = 0; i < totalEdges; i++) {
        int src = edges[i].src;
        int dest = edges[i].dest;
        int srcParent = find(src);
        int destParent = find(dest);

        if (srcParent != destParent) {
            printf("%c - %c: %d\\n", 'a' + src, 'a' + dest, edges[i].weight);
            totalCost += edges[i].weight;
            unionOp(srcParent, destParent);
            edgeCount++;
        }

        if (edgeCount == NODES - 1)
            break;
    }

    printf("Total Cost: %d\\n", totalCost);
}

int main() {
    struct Edge edges[NODES * NODES];
    int edgeIndex = 0;

    for (int i = 0; i < NODES; i++) {
        for (int j = i + 1; j < NODES; j++) {
            if (adj[i][j] != 0) {
                edges[edgeIndex].src = i;
                edges[edgeIndex].dest = j;
                edges[edgeIndex].weight = adj[i][j];
                edgeIndex++;
            }
        }
    }
    Kruskal(edges, edgeIndex);
    return 0;
}

'''

dijkstra = '''
#include <stdio.h>
#include <limits.h>

#define NODES 9
#define INF INT_MAX

int adj[NODES][NODES] = {
    //a, b, c, d, e, f, g, h, i
    { 0, 4, 0, 0, 0, 0, 0, 8, 0 },
    { 4, 0, 8, 0, 0, 0, 0, 11, 0 },
    { 0, 8, 0, 7, 0, 4, 0, 0, 2 },
    { 0, 0, 7, 0, 9, 14, 0, 0, 0 },
    { 0, 0, 0, 9, 0, 10, 0, 0, 0 },
    { 0, 0, 4, 14, 10, 0, 2, 0, 0 },
    { 0, 0, 0, 0, 0, 2, 0, 1, 6 },
    { 8, 11, 0, 0, 0, 0, 1, 0, 7 },
    { 0, 0, 2, 0, 0, 0, 6, 7, 0 },
};

struct Graph {
    char vertices[NODES];
    int adj[NODES][NODES];
} G;

struct Vertex {
    int dist;
    int par;
    int visited;
} V[NODES];


void InitializeSingleSource(int start) {
    int i;
    for (i = 0; i < NODES; i++) {
        V[i].dist = INF;
        V[i].par = -1;
        V[i].visited = 0;
    }
    V[start].dist = 0;
}

int extractMin() {
    int i, min = INF, minIndex = -1;
    for (i = 0; i < NODES; i++) {
        if (!V[i].visited && V[i].dist < min) {
            min = V[i].dist;
            minIndex = i;
        }
    }
    return minIndex;
}

void relax(int u, int v) {
    if (V[v].dist > V[u].dist + G.adj[u][v]) {
        V[v].dist = V[u].dist + G.adj[u][v];
        V[v].par = u;
    }
}

void Djikstra(struct Graph G, int start) {
    int i, u, v;
    InitializeSingleSource(start);
    for (i = 0; i < NODES; i++) {
        u = extractMin();
        V[u].visited = 1;
        for (v = 0; v < NODES; v++) {
            if (!V[v].visited && G.adj[u][v])
                relax(u, v);
        }
    }
    for (i = 0; i < NODES; i++)
        if (V[i].par != -1) {
            printf("%c - %c: %d\\n", G.vertices[start], G.vertices[i], V[i].dist);
        }
}

int main() {
    int i, j;
    for (i = 0; i < NODES; i++)
        for (j = 0; j < NODES; j++)
            G.adj[i][j] = adj[i][j];
    for (i = 0; i < NODES; i++)
        G.vertices[i] = 'A' + i;
    Djikstra(G, 0);
    return 0;
}
'''

floyd_warshall = '''
#include <stdio.h>

#define V 4

#define INF 99999


void floydWarshall(int graph[V][V]) {
    int dist[V][V];
    int i, j, k;

    for (i = 0; i < V; i++) {
        for (j = 0; j < V; j++) {
            dist[i][j] = graph[i][j];
        }
    }

    for (k = 0; k < V; k++) {
        for (i = 0; i < V; i++) {
            for (j = 0; j < V; j++) {
                if (dist[i][k] + dist[k][j] < dist[i][j]){
                    dist[i][j] = dist[i][k] + dist[k][j];
                }
            }
        }
    }

    printf("Shortest distances between every pair of vertices:\\n");
    for (i = 0; i < V; i++) {
        for (j = 0; j < V; j++) {
            if (dist[i][j] == INF)
                printf("%7s", "INF");
            else
                printf("%7d", dist[i][j]);
        }
        printf("\\n");
    }
}

int main() {
    int graph[V][V] = {
        {0, 5, INF, 10},
        {INF, 0, 3, INF},
        {INF, INF, 0, 1},
        {INF, INF, INF, 0}
    };
    floydWarshall(graph);
    return 0;
}

'''

activity_selection = '''
#include <stdio.h>
#include <stdlib.h>

struct Activity {
    int start, finish;
};

int compare(const void *a, const void *b) {
    return ((struct Activity *)a)->finish - ((struct Activity *)b)->finish;
}

void printMaxActivities(struct Activity activities[], int n) {
    qsort(activities, n, sizeof(struct Activity), compare);

    printf("The following activities are selected:\\n");

    int i = 0;
    printf("(%d, %d) ", activities[i].start, activities[i].finish);

    for (int j = 1; j < n; j++) {
        if (activities[j].start >= activities[i].finish) {
            printf("(%d, %d) ", activities[j].start, activities[j].finish);
            i = j;
        }
    }
}

int main() {
    struct Activity activities[] = {{1, 4}, {3, 5}, {0, 6}, {5, 7}, {3, 8}, {5, 9}, {6, 10}, {8, 11}, {8, 12}, {2, 13}, {12, 14}};
    int n = sizeof(activities) / sizeof(activities[0]);
    printMaxActivities(activities, n);
    return 0;
}

'''

bellman_ford = '''
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

#define MAX_VERTICES 100
#define MAX_EDGES 100

struct Edge {
    int source, destination, weight;
};

void BellmanFord(int graph[MAX_EDGES][3], int vertices, int edges, int source) {
    int distance[MAX_VERTICES];
    for (int i = 0; i < vertices; i++)
        distance[i] = INT_MAX;
    distance[source] = 0;
    for (int i = 0; i < vertices - 1; i++) {
        for (int j = 0; j < edges; j++) {
            int u = graph[j][0];
            int v = graph[j][1];
            int weight = graph[j][2];
            if (distance[u] != INT_MAX && distance[u] + weight < distance[v])
                distance[v] = distance[u] + weight;
        }
    }
    for (int i = 0; i < edges; i++) {
        int u = graph[i][0];
        int v = graph[i][1];
        int weight = graph[i][2];
        if (distance[u] != INT_MAX && distance[u] + weight < distance[v]) {
            printf("Graph contains negative weight cycle\\n");
            return;
        }
    }
    printf("Vertex   Distance from Source\\n");
    for (int i = 0; i < vertices; ++i)
        printf("%d \\t\\t %d\\n", i, distance[i]);
}

int main() {
    int vertices = 5; 
    int edges = 8; 
    int graph[MAX_EDGES][3] = {
        {0, 1, -1}, {0, 2, 4}, {1, 2, 3}, {1, 3, 2},
        {1, 4, 2}, {3, 2, 5}, {3, 1, 1}, {4, 3, -3}
    };
    int source = 0; 

    BellmanFord(graph, vertices, edges, source);

    return 0;
}

'''

matrix_chain_multiplication = '''
#include <stdio.h>

#define N 3 

void multiply(int A[][N], int B[][N], int C[][N])
{
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            C[i][j] = 0;
            for (int k = 0; k < N; k++)
            {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

int main()
{
    int A[N][N] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}}; 
    int B[N][N] = {{9, 8, 7}, {6, 5, 4}, {3, 2, 1}}; 
    int C[N][N]; 

    multiply(A, B, C);

    printf("Resultant Matrix C:\\n");
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            printf("%d ", C[i][j]);
        }
        printf("\\n");
    }
    return 0;
}
'''

longest_common_subsequence='''
#include <stdio.h>
#include <string.h>
void longest_common_subsequence_algorithm();
void print_sequence(int a, int b);
int a, b, c, d;
int temp[30][30];
char first_sequence[30], second_sequence[30], longest_sequence[30][30];
int main()
{
    printf("\\nEnter the First String : ");
    scanf("%s", first_sequence);
    printf("\\nEnter the Second String : ");
    scanf("%s", second_sequence);
    printf("\\nLongest Common Subsequence : ");
    longest_common_subsequence_algorithm();
    print_sequence(c, d);
    printf("\\n");
    return 0;
}
void longest_common_subsequence_algorithm()
{
    c = strlen(first_sequence);
    d = strlen(second_sequence);
    for (a = 0; a <= c; a++)
    {
        temp[a][0] = 0;
    }
    for (a = 0; a <= d; a++)
    {
        temp[0][a] = 0;
    }
    for (a = 1; a <= c; a++)
    {
        for (b = 1; b <= d; b++)
        {
            if (first_sequence[a - 1] == second_sequence[b - 1])
            {
                temp[a][b] = temp[a - 1][b - 1] + 1;
                longest_sequence[a][b] = 'c';
            }
            else if (temp[a - 1][b] >= temp[a][b - 1])
            {
                temp[a][b] = temp[a - 1][b];
                longest_sequence[a][b] = 'u';
            }
            else
            {
                temp[a][b] = temp[a][b - 1];
                longest_sequence[a][b] = 'l';
            }
        }
    }
}
void print_sequence(int a, int b)
{
    if (a == 0 || b == 0)
    {
        return;
    }
    if (longest_sequence[a][b] == 'c')
    {
        print_sequence(a - 1, b - 1);
        printf("%c", first_sequence[a - 1]);
    }
    else if (longest_sequence[a][b] == 'u')
    {
        print_sequence(a - 1, b);
    }
    else
    {
        print_sequence(a, b - 1);
    }
}
'''

knapsack = '''
#include<stdio.h>

int max(int a, int b) {
    return (a > b) ? a : b;
}

int knapsack(int W, int wt[], int val[], int n) {
    int i, w;
    int K[n + 1][W + 1];
    for (i = 0; i <= n; i++) {
        for (w = 0; w <= W; w++) {
            if (i == 0 || w == 0)
                K[i][w] = 0;
            else if (wt[i - 1] <= w)
                K[i][w] = max(val[i - 1] + K[i - 1][w - wt[i - 1]], K[i - 1][w]);
            else
                K[i][w] = K[i - 1][w];
        }
    }
    return K[n][W];
}

int main() {
    int val[] = {60, 100, 120};
    int wt[] = {10, 20, 30};
    int W = 50;
    int n = sizeof(val) / sizeof(val[0]);
    printf("Maximum value: %d\\n", knapsack(W, wt, val, n));
    return 0;
}

'''

fractional_knapsack = '''
#include <stdio.h>
#include <stdlib.h>

struct Item {
    int value;
    int weight;
};

int compare(const void *a, const void *b) {
    double ratio1 = (double)((struct Item *)a)->value / ((struct Item *)a)->weight;
    double ratio2 = (double)((struct Item *)b)->value / ((struct Item *)b)->weight;
    return ratio2 > ratio1 ? 1 : -1;
}

double fractionalKnapsack(int capacity, struct Item items[], int n) {
    qsort(items, n, sizeof(struct Item), compare);
    double totalValue = 0.0; 
    int currentWeight = 0;  
    for (int i = 0; i < n; i++) {
        if (currentWeight + items[i].weight <= capacity) {
            totalValue += items[i].value;
            currentWeight += items[i].weight;
        } else {
            int remainingWeight = capacity - currentWeight;
            totalValue += (double)items[i].value / items[i].weight * remainingWeight;
            break; 
        }
    }
    return totalValue;
}

int main() {
    int capacity = 50;
    struct Item items[] = {{60, 10}, {100, 20}, {120, 30}};
    int n = sizeof(items) / sizeof(items[0]);

    double maxValue = fractionalKnapsack(capacity, items, n);
    printf("Maximum value in knapsack = %.2f\\n", maxValue);

    return 0;
}

'''

n_queens = '''
#include<stdio.h>
#include<stdbool.h>
#include<math.h>

#define N 20

int board[N][N];
int count = 0;

void printSolution(int n);
bool isSafe(int row, int col, int n);
bool solveNQueensUtil(int col, int n);
bool solveNQueens(int n);

int main() {
    int n;
    printf("Enter number of Queens : ");
    scanf("%d", &n);
    if (solveNQueens(n))
        printf("\\nTotal solutions: %d\\n", count);
    else
        printf("\\nNo solution exists for %d queens.\\n", n);
    return 0;
}

void printSolution(int n) {
    int i, j;
    printf("\\n\\nSolution : %d\\n\\n", ++count);
    for (i = 0; i < n; ++i) {
        for (j = 0; j < n; ++j) {
            if (board[i][j] == 1)
                printf("Q ");
            else
                printf(". ");
        }
        printf("\\n");
    }
}

bool isSafe(int row, int col, int n) {
    int i, j;
    for (i = 0; i < col; i++) {
        if (board[row][i])
            return false;
    }
    for (i = row, j = col; i >= 0 && j >= 0; i--, j--) {
        if (board[i][j])
            return false;
    }
    for (i = row, j = col; j >= 0 && i < n; i++, j--) {
        if (board[i][j])
            return false;
    }
    return true;
}

bool solveNQueensUtil(int col, int n) {
    if (col == n) {
        printSolution(n);
        return true;
    }
    bool res = false;
    for (int i = 0; i < n; i++) {
        if (isSafe(i, col, n)) {
            board[i][col] = 1;
            res = solveNQueensUtil(col + 1, n) || res;
            board[i][col] = 0;
        }
    }
    return res;
}

bool solveNQueens(int n) {
    if (n <= 0 || n > N) {
        printf("Invalid input.\\n");
        return false;
    }
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            board[i][j] = 0;
        }
    }
    return solveNQueensUtil(0, n);
}
'''

sum_of_subset = '''
#include <stdio.h>
#define MAX 100
int n, m;
int arr[MAX];
int x[MAX];
void sumOfSubsets(int k, int s, int r)
{
    int i;
    x[k] = 1;
    if (s + arr[k] == m)
    {
        for (i = 0; i < n; i++)
        {
            printf("%d ", x[i]);
        }
        printf("\\n");
    }
    else if (s + arr[k] + arr[k + 1] <= m)
    {
        sumOfSubsets(k + 1, s + arr[k], r - arr[k]);
    }
    if (s + arr[k + 1] <= m && s + r - arr[k] >= m)
    {
        x[k] = 0;
        sumOfSubsets(k + 1, s, r - arr[k]);
    }
}
int main()
{
    int i, t;
    t = 0;
    printf("Number of elements : ");
    scanf("%d", &n);
    printf("Enter the elements : ");
    for (i = 0; i < n; i++)
    {
        scanf("%d", &arr[i]);
        t += arr[i];
        x[i] = 0;
    }
    printf("Sum : ");
    scanf("%d", &m);
    sumOfSubsets(0, 0, t);
}
'''

graph_coloring = '''
#include <stdio.h>
#include <conio.h>
static int m, n;
static int c = 0;
static int count = 0;
int g[50][50];
int x[50];

void nextValue(int k)
{
    int j;
    while (1)
    {
        x[k] = (x[k] + 1) % (m + 1);
        if (x[k] == 0)
        {
            return;
        }
        for (j = 1; j <= n; j++)
        {
            if (g[k][j] == 1 && x[k] == x[j])
                break;
        }
        if (j == (n + 1))
        {
            return;
        }
    }
}

void GraphColoring(int k)
{
    int i;
    while (1)
    {
        nextValue(k);
        if (x[k] == 0)
        {
            return;
        }

        if (k == n)
        {
            c = 1;
            for (i = 1; i <= n; i++)
            {
                printf("%d ", x[i]);
            }
            count++;
            printf("\\n");
        }
        else
            GraphColoring(k + 1);
    }
}

int main()
{
    int i, j;
    printf("\\nEnter the number of nodes: ");
    scanf("%d", &n);
    printf("\\nEnter Adjacency Matrix:\\n");
    for (i = 1; i <= n; i++)
    {
        for (j = 1; j <= n; j++)
        {
            scanf("%d", &g[i][j]);
        }
    }
    printf("\\nPossible Solutions are\\n");
    for (m = 1; m <= n; m++)
    {
        if (c == 1)
        {
            break;
        }
        GraphColoring(1);
    }
    printf("\\nThe chromatic number is %d", m - 1);
    printf("\\nThe total number of solutions is %d", count);
}
'''

rabin_karp = '''
#include <stdio.h>
#include <string.h>

#define d 256

void search(char pat[], char txt[], int q) {
    int M = strlen(pat);
    int N = strlen(txt);
    int i, j;
    int p = 0; 
    int t = 0; 
    int h = 1;

    for (i = 0; i < M - 1; i++)
        h = (h * d) % q;

    for (i = 0; i < M; i++) {
        p = (d * p + pat[i]) % q;
        t = (d * t + txt[i]) % q;
    }

    for (i = 0; i <= N - M; i++) {
        if (p == t) {
            for (j = 0; j < M; j++) {
                if (txt[i + j] != pat[j])
                    break;
            }
            if (j == M)
                printf("Pattern found at index %d \\n", i);
        }
        if (i < N - M) {
            t = (d * (t - txt[i] * h) + txt[i + M]) % q;
            if (t < 0)
                t = (t + q);
        }
    }
}

int main() {
    char txt[100], pat[100];
    int q;

    printf("Enter the text: ");
    scanf("%s", txt);

    printf("Enter the pattern: ");
    scanf("%s", pat);

    printf("Enter a prime number: ");
    scanf("%d", &q);

    search(pat, txt, q);
    return 0;
}
'''

kmp = '''
#include <stdio.h>
#include <string.h>

void prefixSuffixArray(char *pat, int M, int *pps) {
    int length = 0;
    pps[0] = 0;
    int i = 1;
    while (i < M) {
        if (pat[i] == pat[length]) {
            length++;
            pps[i] = length;
            i++;
        }
        else {
            if (length != 0)
                length = pps[length - 1];
            else {
                pps[i] = 0;
                i++;
            }
        }
    }
}

void KMPAlgorithm(char *text, char *pattern) {
    int M = strlen(pattern);
    int N = strlen(text);
    int pps[M];
    prefixSuffixArray(pattern, M, pps);
    int i = 0;
    int j = 0;
    int flag = 0;
    while (i < N) {
        if (pattern[j] == text[i]) {
            j++;
            i++;
        }
        if (j == M) {
            flag = 1;
            printf("Found pattern at index %d\\n", i - j);
            j = pps[j - 1];
        }
        else if (i < N && pattern[j] != text[i]) {
            if (j != 0)
                j = pps[j - 1];
            else
                i = i + 1;
        }
    }
    if (flag == 0){
        printf("Pattern not found\\n");
    }
}

int main() {
    char text[100], pattern[100];
    
    printf("Enter the text: ");
    scanf("%s", text);

    printf("Enter the pattern: ");
    scanf("%s", pattern);

    KMPAlgorithm(text, pattern);
    return 0;
}
'''

strassens = '''
#include<stdio.h>

int a[2][2],b[2][2],c[2][2];


void strassen() {
    int s1, s2, s3, s4, s5, s6, s7, s8, s9, s10;
    s1 = b[0][1] - b[1][1];
    s2 = a[0][0] + a[0][1];
    s3 = a[1][0] + a[1][1];
    s4 = b[1][0] + b[0][0];
    s5 = a[0][0] + a[1][1];
    s6 = b[0][0] + b[1][1];
    s7 = a[0][1] - a[1][1];
    s8 = b[1][0] + b[1][1];
    s9 = a[0][0] - a[1][0];
    s10 = b[0][0] + b[0][1];
    
    int p1, p2, p3, p4, p5, p6, p7;
    p1 = s1 * a[0][0];
    p2 = s2 * b[1][1];
    p3 = s3 * b[0][0];
    p4 = s4 * a[1][1];
    p5 = s5 * s6;
    p6 = s7 * s8;
    p7 = s9 * s10;

    c[0][0] = p5 + p4 - p2 + p6;
    c[0][1] = p1 + p2;
    c[1][0] = p3 + p4;
    c[1][1] = p5 + p1 - p3 - p7;
}


int main() {
    int n;
    printf("Enter no of rows in each matrix for n*n matrices:");
    scanf("%d", &n);
    printf("Enter elements for first matrix:");
    for(int i = 0; i < n; i++) {
        for(int j = 0; j < n; j++) {
            printf("i=%d j=%d:",i,j);
            scanf("%d", &a[i][j]);
        }
    }
    printf("Enter elements for 2nd matrix:");
    for(int i = 0; i < n; i++) {
        for(int j = 0; j < n; j++) {
            printf("i=%d j=%d:",i,j);
            scanf("%d", &b[i][j]);
        }
    }

    strassen();

    for(int i = 0; i < 2; i++) {
        for(int j = 0; j < 2; j++) {
            printf("%d ", c[i][j]);
        }
        printf("\\n");
    }
    
    return 0;
}
'''
kasturba = '''
#include <iostream>
#include <string>
using namespace std;
int makeEqualLength(string &str1, string &str2) {
    int len1 = str1.size();
    int len2 = str2.size();
    if (len1 < len2) str1.insert(0, len2 - len1, '0');
    else if (len2 < len1) str2.insert(0, len1 - len2, '0');
    return max(len1, len2);
}
string addStrings(string a, string b) {
    string result;
    int carry = 0;
    for (int i = a.size() - 1; i >= 0; i--) {
        int sum = (a[i] - '0') + (b[i] - '0') + carry;
        result = char(sum % 10 + '0') + result;
        carry = sum / 10;
    }
    if (carry) result = char(carry + '0') + result;
    return result;
}
int multiplySingleDigits(char a, char b) {
    return (a - '0') * (b - '0');
}
string multiplyKaratsuba(string X, string Y) {
    int n = makeEqualLength(X, Y);
    if (n == 0) return "0";
    if (n == 1) return to_string(multiplySingleDigits(X[0], Y[0]));
    int fh = n / 2;
    int sh = n - fh;
    string Xl = X.substr(0, fh);
    string Xr = X.substr(fh);
    string Yl = Y.substr(0, fh);
    string Yr = Y.substr(fh);
    string P1 = multiplyKaratsuba(Xl, Yl);
    string P2 = multiplyKaratsuba(Xr, Yr);
    string P3 = multiplyKaratsuba(addStrings(Xl, Xr), addStrings(Yl, Yr));
    int numZeros = 2 * sh;
    string result = addStrings(P1 + string(numZeros, '0'), addStrings(P3 + string(sh, '0'), P2));
    return result;
}
int main() {
    string X, Y;
    cin >> X >> Y;
    cout << multiplyKaratsuba(X, Y);
    return 0;
}

'''

activity_selection = '''
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
bool compare(pair<int, int> a, pair<int, int> b) {
    return a.second < b.second;
}
int main() {
    int n;
    cin >> n;
    vector<pair<int, int>> activities(n);
    for (int i = 0; i < n; i++) cin >> activities[i].first >> activities[i].second;
    sort(activities.begin(), activities.end(), compare);
    int count = 1, last = activities[0].second;
    for (int i = 1; i < n; i++) {
        if (activities[i].first >= last) {
            count++;
            last = activities[i].second;
        }
    }
    cout << count;
    return 0;
}

'''

job_seq_deadline_greedy = '''
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
struct Job {
    int id, deadline, profit;
};
bool cmp(Job a, Job b) {
    return a.profit > b.profit;
}
int main() {
    int n;
    cin >> n;
    vector<Job> jobs(n);
    for (int i = 0; i < n; i++) cin >> jobs[i].id >> jobs[i].deadline >> jobs[i].profit;
    sort(jobs.begin(), jobs.end(), cmp);
    int max_deadline = 0;
    for (int i = 0; i < n; i++) max_deadline = max(max_deadline, jobs[i].deadline);
    vector<int> slot(max_deadline + 1, -1);
    int count = 0, profit = 0;
    for (int i = 0; i < n; i++) {
        for (int j = jobs[i].deadline; j > 0; j--) {
            if (slot[j] == -1) {
                slot[j] = jobs[i].id;
                profit += jobs[i].profit;
                count++;
                break;
            }
        }
    }
    cout << profit;
    return 0;
}

'''

huffman_tree = '''
#include <iostream>
#include <queue>
using namespace std;
struct Node {
    char data;
    int freq;
    Node *left, *right;
    Node(char d, int f) : data(d), freq(f), left(NULL), right(NULL) {}
};
struct compare {
    bool operator()(Node* l, Node* r) {
        return l->freq > r->freq;
    }
};
void printCodes(Node* root, string str) {
    if (!root) return;
    if (root->data != '$') cout << root->data << ": " << str << endl;
    printCodes(root->left, str + "0");
    printCodes(root->right, str + "1");
}
int main() {
    int n;
    cin >> n;
    char ch;
    int freq;
    priority_queue<Node*, vector<Node*>, compare> minHeap;
    for (int i = 0; i < n; i++) {
        cin >> ch >> freq;
        minHeap.push(new Node(ch, freq));
    }
    while (minHeap.size() > 1) {
        Node *left = minHeap.top(); minHeap.pop();
        Node *right = minHeap.top(); minHeap.pop();
        Node *top = new Node('$', left->freq + right->freq);
        top->left = left;
        top->right = right;
        minHeap.push(top);
    }
    printCodes(minHeap.top(), "");
    return 0;
}

'''
travelling_salesman_dp = '''
#include <iostream>
#include <vector>
#include <cmath>
using namespace std;
const int INF = 1e9;
int main() {
    int n;
    cin >> n;
    vector<vector<int>> dist(n, vector<int>(n));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            cin >> dist[i][j];
    vector<vector<int>> dp(1 << n, vector<int>(n, INF));
    dp[1][0] = 0;
    for (int mask = 1; mask < (1 << n); mask++) {
        for (int u = 0; u < n; u++) {
            if (mask & (1 << u)) {
                for (int v = 0; v < n; v++) {
                    if (!(mask & (1 << v)))
                        dp[mask | (1 << v)][v] = min(dp[mask | (1 << v)][v], dp[mask][u] + dist[u][v]);
                }
            }
        }
    }
    int res = INF;
    for (int i = 1; i < n; i++) res = min(res, dp[(1 << n) - 1][i] + dist[i][0]);
    cout << res;
    return 0;
}

'''
multistage_graph = '''
#include <iostream>
#include <vector>
using namespace std;
const int INF = 1e9;
int main() {
    int V;
    cin >> V;
    vector<vector<int>> dist(V, vector<int>(V));
    for (int i = 0; i < V; i++)
        for (int j = 0; j < V; j++)
            cin >> dist[i][j];
    for (int k = 0; k < V; k++)
        for (int i = 0; i < V; i++)
            for (int j = 0; j < V; j++)
                if (dist[i][k] + dist[k][j] < dist[i][j])
                    dist[i][j] = dist[i][k] + dist[k][j];
    for (int i = 0; i < V; i++) {
        for (int j = 0; j < V; j++)
            cout << dist[i][j] << " ";
        cout << endl;
    }
    return 0;
}

'''
fifteen_puzzle = '''
#include <iostream>
#include <vector>
#include <queue>
#include <set>
#include <algorithm>
using namespace std;
string goal = "123456789ABCDEF0";
int dx[] = {-1, 1, 0, 0};
int dy[] = {0, 0, -1, 1};
bool isValid(int x, int y) {
    return x >= 0 && x < 4 && y >= 0 && y < 4;
}
int bfs(string start) {
    set<string> visited;
    queue<pair<string, int>> q;
    q.push({start, 0});
    visited.insert(start);
    while (!q.empty()) {
        auto [state, depth] = q.front();
        q.pop();
        if (state == goal) return depth;
        int pos = state.find('0');
        int x = pos / 4, y = pos % 4;
        for (int i = 0; i < 4; i++) {
            int nx = x + dx[i], ny = y + dy[i];
            if (isValid(nx, ny)) {
                int new_pos = nx * 4 + ny;
                string next = state;
                swap(next[pos], next[new_pos]);
                if (visited.find(next) == visited.end()) {
                    visited.insert(next);
                    q.push({next, depth + 1});
                }
            }
        }
    }
    return -1;
}
int main() {
    string start = "";
    for (int i = 0; i < 16; i++) {
        string tile;
        cin >> tile;
        if (tile == "0") start += "0";
        else start += tile;
    }
    int moves = bfs(start);
    if (moves != -1) cout << moves;
    else cout << "Unsolvable";
    return 0;
}

'''
daa_exp = {
    'Insertion Sort.c' : insertion_sort,
    'Selection Sort.c' : selection_sort,
    'Merge Sort.c' : merge_sort,
    'Quick Sort.c' : quick_sort,
    'Binary Search.c' : binary_search,
    'Min Max.c' : min_max,
    'Prims.c' : prims,
    'Kruskal.c' : kruskal,
    'Dijkstra.c' : dijkstra,
    'Floyd Warshall.c' : floyd_warshall,
    'Activity Selection.c' : activity_selection,
    'Bellman Ford.c' : bellman_ford,
    'Matrix Chain Multiplication.c' : matrix_chain_multiplication,
    'Longest Common Subsequence.c' : longest_common_subsequence,
    '0/1 Knapsack.c' : knapsack,
    'Fractional Knapsack.c' : fractional_knapsack,
    'N-Queens.c' : n_queens,
    'Sum of Subset.c' : sum_of_subset,
    'Graph Coloring.c' : graph_coloring,
    'Rabin Karp.c' : rabin_karp,
    'KMP.c' : kmp,
    'Strassens.c' : strassens,
    "Kasturba.cpp": kasturba,
    "Activity Selection.cpp": activity_selection,
    "Job Sequence Deadline Greedy.cpp": job_seq_deadline_greedy,
    "Huffman Tree.cpp": huffman_tree,
    "Travelling Salesman DP.cpp": travelling_salesman_dp,
    "Multistage Graph.cpp": multistage_graph,
    "Fifteen Puzzle.cpp": fifteen_puzzle
}

def daa_():
    for filename, content in daa_exp.items():
        print(filename)
    exp = input("Enter Code : ")
    with open(exp, 'w') as file:
        file.write(daa_exp[exp])
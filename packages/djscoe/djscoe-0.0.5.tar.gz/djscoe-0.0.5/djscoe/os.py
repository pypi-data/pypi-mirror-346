import dis
from math import prod


multithreading = '''
class Bus extends Thread{
    int tickets;
    Bus(int tickets){
        this.tickets = tickets; 
    }
    public void run(){
        if(tickets > 0){
            try{
                Thread.sleep(1500);
                tickets--;
                System.out.println("Ticket booked by "+Thread.currentThread().getName());
            }
            catch (Exception e){
            }
        }
        else{
            System.out.println("Sorry House Full "+Thread.currentThread().getName());
        }
    }
}

public class Multithreading {
    public static void main(String args[]){
        System.out.println("Asynchronization");
        Bus b1 = new Bus(1);
        b1.run();
        b1.run();

        System.out.println("Synchronization");
        Bus b = new Bus(1);
        Thread t1 = new Thread(b);
        Thread t2 = new Thread(b);
        t1.setName("Mihir");
        t2.setName("Prinkal");
        t1.start();
        t2.start();


    }
}
'''

fcfs = '''
#include <iostream>

struct Process
{
    int no, at, bt, ct, tat, wt;
};

void sortPro(struct Process *program, int start, int end, bool isAt)
{
    if (isAt)
    {
        for (int i = start; i < end; i++)
        {
            for (int j = start; j <= end - i - 1; j++)
            {
                if (program[j].at > program[j + 1].at)
                {
                    struct Process temp = program[j];
                    program[j] = program[j + 1];
                    program[j + 1] = temp;
                }
            }
        }
    }
    else
    {
        for (int i = start; i < end; i++)
        {
            if (program[i].bt > program[i + 1].bt)
            {
                struct Process temp;
                temp = program[i];
                program[i + 1] = temp;
                program[i] = program[i + 1];
            }
        }
    }
}

int main()
{
    int noOfProcesses;
    printf("Enter the number of processes: ");
    // scanf("%d", &noOfProcesses);
    noOfProcesses = 3;

    int ptime = 0;
    float atat = 0, awt = 0;

    struct Process program[noOfProcesses];

    printf("Enter the arrival times\\n");
    for (int i = 0; i < noOfProcesses; i++)
    {
        printf("ARRIVAL Time of %d: ", (i + 1));
        // scanf("%d", &program[i].at);
        program[i].at = 4 - i;
        program[i].no = i;
    }

    printf("Enter the burst times\\n");
    for (int i = 0; i < noOfProcesses; i++)
    {
        printf("BURST Time of %d: ", (i + 1));
        // scanf("%d", &program[i].bt);
        program[i].bt = 5 + i;
    }

    for (int i = 0; i < noOfProcesses; i++)
    {
        printf("\\nP%d\\t%d\\t%d\\n", (i + 1), program[i].at, program[i].bt);
    }

    sortPro(program, 0, noOfProcesses - 1, true);

    for (int i = 0; i < noOfProcesses; i++)
    {
        printf("P%d\\t%d\\t%d\\n", (i + 1), program[i].at, program[i].bt);
    }

    printf("Order of execution of the Processes are:\\n");
    for (int i = 0; i < noOfProcesses; i++)
    {
        if (i == noOfProcesses - 1)
            printf("P%d\\n", program[i].no);
        else
            printf("P%d, ", program[i].no);
    }

    int i;
    for (i = 0; i < noOfProcesses; i++)
    {
        if (i == 0 && program[i].at != 0)
        {
            ptime = program[i].at + program[i].bt;
        }
        else
        {
            ptime += program[i].bt;
        }
        program[i].ct = ptime;
        program[i].tat = program[i].ct - program[i].at;
        program[i].wt = program[i].tat - program[i].bt;
        atat += program[i].tat;
        awt += program[i].wt;
    }
    atat /= noOfProcesses;
    awt /= noOfProcesses;

    printf("\\nAnalysis Table\\nProcess\\tAT\\tBT\\tCT\\tTAT\\tWT\\n");
    for (int i = 0; i < noOfProcesses; i++)
    {
        printf("P%d\\t%d\\t%d\\t%d\\t%d\\t%d\\n", program[i].no, program[i].at, program[i].bt, program[i].ct, program[i].tat, program[i].wt);
    }
    printf("Average Turn Around Time = %f\\n", atat);
    printf("Average Waiting Time = %f\\n", awt);

    return 0;
}

'''

sjf = '''
#include <bits/stdc++.h>
using namespace std;
int main()
{
    vector<pair<float, float>> vect;
    vector<pair<float, float>> vect1;
    vector<pair<float, float>>::iterator it;
    vector<float> CT;
    vector<float> TT;
    vector<float> WT;
    int burst = 0, Total = 0;
    int p;
    cout << "Enter no processess: ";
    cin >> p;
    float AT[p], BT[p];
    cout << "AT BT\\n";
    for (int i = 0; i < p; i++)
    {
        cin >> AT[i];
        cin >> BT[i];
    }
    int n = sizeof(AT) / sizeof(AT[0]);
    for (int i = 0; i < n; i++)
    {
        vect.push_back(make_pair(AT[i], BT[i]));
    }
    sort(vect.begin(), vect.end());
    int cmpl_T = vect[0].first + vect[0].second;
    vect1.push_back(make_pair(vect[0].first, vect[0].second));
    CT.push_back(cmpl_T);
    vect.erase(vect.begin());
    int min = 999;
    int index;
    int Total1 = 0;
    Total = 0;
    while (vect.size() > 0)
    {
        it = vect.begin();
        min = 999;
        for (int i = 0; i < vect.size(); i++)
        {
            if (vect[i].first <= cmpl_T && min > vect[i].second)
            {
                min = vect[i].second;
                index = i;
            }
        }
        if (min == 999)
        {
            for (int i = 0; i < vect.size(); i++)
            {
                if (min > vect[i].second)
                {
                    min = vect[i].second;
                    index = i;
                }
            }
            cmpl_T = vect[index].first + vect[index].second;
        }
        else
        {
            cmpl_T += vect[index].second;
        }
        CT.push_back(cmpl_T);
        int at = vect[index].first;
        int bt = vect[index].second;
        vect1.push_back(make_pair(at, bt));
        vect.erase(it + index);
    }
    for (int i = 0; i < n; i++)
    {
        int tt = CT[i] - vect1[i].first;
        int wt = tt - vect1[i].second;
        TT.push_back(tt);
        WT.push_back(wt);
        Total += TT[i];
        Total1 += WT[i];
    }
    float Avg_TT = Total / (float)n;
    float Avg_WT = Total1 / (float)n;
    printf("Process\\t\\tAT\\tBT\\tCT\\tTT\\tWT\\n");
    for (int i = 0; i < vect1.size(); i++)
    {
        printf("%d\\t\\t%.2f\\t%.2f\\t%.2f\\t%.2f\\t%.2f\\n", i + 1, vect1[i].first, vect1[i].second,
               CT[i], TT[i], WT[i]);
    }
    printf("Average waiting time is : %.2f\\n", Avg_WT);
    printf("Average turn around time is : %.2f\\n", Avg_TT);
    return 0;
}
'''

producer_consumer = '''
#include <stdio.h>

int s = 0, n = 0, e = 4, b[4];

int Wait(int *s) {
    return (--*s);
}

int Signal(int *s) {
    return (++*s);
}

void producer() {
    int a;

    printf("\\nEnter value to Produce : ");
    scanf("%d", &a);

    Wait(&e);
    Wait(&s);

    b[n] = a;

    Signal(&s);
    Signal(&n);

    printf("\\nBuffer : ");
    for (int i = 0; i < n; i++) {
        printf("%d ", b[i]);
    }
    printf("\\n");
}

void consumer() {
    Wait(&s);
    for (int i = 1; i < n; i++) {
        b[i - 1] = b[i];
    }
    Wait(&n);
    Signal(&s);
    Signal(&e);

    printf("\\nBuffer : ");

    for (int i = 0; i < n; ++i) {
        printf("%d ", b[i]);
    }
    printf("\\n");
}

int main() {
    int c;
    printf("Hello\\n");

    do {
        printf("\\n1  -->  Produce\\n2  -->  Consume\\n3  -->  Exit\\n");
        printf("\\nEnter your choice : ");
        scanf("%d", &c);

        switch (c) {
        case 1:
            if (e == 0) {
                printf("\\nBuffer is full\\n");
            }
            else {
                producer();
            }
            break;
        case 2:
            if (e == 4) {
                printf("\\nBuffer is empty\\n");
            }
            else {
                consumer();
            }
            break;
        case 3:
            printf("\\nExiting...\\n");
            break;
        default:
            printf("Enter a valid choice\\n");
        }
    } while (c != 3);

    return 0;
}
'''

bankers = '''
#include <stdio.h>

int main()
{

    int n, m;
    printf("Enter the number of orders : ");
    scanf("%d", &n);

    printf("Enter the number of resources : ");
    scanf("%d", &m);

    int alloc[n][m], max[n][m], avail[m];

    printf("Enter the details for orders\\n");
    for (int i = 0; i < n; i++)
    {
        printf("\\nOrder P%d\\nEnter supplied resources : ", i);

        for (int j = 0; j < m; j++)
        {
            scanf("%d", &alloc[i][j]);
        }

        printf("Enter maximum requirements : ");

        for (int j = 0; j < m; j++)
        {
            scanf("%d", &max[i][j]);
        }
    }
    printf("\\nEnter available resources : ");

    for (int j = 0; j < m; j++)
    {
        scanf("%d", &avail[j]);
    }

    int f[n], ans[n], ind = 0;
    for (int i = 0; i < n; i++)
    {
        f[i] = 0;
    }

    int need[n][m];

    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < m; j++)
        {
            need[i][j] = max[i][j] - alloc[i][j];
        }
    }

    for (int k = 0; k < n; k++)
    {
        for (int i = 0; i < n; i++)
        {
            if (f[i] == 0)
            {
                int flag = 0;

                for (int j = 0; j < m; j++)
                {
                    if (need[i][j] > avail[j])
                    {
                        flag = 1;
                        break;
                    }
                }
                if (flag == 0)
                {
                    ans[ind++] = i;
                    for (int j = 0; j < m; j++)
                    {
                        avail[j] += alloc[i][j];
                    }
                    f[i] = 1;
                }
            }
        }
    }

    int flag = 1;

    for (int i = 0; i < n; i++)
    {
        if (f[i] == 0)
        {
            flag = 0;
            printf("\\ntThe given sequence is not safe \\n");
            break;
        }
    }

    if (flag == 1)
    {
        printf("\\nFollowing is SAFE Sequence \\n");
        for (int i = 0; i < n - 1; i++)
        {
            printf(" P%d ->", ans[i]);
        }
        printf(" P%d", ans[n - 1]);
    }

    return 0;
}
'''

best_fit = '''
#include <bits/stdc++.h>
using namespace std;

int main()
{
    int noOfPartitions;
    cout << "Enter the number of patitions: ";
    cin >> noOfPartitions;
    int partitionMemory[noOfPartitions], tempPMemory[noOfPartitions];
    for (int i = 0; i < noOfPartitions; i++)
    {
        cout << "Partition " << i + 1 << ": ";
        cin >> partitionMemory[i];
        tempPMemory[i] = partitionMemory[i];
    }
    int noOfProcesses;
    cout << "Enter the number of processes: ";
    cin >> noOfProcesses;
    int processesMemory[noOfProcesses];
    for (int i = 0; i < noOfProcesses; i++)
    {
        cout << "Partition " << i + 1 << ": ";
        cin >> processesMemory[i];
    }
    string bestFit[noOfPartitions], notAllocatedProcesses;
    for (int i = 0; i < noOfPartitions; i++)
    {
        bestFit[i] = "X";
    }
    for (int i = 0; i < noOfProcesses; i++)
    {
        bool isAlloc = false;
        int minSize;
        for (int j = 0; j < noOfPartitions; j++)
        {
            if (processesMemory[i] <= partitionMemory[j] && !isAlloc)
            {
                minSize = j;
                isAlloc = true;
            }
            else if (processesMemory[i] <= partitionMemory[j])
            {
                if (partitionMemory[j] < partitionMemory[minSize])
                {
                    minSize = j;
                }
            }
        }
        if (isAlloc)
        {
            partitionMemory[minSize] -= processesMemory[i];
            if (bestFit[minSize] == "X")
            {

                bestFit[minSize] = "P" + to_string(i + 1);
            }
            else
            {
                bestFit[minSize] += ", P" + to_string(i + 1);
            }
            isAlloc = true;
        }
        else if (!isAlloc && notAllocatedProcesses.empty())
        {
            notAllocatedProcesses = "P" + to_string(i + 1);
        }
        else if (!isAlloc)
        {
            notAllocatedProcesses += ", P" + to_string(i + 1);
        }
    }
    cout << "\\nPartitions\\t\\tBest Fit\\n";
    for (int i = 0; i < noOfPartitions; i++)
    {
        cout << tempPMemory[i] << "\\t\\t\\t" << bestFit[i] << "\\n";
    }
    if (notAllocatedProcesses.empty())
    {
        cout << "There are no unallocated processes!\\n";
    }
    else
    {
        cout << "The unallocated processes are: " << notAllocatedProcesses << "\\n";
    }

    return 0;
}
'''

first_fit = '''
#include <bits/stdc++.h>
using namespace std;

int main()
{
    int noOfPartitions;
    cout << "Enter the number of patitions: ";
    cin >> noOfPartitions;
    int partitionMemory[noOfPartitions], tempPMemory[noOfPartitions];
    for (int i = 0; i < noOfPartitions; i++)
    {
        cout << "Partition " << i + 1 << ": ";
        cin >> partitionMemory[i];
        tempPMemory[i] = partitionMemory[i];
    }
    int noOfProcesses;
    cout << "Enter the number of processes: ";
    cin >> noOfProcesses;
    int processesMemory[noOfProcesses];
    for (int i = 0; i < noOfProcesses; i++)
    {
        cout << "Partition " << i + 1 << ": ";
        cin >> processesMemory[i];
    }
    string firstFit[noOfPartitions], notAllocatedProcesses;
    for (int i = 0; i < noOfPartitions; i++)
    {
        firstFit[i] = "X";
    }
    for (int i = 0; i < noOfProcesses; i++)
    {
        bool isAlloc = false;
        for (int j = 0; j < noOfPartitions; j++)
        {
            if (processesMemory[i] <= partitionMemory[j])
            {
                partitionMemory[j] -= processesMemory[i];
                if (firstFit[j] == "X")
                {

                    firstFit[j] = "P" + to_string(i + 1);
                }
                else
                {
                    firstFit[j] += ", P" + to_string(i + 1);
                }
                isAlloc = true;
                break;
            }
        }
        if (!isAlloc && notAllocatedProcesses.empty())
        {
            notAllocatedProcesses = "P" + to_string(i + 1);
        }
        else if (!isAlloc)
        {
            notAllocatedProcesses += ", P" + to_string(i + 1);
        }
    }
    cout << "\\nPartitions\\t\\tFirst Fit\\n";
    for (int i = 0; i < noOfPartitions; i++)
    {
        cout << tempPMemory[i] << "\\t\\t\\t" << firstFit[i] << "\\n";
    }
    if (notAllocatedProcesses.empty())
    {
        cout << "There are no unallocated processes!\\n";
    }
    else
    {
        cout << "The unallocated processes are: " << notAllocatedProcesses << "\\n";
    }

    return 0;
}
'''

worst_fit = '''
#include <bits/stdc++.h>
using namespace std;

int main()
{
    int noOfPartitions;
    cout << "Enter the number of patitions: ";
    cin >> noOfPartitions;
    int partitionMemory[noOfPartitions], tempPMemory[noOfPartitions];
    for (int i = 0; i < noOfPartitions; i++)
    {
        cout << "Partition " << i + 1 << ": ";
        cin >> partitionMemory[i];
        tempPMemory[i] = partitionMemory[i];
    }
    int noOfProcesses;
    cout << "Enter the number of processes: ";
    cin >> noOfProcesses;
    int processesMemory[noOfProcesses];
    for (int i = 0; i < noOfProcesses; i++)
    {
        cout << "Partition " << i + 1 << ": ";
        cin >> processesMemory[i];
    }
    string worstFit[noOfPartitions], notAllocatedProcesses;
    for (int i = 0; i < noOfPartitions; i++)
    {
        worstFit[i] = "X";
    }
    for (int i = 0; i < noOfProcesses; i++)
    {
        bool isAlloc = false;
        int maxSize;
        for (int j = 0; j < noOfPartitions; j++)
        {
            if (processesMemory[i] <= partitionMemory[j] && !isAlloc)
            {
                maxSize = j;
                isAlloc = true;
            }
            else if (processesMemory[i] <= partitionMemory[j])
            {
                if (partitionMemory[j] > partitionMemory[maxSize])
                {
                    maxSize = j;
                }
            }
        }
        if (isAlloc)
        {
            partitionMemory[maxSize] -= processesMemory[i];
            if (worstFit[maxSize] == "X")
            {

                worstFit[maxSize] = "P" + to_string(i + 1);
            }
            else
            {
                worstFit[maxSize] += ", P" + to_string(i + 1);
            }
            isAlloc = true;
        }
        else if (!isAlloc && notAllocatedProcesses.empty())
        {
            notAllocatedProcesses = "P" + to_string(i + 1);
        }
        else if (!isAlloc)
        {
            notAllocatedProcesses += ", P" + to_string(i + 1);
        }
    }
    cout << "\\nPartitions\\t\\tWorst Fit\\n";
    for (int i = 0; i < noOfPartitions; i++)
    {
        cout << tempPMemory[i] << "\\t\\t\\t" << worstFit[i] << "\\n";
    }
    if (notAllocatedProcesses.empty())
    {
        cout << "There are no unallocated processes!\\n";
    }
    else
    {
        cout << "The unallocated processes are: " << notAllocatedProcesses << "\\n";
    }

    return 0;
}
'''

page_replacement = '''
#include <stdio.h>

int search(int fSize, int n, int pageStream[], int frame[], int current)
{
    int check[fSize];
    for (int i = 0; i < fSize; i++)
    {
        check[i] = 0;
    }
    int count = 0;
    for (int i = current; i < n; i++)
    {
        for (int j = 0; j < fSize; j++)
        {
            if (frame[j] == pageStream[i])
            {
                check[j] = 1;
                count++;
            }
        }
        if (count == fSize - 1)
        {
            break;
        }
    }

    for (int i = 0; i < fSize; i++)
    {
        if (check[i] == 0)
        {
            return i;
        }
    }

    return 0;
}

int searchLeast(int fSize, int n, int pageStream[], int frame[], int current)
{
    int check[fSize];
    for (int i = 0; i < fSize; i++)
    {
        check[i] = 0;
    }
    int count = 0;
    for (int i = current; i >= 0; i--)
    {
        for (int j = 0; j < fSize; j++)
        {
            if (frame[j] == pageStream[i])
            {
                check[j] = 1;
                count++;
            }
        }
        if (count == fSize - 1)
        {
            break;
        }
    }

    for (int i = 0; i < fSize; i++)
    {
        if (check[i] == 0)
        {
            return i;
        }
    }

    return 0;
}

void optimal(int fSize, int n, int pageStream[])
{

    int frame[fSize], pageFaults = 0, i = 0, ind;
    for (int j = 0; j < fSize; j++)
    {
        frame[j] = -1;
    }

    printf("Incoming Stream\\t\\tFrames\\n");
    while (i < n)
    {

        int found = 0;

        for (int j = 0; j < fSize; j++)
        {
            if (frame[j] == pageStream[i])
            {
                found = 1;
                break;
            }
        }
        if (found == 0)
        {
            ind = search(fSize, n, pageStream, frame, i);
            frame[ind] = pageStream[i];
            pageFaults++;
        }

        printf("%d\\t\\t\\t", pageStream[i]);
        for (int j = 0; j < fSize; j++)
        {
            if (frame[j] == -1)
            {
                printf("  ");
            }
            else
            {
                printf("%d ", frame[j]);
            }
        }
        printf("\\n");
        i++;
    }

    printf("\\nNumber of faults : %d", pageFaults);
    printf("\\nNumber of hits : %d", n - pageFaults);
}
void lfu(int fSize, int n, int pageStream[])
{

    int frame[fSize], pageFaults = 0, i = 0, ind;
    for (int j = 0; j < fSize; j++)
    {
        frame[j] = -1;
    }

    printf("Incoming Stream\\t\\tFrames\\n");
    while (i < n)
    {

        int found = 0;

        for (int j = 0; j < fSize; j++)
        {
            if (frame[j] == pageStream[i])
            {
                found = 1;
                break;
            }
        }
        if (found == 0)
        {
            ind = searchLeast(fSize, n, pageStream, frame, i);
            frame[ind] = pageStream[i];
            pageFaults++;
        }

        printf("%d\\t\\t\\t", pageStream[i]);
        for (int j = 0; j < fSize; j++)
        {
            if (frame[j] == -1)
            {
                printf("  ");
            }
            else
            {
                printf("%d ", frame[j]);
            }
        }
        printf("\\n");
        i++;
    }

    printf("\\nNumber of faults : %d", pageFaults);
    printf("\\nNumber of hits : %d", n - pageFaults);
}
void fifo(int fSize, int n, int pageStream[])
{

    int frame[fSize], counter = 0, pageFaults = 0, i = 0;
    for (int j = 0; j < fSize; j++)
    {
        frame[j] = -1;
    }

    printf("Incoming Stream\\t\\tFrames\\n");
    while (i < n)
    {

        int found = 0;

        for (int j = 0; j < fSize; j++)
        {
            if (frame[j] == pageStream[i])
            {
                found = 1;
                break;
            }
        }
        if (found == 0)
        {
            frame[(counter) % (fSize)] = pageStream[i];
            pageFaults++;
            counter++;
        }

        printf("%d\\t\\t\\t", pageStream[i]);
        for (int j = 0; j < fSize; j++)
        {
            if (frame[j] == -1)
            {
                printf("  ");
            }
            else
            {
                printf("%d ", frame[j]);
            }
        }
        printf("\\n");
        i++;
    }

    printf("\\nNumber of faults : %d", pageFaults);
    printf("\\nNumber of hits : %d", n - pageFaults);
}

void lru(int fSize, int n, int pageStream[])
{

    int frame[fSize], check[fSize], pageFaults = 0, i = 0, index = 0, min;
    for (int j = 0; j < fSize; j++)
    {
        frame[j] = -1;
        check[j] = 0;
    }

    printf("Incoming Stream\\t\\tFrames\\n");
    while (i < n)
    {

        int found = 0;

        for (int j = 0; j < fSize; j++)
        {
            if (frame[j] == pageStream[i])
            {
                found = 1;
                check[j]++;
                break;
            }
        }
        if (found == 0)
        {
            min = n;
            int s = 0;
            for (int j = 0; j < fSize; j++)
            {
                if (min > check[j])
                {
                    min = check[j];
                    index = j;
                }
                else if (min == check[j])
                {
                    s++;
                }
            }
            if (s > 0)
            {
                index = searchLeast(fSize, n, pageStream, frame, i);
            }
            frame[index] = pageStream[i];
            check[index] = 1;
            pageFaults++;
        }

        printf("%d\\t\\t\\t", pageStream[i]);
        for (int j = 0; j < fSize; j++)
        {
            if (frame[j] == -1)
            {
                printf("  ");
            }
            else
            {
                printf("%d ", frame[j]);
            }
        }
        printf("\\n");
        i++;
    }

    printf("\\nNumber of faults : %d", pageFaults);
    printf("\\nNumber of hits : %d", n - pageFaults);
}

int main()
{

    int fSize, n;

    printf("Enter the frame size : ");
    scanf("%d", &fSize);

    printf("\\nEnter the number of entries : ");
    scanf("%d", &n);

    int pageStream[n];
    printf("\\nEnter the data of stream : ");
    for (int i = 0; i < n; i++)
    {
        scanf("%d", &pageStream[i]);
    }

    int choice;
    printf("1.Fifo\\n2.Optimal\\n3.Lfu\\n4.Lru\\n");
    printf("Select Type of Page Replacement Policy : ");
    scanf("%d", &choice);

    switch (choice)
    {
    case 1:
        fifo(fSize, n, pageStream);
        break;
    case 2:
        optimal(fSize, n, pageStream);
        break;
    case 3:
        lfu(fSize, n, pageStream);
        break;
    case 4:
        lru(fSize, n, pageStream);
        break;
    default:
        break;
    }

    return 0;
}
'''

disk_scheduling = '''
#include <stdio.h>

int absolute(int x, int y)
{
    if (x >= y)
    {
        return x - y;
    }
    else
    {
        return y - x;
    }
}

int FCFS(int n, int p, int m[], int ans[])
{
    int total = 0;
    for (int i = 0; i < n; i++)
    {
        if (i == 0)
        {
            total += absolute(p, m[i]);
        }
        else
        {
            total += absolute(m[i - 1], m[i]);
        }
        ans[i] = m[i];
    }

    return total;
}

int SSTF(int n, int p, int m[], int ans[])
{
    int total = 0;
    int current, v[n];
    for (int i = 0; i < n; i++)
    {
        v[i] = 0;
    }

    for (int i = 0; i < n; i++)
    {
        if (i == 0)
        {
            current = p;
        }
        else
        {
            current = ans[i - 1];
        }
        int min = 199, j, x;
        for (j = 0; j < n; j++)
        {
            if (absolute(current, m[j]) <= min && v[j] == 0)
            {
                min = absolute(current, m[j]);
                x = j;
            }
        }
        v[x] = 1;
        total += min;
        ans[i] = m[x];
    }

    return total;
}

int SCAN(int n, int p, int m[], int ans[], int u)
{
    int total = 0;
    int a, x;
    for (int i = 0; i < n; i++)
    {
        if (p < m[i])
        {
            a = x = i;
            break;
        }
    }
    if (u == 0)
    {
        a--;
    }

    for (int i = 0; i < n + 1; i++)
    {
        printf("\\na=%d x=%d u=%d\\n", a, x, u);
        if (u == 1)
        {
            if (a < n && a >= x)
            {
                ans[i] = m[a];
                a++;
            }
            else if (a == n)
            {
                ans[i] = 199;
                a = a - x;
            }
            else
            {
                ans[i] = m[a];
                a--;
            }
        }
        else
        {
            if (a >= 0 && a < x)
            {
                ans[i] = m[a];
                a--;
            }
            else if (a == -1)
            {
                ans[i] = 0;
                a = x;
            }
            else
            {
                ans[i] = m[a];
                a++;
            }
        }
    }

    if (u == 1)
    {
        total += absolute(199, p) + absolute(199, m[0]);
    }
    else
    {
        total += absolute(0, p) + absolute(0, m[n - 1]);
    }

    return total;
}
int CSCAN(int n, int p, int m[], int ans[], int u)
{
    int total = 0;
    int a, x;
    for (int i = 0; i < n; i++)
    {
        if (p < m[i])
        {
            a = x = i;
            break;
        }
    }
    if (u == 0)
    {
        a--;
    }

    for (int i = 0; i < n + 2; i++)
    {
        printf("\\na=%d x=%d u=%d\\n", a, x, u);
        if (u == 1)
        {
            if (a < n && a >= x)
            {
                ans[i] = m[a];
                a++;
            }
            else if (a == n)
            {
                ans[i] = 199;
                a = -1;
            }
            else if (a == -1)
            {
                ans[i] = 0;
                a++;
            }
            else
            {
                ans[i] = m[a];
                a++;
            }
        }
        else
        {
            if (a >= 0 && a < x)
            {
                ans[i] = m[a];
                a--;
            }
            else if (a == -1)
            {
                ans[i] = 0;
                a = n;
            }
            else if (a == n)
            {
                ans[i] = 199;
                a--;
            }
            else
            {
                ans[i] = m[a];
                a--;
            }
        }
    }

    if (u == 1)
    {
        total = absolute(199, p) + 199 + absolute(0, m[x - 1]);
    }
    else
    {
        total = absolute(0, p) + 199 + absolute(199, m[x]);
    }

    return total;
}
int LOOK(int n, int p, int m[], int ans[], int u)
{
    int total = 0;
    int a, x;
    for (int i = 0; i < n; i++)
    {
        if (p < m[i])
        {
            a = x = i;
            break;
        }
    }
    if (u == 0)
    {
        a--;
    }

    for (int i = 0; i < n; i++)
    {
        printf("\\na=%d x=%d u=%d\\n", a, x, u);
        if (u == 1)
        {
            if (a < n && a >= x)
            {
                ans[i] = m[a];
                a++;
                if (a == n)
                {
                    a = a - x;
                }
            }
            else
            {
                ans[i] = m[a];
                a--;
            }
        }
        else
        {
            if (a >= 0 && a < x)
            {
                ans[i] = m[a];
                a--;
                if (a == -1)
                {
                    a = x;
                }
            }
            else
            {
                ans[i] = m[a];
                a++;
            }
        }
    }

    if (u == 1)
    {
        total = absolute(m[n - 1], p) + absolute(m[n - 1], m[0]);
    }
    else
    {
        total = absolute(m[0], p) + absolute(m[0], m[n - 1]);
    }

    return total;
}
int CLOOK(int n, int p, int m[], int ans[], int u)
{
    int total = 0;
    int a, x;
    for (int i = 0; i < n; i++)
    {
        if (p < m[i])
        {
            a = x = i;
            break;
        }
    }
    if (u == 0)
    {
        a--;
    }

    for (int i = 0; i < n; i++)
    {
        printf("\\na=%d x=%d u=%d\\n", a, x, u);
        if (u == 1)
        {
            if (a < n && a >= x)
            {
                ans[i] = m[a];
                a++;
                if (a == n)
                {
                    a = 0;
                }
            }
            else
            {
                ans[i] = m[a];
                a++;
            }
        }
        else
        {
            if (a >= 0 && a < x)
            {
                ans[i] = m[a];
                a--;
                if (a == -1)
                {
                    a = n - 1;
                }
            }
            else
            {
                ans[i] = m[a];
                a--;
            }
        }
    }

    if (u == 1)
    {
        total = absolute(m[n - 1], p) + absolute(m[n - 1], m[0]) + absolute(m[0], m[x - 1]);
    }
    else
    {
        total = absolute(m[0], p) + absolute(m[n - 1], m[0]) + absolute(m[n - 1], m[x]);
    }

    return total;
}

void print(int n, int p, int ans[], int total)
{
    printf("\\nTrack movements are as follows : \\n");
    printf("%d -> %d", p, ans[0]);
    for (int i = 1; i < n; i++)
    {
        printf(" -> %d", ans[i]);
    }

    printf("\\nTotal seek time is : %d\\n", total);
}

int main()
{

    int n, p;
    printf("\\nEnter the number of movements : ");
    scanf("%d", &n);

    int m[n];
    printf("\\nEnter %d movements (0 - 199) : ", n);
    for (int i = 0; i < n; i++)
    {
        scanf("%d", &m[i]);
    }

    printf("\\nEnter the current head location : ");
    scanf("%d", &p);
    // int n=5,p=65;
    // int m[]={25,51,60,132,189};
    int total, ans[n];
    int c;
    do
    {
        printf("\\n1  -->  FCFS\\n2  -->  SSTF\\n3  -->  SCAN\\n4  -->  CSCAN\\n5  -->  LOOK\\n6  -->  CLOOK\\n7  -->  EXIT\\n");
        printf("\\nEnter your choice : ");
        scanf("%d", &c);
        int u;
        switch (c)
        {
        case 1:
            total = FCFS(n, p, m, ans);
            print(n, p, ans, total);
            break;
        case 2:
            total = SSTF(n, p, m, ans);
            print(n, p, ans, total);
            break;
        case 3:
            u = 0;
            total = SCAN(n, p, m, ans, u);
            print(n + 1, p, ans, total);
            break;
        case 4:
            u = 0;
            total = CSCAN(n, p, m, ans, u);
            print(n + 2, p, ans, total);
            break;
        case 5:
            u = 1;
            total = LOOK(n, p, m, ans, u);
            print(n, p, ans, total);
            break;
        case 6:
            u = 1;
            total = CLOOK(n, p, m, ans, u);
            print(n, p, ans, total);
            break;
        case 7:
            printf("\\nExiting...\\n");
            break;
        default:
            printf("Enter a valid choice\\n");
        }
    } while (c != 7);

    return 0;
}
'''

os_exp = {
    'Multithreading.java' : multithreading,
    'FCFS.cpp' : fcfs,
    'SJF.cpp' : sjf,
    'ProducerConsumer.c' : producer_consumer,
    'Bankers.c' : bankers,
    'Best Fit.cpp' : best_fit,
    'First Fit.cpp' : first_fit,
    'Worst Fit.cpp' : worst_fit,
    'Page Replacement.c' : page_replacement,
    'Disk Scheduling.c' : disk_scheduling
}

def os_():
    for filename, content in os_exp.items():
        print(filename)
    exp = input("Enter Code : ")
    with open(exp, 'w') as file:
        file.write(os_exp[exp])
booth = '''
def twos_complement(n):
    ones = ''
    for i in n:
        ones += str(1 - int(i))
    twos = ''
    carry = '1'
    for i in ones[-1::-1]:
        val = str(int(i) + int(carry))
        if val < "2":
            twos += val
            carry = '0'
        else:
            carry = '1'
            twos += '0'
    return twos[-1::-1]

def add(a, m):
    sumy = ''
    carry = '0'
    length = len(a)
    for i in range(length - 1, -1, -1):
        val = str(int(a[i]) + int(m[i]) + int(carry))
        if val < "2":
            sumy += val
            carry = '0'
        elif val == "2":
            sumy += '0'
            carry = '1'
        elif val == "3":
            sumy += '1'
            carry = '1'
    return sumy[:length][-1::-1]

def ARS(a, q, q_): 
    q_ = q[-1]
    q = a[-1] + q[:len(q) - 1] 
    a = a[0] + a[:len(a) - 1]
    return a, q, q_

m_dec = int(input("Enter M : "))
q_dec = int(input("Enter Q : "))

f1, f2 = False, False
if m_dec < 0:
    m = bin(m_dec)[3:]
    f1 = True
else:
    m = bin(m_dec)[2:]
if q_dec < 0:
    q = bin(q_dec)[3:]
    f2 = True
else:
    q = bin(q_dec)[2:]

count = (len(q) if q_dec > m_dec else len(m))
count += 1

q = "0" * (count - len(q)) + q
m = "0" * (count - len(m)) + m

if f1:
    m = twos_complement(m)
if f2:
    q = twos_complement(q)
m_minus = twos_complement(m)

a = "0" * (count)
q_ = "0"

print("---------------------------")
print(a, q, q_)
print("---------------------------")

for i in range(count):
    if (q[-1], q_) == ("0", "0") or (q[-1], q_) == ("1", "1"):
        a, q, q_ = ARS(a, q, q_)
        print(a, q, q_, "\\tARS")
    elif (q[-1], q_) == ("0", "1"):
        a = add(a, m)
        print(a, q, q_, "\\ta <- a + m")
        a, q, q_ = ARS(a, q, q_)
        print(a, q, q_, "\\tARS")
    elif (q[-1], q_) == ("1", "0"):
        a = add(a, m_minus)
        print(a, q, q_, "\\ta <- a - m")
        a, q, q_ = ARS(a, q, q_)
        print(a, q, q_, "\\tARS")
    print("---------------------------")
'''

non_restoring = '''
def add(a, m):
    sumy = ''
    carry = '0'
    length = len(a)
    for i in range(length -1, -1, -1):
        val = str(int(a[i]) + int(m[i]) + int(carry))
        if val < "2":
            sumy += val
            carry = '0'
        elif val == "2":
            sumy += '0'
            carry = '1'
        elif val == "3":
            sumy += '1'
            carry = '1'
    return carry, sumy[:length][-1::-1]

def RS(c, a, q):
    q = a[-1] + q[:len(q)-1]
    a = c + a[:len(a)-1]
    c = "0"
    return c, a, q

m_dec = int(input("Enter M : "))
q_dec = int(input("Enter Q : "))
m = bin(m_dec)[2:]
q = bin(q_dec)[2:]

count = (len(q) if q_dec>m_dec else len(m))

q = "0"*(count - len(q)) + q
m = "0"*(count - len(m)) + m
a = "0"*(count)
c = "0"

print("---------------------------")
print(c,a,q)
print("---------------------------")
for i in range(count):
    if q[-1] == "1":
        c, a = add(a, m)
        print(c,a,q, "\\ta <- a + m")
    c, a, q = RS(c, a, q)
    print(c,a,q, "\\tRS")
    print("---------------------------")
'''

restoring = '''
def twos_compliment(n):
    ones = ''
    for i in n:
        ones += str(1 - int(i))
    twos = ''
    carry = '1'
    for i in ones[-1::-1]:
        val = str(int(i) + int(carry))
        if val < "2":
            twos += val
            carry = '0'
        else:
            carry = '1'
            twos += '0'
    return twos[-1::-1]

def LS(a, q):
    a = a[1:] + q[0]
    q = q[1:] + '_'
    return a, q

def add(a, m):
    sumy = ''
    carry = '0'
    length = len(a)
    for i in range(length -1, -1, -1):
        val = str(int(a[i]) + int(m[i]) + int(carry))
        if val < "2":
            sumy += val
            carry = '0'
        elif val == "2":
            sumy += '0'
            carry = '1'
        elif val == "3":
            sumy += '1'
            carry = '1'
    return sumy[:length][-1::-1]

m_dec = int(input("Enter M : "))
q_dec = int(input("Enter Q : "))
m = bin(m_dec)[2:]
q = bin(q_dec)[2:]

count = (len(q) if q_dec>m_dec else len(m))
count += 1

q = "0"*(count - len(q)) + q
m = "0"*(count - len(m)) + m
m_minus = twos_compliment(m)
a = "0"*(count)

print("------------------------")
print(a,q)
print("------------------------")
for i in range(count):
    a, q = LS(a, q)
    print(a, q, "\\tLS")
    a = add(a, m_minus)
    print(a, q, "\\ta <- a - m")
    if a[0] == "1":
        a = add(a, m)
        print(a, q, "\\ta <- a + m")
        q = q[:count-1] + "0"
        print(a, q, "\\tq[0] = 0")
    else:
        q = q[:count-1] + "1"
        print(a, q, "\\tq[0] = 1")
    print("------------------------")
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

addition = '''
; multi-segment executable file template.

data segment
    ; add your data here!
    pkey db "press any key...$"
ends

stack segment
    dw   128  dup(0)
ends

code segment
start:
; set segment registers:
    mov ax, data
    mov ds, ax
    mov es, ax

    ; Mihir Panchal Addition Code
    
    MOV AX,[1000h]
    MOV BX,[1002h]
    MOV CL,00h
    ADD AX,BX 
    
    MOV [1004h],AX
    JNC jump 
    
    INC CL
    jump:
    MOV [1006h],CL
    HLT   
    lea dx, pkey
    mov ah, 9
    int 21h        ; output string at ds:dx
    
    ; wait for any key....    
    mov ah, 1
    int 21h
    
    mov ax, 4c00h ; exit to operating system.
    int 21h    
ends

end start ; set entry point and stop the assembler.

'''

subtraction = '''
; multi-segment executable file template.

data segment
    ; add your data here!
    pkey db "press any key...$"
ends

stack segment
    dw   128  dup(0)
ends

code segment
start:
; set segment registers:
    mov ax, data
    mov ds, ax
    mov es, ax

    ; Mihir Panchal Subraction
                    
    MOV AX,[1000h]
    MOV BX,[1002h]
    MOV CL,00h
    SUB AX,BX 
    
    MOV [1004h],AX
    JNC jump 
    
    INC CL
    jump:
    MOV [1006h],CL
    HLT


    lea dx, pkey
    mov ah, 9
    int 21h        ; output string at ds:dx
    
    ; wait for any key....    
    mov ah, 1
    int 21h
    
    mov ax, 4c00h ; exit to operating system.
    int 21h    
ends

end start ; set entry point and stop the assembler.

'''

ascending = '''
; multi-segment executable file template.
;Ascending
data segment
    ; add your data here!
    string1 db 99h,12h,56h,45h,36h
ends

stack segment
    dw   128  dup(0)
ends

code segment
 assume cs :code,ds:data
    start: mov ax,data
    mov ds,ax
    
    mov ch,04h
    
    up2:mov cl,04h
    lea si,string1
    
    up1: mov al,[si]
    mov bl,[si+1]
    cmp al,bl
    jc down
    mov dl,[si+1]
    xchg [si],dl
    mov [si+1],dl
    
    down: inc si
    dec cl
    jnz up1
    dec ch
    jnz up2
    
   
ends

end start ; set entry point and stop the assembler.

'''

descending = '''
; multi-segment executable file template.
;DESCENDING
data segment
    ; add your data here!
    string1 db 99h,12h,56h,45h,36h
ends

stack segment
    dw   128  dup(0)
ends

code segment
 assume cs :code,ds:data
    start: mov ax,data
    mov ds,ax
    
    mov ch,04h
    
    up2:mov cl,04h
    lea si,string1
    
    up1: mov al,[si]
    mov bl,[si+1]
    cmp al,bl
    jnc down
    mov dl,[si+1]
    xchg [si],dl
    mov [si+1],dl
    
    down: inc si
    dec cl
    jnz up1
    dec ch
    jnz up2
    
   
ends

end start ; set entry point and stop the assembler.

'''

block_transfer = '''
; Mihir Panchal 60004230275

data segment
seg1 db 1h ,2h ,3h
ends
extra segment
seg2 db ?
ends
code segment
start:
mov ax, data
mov ds, ax
mov ax, extra
mov es, ax
; add your code here
lea si , seg1
lea di , seg2 
mov cx, 03h
x: mov ah,ds:[si]
mov es:[di],ah

inc si
inc di
dec cx 
jnz x

ends
end start
'''

min_max = '''
; Mihir Panchal 60004230275

DATA SEGMENT
ARR DB 5,3,7,1,9,2,6,8,4,0
LEN DW $-ARR
MIN DB ?
MAX DB ?
DATA ENDS

CODE SEGMENT
ASSUME DS:DATA CS:CODE
START:
MOV AX,DATA
MOV DS,AX

LEA SI,ARR
MOV AL,ARR[SI]
MOV MIN,AL
MOV MAX,AL

MOV CX,LEN
REPEAT:
MOV AL,ARR[SI]
CMP MIN,AL
JL CHECKMAX

MOV MIN,AL
CHECKMAX:
CMP MAX,AL
JG DONE

MOV MAX,AL
DONE:
INC SI
LOOP REPEAT

MOV AH,4CH
INT 21H
CODE ENDS
END START
'''

ascending_macro = '''
; Mihir Panchal Ascending Macro 60004230275

sort macro 
MOV CH,04H
 
UP2: MOV CL,04H
LEA SI,STRING1
 
UP1: MOV AL,[SI]
MOV BL,[SI+1]
CMP AL,BL
JC DOWN
MOV DL,[SI+1]
XCHG [SI],DL
MOV [SI+1],DL
 
DOWN: INC SI
DEC CL
JNZ UP1
DEC CH
JNZ UP2 
endm


DATA SEGMENT
STRING1 DB 99H,12H,56H,45H,36H
DATA ENDS
 
CODE SEGMENT
ASSUME CS:CODE,DS:DATA
START: MOV AX,DATA
MOV DS,AX
sort 
CODE ENDS
END START


'''

factorial_asm='''
; Mihir Panchal Factorial

data segment
    fact dw ?
    num dw 05h
data ends

code segment
    start:mov ax, data
    mov ds, ax
    mov ax, 01h
    mov cx, num
    l1:
        mul cx
        dec cx
        jnz l1
    mov fact, ax
code ends
end start
'''

factorial_macro='''
; Mihir Panchal Factorial using Macro

data segment
    fact dw ?
    num dw 05h
data ends

macro factorial n
    mov cx, n
    l1:
        mul cx
        dec cx
        jnz l1
endm

code segment
    start:mov ax, data
    mov ds, ax
    mov ax, 01h
    factorial num
    mov fact, ax
code ends
end start

'''

dos_interrupt = '''
data segment

MSG DB "Enter a character:$"

data ends

;Mihir

code segment

assume cs:code, ds:data

start:

mov ax,data

mov ds,ax

lea DX,MSG

MOV AH,09h

INT 21H

mov ah,01

int 21h

mov dl,al

mov ah,02

int 21h

mov ah,4ch

int 21h

code ends

end start
'''

poa_exp = {
    'booths.py': booth,
    'non_restoring.py': non_restoring,
    'restoring.py': restoring,
    'best_fit.cpp': best_fit,
    'first_fit.cpp': first_fit,
    'worst_fit.cpp': worst_fit,
    'page_replacement.c': page_replacement,
    'addition.asm': addition,
    'subtraction.asm': subtraction,
    'ascending.asm': ascending,
    'descending.asm': descending,
    'block_transfer.asm': block_transfer,
    'min_max.asm': min_max,
    'ascending_macro.asm': ascending_macro,
    'factorial.asm': factorial_asm,
    'factorial_macro.asm': factorial_macro,
    'dos_interrupt.asm': dos_interrupt,
}

def poa_():
    for filename, content in poa_exp.items():
        print(filename)
    exp = input("Enter Code : ")
    with open(exp, 'w') as file:
        file.write(poa_exp[exp])
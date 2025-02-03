#include <stdio.h>
#include <string.h>

#define MAX_N 100
//---------------- List ----------------------------
typedef int ElementType;
typedef int Position;

typedef struct {
    ElementType Elements[MAX_N];
    Position Last; // vi tri cuoi, bat dau tu 1
} List;

void makenullList(List* pL)
{
    pL->Last = 0;
}

int isFullList(List L)
{
    return L.Last == MAX_N;
}

int emptyList(List L)
{
    return L.Last == 0;
}

//
ElementType firstList(List L)
{
    if (!emptyList(L)) {
        return L.Elements[0];
    }
    printf("Loi List rong");
    return -9999;
}

// Lay phan tu thu i, vi tri bat dau tu 1
ElementType retrieve(List L, Position p)
{
    return L.Elements[p - 1];
}

Position locate(List L, ElementType x)
{
    if (!emptyList(L)) {
        Position p;
        for (p = 1; p <= L.Last; p++) {
            if (x == L.Elements[p - 1]) {
                return p;
            }
        }
    }
    return -1; // list rong
}

//---------------- Insert -----------------------
void pushback(List* pL, ElementType x)
{
    pL->Elements[pL->Last] = x;
    pL->Last++;
}

// them phan tu x vao vi tri p
// vi tri chen: 1 <= p <= Last + 1
void insertList(List* pL, Position p, ElementType x)
{
    if (!isFullList(*pL)) {
        if (p >= 1 && p <= pL->Last) {
            Position q;
            for (q = pL->Last; q > p - 1; q--) {
                pL->Elements[q] = pL->Elements[q - 1];
            }
            pL->Last++;
            pL->Elements[p - 1] = x;
        } else {
            printf("Vi tri chen khong hop le");
        }
    } else {
        printf("Loi list day");
    }
}

//---------------- Delete -----------------------

// xoa phan tu o cuoi
void popList(List* pL)
{
    if (!emptyList(*pL)) {
        pL->Last--;
    } else {
        printf("Loi mang rong");
    }
}

// xoa phan tu o vi tri p
void deleteList(List* pL, Position p)
{
    if (!emptyList(*pL)) {
        if (p >= 1 && p <= pL->Last) {
            Position q;
            for (q = p; q < pL->Last; q++) {
                pL->Elements[q - 1] = pL->Elements[q];
            }
        } else {
            printf("Loi vi tri khong hop le");
        }
    } else {
        printf("Loi mang rong");
    }
}

//------------------ Utility ----------------------------

void printList(List* pL)
{
    int p;
    for (p = 1; p <= pL->Last; p++) {
        printf("%d ", retrieve(*pL, p));
    }
    printf("\n");
}

int lengthList(List* pL)
{
    return pL->Last;
}
List unionList(List* pL1, List* pL2)
{
    // List* uni = (List*)malloc(sizeof(List));
    List uni;
    makenullList(&uni);
    int pushed[MAX_N] = { 0 };
    int p;
    for (p = 1; p <= lengthList(pL1); p++) {
        ElementType entry = retrieve(*pL1, p);
        pushback(&uni, entry);
        pushed[entry] = 1;
    }
    for (p = 1; p <= lengthList(pL2); p++) {
        ElementType entry = retrieve(*pL2, p);
        if (!pushed[entry]) {
            pushback(&uni, entry);
        }
    }
    return uni;
}

//----------------------------------------
typedef struct {
    int n; // So luong trang thai toi da
    List lst[MAX_N / 2][MAX_N / 2]; // lst -> luu trang thai ket qua voi index [trang thai dau][ky tu nhap]
} Graph;

void init_Graph(Graph* pG, int n)
{
    pG->n = n;
    int i, j;
    for (i = 0; i < n; i++) {
        for (j = 0; j < n + 1; j++) { // them 1 cot cho ky tu 'e'
            List L;
            makenullList(&L);
            pG->lst[i][j] = L;
        }
    }
}

void add_edge(Graph* pG, int u, char w, int v)
{
    if (w == 'e') {
        pushback(&pG->lst[u][pG->n], v);
    } else {
        pushback(&pG->lst[u][w - '0'], v);
    }
}

// To chuc file NFA_sodo:
//  1. Q: so luong cua tap trang thai. vd: 3 -> q0, q1, q2
//  2. sigma: chuoi ky tu nhap (khong bao gom epsilon). vd: 3 -> 0, 1, 2
//  3. d: so luong ham chuyen
//  4. delta: danh sach ham chuyen: trang thai dau, ky tu nhap, trang thai ket qua
//  5. ky tu bat dau.
//  6. f: so luong cua tap ket thuc.
//  7. F: tap ky tu ket thuc

void read_NFAe(int* Q, int* sigma, Graph* pG, int* q0, List* F)
{
    int i, j, d, f;
    FILE* file = fopen("NFAe_sodo.txt", "r");
    fscanf(file, "%d", Q);
    fscanf(file, "%d", sigma);
    fscanf(file, "%d", &d);
    init_Graph(pG, *Q);

    int u, v;
    char w;
    for (i = 0; i < d; i++) {
        fscanf(file, "%d %c %d", &u, &w, &v);
        add_edge(pG, u, w, v);
    }
    fscanf(file, "%d", q0);

    fscanf(file, "%d", &f);
    makenullList(F);
    int temp;
    for (i = 0; i < f; i++) {
        fscanf(file, "%d", &temp);
        pushback(F, temp);
    }

    fclose(file);
}

//----------------------------Giai thuat-------------------------------

// Tim e-closure cua trang thai q

void e_closure(Graph* pG, List* pQ, List* res)
{
    int position;
    for (position = 1; position <= lengthList(pQ); position++) {
        ElementType q = retrieve(*pQ, position);
        if (!locate(*res, q) || emptyList(*res))
            pushback(res, q); // e_closure cua q thi bao gom luon q

        List lst = pG->lst[q][pG->n];
        if (!emptyList(lst)) {
            *res = unionList(res, &lst);
            e_closure(pG, &lst, res);
        }
    }
}

List delta(Graph* pG, List* pQ, char c)
{
    List res;
    makenullList(&res);

    int position;
    for (position = 1; position <= lengthList(pQ); position++) {
        ElementType q = retrieve(*pQ, position);
        res = unionList(&res, &pG->lst[q][c - '0']);
    }
    return res;
}

void solve(int Q, int sigma, Graph* pG, int q0, List* F)
{
    // Doc file
    FILE* file = fopen("NFAe_testcase.txt", "r");
    // To chuc file test case: chuoi test case ket thuc bang ky tu '$', cach nhau theo dong
    int i, n;
    while (!feof(file)) {
        char string[MAX_N];
        fgets(string, MAX_N, file);

        // Remove trailing newline
        size_t len = strlen(string);
        if (len > 0 && string[len - 1] == '\n') {
            string[len - 1] = '\0';
        }

        // Bat dau giai thuat
        List q, Q0;
        makenullList(&q);
        makenullList(&Q0);
        pushback(&Q0, q0);
        e_closure(pG, &Q0, &q);
        int i = 0;
        char c = string[i];
        while (c != '$') {
            List d = delta(pG, &q, c);
            makenullList(&q); // reset List q
            e_closure(pG, &d, &q);
            c = string[++i];
        }

        // Kiem tra trang thai ket thuc co nam trong q hay khong
        int position;
        int finish = 0;
        char t[MAX_N];
        strncpy(t, string, strlen(string)-1); // copy chuoi khong chua ky tu '$'
        for (position = 1; position <= lengthList(&q); position++) {
            ElementType x = retrieve(q, position);
            if (locate(q, x)) {
                printf("NFAe nhan chuoi %s\n", t);
                finish = 1;
            }
            break;
        }
        if (!finish)
            printf("NFAe KHONG nhan chuoi %s\n", t);
    }
    fclose(file);
}

int main()
{
    int Q, sigma, q0;
    Graph G;
    List F;
    read_NFAe(&Q, &sigma, &G, &q0, &F);
    solve(Q, sigma, &G, q0, &F);
    return 0;
}
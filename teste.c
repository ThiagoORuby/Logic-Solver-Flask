#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

// Bubble sort
int sort(int arr[], int i, int tam){
    if(i >= tam - 1) return 0;
    bubble(arr, i, tam);
    sort(arr, i, tam-1);
}

int bubble(int arr[], int i, int end){
    if(i >= (end - 1)) return 0;

    if(arr[i] >= arr[i+1])
    {
        int aux = arr[i];
        arr[i] = arr[i+1];
        arr[i+1] = aux;
    }
    bubble(arr, i+1, end);
}

int mdc(int a, int b){
    if(b == 0) return a;
    return mdc(b, a%b);
}

int isPrime(int n, int i){
    if(n == 2) return 1;
    if(n % i == 0 || n <= 1) return 0;
    if(i*i > n) return 1;
    return isPrime(n, i+1);
}

int nextPrime(int n){
    if(isPrime(n,2)) return n;
    return nextPrime(n+1);
}

int somaDigitos(int n){
    if(n/10 == 0) return n;
    return n%10 + somaDigitos(n/10);
}

int valores(int i, int x, int kcaj[], int ordep[]){
    if(i == x) return 1;
    scanf("%d%d", &kcaj[i], &ordep[i]);
    if((kcaj[i] < 1 || kcaj[i] > 1500) || (ordep[i] < 1 || ordep[i] > 1500)) return 0;
    return valores(i+1, x, kcaj, ordep);
}

int vencedor(int fp1, int kcaj[], int fp2, int ordep[], int x){
    int pts1 = 0, pts2 = 0, sum1, sum2;
    sum1 = somaDigitos(nextPrime(fp1+1));
    sum2 = somaDigitos(nextPrime(fp2+1));
    int orp = ordep[x-1];
    int md = mdc(fp2, orp);
    pts1 = isPrime(fp1, 2) + (mdc(fp1, kcaj[x-1]) == 1) + isPrime(sum1,2);
    pts2 = isPrime(fp2, 2) + (md==1) + isPrime(sum2,2);
    printf("%d\n", pts1 < pts2);
    if(pts1 < pts2){
        return 1;
    }
    return 0;
}

void partida(int n){
    int x, fp1, fp2;
    if(n == 0) return; 
    scanf("%d", &x);
    int kcaj[x], ordep[x];
    int ret = valores(0, x, kcaj, ordep);
    if(ret){
        sort(kcaj, 0, x);
        sort(ordep, 0, x);
        for(int i = 0; i < x; i++){
            printf("%d ", kcaj[i]);
        }
        printf("\n");
        for(int i = 0; i < x; i++){
            printf("%d ", ordep[i]);
        }
        printf("\n");
        fp1 = kcaj[0] + kcaj[x-1] + kcaj[x/2];
        fp2 = ordep[0] + ordep[x-1] + ordep[x/2];
        int venc = vencedor(fp1, kcaj, fp2, ordep, x);
        printf(venc);
        //if (venc == 1) printf("Kcaj %d\n", fp1);
        //else if (venc == 2) printf("Ordep %d\n", fp2);
        //else printf("empate\n");
        printf("%d %d", fp1, fp2);
    } else {
        printf("valor fora do limite!");
    }
    partida(n-1);
}

int main() {
    int n;
    scanf("%d", &n);
    partida(n);
    int fp2 = 1978;
    int b = 1455;
    printf("\n%d", mdc(fp2, b));
	return 0;
}
#include<iostream>
#include<stdlib.h>
#include<vector>

using namespace std;

#define ll long long

int main()
{
    ll t;
    cin >> t;
    while(t--){
        ll h,c,t;
        cin >> h >> c >> t;
        if(2*t<=h+c) cout << 2 << endl;
        else if(t>=h) cout << 1 << endl;
        else{
            ll k = (t-h)/(c+h-2*t);
            ll k1 = k;
            ll k2 = k1+1;
            if (llabs((h+c)*k1+h-t*(2*k1+1))*(2*k2+1) <= llabs((h+c)*k2+h-t*(2*k2+1))*(2*k1+1))
                cout << 2*k1+1 << endl;
            else
                cout << 2*k2+1 << endl;
        }
    }
    return 0;
}




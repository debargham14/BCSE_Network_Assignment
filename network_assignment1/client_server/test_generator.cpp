#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
int main () {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    freopen ("test.txt", "w", stdout);

    for (ll i = 0; i < 1 << 16; i++) {
        int k = 16;
        ll value = i;
        string temp = "";
        while(k--) {
            if (value & 1)
                temp += "1";
            else
                temp += "0";
            value /= 2;
        }
        temp += temp;
        reverse(temp.begin(), temp.end());
        cout << temp << "\n";
    }

    return 0;
}

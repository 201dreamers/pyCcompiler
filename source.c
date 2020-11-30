int ccc() {
    int a = 8;
    a /= 4;
    return a;
}

int main() {
    int cc = 8;
    int b = ccc();
    cc /= b;
    return cc * 2;
}

int main() {
	int c = 8;
	int a;
	int b = 1;
	do {
		c /= 2;
		b = b * 2;
		a = c == 1 ? 0 : 1;
	} while (0);
	return b;
}
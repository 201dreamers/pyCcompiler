int fibb_recursion (int n) {
	n = n < 0 ? 0 : n;
	return n < 2 ? n : fibb_recursion(n - 1) + fibb_recursion(n - 2);
}

int fibb_iteration(int n) {
	int res = 0;
	int tmp1 = 0;
	int tmp2 = 1;
	
	int i = 0;
	do {
		res = tmp1 + tmp2;
		tmp1 = tmp2;
		tmp2 = res;
		i = i + 1;
	} while (i < n - 1);

	res = n < 0 ? 0 : res;
	res = n == 1 ? 1 : res;

	return res;
}

int main() {
	return fibb_iteration(6);
}
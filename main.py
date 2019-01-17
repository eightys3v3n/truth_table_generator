import unittest


def tobinary(i, length=0):
    s = "{num:0>{length}b}".format(num=i, length=length)
    b = []
    for c in s:
        b.append(int(c))
    return tuple(b)


def binary_perms(bits):
    largest = 2**bits
    perms = []
    for i in range(0, largest):
        perms.append(tobinary(i, length=bits))
    return tuple(perms)


def truth_table(*, func, args):
    table = []
    perms = binary_perms(len(args))
    for perm in perms:
        table.append((perm, func(*perm)))
    return tuple(table)


def parse_args(func_str):
    args = []
    for c in func_str:
        if c.isalpha() and c.upper() == c:
            args.append(c)
    return tuple(args)


def parse_func(func_str):
    args = parse_args(func_str)
    args_str = str(args).replace("'", "").replace("(", "").replace(")", "")
    func = eval("lambda {}:{}".format(args_str, func_str))
    return func, args


def print_truth_table(func_str):
    func, args = parse_func(func_str)
    table = truth_table(func=func, args=args)
    row_sizes = [1]*(len(args)+1)
    row_sizes[-1] = len(func_str)
    print(str(args).replace("(", "").replace(")", "").replace("'", ""), ", ", func_str, sep="")
    for row in table:
        print(str(row).replace("(", "").replace(")", ""))



class Tests(unittest.TestCase):
    def test_tobinary(self):
        self.assertEqual((0, 0, 0, 0), tobinary(0, length=4))
        self.assertEqual((1, 0, 1, 0), tobinary(10, 4))

    def test_binary_perms(self):
        expect = ((0, 0), (0, 1), (1, 0), (1, 1))
        actual = binary_perms(2)
        self.assertCountEqual(expect, actual)

        expect = ((0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1))
        actual = binary_perms(3)
        self.assertCountEqual(expect, actual)

    def test_truth_table(self):
        expect = (((0, 0), 0),
                  ((0, 1), 0),
                  ((1, 0), 0),
                  ((1, 1), 1))
        actual = truth_table(func=lambda A, B: A and B, args=("A", "B"))
        self.assertEqual(expect, actual)

    def test_parse_args(self):
        self.assertEqual(("A", "B", "C"), parse_args("(A and B) or C"))

    def test_parse_func(self):
        expect = lambda A, B: A and B
        actual, _ = parse_func("A and B")
        for b in binary_perms(2):
            self.assertEqual(expect(*b), actual(*b), "expect({}) != actual({})".format(expect(*b), actual(*b)))


if __name__ == "__main__":
    unittest.main()

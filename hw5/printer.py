from yat.model import *
import sys


class PrettyPrinter:

    def __init__(self):
        self.tabs = ''

    def visit(self, tree):
        tree.accept(self)
        print(';')

    def visit_block(self, exprs):
        if not exprs:
            return
        self.tabs += '    '
        for expr in exprs:
            print(self.tabs, end='')
            expr.accept(self)
            print(';')
        self.tabs = self.tabs[:len(self.tabs) - 4]

    def visit_conditional(self, cond):
        print('if (', end='')
        cond.condtion.accept(self)
        print(') {')
        self.visit_block(cond.if_true)
        print(self.tabs + '}', end='')
        if cond.if_false:
            print(' else {')
            self.visit_block(cond.if_false)
            print(self.tabs + '}', end='')

    def visit_function_definition(self, fd):
        print('def ' + fd.name + '(' + ', '.join(fd.function.args) + ') {')
        self.visit_block(fd.function.body)
        print(self.tabs + '}', end='')

    def visit_print(self, prnt):
        print('print ', end='')
        prnt.expr.accept(self)

    def visit_read(self, read):
        print('read ' + read.name, end='')

    def visit_number(self, nmb):
        print(nmb.value, end='')

    def visit_reference(self, ref):
        print(ref.name, end='')

    def visit_binary_operation(self, bo):
        if bo.lhs.prior >= bo.prior:
            bo.lhs.accept(self)
            print(' ' + bo.op + ' ', end='')
        else:
            print('(', end='')
            bo.lhs.accept(self)
            print(') ' + bo.op + ' ', end='')

        if bo.rhs.prior >= bo.prior:
            bo.rhs.accept(self)
        else:
            print('(', end='')
            bo.rhs.accept(self)
            print(')', end='')

    def visit_unary_operation(self, uo):
        if uo.expr.prior > 6:
            print(uo.op, end='')
            uo.expr.accept(self)
        else:
            print(uo.op + '(', end='')
            io.expr.accept(self)
            print(')', end='')

    def visit_function_call(self, fc):
        print(fc.fun_expr.name, end='')
        print('(', end='')
        if fc.args:
            fl = 0
            for i in fc.args:
                if fl:
                    print(', ', end='')
                else:
                    fl = 1
                i.accept(self)
        print(')', end='')


def redirect_input():
    global tmp
    tmp = sys.stdout
    sys.stdout = open("output", "w")


def redirect_input_back():
    global tmp
    sys.stdout.close()
    fin = open("output", "r")
    inp = fin.read()
    sys.stdout = tmp
    fin.close()
    return inp


def test_number():
    redirect_input()
    ten = Number(10)
    printer = PrettyPrinter()
    printer.visit(ten)
    inp = redirect_input_back()
    assert inp == "10;\n"


def test_reference():
    redirect_input()
    reference = Reference('x')
    printer = PrettyPrinter()
    printer.visit(reference)
    inp = redirect_input_back()
    assert inp == "x;\n"


def test_read():
    redirect_input()
    read = Read('x')
    printer = PrettyPrinter()
    printer.visit(read)
    inp = redirect_input_back()
    assert inp == "read x;\n"


def test_print():
    redirect_input()
    number = Number(42)
    print = Print(number)
    printer = PrettyPrinter()
    printer.visit(print)
    inp = redirect_input_back()
    assert inp == "print 42;\n"


def test_function_definition():
    redirect_input()
    function = Function([], [])
    definition = FunctionDefinition('foo', function)
    printer = PrettyPrinter()
    printer.visit(definition)
    inp = redirect_input_back()
    assert inp == "def foo() {\n};\n"


def test_unary_operation():
    redirect_input()
    number = Number(42)
    unary = UnaryOperation('-', number)
    printer = PrettyPrinter()
    printer.visit(unary)
    inp = redirect_input_back()
    assert inp == "-42;\n"


def test_binary_operation():
    redirect_input()
    n0, n1, n2 = Number(1), Number(2), Number(3)
    add = BinaryOperation(n1, '+', n2)
    mul = BinaryOperation(n0, '*', add)
    printer = PrettyPrinter()
    printer.visit(mul)
    inp = redirect_input_back()
    assert inp == "1 * (2 + 3);\n"


def test_conditional():
    redirect_input()
    number = Number(42)
    conditional = Conditional(number, [], [])
    printer = PrettyPrinter()
    printer.visit(conditional)
    inp = redirect_input_back()
    assert inp == "if (42) {\n};\n"


def test_function_call():
    redirect_input()
    reference = Reference("foo")
    call = FunctionCall(reference, [Number(1), Number(2), Number(3)])
    printer = PrettyPrinter()
    printer.visit(call)
    inp = redirect_input_back()
    assert inp == "foo(1, 2, 3);\n"


def big_test():
    printer = PrettyPrinter()
    scope = Scope()
    q1 = FunctionDefinition('max', Function(('a', 'b'),
                                            [Conditional(BinaryOperation(
                                                Reference('a'),
                                                '>',
                                                Reference('b')),
                                                [Reference('a')],
                                                [Reference('b')])]))

    printer.visit(q1)
    q2 = FunctionDefinition('print_max',
                            Function((),
                                     [Read('x'),
                                      Read('y'),
                                      Print(FunctionCall(q1, [Reference('x'),
                                                              Reference('y')]))]))

    printer.visit(q2)
    printer.visit(FunctionCall(q2, ()))


if __name__ == '__main__':
    test_number()
    test_reference()
    test_read()
    test_print()
    test_function_definition()
    test_unary_operation()
    test_binary_operation()
    test_conditional()
    test_function_call()

    # big_test()

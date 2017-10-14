from yat.model import *


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


def test_number():
    ten = Number(10)
    printer = PrettyPrinter()
    printer.visit(ten)


def test_reference():
    reference = Reference('x')
    printer = PrettyPrinter()
    printer.visit(reference)


def test_read():
    read = Read('x')
    printer = PrettyPrinter()
    printer.visit(read)


def test_print():
    number = Number(42)
    print = Print(number)
    printer = PrettyPrinter()
    printer.visit(print)


def test_function_definition():
    function = Function([], [])
    definition = FunctionDefinition('foo', function)
    printer = PrettyPrinter()
    printer.visit(definition)


def test_unary_operation():
    number = Number(42)
    unary = UnaryOperation('-', number)
    printer = PrettyPrinter()
    printer.visit(unary)


def test_binary_operation():
    n0, n1, n2 = Number(1), Number(2), Number(3)
    add = BinaryOperation(n1, '+', n2)
    mul = BinaryOperation(n0, '*', add)
    printer = PrettyPrinter()
    printer.visit(mul)


def test_conditional():
    number = Number(42)
    conditional = Conditional(number, [], [])
    printer = PrettyPrinter()
    printer.visit(conditional)


def test_function_call():
    reference = Reference("foo")
    call = FunctionCall(reference, [Number(1), Number(2), Number(3)])
    printer = PrettyPrinter()
    printer.visit(call)


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
    # test_number()
    # test_reference()
    # test_read()
    # test_print()
    # test_function_definition()
    # test_unary_operation()
    # test_binary_operation()
    # test_conditional()
    # test_function_call()
    big_test()

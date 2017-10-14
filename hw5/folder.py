from yat.model import *


class ConstantFolder:

    def __init__(self):
        pass

    def visit(self, tree):
        return tree.accept(self)

    def visit_block(self, exprs):
        if not exprs:
            return []
        return [expr.accept(self) for expr in exprs]

    def visit_conditional(self, cond):
        return Conditional(cond.condtion.accept(self),
                           self.visit_block(cond.if_true),
                           self.visit_block(cond.if_false))

    def visit_function_definition(self, fd):
        return fd

    def visit_print(self, prnt):
        return Print(prnt.expr.accept(self))

    def visit_read(self, read):
        return read

    def visit_number(self, nmb):
        return nmb

    def visit_reference(self, ref):
        return ref

    def visit_binary_operation(self, bo):
        lhs = bo.lhs.accept(self)
        rhs = bo.rhs.accept(self)
        fl = isinstance(lhs, Number)
        fr = isinstance(rhs, Number)
        if fl and fr:
            return BinaryOperation(lhs, bo.op, rhs).evaluate(Scope())
        elif fl:
            if lhs.value == 0:
                if bo.op == '*' or bo.op == '&&':
                    return Number(0)
                elif bo.op == '+' or bo.op == '||':
                    return rhs
            elif lhs.value == 1:
                if bo.op == '||':
                    return Number(1)
                elif bo.op == '&&' or bo.op == '*':
                    return rhs
        elif fr:
            if rhs.value == 0:
                if bo.op == '*' or bo.op == '&&':
                    return Number(0)
                elif bo.op == '+' or bo.op == '-' or bo.op == '||':
                    return lhs
            elif rhs.value == 1:
                if bo.op == '||':
                    return Number(1)
                elif bo.op == '&&' or bo.op == '*' or bo.op == '/':
                    return lhs
        elif fl == fr and bo.op == '-':
            return Number(0)
        return BinaryOperation(lhs, bo.op, rhs)

    def visit_unary_operation(self, uo):
        expr = uo.expr.accept(self)
        if isinstance(expr, Number):
            return UnaryOperation(uo.op, expr).evaluate(Scope())
        return UnaryOperation(uo.op, expr)

    def visit_function_call(self, fc):
        fun_expr = fc.fun_expr.accept(self)
        args = [expr.accept(self) for expr in fc.args]
        return FunctionCall(fun_expr, args)

    def visit_function(self, func):
        body = self.visit_block(func.body)
        return Function(func.args, body)


def test_number():
    a = Number(1)
    fld = ConstantFolder()
    b = fld.visit(a)
    assert b == a


def test_binary_operation():
    fld = ConstantFolder()
    a = fld.visit(BinaryOperation(Number(1), '+', Number(2)))
    assert a == Number(3)
    b = fld.visit(BinaryOperation(Number(0), '*', Reference('z')))
    assert b == Number(0)
    c = fld.visit(BinaryOperation(Reference('z'), '*', Number(0)))
    assert c == Number(0)
    d = fld.visit(BinaryOperation(Reference('z'), '-', Reference('z')))
    assert d == Number(0)


def test_unary_operation():
    fld = ConstantFolder()
    assert fld.visit(UnaryOperation('-', Number(2))) == Number(-2)


def test_condition():
    fld = ConstantFolder()
    q = Conditional(BinaryOperation(Number(0), '-', Number(6)), [Number(3)])
    q2 = fld.visit(q)
    assert q2.condtion == Number(-6)

if __name__ == '__main__':
    test_number()
    test_binary_operation()
    test_unary_operation()
    test_condition()

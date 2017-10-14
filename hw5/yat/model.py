class Scope:

    def __init__(self, parent=None):
        self.data = dict()
        self.parent = parent

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        if self.parent:
            return self.parent[key]
        raise KeyError


class Number:

    def __init__(self, value):
        self.value = value
        self.prior = 7

    def evaluate(self, scope):
        return self

    def __eq__(self, other):
        return self.value == other.value

    def accept(self, visitor):
        return visitor.visit_number(self)


class Function:

    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        return self

    def accept(self, visitor):
        return visitor.visit_function(self)


class FunctionDefinition:

    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function

    def accept(self, visitor):
        return visitor.visit_function_definition(self)


class Conditional:

    def __init__(self, condtion, if_true, if_false=None):
        self.condtion = condtion
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        if self.condtion.evaluate(scope).value == 0:
            block = self.if_false
        else:
            block = self.if_true
        res = None
        block = block or []
        for expr in block:
            res = expr.evaluate(scope)
        return res

    def accept(self, visitor):
        return visitor.visit_conditional(self)


class Print:

    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        res = self.expr.evaluate(scope)
        print(res.value)
        return res

    def accept(self, visitor):
        return visitor.visit_print(self)


class Read:

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        value = int(input())
        scope[self.name] = Number(value)

    def accept(self, visitor):
        return visitor.visit_read(self)


class FunctionCall:

    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args
        self.prior = 7

    def evaluate(self, scope):
        function = self.fun_expr.evaluate(scope)
        call_scope = Scope(scope)
        for expr, name in zip(self.args, function.args):
            call_scope[name] = expr.evaluate(scope)
        res = None
        for expr in function.body:
            res = expr.evaluate(call_scope)
        return res

    def accept(self, visitor):
        return visitor.visit_function_call(self)


class Reference:

    def __init__(self, name):
        self.name = name
        self.prior = 7

    def evaluate(self, scope):
        return scope[self.name]

    def __eq__(self, other):
        return self.name == other.name

    def accept(self, visitor):
        return visitor.visit_reference(self)


class BinaryOperation:

    priority = {'||': 0,
                '&&': 1,
                '==': 2, '!=': 2,
                '<': 3, '<=': 3, '>': 3, '>=': 3,
                '-': 4, '+': 4,
                '*': 5, '/': 5, '%': 5}

    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op
        self.prior = self.priority[op]

    def evaluate(self, scope):
        l = self.lhs.evaluate(scope).value
        r = self.rhs.evaluate(scope).value
        op = self.op
        if op == "&&":
            op = "and"
        elif op == "||":
            op = "or"
        elif op == "/":
            op = "//"
        return Number(int(eval(str(l) + ' ' + op + ' ' + str(r))))

    def accept(self, visitor):
        return visitor.visit_binary_operation(self)


class UnaryOperation:

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr
        self.prior = 6

    def evaluate(self, scope):
        v = self.expr.evaluate(scope).value
        if self.op == "-":
            return Number(-v)
        else:
            return Number(int(not bool(v)))

    def accept(self, visitor):
        return visitor.visit_unary_operation(self)

if __name__ == '__main__':
    pass

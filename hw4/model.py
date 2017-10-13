class Scope:

    """Scope - представляет доступ к значениям по именам
    (к функциям и именованным константам).
    Scope может иметь родителя, и если поиск по имени
    в текущем Scope не успешен, то если у Scope есть родитель,
    то поиск делегируется родителю.
    Scope должен поддерживать dict-like интерфейс доступа
    (см. на специальные функции __getitem__ и __setitem__)
    """

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

    """Number - представляет число в программе.
    Все числа в нашем языке целые."""

    def __init__(self, value):
        self.value = value

    def evaluate(self, scope):
        return self

    def __eq__(self, other):
        return self.value == other.value


class Function:

    """Function - представляет функцию в программе.
    Функция - второй тип поддерживаемый языком.
    Функции можно передавать в другие функции,
    и возвращать из функций.
    Функция состоит из тела и списка имен аргументов.
    Тело функции это список выражений,
    т. е.  у каждого из них есть метод evaluate.
    Список имен аргументов - список имен
    формальных параметров функции.
    Аналогично Number, метод evaluate должен возвращать self.
    """

    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        return self


class FunctionDefinition:

    """FunctionDefinition - представляет определение функции,
    т. е. связывает некоторое имя с объектом Function.
    Результатом вычисления FunctionDefinition является
    обновление текущего Scope - в него
    добавляется новое значение типа Function."""

    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function


class Conditional:

    """
    Conditional - представляет ветвление в программе, т. е. if.
    """

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


class Print:

    """Print - печатает значение выражения на отдельной строке."""

    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        res = self.expr.evaluate(scope)
        print(res.value)
        return res


class Read:

    """Read - читает число из стандартного потока ввода
     и обновляет текущий Scope.
     Каждое входное число располагается на отдельной строке
     (никаких пустых строк и лишних символов не будет).
     """

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        value = int(input())
        scope[self.name] = Number(value)


class FunctionCall:

    """
    FunctionCall - представляет вызов функции в программе.
    В результате вызова функции должен создаваться новый объект Scope,
    являющий дочерним для текущего Scope
    (т. е. текущий Scope должен стать для него родителем).
    Новый Scope станет текущим Scope-ом при вычислении тела функции.
    """

    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        function = self.fun_expr.evaluate(scope)
        call_scope = Scope(scope)
        for expr, name in zip(self.args, function.args):
            call_scope[name] = expr.evaluate(scope)
        res = None
        for expr in function.body:
            res = expr.evaluate(call_scope)
        return res


class Reference:

    """Reference - получение объекта
    (функции или переменной) по его имени."""

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


class BinaryOperation:

    """BinaryOperation - представляет бинарную операцию над двумя выражениями.
    Результатом вычисления бинарной операции является объект Number.
    Поддерживаемые операции:
    “+”, “-”, “*”, “/”, “%”, “==”, “!=”,
    “<”, “>”, “<=”, “>=”, “&&”, “||”."""

    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op

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


class UnaryOperation:

    """UnaryOperation - представляет унарную операцию над выражением.
    Результатом вычисления унарной операции является объект Number.
    Поддерживаемые операции: “-”, “!”."""

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        v = self.expr.evaluate(scope).value
        if self.op == "-":
            return Number(-v)
        else:
            return Number(int(not bool(v)))


def example():
    parent = Scope()
    parent["foo"] = Function(('hello', 'world'),
                             [Print(BinaryOperation(Reference('hello'),
                                                    '+',
                                                    Reference('world')))])
    parent["bar"] = Number(10)
    scope = Scope(parent)
    assert 10 == scope["bar"].value
    scope["bar"] = Number(20)
    assert scope["bar"].value == 20
    print('It should print 2: ', end=' ')
    FunctionCall(FunctionDefinition('foo', parent['foo']),
                 [Number(5), UnaryOperation('-', Number(3))]).evaluate(scope)


def test_scope():
    scope1 = Scope()
    scope1["a"] = Number(1)
    scope2 = Scope(scope1)
    scope2["b"] = Number(2)
    assert scope1["a"] == Number(1)
    assert scope2["b"] == Number(2)
    assert scope2["a"] == Number(1)


def test_number():
    scope = Scope()
    a = Number(1)
    assert a.evaluate(scope) == a
    b = Number(1)
    assert b == a


def test_reference():
    scope = Scope()
    scope['a'] = Number(4)
    assert Reference('a').evaluate(scope) == Number(4)


def test_function():
    scope = Scope()
    f = Function(("a", "b"), [BinaryOperation(
        Reference('a'), '+', Reference('b'))])
    assert f.evaluate(scope) == f
    f1 = FunctionDefinition("sum", f)
    f2 = FunctionCall(f1, [Number(1), Number(3)])
    assert f2.evaluate(scope) == Number(4)


def test_read_and_print():
    scope = Scope()
    scope['input'] = Read('a')
    scope['input'].evaluate(scope)
    print('now it should print your number:')
    scope['output'] = Print(Reference('a'))
    scope['output'].evaluate(scope)


def test_binary_operation():
    scope = Scope()
    scope["a"] = Number(9)
    scope["b"] = Number(4)
    scope["a0"] = Number(0)
    scope["a1"] = Number(1)
    plus = BinaryOperation(Reference('a'), '+', Reference('b'))
    minus = BinaryOperation(Reference('a'), '-', Reference('b'))
    mult = BinaryOperation(Reference('a'), '*', Reference('b'))
    div = BinaryOperation(Reference('a'), '/', Reference('b'))
    mod = BinaryOperation(Reference('a'), '%', Reference('b'))
    eq = BinaryOperation(Reference('a'), '==', Reference('b'))
    eq2 = BinaryOperation(Reference('a'), '==', Reference('a'))
    neq = BinaryOperation(Reference('a'), '!=', Reference('b'))
    neq2 = BinaryOperation(Reference('a'), '!=', Reference('a'))
    le = BinaryOperation(Reference('a'), '<', Reference('b'))
    ge = BinaryOperation(Reference('a'), '>', Reference('b'))
    leq = BinaryOperation(Reference('a'), '<=', Reference('b'))
    leq2 = BinaryOperation(Reference('a'), '<=', Reference('a'))
    geq = BinaryOperation(Reference('a'), '>=', Reference('b'))
    geq2 = BinaryOperation(Reference('a'), '>=', Reference('a'))
    _or = BinaryOperation(Reference('a0'), '||', Reference('a1'))
    _and = BinaryOperation(Reference('a0'), '&&', Reference('a1'))
    assert plus.evaluate(scope) == Number(13)
    assert minus.evaluate(scope) == Number(5)
    assert mult.evaluate(scope) == Number(36)
    assert div.evaluate(scope) == Number(2)
    assert mod.evaluate(scope) == Number(1)
    assert eq.evaluate(scope) == Number(0)
    assert eq2.evaluate(scope) == Number(1)
    assert neq.evaluate(scope) == Number(1)
    assert neq2.evaluate(scope) == Number(0)
    assert le.evaluate(scope) == Number(0)
    assert ge.evaluate(scope) == Number(1)
    assert leq.evaluate(scope) == Number(0)
    assert leq2.evaluate(scope) == Number(1)
    assert geq.evaluate(scope) == Number(1)
    assert geq2.evaluate(scope) == Number(1)
    assert _or.evaluate(scope) == Number(1)
    assert _and.evaluate(scope) == Number(0)


def test_unary_operation():
    scope = Scope()
    scope['a'] = Number(4)
    minus = UnaryOperation('-', Reference('a'))
    assert minus.evaluate(scope) == Number(-4)
    _not = UnaryOperation('!', Reference('a'))
    assert _not.evaluate(scope) == Number(0)


def test_condition():
    scope = Scope()
    scope["a"] = Number(0)
    scope["b"] = Number(0)
    c = Conditional(
        BinaryOperation(
            Reference('a'),
            '||',
            Reference('b')),
        [Number(1)],
        [Number(0)])
    assert c.evaluate(scope).value == 0


def my_tests():
    scope = Scope()
    scope["max"] = Function(('a', 'b'),
                            [Conditional(BinaryOperation(
                                Reference('a'),
                                '>',
                                Reference('b')),
                                [Reference('a')],
                                [Reference('b')])])

    scope["print_max"] = Function((),
                                  [Read('x'),
                                   Read('y'),
                                   Print(FunctionCall(FunctionDefinition('max',
                                                                         scope['max']),
                                                      [Reference('x'),
                                                       Reference('y')]))])
    print('it should print the max of your numbers:')
    FunctionCall(FunctionDefinition('print_max', scope[
                 'print_max']), []).evaluate(scope)


if __name__ == '__main__':
    test_scope()
    test_number()
    test_reference()
    # test_read_and_print()
    test_function()
    test_binary_operation()
    test_unary_operation()
    test_condition()
    # example()
    # my_tests()

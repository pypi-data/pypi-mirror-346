import re
import ast
import inspect


class IndentationManager:
    """
    Keeps track of indentation and scope for an AstTranslator
    """

    def __init__(self, converter, class_name=None, in_function=None):
        self.converter = converter
        self.class_name = class_name or converter.class_name
        self.in_function = in_function if in_function is not None else converter.in_function
        self.start_class_name = converter.class_name
        self.start_in_method = converter.in_method
        self.start_in_function = converter.in_function

    def __enter__(self):
        if self.class_name and self.in_function:
            self.converter.in_method = True
        self.converter.in_function = self.in_function
        self.converter.class_name = self.class_name
        self.converter.indent_up()

    def __exit__(self, *a):
        self.converter.in_function = self.start_in_function
        self.converter.in_method = self.start_in_method
        self.converter.class_name = self.start_class_name
        self.converter.indent_down()


class SourceCode:
    """
    Python source code wrapper / parser
    """

    def __init__(self, source):
        if isinstance(source, ast.AST):
            self.source = ast.unparse(source)
            self.ast = ast
            self.comments = CommentData("")
        else:
            self.source = source
            self.comments = CommentData(source)
            self.ast = ast.parse(source, type_comments=True)


class CommentData:
    """
    Class keeping track of comments present in the source but discarded by the AST
    """

    RE_COMMENT = re.compile(r"^\s*(.+)?# ?(.*)$")
    RE_ELSE = re.compile(r"^\s*(else|elif .*):")

    class Comment:
        def __init__(self, line, text, is_tail, is_else):
            self.line = line
            self.text = text
            self.is_tail = is_tail
            self.is_else = is_else
            self.is_line = not is_else and not is_tail

    class CommentReader:
        def __init__(self, comments):
            self.comments = comments
            self.next_line = None
            self.current_line = 0
            self.index = 0
            self.get_next()

        def prepare(self, node):
            if hasattr(node, "lineno"):
                self.current_line = node.lineno

        def get_next(self):
            self.next_line = self.current_comment().line if self.index < len(self.comments) else None

        def current_comment(self):
            return self.comments[self.index]

        def has_line_comment(self):
            if self.next_line is None:
                return False

            if self.current_line >= self.next_line:
                return self.current_comment().is_line

            return False

        def has_tail_comment(self):
            if self.next_line is None:
                return False

            if self.current_line >= self.next_line:
                return self.current_comment().is_tail

            return False

        def has_else(self):
            if self.next_line is None:
                return False

            if self.current_line >= self.next_line:
                return self.current_comment().is_else

            return False

        def get_comment(self):
            return self.current_comment().text

        def next(self):
            self.index += 1
            self.get_next()

        def skip_newline(self):
            if self.next_line and self.current_line + 1 >= self.next_line:
                if self.current_comment().is_line and self.current_comment().text is None:
                    self.next()

    def __init__(self, source):
        self.comments = []

        for lineno, line in enumerate(source.splitlines()):
            melse = self.RE_ELSE.match(line)
            if melse:
                self.comments.append(self.Comment(lineno + 1, None, False, True))

            match = self.RE_COMMENT.match(line)
            if match:
                self.add_comment(lineno + 1, match.group(2), match.group(1) is not None)
            elif line.strip() == "":
                self.add_empty(lineno + 1)

    def add_comment(self, line, text, is_tail):
        self.comments.append(self.Comment(line, text, is_tail, False))

    def add_empty(self, line):
        self.comments.append(self.Comment(line, None, False, False))

    def reader(self):
        return self.CommentReader(self.comments)


class Range:
    """
    AST range / slice helper
    """

    def __init__(self, ast_node, translator, start=None, stop=None, step=None):
        self.ast_node = ast_node
        self.start = None
        self.stop = None
        self.step = None
        self.translator = translator
        if stop is None and start is None and step is None:
            if len(ast_node.args) == 1:
                self.stop = translator.expression_to_string(ast_node.args[0], False)
            else:
                self.start = translator.expression_to_string(ast_node.args[0], False)
                self.stop = translator.expression_to_string(ast_node.args[1], False)
                if len(ast_node.args) > 2:
                    self.step = translator.expression_to_string(ast_node.args[2], False)
        else:
            if start is not None:
                self.start = translator.expression_to_string(start, False)
            if stop is not None:
                self.stop = translator.expression_to_string(stop, False)
            if step is not None:
                self.step = translator.expression_to_string(step, False)

    def fill_defaults(self, step=False):
        if self.start is None:
            self.start = self.translator.expression_to_string(ast.Constant(0), False)
        if step and self.step is None:
            self.step = self.translator.expression_to_string(ast.Constant(1), False)

    def __str__(self):
        return self.translator.expression_to_string(self.ast_node, False)


def build_precedence_map(*operators):
    """
    Used to build AstTranslator.operator_precedence from lists of operators in decreasing precedence
    """

    prec = len(operators)
    out = {}
    for op_rank in operators:
        for op in op_rank:
            out[op] = prec
        prec -= 1
    return out


class AstTranslator:
    """
    Base class that processes an AST and converts it into different code
    """

    ops = {}
    operator_precedence = {}

    def __init__(self, indent_style=None):
        self.indent_style = indent_style or IndentationStyle()
        self.naming_style = str
        self.indent_level = 0
        self.output = ""
        self.class_name = None
        self.in_method = False
        self.in_function = False
        self.scope = [{}]

    def convert(self, source: SourceCode):
        self.output = ""
        self.comments = source.comments.reader()
        self.convert_ast(source.ast)
        return self.output

    def push_scope(self):
        self.scope.insert(0, {})

    def pop_scope(self):
        self.scope.pop(0)

    def var_add(self, var, type=None):
        if type is None:
            type = ""
        elif not isinstance(type, str):
            type = self.expression_to_string(type, True)
        self.scope[0][var] = type

    def get_var_type(self, var):
        for scope in self.scope:
            if var in scope:
                return scope[var]
        return ""

    def has_var(self, var):
        for scope in self.scope:
            if var in scope:
                return True
        return False

    def maybe_range(self, ast_node):
        if isinstance(ast_node, ast.Call) and isinstance(ast_node.func, ast.Name) and ast_node.func.id == "range":
            return Range(ast_node, self)
        return self.expression_to_string(ast_node, False)

    def indent_string(self, offset=0):
        return self.indent_style.indent_string(self.indent_level + offset)

    def unknown(self, obj, as_string=False):
        msg = repr(obj)
        if isinstance(obj, ast.AST):
            msg += "\n" + ast.dump(obj, indent=4)
        raise ValueError(msg)
        # unknown = "\n" + msg + "\n"
        # if as_string:
        #     return unknown
        # self.output += unknown

    def process_line_comments(self):
        while self.comments.has_line_comment():
            comment = self.comments.get_comment()
            if comment is None:
                self.output += "\n"
            else:
                self.output += self.indent_string() + self.convert_line_comment(comment) + "\n"
            self.comments.next()

    def find_else(self, lineno):
        self.comments.current_line = lineno

    def push_code(self, code, line_comments=True, indent_offset=0):
        if line_comments:
            self.process_line_comments()
        if self.comments.has_else():
            self.comments.next()

        self.output += self.indent_string(indent_offset) + code

        if self.comments.has_tail_comment():
            self.output += " " + self.convert_line_comment(self.comments.get_comment())
            self.comments.next()

        self.output += "\n"

    def indent_up(self):
        self.indent_level += 1

    def indent_down(self):
        self.indent_level -= 1

    def format_comment(self, comment):
        self.push_code(comment)

    def format_doc_comment(self, comment):
        self.format_comment(comment)

    def convert_doc_comment(self, body):
        if len(body) > 0 and isinstance(body[0], ast.Expr):
            expr = body[0].value
            if isinstance(expr, ast.Constant) and isinstance(expr.value, str):
                comment = expr.value
                if comment.startswith("!"):
                    comment = comment[1:]
                self.format_doc_comment(inspect.cleandoc(comment).splitlines())
                return body[1:]
        return body

    def function_def(self, name, args, returns, body, is_async, is_method, is_getter):
        raise NotImplementedError

    def values_to_string(self, *args, annotation=False):
        return tuple(self.expression_to_string(v, annotation) for v in args)

    def begin_class(self, obj):
        raise NotImplementedError

    def end_block(self):
        pass

    def declare(self, target, annotation, value, ast_value):
        raise NotImplementedError

    def assign(self, targets, value):
        raise NotImplementedError

    def assign_op(self, target, op, value):
        raise NotImplementedError

    def begin_if(self, expr):
        raise NotImplementedError

    def begin_elif(self, expr):
        raise NotImplementedError

    def begin_for(self, target, iter, is_async):
        raise NotImplementedError

    def begin_else(self):
        raise NotImplementedError

    def begin_while(self, cond):
        raise NotImplementedError

    def basic_statement(self, statement):
        raise NotImplementedError

    def return_statement(self, value):
        breakpoint()
        raise NotImplementedError

    def begin_switch(self, expr):
        raise NotImplementedError

    def begin_switch_case(self, pattern):
        raise NotImplementedError

    def end_switch_case(self):
        raise NotImplementedError

    def import_statement(self, obj):
        raise NotImplementedError

    def import_from_statement(self, obj):
        raise NotImplementedError

    def delete_statement(self, targets):
        raise NotImplementedError

    def type_alias(self, name, value):
        raise NotImplementedError

    def expr_func(self, name, args):
        raise NotImplementedError

    def expression_statement(self, v):
        self.push_code(v)

    def convert_ast(self, obj):
        self.comments.prepare(obj)

        match obj:
            case ast.Module():
                self.convert_ast(obj.body)
            case list():
                self.push_scope()
                for code in obj:
                    self.convert_ast(code)
                self.pop_scope()
            case ast.ClassDef():
                body = self.convert_doc_comment(obj.body)
                self.begin_class(obj.name)
                with IndentationManager(self, obj.name):
                    self.convert_ast(body)
                self.end_block()
            case ast.Expr():
                self.convert_ast(obj.value)
            case ast.FunctionDef() | ast.AsyncFunctionDef():
                body = self.convert_doc_comment(obj.body)
                is_async = isinstance(obj, ast.AsyncFunctionDef)
                is_getter = False
                is_method = self.class_name is not None

                if is_method:
                    for deco in obj.decorator_list:
                        if isinstance(deco, ast.Name) and deco.id == "property":
                            is_getter = True

                self.in_function = True
                returns = self.expression_to_string(obj.returns, True) if obj.returns else None
                self.push_scope()
                self.function_def(obj.name, obj.args, returns, body, is_async, is_method, is_getter)
                self.in_function = False
                self.pop_scope()
            case ast.Assign():
                targets = list(map(self.expression_to_string, obj.targets))
                value = self.expression_to_string(obj.value)
                self.assign(targets, value)
            case ast.AnnAssign():
                target = self.expression_to_string(obj.target)
                annotation = self.expression_to_string(obj.annotation, annotation=True)
                value = self.expression_to_string(obj.value) if obj.value else None
                self.var_add(target, annotation)
                self.declare(target, annotation, value, obj.value)
            case ast.If():
                self.begin_if(self.expression_to_string(obj.test))
                with IndentationManager(self, None):
                    self.convert_ast(obj.body)
                while obj.orelse:
                    self.find_else(getattr(obj.orelse[0], "lineno", obj.end_lineno))
                    if len(obj.orelse) == 1 and isinstance(obj.orelse[0], ast.If):
                        obj = obj.orelse[0]
                        self.begin_elif(self.expression_to_string(obj.test))
                        with IndentationManager(self, None):
                            self.convert_ast(obj.body)
                    else:
                        self.begin_else()
                        with IndentationManager(self, None):
                            self.convert_ast(obj.orelse)
                        break
                self.end_block()
            case ast.Constant():
                self.format_comment(inspect.cleandoc(str(obj.value)).splitlines())
            case ast.expr():
                self.expression_statement(self.expression_to_string(obj))
            case ast.Continue():
                self.basic_statement("continue")
            case ast.Break():
                self.basic_statement("break")
            case ast.Return():
                self.return_statement(None if obj.value is None else self.expression_to_string(obj.value))
            case ast.AugAssign():
                self.assign_op(*self.values_to_string(obj.target, obj.op, obj.value))
            case ast.For() | ast.AsyncFor():
                is_async = isinstance(obj, ast.AsyncFor)
                target = self.expression_to_string(obj.target)
                iter = self.maybe_range(obj.iter)
                self.begin_for(target, iter, is_async)
                with IndentationManager(self, None):
                    self.convert_ast(obj.body)
                self.end_block()
            case ast.While():
                cond = self.expression_to_string(obj.test)
                self.begin_while(cond)
                with IndentationManager(self, None):
                    self.convert_ast(obj.body)
                self.end_block()
            case ast.Pass():
                pass
            case ast.Match():
                expr = self.expression_to_string(obj.subject)
                self.begin_switch(expr)
                with IndentationManager(self, None):
                    self.convert_ast(obj.cases)
                self.end_block()
            case ast.match_case():
                if isinstance(obj.pattern, ast.MatchAs) and obj.pattern.name is None:
                    pattern = None
                else:
                    pattern = self.expression_to_string(obj.pattern)
                self.begin_switch_case(pattern)
                with IndentationManager(self, None):
                    self.convert_ast(obj.body)
                    self.end_switch_case()
            case ast.Import():
                self.import_statement(obj)
            case ast.ImportFrom():
                self.import_from_statement(obj)
            case ast.Delete():
                self.delete_statement(map(self.expression_to_string, obj.targets))
            case ast.TypeAlias():
                name = self.expression_to_string(obj.name, False)
                value = self.expression_to_string(obj.value, True)
                self.type_alias(name, value)
            case _:
                self.unknown(obj)

    def convert_constant(self, value, annotation):
        return repr(value)

    def convert_name(self, name, annotation):
        return name

    def expr_unop(self, op, value):
        return "%s%s" % (op, value)

    def expr_binop(self, op, *operands):
        return (" %s " % op).join(operands)

    def other_expression(self, value, annotation):
        return self.unknown(value, True)

    def expr_attribute(self, object, member):
        return "%s.%s" % (object, member)

    def convert_line_comment(self, comment):
        raise NotImplementedError

    def expr_generator(self, obj, generator, target, iter, body, ifs, annotation):
        raise NotImplementedError

    def expr_bracket(self, operator, operand, annotation):
        operand_string = self.expression_to_string(operand, annotation)

        if isinstance(operand, (ast.BinOp, ast.BoolOp)):
            op_str = self.expression_to_string(operand.op, annotation)
        elif isinstance(operand, ast.Compare):
            op_str = self.expression_to_string(operand.ops[0], annotation)
        elif isinstance(operand, ast.IfExp):
            op_str = "if"
        else:
            return operand_string

        inner_precedence = self.operator_precedence.get(op_str, 0)
        outer_precedence = self.operator_precedence.get(operator, 0)
        if inner_precedence < outer_precedence:
            return "(%s)" % operand_string

        return operand_string

    def expr_await(self, value):
        return value

    def expression_to_string(self, value, annotation=False):
        match value:
            case ast.Constant():
                return self.convert_constant(value.value, annotation)
            case ast.Name():
                return self.convert_name(value.id, annotation)
            case ast.Attribute():
                object = self.expression_to_string(value.value, annotation)
                member = value.attr
                return self.expr_attribute(object, member)
            case ast.cmpop() | ast.operator() | ast.unaryop() | ast.boolop():
                return self.ops[value.__class__.__name__]
            case ast.Call():
                name = self.expression_to_string(value.func, annotation)
                args = [self.expression_to_string(v, annotation) for v in value.args]
                return self.expr_func(name, args)
            case ast.BinOp():
                op = self.expression_to_string(value.op, annotation)
                return self.expr_binop(
                    op,
                    self.expr_bracket(op, value.left, annotation),
                    self.expr_bracket(op, value.right, annotation)
                )
            case ast.UnaryOp():
                return self.expr_unop(*self.values_to_string(value.op, value.operand, annotation=annotation))
            case ast.BoolOp():
                op = self.expression_to_string(value.op, annotation)
                return self.expr_binop(op, *(
                    self.expr_bracket(op, v, annotation)
                    for v in value.values
                ))
            case ast.Tuple():
                return self.expr_sequence_literal_converter(value.elts, tuple, annotation)
            case ast.List():
                return self.expr_sequence_literal_converter(value.elts, list, annotation)
            case ast.Set():
                return self.expr_sequence_literal_converter(value.elts, set, annotation)
            case ast.Compare():
                return self.expr_compare(value, annotation)
            case ast.MatchValue():
                return self.expression_to_string(value.value, annotation)
            case ast.Dict():
                return self.expr_dict(
                    self.values_to_string(*it, annotation=annotation)
                    for it in zip(value.keys, value.values)
                )
            case ast.IfExp():
                return self.expr_if(*self.values_to_string(value.test, value.body, value.orelse, annotation=annotation))
            case ast.Subscript():
                value_str = self.expression_to_string(value.value, annotation=annotation)
                if isinstance(value.slice, ast.Slice):
                    index = Range(value.slice, self, value.slice.lower, value.slice.upper, value.slice.step)
                    return self.expr_subscript_range(value_str, index)
                else:
                    index = self.expression_to_string(value.slice, annotation=annotation)
                    return self.expr_subscript(value_str, index)
            case ast.Starred():
                return self.expr_starred(self.expression_to_string(value.value, annotation))
            case ast.Await():
                return self.expr_await(self.expression_to_string(value.value, annotation))
            case ast.GeneratorExp() | ast.ListComp() | ast.SetComp():
                generator = value.generators[0]  # TODO can it have more than 1?
                # TODO range
                iter = self.maybe_range(generator.iter)
                ifs = generator.ifs
                target = self.expression_to_string(generator.target, annotation)
                body = self.expression_to_string(value.elt, annotation)
                return self.expr_generator(value, generator, target, iter, body, ifs, annotation)
            case ast.Lambda():
                return self.expr_lambda(value.args, self.expression_to_string(value.body))

        return self.other_expression(value, annotation)

    def expr_sequence_literal_converter(self, elements, type, annotation):
        return self.expr_sequence_literal([self.expression_to_string(v, annotation) for v in elements], type)

    def expr_sequence_literal(self, elements, type):
        raise NotImplementedError

    def expr_compare(self, value, annotation):
        raise NotImplementedError

    def expr_dict(self, items):
        raise NotImplementedError

    def expr_if(self, cond, then, otherwise):
        raise NotImplementedError

    def expr_subscript_range(self, value, index):
        raise NotImplementedError

    def expr_subscript(self, value, index):
        raise NotImplementedError

    def expr_starred(self, value):
        raise NotImplementedError

    def expr_lambda(self, args, expr):
        raise NotImplementedError()


class IndentationStyle:
    def __init__(self, spaces=4, character=" "):
        self.spaces = spaces
        self.character = character

    def indent_string(self, level):
        return int(level * self.spaces) * self.character

    def begin_block(self, translator: AstTranslator, header: str):
        raise NotImplementedError

    def mid_block(self, translator: AstTranslator, header: str):
        raise NotImplementedError

    def end_block(self, translator: AstTranslator):
        raise NotImplementedError

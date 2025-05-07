from ..python_source import Range
from ..c_like import CLike


class PhpTranslator(CLike):
    ops = {
        **CLike.ops,
        "Is": "===",
        "IsNot": "!==",
    }
    keywords = {}

    def function_def(self, name, args, returns, body, is_async, is_method, is_getter):
        start = "function "
        suffix = ""

        if returns:
            suffix = ": %s" % returns

        if is_method:
            if name == "__init__":
                name = "__construct"
            elif name == "__repr__" or name == "__str__":
                name = "__toString"
            elif name == "__call__":
                name = "__invoke"

        start += "%s(" % self.styled_name(name)

        args_start = 0
        if self.class_name and len(args.args) > 0 and args.args[0].arg in ("self", "cls"):
            args_start = 1

        start += self.function_params(args, args_start) + ")" + suffix
        self.function_body(start, body)

    def function_params(self, args, args_start):
        ts_args = []
        for i in range(args_start, len(args.args)):
            ts_arg = ""
            arg_name = self.styled_name(args.args[i].arg)
            if args.args[i].annotation is not None:
                ts_arg = self.expression_to_string(args.args[i].annotation, True) + " "
            ts_arg += self.var_name(arg_name)

            reverse_i = len(args.args) - i
            if reverse_i <= len(args.defaults):
                ts_arg += " = %s" % self.expression_to_string(args.defaults[-reverse_i])
            ts_args.append(ts_arg)
            self.var_add(arg_name)

        return ", ".join(ts_args)

    def var_name(self, name):
        return "$" + name

    def declare(self, target, annotation, value, ast_value):
        code = ""
        if self.class_name and not self.in_method:
            code = "static "

        name = self.styled_name(target)
        code += self.var_name(name)
        self.var_add(name)

        if value:
            code += " = %s" % value
        self.push_code(code + ";")

    def begin_for(self, target, iter, is_async):
        if isinstance(iter, Range):
            code_start = "for "
            iter.fill_defaults(False)
            code_start += "( $%s = %s; " % (target, iter.start)
            code_start += "%s < %s; " % (target, iter.stop)
            if iter.step is None:
                code_start += "$%s++" % (target)
            else:
                code_start += "$%s += %s" % (target, iter.step)
            code_start += " )"
        else:
            code_start = "foreach ( %s as $%s )" % (iter, target)
        self.begin_block(code_start)
        self.var_add(target.lstrip("$"))

    def delete_statement(self, targets):
        self.push_code("delete %s;" % ", ".join(targets))

    def convert_constant(self, value, annotation):
        if value is None:
            return "null"
        return super().convert_constant(value, annotation)

    def convert_name(self, name, annotation):
        if name in ("list", "tuple"):
            return "array"
        if name in ("str"):
            return "string"

        converted = super().convert_name(name, annotation)
        if self.has_var(converted):
            return "$" + converted
        return converted

    def expr_func(self, name, args):
        if name[0].isupper() and name.isalnum():
            name = "new %s" % name
        return super().expr_func(name, args)

    def expr_attribute(self, object, member):
        if object == "math":
            if member == "pi":
                return "M_PI"
            return member
        return "%s->%s" % (object, self.styled_name(member))

    def expr_sequence_literal(self, elements, type):
        if type is set:
            return "new Set([%s])" % ", ".join(elements)
        return "[%s]" % ", ".join(elements)

    def expr_dict(self, items):
        return "[%s]" % ", ".join("%s => %s" % item for item in items)

    def import_statement(self, obj):
        base = obj.module.replace(".", "\\") + "\\"
        for alias in obj.names:
            use = "use %s" % (base + alias.name)
            if alias.asname:
                use += " as %s" % alias.asname
            self.push_code(use + ";")

    def import_from_statement(self, obj):
        self.import_statement(obj)

    def expr_lambda(self, args, expr):
        return "function(%s){return %s;}" % (self.function_params(args, 0), expr)

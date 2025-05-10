from .tokens import Token, TokenType
from .exceptions import ExitREPL
import importlib, datetime, itertools


class Interpreter:
    def __init__(self):
        self.symbols = {}  # 符号表
        self.libraries = {}  # 存储已导入的库
        self.functions = {}  # 存储函数定义

    def visit_FUNC_DEF(self, node):
        # 将函数定义存储到全局符号表中
        self.symbols[node['name']] = {
            'type': 'FUNCTION',
            'params': node['params'],
            'body': node['body']
        }
        return None

    def visit_FUNC_CALL(self, node):
        # 获取函数定义
        func = self.symbols.get(node['name'])
        if not func or func.get('type') != 'FUNCTION':
            raise Exception(f"Function {node['name']} not defined")

        # 绑定参数
        params = func['params']
        args = node['args']
        if len(params) != len(args):
            raise Exception(f"Args are not match: need {len(params)}，got {len(args)}")

        # 创建新作用域
        old_symbols = self.symbols.copy()
        local_symbols = {param: self.visit(arg) for param, arg in zip(params, args)}

        # 执行函数体
        result = None
        for stmt in func['body']:
            # 使用局部符号表
            self.symbols.update(local_symbols)
            result = self.visit(stmt)
            if stmt['type'] == 'RETURN':
                break

        # 恢复作用域
        self.symbols = old_symbols
        return result

    def visit_RETURN(self, node):
        return self.visit(node['value'])

    def visit_VERSION_CALL(self, node):
        current_year = datetime.datetime.now().year
        return f"JxLang 0.3.126 2025-{current_year}"

    def visit_CITE(self, node):
        module_path = node['path']
        alias = node['alias']
        try:
            # 直接导入完整路径的模块
            full_path = '.'.join(module_path)
            current = importlib.import_module(full_path)

            # 存储到符号表
            module_name = alias if alias else module_path[-1]  # 使用别名或最后一个名称
            self.libraries[module_name] = current
            self.symbols[module_name] = current

            return current
        except ModuleNotFoundError:
            raise Exception(f"Python library '{full_path}' not found")
        except AttributeError:
            raise Exception(f"Module '{full_path}' has no attribute '{module_path[-1]}'")

    def visit_MEMBER_ACCESS(self, node):
        obj = self.visit(node['object'])
        member = node['member']

        if isinstance(obj, dict) and obj.get('type') == 'STRUCT_INSTANCE':
            if member not in obj['members']:
                raise Exception(f"Undefined member '{member}' in struct {obj['struct_type']}")
            # 获取成员值
            member_value = obj['members'][member]
            # 如果成员值是AST节点，则访问其实际值
            if isinstance(member_value, dict):
                if member_value.get('type') == 'STRUCT_INSTANCE':
                    return member_value  # 返回结构体实例，以便继续访问其成员
                elif 'type' in member_value:
                    return self.visit(member_value)
            return member_value
        else:
            raise Exception(f"Cannot access member '{member}' on non-struct object")

    def visit_CALL(self, node):
        # 解析函数对象
        func = self.visit(node['func'])
        # 解析参数
        args = []
        for arg in node['args']:
            value = self.visit(arg)
            # 如果是JX_LIST类型，转换为普通Python列表
            if isinstance(value, dict) and value.get('type') == 'JX_LIST':
                args.append(value['data'])
            else:
                args.append(value)

        # 检查是否是我们的函数定义
        if isinstance(func, dict) and func.get('type') == 'FUNCTION':
            # 创建新作用域
            old_symbols = self.symbols.copy()
            local_symbols = {param: arg for param, arg in zip(func['params'], args)}

            # 执行函数体
            result = None
            for stmt in func['body']:
                # 使用局部符号表
                self.symbols.update(local_symbols)
                result = self.visit(stmt)
                if stmt['type'] == 'RETURN':
                    break

            # 恢复作用域
            self.symbols = old_symbols
            return result
        else:
            # 调用 Python 函数
            try:
                return func(*args)
            except Exception as e:
                raise Exception(f"Error calling function: {str(e)}")

    def visit_BIN_OP(self, node):
        left = self.visit(node['left'])
        right = self.visit(node['right'])
        op = node['op']

        if op == TokenType.PLUS:
            return left + right
        elif op == TokenType.MINUS:
            return left - right
        elif op == TokenType.MUL:
            return left * right
        elif op == TokenType.DIV:
            return left / right  # 注意除零错误
        elif op == TokenType.MOD:
            return left % right
        else:
            raise Exception("Unknown operator")

    # 处理列表求值
    def visit_LIST(self, node):
        # 这个方法处理 table(...) 和 [...] 语法解析出的列表节点
        # 假设解析器生成的节点类型是 'LIST'，包含 'value' 或 'elements'
        elements = node.get('value', node.get('elements', []))
        evaluated_elements = [self.visit(elem) for elem in elements]
        return {'type': 'JX_LIST', 'data': evaluated_elements, 'outlist': []}

    def visit_INDEX_ACCESS(self, node):
        obj_wrapper = self.visit(node['object'])
        index = self.visit(node['index'])
        if isinstance(obj_wrapper, dict) and obj_wrapper.get('type') == 'JX_LIST':
            # 访问包装器内部的 data 列表
            data_list = obj_wrapper['data']
            if not isinstance(index, int):
                raise Exception(f"List index must be int，but got {type(index).__name__}")
            if 0 <= index < len(data_list):
                return data_list[index]
            else:
                raise Exception(f"Index {index} out of bounds")
        elif isinstance(obj_wrapper, list):  # 支持访问普通Python列表（例如嵌套列表的子列表）
            if not isinstance(index, int):
                raise Exception(f"List index must be int，but got {type(index).__name__}")
            if 0 <= index < len(obj_wrapper):
                return obj_wrapper[index]
            else:
                raise Exception(f"Index {index} out of bounds")
        else:
            raise Exception("Index access can only be used for lists or JX_LIST wrappers")

    # 处理布尔值
    def visit_BOOL(self, node):
        return node['value']

    # 处理浮点数
    def visit_FLOAT(self, node):
        return node['value']

    # 处理字符串
    def visit_STRING(self, node):
        return node['value']

    def visit(self, node):
        method_name = f'visit_{node["type"]}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{node['type']} method")

    def visit_LET(self, node):
        for var_name, value_node in node['vars']:
            value = self.visit(value_node)

            # 处理成员访问链
            if isinstance(var_name, dict) and var_name.get('type') == 'MEMBER_ACCESS_CHAIN':
                chain = var_name['chain']
                # 获取最外层的对象
                current_obj = self.symbols[chain[0]]
                if not isinstance(current_obj, dict) or current_obj.get('type') != 'STRUCT_INSTANCE':
                    raise Exception(f"Variable {chain[0]} is not a struct instance")

                # 遍历成员链直到倒数第二个成员
                for member in chain[1:-1]:
                    if member not in current_obj['members']:
                        raise Exception(f"Undefined member '{member}' in struct {current_obj['struct_type']}")
                    current_obj = current_obj['members'][member]
                    if not isinstance(current_obj, dict) or current_obj.get('type') != 'STRUCT_INSTANCE':
                        raise Exception(f"Member '{member}' is not a struct instance")

                # 设置最后一个成员的值
                last_member = chain[-1]
                if last_member not in current_obj['members']:
                    raise Exception(f"Undefined member '{last_member}' in struct {current_obj['struct_type']}")
                current_obj['members'][last_member] = value

            # 处理索引访问
            elif isinstance(var_name, dict) and var_name.get('type') == 'INDEX_ACCESS':
                list_var_name = var_name['object']
                if isinstance(list_var_name, dict) and list_var_name.get('type') == 'VAR':
                    list_var_name = list_var_name['value']

                if list_var_name not in self.symbols:
                    raise Exception(f"Undefined variable {list_var_name}")

                target_obj_wrapper = self.symbols[list_var_name]
                if not (isinstance(target_obj_wrapper, dict) and target_obj_wrapper.get('type') == 'JX_LIST'):
                    raise Exception(f"Variable {list_var_name} is not an assignable list")

                target_obj = target_obj_wrapper['data']
                target_index = self.visit(var_name['index'])
                if not isinstance(target_index, int):
                    raise Exception("List index must be an integer")

                if 0 <= target_index < len(target_obj):
                    target_obj[target_index] = value
                else:
                    raise Exception(f"Index {target_index} out of bounds for list {list_var_name}")

            # 处理普通变量赋值
            else:
                if not isinstance(var_name, str):
                    if isinstance(var_name, dict) and var_name.get('type') == 'VAR':
                        var_name = var_name['value']
                    else:
                        raise Exception("Invalid variable name structure in LET")

                if isinstance(value, dict) and value.get('type') == 'JX_LIST':
                    self.symbols[var_name] = value
                else:
                    self.symbols[var_name] = value
        return None

    def visit_FOR_LOOP(self, node):
        variables = node['vars']
        iterable_spec = node['iterable_spec']
        body_statements = node['body']  # 现在是一个语句列表
        num_vars = len(variables)

        if iterable_spec['type'] == 'RANGE':
            start = self.visit(iterable_spec['start'])
            end = self.visit(iterable_spec['end'])
            if not isinstance(start, int) or not isinstance(end, int):
                raise Exception("Loop range limits must be integers")

            ranges = [range(start, end + 1)] * num_vars

            for values in itertools.product(*ranges):
                original_symbols = self.symbols
                loop_scope = original_symbols.copy()
                for var, val in zip(variables, values):
                    loop_scope[var] = val
                self.symbols = loop_scope
                try:
                    # 执行循环体中的每条语句
                    for stmt in body_statements:
                        self.visit(stmt)
                finally:
                    self.symbols = original_symbols

        elif iterable_spec['type'] == 'ITERABLE':
            iterable_value = self.visit(iterable_spec['source'])
            actual_iterable = None
            if isinstance(iterable_value, dict) and iterable_value.get('type') == 'JX_LIST':
                actual_iterable = iterable_value['data']
            else:
                actual_iterable = iterable_value

            try:
                iterator = iter(actual_iterable)
            except TypeError:
                raise Exception(
                    f"Loop source must be an iterable (like list or string). Got: {type(actual_iterable).__name__}")

            for item in iterator:
                original_symbols = self.symbols
                loop_scope = original_symbols.copy()

                if num_vars == 1:
                    loop_scope[variables[0]] = item
                else:
                    try:
                        if len(item) != num_vars:
                            raise ValueError(f"Cannot unpack {len(item)} items into {num_vars} variables.")
                        for i, var in enumerate(variables):
                            loop_scope[var] = item[i]
                    except TypeError:
                        raise Exception(f"Cannot unpack item of type {type(item).__name__} into {num_vars} variables.")
                    except ValueError as e:
                        raise Exception(str(e))

                self.symbols = loop_scope
                try:
                    # 执行循环体中的每条语句
                    for stmt in body_statements:
                        self.visit(stmt)
                finally:
                    self.symbols = original_symbols

        else:
            raise Exception(f"Internal error: Unknown iterable spec type '{iterable_spec['type']}'")

        return None

    def visit_TABLE(self, node):
        # 这个方法处理 table(...) 语法解析出的嵌套列表节点
        evaluated_sublists = [self.visit(sublist) for sublist in node['value']]
        # 对于嵌套列表，我们目前只返回嵌套的Python列表，暂不支持嵌套的outlist
        # 如果需要支持，这里的结构需要更复杂
        return [sublist['data'] for sublist in evaluated_sublists if
                isinstance(sublist, dict) and sublist.get('type') == 'JX_LIST']

    def visit_INT(self, node):
        return node['value']

    def visit_VAR(self, node):
        var_name = node['value']
        if var_name in self.symbols:
            # 如果是列表包装器，返回包装器本身，否则返回值
            return self.symbols[var_name]
        else:
            raise Exception(f"Undefined variable {var_name}")

    # 处理 enter()
    def visit_ENTER_CALL(self, node):
        user_input = input()
        try:
            return int(user_input)  # 尝试转为整数
        except ValueError:
            try:
                return float(user_input)  # 尝试转为浮点数
            except ValueError:
                return user_input  # 保留为字符串

    # 处理 say(expr)
    def visit_SAY(self, node):
        value = self.visit(node['expr'])
        print(value)
        return None

    # 处理 endend()
    def visit_ENDEND(self, node):
        arg = node.get('arg')
        if arg is not None:
            if not (0 <= arg <= 9):  # 检查参数范围
                raise Exception("endend() argument must be between 0 and 9")
            raise ExitREPL(arg)
        else:
            raise ExitREPL(0)  # 默认退出码为 0

    def visit_SHAPE(self, node):
        value = self.visit(node['expr'])
        if isinstance(value, dict):
            if value.get('type') == 'JX_LIST':
                if all(isinstance(item, list) for item in value['data']):
                    return "table"
                else:
                    return "list"
            elif value.get('type') == 'FUNCTION':
                return "function"
            elif value.get('type') == 'CALL':
                return "function"
        elif isinstance(value, int):
            return "int"
        elif isinstance(value, float):
            return "float"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, bool):
            return "bool"
        elif isinstance(value, list):
            if all(isinstance(item, list) for item in value):
                return "table"
            else:
                return "list"
        elif value is None:
            return "none"
        else:
            return str(type(value).__name__)

    def visit_PUSH(self, node):
        element = self.visit(node['element'])
        target_node = node['list']

        if isinstance(target_node, dict) and target_node.get('type') == 'INDEX_ACCESS':
            # 处理索引插入: push 5 -> a[1]
            list_var_node = target_node['object']
            index_node = target_node['index']

            # 假设 list_var_node 是 {'type': 'VAR', 'value': 'a'}
            if not (isinstance(list_var_node, dict) and list_var_node.get('type') == 'VAR'):
                raise Exception("Target object for indexed push must be a variable")
            list_var_name = list_var_node['value']
            if list_var_name not in self.symbols:
                raise Exception(f"Undefined variable {list_var_name}")

            list_wrapper = self.symbols[list_var_name]
            if not (isinstance(list_wrapper, dict) and list_wrapper.get('type') == 'JX_LIST'):
                raise Exception("Target for push is not a JX_LIST")

            index = self.visit(index_node)
            if not isinstance(index, int):
                raise Exception("Index for push must be an integer")

            list_wrapper['data'].insert(index, element)

        else:
            # 处理列表末尾添加: push 5 -> a
            list_wrapper = self.visit(target_node)  # target_node 应该是 VAR 节点
            if not (isinstance(list_wrapper, dict) and list_wrapper.get('type') == 'JX_LIST'):
                raise Exception("Target for push is not a JX_LIST")
            list_wrapper['data'].append(element)
        return None  # push 操作不返回值

    def visit_OUT(self, node):
        element_to_remove = self.visit(node['element'])
        target_node = node['list']
        list_wrapper = self.visit(target_node)
        all_same = node['all_same']  # 获取 all_same 标志

        if not (isinstance(list_wrapper, dict) and list_wrapper.get('type') == 'JX_LIST'):
            raise Exception("Target for out is not a JX_LIST")

        data_list = list_wrapper['data']
        outlist = list_wrapper['outlist']

        if all_same:
            # 删除所有匹配项
            found_count = 0
            new_list = []
            for item in data_list:
                if item == element_to_remove:
                    found_count += 1
                else:
                    new_list.append(item)

            if found_count > 0:
                list_wrapper['data'] = new_list
                for _ in range(found_count):
                    outlist.append(element_to_remove)
            else:
                raise Exception("Element not found in list for out operation")
        else:
            # 删除第一个匹配项
            try:
                index_to_remove = data_list.index(element_to_remove)
                removed_item = data_list.pop(index_to_remove)
                outlist.append(removed_item)
            except ValueError:
                raise Exception("Element not found in list for out operation")

        return None  # out 操作不返回值

    def visit_THROW(self, node):
        element_to_remove = self.visit(node['element'])
        target_node = node['list']
        list_wrapper = self.visit(target_node)

        if not (isinstance(list_wrapper, dict) and list_wrapper.get('type') == 'JX_LIST'):
            raise Exception("Target for throw is not a JX_LIST")

        if element_to_remove in list_wrapper['data']:
            list_wrapper['data'].remove(element_to_remove)
            # 不添加到 outlist
        else:
            raise Exception("Element not found in list for throw operation")
        return None  # throw 操作不返回值

    def visit_COMPARE_OP(self, node):
        left = self.visit(node['left'])
        right = self.visit(node['right'])
        op = node['op']

        if op == TokenType.EQ:
            return left == right
        elif op == TokenType.NEQ:
            return left != right
        elif op == TokenType.GT:
            return left > right
        elif op == TokenType.LT:
            return left < right
        elif op == TokenType.GTE:
            return left >= right
        elif op == TokenType.LTE:
            return left <= right
        else:
            raise Exception("Unknown comparison operator")

    def visit_STRUCT_DEF(self, node):
        # 将结构体定义存储到符号表中
        self.symbols[node['name']] = {
            'type': 'STRUCT_TYPE',
            'members': node['members']
        }
        return None

    def visit_STRUCT_INSTANCE(self, node):
        # 获取结构体定义
        struct_def = self.symbols.get(node['name'])
        if not struct_def or struct_def.get('type') != 'STRUCT_TYPE':
            raise Exception(f"Undefined struct type: {node['name']}")

        # 创建结构体实例
        instance = {
            'type': 'STRUCT_INSTANCE',
            'struct_type': node['name'],
            'members': {}
        }

        # 检查成员是否匹配定义
        defined_members = {m[0] for m in struct_def['members']}
        for member_name, value in node['members'].items():
            if member_name not in defined_members:
                raise Exception(f"Undefined member '{member_name}' in struct {node['name']}")
            # 直接存储值，不需要再次访问
            instance['members'][member_name] = value if isinstance(value, dict) and value.get(
                'type') == 'STRING' else self.visit(value)

        return instance

    def visit_MEMBER_ACCESS(self, node):
        obj = self.visit(node['object'])
        member = node['member']

        if isinstance(obj, dict) and obj.get('type') == 'STRUCT_INSTANCE':
            if member not in obj['members']:
                raise Exception(f"Undefined member '{member}' in struct {obj['struct_type']}")
            # 获取成员值
            member_value = obj['members'][member]
            # 如果成员值是AST节点，则访问其实际值
            if isinstance(member_value, dict):
                if member_value.get('type') == 'STRUCT_INSTANCE':
                    return member_value  # 返回结构体实例，以便继续访问其成员
                elif 'type' in member_value:
                    return self.visit(member_value)
            return member_value
        else:
            raise Exception(f"Cannot access member '{member}' on non-struct object")
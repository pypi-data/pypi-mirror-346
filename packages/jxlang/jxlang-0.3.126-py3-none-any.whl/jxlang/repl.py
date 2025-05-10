from .interpreter import Interpreter
from .exceptions import ExitREPL
from .lexer import Lexer
from .parser import Parser
from .tokens import TokenType


def repl():
    print("JxLang MI (输入 endend() 退出，输入 version() 查看版本)")
    interpreter = Interpreter()
    while True:
        text_lines = []
        prompt = "jxlang> "  # 每次新语句开始时重置提示符
        while True:
            try:
                line = input(prompt).strip().replace('\r', '')
                if not line and not text_lines:  # 完全空行，且不是多行输入中间的空行
                    continue
                text_lines.append(line)
                full_text = "\n".join(text_lines)

                # 检查是否需要继续输入
                temp_lexer = Lexer(full_text)
                needs_more_input = False
                paren_count = 0
                bracket_count = 0
                colon_count = 0

                # 检查括号和冒号匹配
                for char in full_text:
                    if char == '(':
                        paren_count += 1
                    elif char == ')':
                        paren_count -= 1
                    elif char == '[':
                        bracket_count += 1
                    elif char == ']':
                        bracket_count -= 1
                    elif char == ':':
                        colon_count += 1

                # 如果括号不匹配或最后一个非空行以冒号结尾，需要继续输入
                if paren_count > 0 or bracket_count > 0 or (line and line[-1] == ':'):
                    needs_more_input = True
                    prompt = "    ...     "
                    continue

                # 检查是否有意义的Token
                has_meaningful_token = False
                while True:
                    token = temp_lexer.get_next_token()
                    if token.type not in (TokenType.NEWLINE, TokenType.EOF):
                        has_meaningful_token = True
                        break
                    if token.type == TokenType.EOF:
                        break

                # 如果只有换行或EOF，并且不是在多行输入过程中，则认为输入无效/空，重新提示
                if not has_meaningful_token and prompt == "jxlang> ":
                    text_lines = []
                    continue

                # 尝试解析
                lexer = Lexer(full_text)
                parser = Parser(lexer)
                try:
                    tree = parser.parse()
                    break  # 如果解析成功，跳出内层循环
                except EOFError:
                    # 如果解析器需要更多输入，继续循环
                    needs_more_input = True
                    prompt = "    ...     "
                    continue
                except Exception as e:
                    # 如果是其他解析错误，直接抛出
                    raise e

            except EOFError:
                if prompt == "jxlang> ":
                    text_lines = []
                    continue
                else:
                    prompt = "    ...     "
            except Exception as e:
                print(f"Syntax Error: {e}")
                text_lines = []
                break

        # 如果 text_lines 为空，跳过执行
        if not text_lines:
            continue

        # 执行解析后的代码
        try:
            result = interpreter.visit(tree)
            if result is not None:
                if isinstance(result, dict) and result.get('type') == 'JX_LIST':
                    print(result['data'])
                else:
                    print(result)
        except ExitREPL as e:
            print(f"Exiting with code {e.code}")
            break
        except Exception as e:
            print(f"Runtime Error: {e}")
from flask import Flask, render_template, request
import json

app = Flask(__name__)

class SLRParser:
    def __init__(self, parsing_table, grammar_rules, start_symbol):
        self.parsing_table = parsing_table  
        self.grammar_rules = grammar_rules  
        self.start_symbol = start_symbol    

    def parse(self, input_string):
        input_string += '$'  
        stack = [0]  
        pointer = 0  

        while True:
            state = stack[-1]
            symbol = input_string[pointer]
            action = self.parsing_table.get((state, symbol))

            if action is None:
                return "Rejected: No valid action"
            
            if action[0] == 's':  
                stack.append(int(action[1:]))
                pointer += 1
            elif action[0] == 'r':  
                rule_index = int(action[1:])
                lhs, rhs = self.grammar_rules[rule_index]
                for _ in range(len(rhs)):
                    stack.pop()
                goto_state = self.parsing_table.get((stack[-1], lhs))
                if goto_state is None:
                    return "Rejected: No valid goto"
                stack.append(goto_state)
            elif action == 'accept':  
                return "Accepted"
            else:
                return "Rejected: Invalid action"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    parsing_table_input = ""
    grammar_rules_input = ""
    input_string = ""

    if request.method == 'POST':
        try:
            parsing_table_input = request.form['parsing_table']
            grammar_rules_input = request.form['grammar_rules']
            input_string = request.form['input_string']
            
            parsing_table = json.loads(parsing_table_input)
            parsing_table = {eval(k): v for k, v in parsing_table.items()}  
            
            grammar_rules = json.loads(grammar_rules_input)
            grammar_rules = {int(k): tuple(v) for k, v in grammar_rules.items()}  
            
            slr_parser = SLRParser(parsing_table, grammar_rules, 'S')
            result = slr_parser.parse(input_string)
        except Exception as e:
            result = f"Error: {str(e)}"
    
    return render_template('index.html', result=result, parsing_table_input=parsing_table_input, grammar_rules_input=grammar_rules_input, input_string=input_string)

if __name__ == '__main__':
    app.run(debug=True)

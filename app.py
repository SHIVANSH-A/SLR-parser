from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

def slr_parser(input_string, parsing_table, grammar):
    tokens = input_string.split()
    tokens.append('$')  # End of input marker
    stack = [0]  # Start state
    position = 0
    moves = []

    while True:
        if position >= len(tokens):
            moves.append("Error: Input consumed but parsing not complete")
            return False, moves

        current_token = tokens[position]
        current_state = stack[-1]
        action_key = f"({current_state}, '{current_token}')"

        if action_key not in parsing_table:
            moves.append(f"Error: No action for state {current_state} and token '{current_token}'")
            return False, moves

        action = parsing_table[action_key]
        moves.append(f"State: {current_state}, Token: '{current_token}', Action: {action}")

        if action == "accept":
            moves.append("String accepted!")
            return True, moves

        elif action.startswith('s'):  # Shift
            next_state = int(action[1:])
            stack.append(current_token)
            stack.append(next_state)
            position += 1

        elif action.startswith('r'):  # Reduce
            rule_num = action[1:]
            if rule_num not in grammar:
                moves.append(f"Error: Invalid rule number {rule_num}")
                return False, moves
            
            lhs, rhs = grammar[rule_num]
            rhs_tokens = rhs.split()
            for _ in range(len(rhs_tokens) * 2):  # Pop twice for each symbol
                stack.pop()
            
            current_state = stack[-1]
            stack.append(lhs)

            goto_key = f"({current_state}, '{lhs}')"
            if goto_key not in parsing_table:
                moves.append(f"Error: No goto action for state {current_state} and non-terminal '{lhs}'")
                return False, moves

            stack.append(int(parsing_table[goto_key]))
        else:
            moves.append(f"Error: Invalid action {action}")
            return False, moves


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            parsing_table_input = request.form['parsing_table'].strip()
            grammar_rules_input = request.form['grammar_rules'].strip()
            input_string = request.form['input_string'].strip()

            if not parsing_table_input:
                return render_template('index.html', error="Parsing table input is empty.")

            if not grammar_rules_input:
                return render_template('index.html', error="Grammar rules input is empty.")

            try:
                parsing_table = json.loads(parsing_table_input)
                grammar_rules = json.loads(grammar_rules_input)
            except json.JSONDecodeError as e:
                return render_template('index.html', error=f"Invalid JSON format: {str(e)}")

            accepted, moves = slr_parser(input_string, parsing_table, grammar_rules)
            result = "Accepted" if accepted else "Rejected"

            return render_template('index.html', 
                                   parsing_table_input=parsing_table_input, 
                                   grammar_rules_input=grammar_rules_input, 
                                   input_string=input_string, 
                                   result=result, moves=moves)
        except Exception as e:
            return render_template('index.html', error=str(e))

    return render_template('index.html', parsing_table_input="", grammar_rules_input="", input_string="", result=None)


if __name__ == '__main__':
    app.run(debug=True)

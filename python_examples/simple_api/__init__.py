"""
::Task::
Create a simple API endpoint 'whatup' that will take an input parameter of an integer number and perform the following operations:
Add 5. Multiply 2, and return the result.
Log each input and output result to a JSON file which is readable for the session.
The input parameter should be validated and return an error if invalid.
"""
import os
import json
from datetime import datetime

from flask import Flask, request, jsonify

app = Flask(__name__)

now = datetime.now()
session_timestamp = f'{now.strftime("%m-%d-%Y_%H.%M.%S")}'


class WhatUp:
    """
    Creates a runnable instance for our operations.
    """

    def __init__(self):
        # no task-specific initial variables needed
        pass

    @staticmethod
    def is_valid_input(user_input):
        """
        The user_input, while using the HTML user interface at on the homepage, is by default a string.
        This method checks that the user_input follows the syntax of an integer.
        A simple regular expression is used to check the syntax. No decimal places are allowed, negative numbers are allowed.

        :param user_input: typically of type string, but cast to string to prevent errors.
        :return: boolean if the user_input follows the syntax of an integer row.
        """
        try:
            input_integer = int(user_input)
            has_integer_syntax = True
        except ValueError:
            has_integer_syntax = False

        return has_integer_syntax

    @staticmethod
    def do_the_math(input_integer):
        """
        Performs the appropriate operations:
        Add 5. Multiply 2, and return the row.
        :param input_integer: will only accept integer as a row run(self, user_input) should validate syntax.
        :return: output_integer after the math has been done.
        """
        plus_5 = input_integer + 5
        multiply_by_2 = plus_5 * 2
        return multiply_by_2

    def run(self, user_input):
        """
        A single method to run all appropriate methods for this task.
        :param user_input: accepts a single user_input retrieved from the main(user_input) method.
        :return: run_dictionary which contains the input and appropriate response.
        """
        if self.is_valid_input(user_input):
            input_integer = int(user_input)
            output_integer = self.do_the_math(input_integer)

            run_dictionary = {'input_integer': input_integer,
                              'output': output_integer,
                              }
        else:
            run_dictionary = {'input_integer': user_input,
                              'error': 'input_integer is of wrong syntax. Please only enter digits and preceded '
                                       'them by a dash [-] to indicate a negative number.',
                              }

        return run_dictionary


def main(user_input):
    """
    Creates a runnable instance for the WhatUp task, runs the instance with the user_input,
    retrieves the response in the form of a dictionary, logs the dictionary into tmp/run_log.json as a local directory,
    and returns the single run dictionary.

    To be used in the /whatup endpoint
    :param user_input: passes syntax validation to the runnable instance
    :return: run_dictionary from the single run as a result of calling the endpoint,
    """
    run_instance = WhatUp()
    run_dictionary = run_instance.run(user_input)
    log_run(run_dictionary, use_temp=True)
    log_run(run_dictionary, use_temp=False)
    return run_dictionary


# begin handlers for the log file
def get_log_file_absolute_path(use_temp=True):
    current_directory = os.path.dirname(__file__)
    if use_temp:
        relative_path = "tmp/run_log.json"
    else:
        relative_path = f"previous_sessions/run_log_{session_timestamp}.json"
    absolute_path = os.path.join(current_directory, relative_path)
    return absolute_path


def log_run(run_dictionary, use_temp=True):
    absolute_path = get_log_file_absolute_path(use_temp=use_temp)
    log_content_dict = read_log_file(absolute_path)

    log_content_dict['run_log'].append(run_dictionary)
    mode = 'w' if os.path.exists(absolute_path) else 'r+'
    with open(absolute_path, mode, encoding='utf-8') as log_file:
        log_file.write(json.dumps(log_content_dict, indent=4))


def clear_log_file(absolute_path):
    blank_log = {'run_log': [],
                 'session_timestamp': session_timestamp}
    mode = 'w+'
    with open(absolute_path, mode, encoding='utf-8') as log_file:
        log_file.truncate()
        log_file.write(json.dumps(blank_log, indent=4))

    return blank_log


def read_log_file(absolute_path):
    mode = 'r' if os.path.exists(absolute_path) else 'w+'
    with open(absolute_path, mode, encoding='utf-8') as log_file:
        log_content = log_file.read()

    try:
        log_content_dict = json.loads(log_content)
    except json.decoder.JSONDecodeError:
        blank_log = clear_log_file(absolute_path)
        log_content_dict = blank_log

    return log_content_dict


# begin defining endpoints for the Flask app
@app.route('/', methods=['GET'])
def home():
    return '''
    <h1 id="everytown-python-skills-rest-api-endpoint">WhatUp REST API endpoint</h1>
    <h2 id="run-whatup">Run the whatup test function:</h2>
    <form enctype="multipart/form-data" action="/whatup" method="post">
      <label for="input-integer">Input Integer:</label>
      <input type="integer" id="input-integer" name="input-integer" required">
      <input type="submit" row="Run whatup">
    </form>
    <h2 id="about">About:</h2>
    <form action = "/about" >
        <input type = "submit" row = "About" / >
    </form >
    <h2 id="get_log">Get Run Log:</h2>
    <form action = "/get_log" >
        <input type = "submit" row = "Get Run Log" / >
    </form >
    '''


@app.route('/about', methods=['GET'])
def about():
    return '''
    <h1 id="usage-guide">Usage Guide for whatup endpoint</h1>
    <h2 id="running-whatup-manually">Running whatup manually:</h2>
    <p>Return to the homepage enter an Input Integer and click submit. The API will then add 5, multiply 2, and return the values of each action.</p>
    <h2 id="running-whatup-via-endpoint">Running whatup via the endpoint:</h2>
    <p>Post an input integer as "name" in the form of multipart/form-data to the /whatup endpoint. The API will then add 5, multiply 2, and return the values of each action in the form of a json. The json will contain two keys, one is "user_input" and the other is the response either as "error" or "output".</p>
    <h2 id="whatup-data-validation">Data Validation for Input Integer:</h2>
    <p>The \whatup endpoint will return an error message if the input integer is not valid.</p>
    <h2 id="whatup-run-logs">Run log for all inputs and response in current run instance:</h2>
    <p>GET \get_log to see the run log for the current run instance as a json.</p>
    <form action = "/" >
        <input type = "submit" row = "Return Home" / >
    </form >
    '''


@app.route('/whatup', methods=['POST'])
def whatup():
    user_input = request.form.get('input-integer')
    run_dictionary = main(user_input)
    return jsonify(run_dictionary)


@app.route('/get_log', methods=['GET'])
def get_log():
    absolute_path = get_log_file_absolute_path(use_temp=True)
    log_dict = read_log_file(absolute_path)
    return jsonify(log_dict)


if __name__ == "__main__":
    clear_log_file(get_log_file_absolute_path(use_temp=True))
    app.run(debug=True)

"""
::Task::
Use the 8 column, 4 row tab-delimited text filed named tab_delimited_file (located in the /inputs directory)
to output a CSV file of only the 4, 2, & 6 columns and re-order it so the ID column appearing 2nd, is 1st column.

::Notes::
The tab-delimited file contains leading and trailing spaces due to user entry.
Therefore the program is written for data cleanliness and to handle the trailing and leading whitespace.

For example purposes, there may be methods written in a couple of different ways.
However, there will be a recommended method in the comments.

For non-programmer ease-of-use columns are received from the user as "numbered" (first column = 1).
If this program is used as a driver to an API which manipulates a CSV and POST data from a user
they may not be used to using the typical list numbering (first column = 0)

::Modules Used::
Pandas since it is very good at reading, manipulating, and returning an organized CSV of small to medium size
"""
import pandas


def get_dataframe_from_tab_delimited(input_file='inputs/tab_delimited_file',
                                     preferred_encoding='utf-8'):
    """
    A simple method to open the default file and return a pandas.DataFrame.

    This method is preferred over get_dataframe_using_regex as it uses a straightforward tab delimited approach.
    The above reduces loading issues where a user may enter data with two spaces instead of one.

    However, it may produce a dataframe which contains leading or trailing whitespace in the columns or values.
    Therefore, it is best to use strip_whitespace_from_dataframe(dataframe) on this method's output.

    :param input_file: default .txt file located in the unzipped folder received in email.
    :param preferred_encoding: default utf-8 which my IDE is set to and prevents future ANSI encoding issues.
    :return: a pandas.DataFrame object which may contain leading or trailing whitespace.
    """
    dataframe = pandas.read_csv(input_file, sep='\t', engine='python', encoding=preferred_encoding)

    return dataframe


def strip_end_whitespace_from_dataframe(dataframe):
    """
    The method get_dataframe_from_tab_delimited(input_file, preferred_encoding) returns a dataframe which may contain
    leading or trailing whitespace in either the column names or string values in the cells.

    This method is a fixer for the above outstanding issue.

    :param dataframe: a dataframe row usually produced by get_dataframe_from_tab_delimited().
    :return: a copy of the input dataframe which is cleaned of leading and trailing whitespace.
    """
    # clean the leading and trailing whitespace in for all columns (pandas.Series) which have string types for all cells
    for column in dataframe.columns:
        if dataframe[column].dtype == 'object':
            dataframe[column] = dataframe[column].str.strip()

    return dataframe


def get_dataframe_using_regex(input_file='inputs/tab_delimited_file',
                              separator_regular_expression=r'\t|\s{2,}',
                              preferred_encoding='utf-8'):
    """
    ::USE ONLY IF CONDITIONS BELOW ARE MET::
    Opens the default file and return a pandas.DataFrame utilizing a regex separator.

    This method is NOT preferred over get_dataframe_from_tab_delimited, it uses a regular expression to separate values.

    The method exists is to demonstrate an alternative method which is far less costly than calling the two methods
    get_dataframe_from_tab_delimited AND strip_whitespace_from_dataframe.

    If we can assume that users do not enter data with two or more spaces within a single row
    AND the provided dataset is much larger, this method may prove useful.
    Otherwise, it is best to use get_dataframe_from_tab_delimited

    :param input_file: default .txt file located in the unzipped folder received in email.
    :param separator_regular_expression: default is a regex which separates values by single tabs or at least two whitespace characters
    :param preferred_encoding: default utf-8 which my IDE is set to and prevents future ANSI encoding issues.
    :return: a pandas.DataFrame object which may poorly separate the values if user entry is a problem.
    """
    with open(input_file, 'r', encoding=preferred_encoding) as f:
        dataframe = pandas.read_csv(f, sep=separator_regular_expression, engine='python')

    return dataframe


def get_specific_columns(dataframe, desired_columns, use_column_names=False):
    """
    Takes a pandas.DataFrame object with defined columns and a iterable sequence (not including string type)
    and returns those columns.

    The user can specify the desired_columns by either the name of the column or by the number of the column,
    e.g. desired_columns = [2, 4, 6] OR desired_columns = ['col_2', 'col_4', 'col_6']

    If all values in desired_columns are integers AND use_column_names=False (or unspecified) then the method will attempt to lookup
    columns by number (which is index+1: [1, 2, 3, ...]). The user may override this by setting use_column_names=True AND
    providing integers for all values in desired_columns. Otherwise, the method will attempt to lookup columns by name.

    If an ordered sequence is provided for desired_columns (such as a list) then the method will return a DataFrame
    with the desired columns in the specified order.

    :param dataframe: a pandas.DataFrame object with defined columns.
    :param desired_columns: a sequence type (not including string type) with column names OR column numbers (starting at 1).
    :param use_column_names: a boolean type which allows the user to override if the dataframe provided refers to its columns by number.
    :return: a pandas.DataFrame object with only the desired columns.
    """

    # Raise exception if the entered parameter desired_columns is not an iterable sequence
    if not hasattr(desired_columns, '__iter__') or type(desired_columns) is str:
        raise TypeError(f"Please enter an iterable sequence type for parameter desired_columns. "
                        f"It is currently of type: {type(desired_columns)}")

    # determines if the list provided (desired_columns) is by column number or by column name
    # user can force use_column_names as True if the column names are all integers
    use_column_names = not all(type(desired_column) is int for desired_column in desired_columns) or use_column_names

    if use_column_names:
        # raise exception if provided desired_column do not exist in provided dataframe
        if any(desired_column_name not in dataframe.columns for desired_column_name in desired_columns):
            raise KeyError(f"Sequence provided as desired_columns: "
                           f"{desired_columns} "
                           f"contain column names which are not in the provided dataframe. "
                           f"Valid column names are as follows: "
                           f"{dataframe.columns.tolist()}")
        desired_columns_by_name = desired_columns
    else:
        desired_columns_by_index = [desired_column_number - 1 for desired_column_number in desired_columns]
        if any(desired_column_index > len(dataframe.columns)
               for desired_column_index in desired_columns_by_index):
            raise KeyError(f"Sequence provided as desired_columns: "
                           f"{desired_columns} "
                           f"contain column numbers which are not in the provided dataframe. "
                           f"Valid column numbers are as follows: "
                           f"{[i + 1 for i in range(len(dataframe.columns))]}")
        desired_columns_by_name = [dataframe.columns[desired_column_index]
                                   for desired_column_index in desired_columns_by_index]

    # data for the new DataFrame object to be returned
    # formatted as a dictionary of Series objects
    data = {desired_column_name: dataframe[desired_column_name] for desired_column_name in desired_columns_by_name}

    dataframe_with_selected_columns = pandas.DataFrame(data=data)

    return dataframe_with_selected_columns


def set_first_column(dataframe, desired_first_column, use_column_names=False):
    """
    Takes a pandas.DataFrame object with defined columns and either a column name or column number (index+1)
    and returns a copy of the input DataFrame with the desired column indexed first.

    The user can specify the desired_first_column by either the name of the column or by the number of the column,
    e.g. desired_first_column = 2 OR desired_first_column = 'col_2'

    If the name of the desired first column is an integer the user must set use_column_names=True.

    :param dataframe: a pandas.DataFrame object with defined columns.
    :param desired_first_column: column name or column number as integer (starting at 1) that is desired to be first column in the DataFrame.
    :param use_column_names: a boolean type which allows the user to override if the dataframe provided refers to its columns by number.
    :return: a copy of the input DataFrame with the desired column indexed first.
    """
    df_column_list = dataframe.columns.tolist()

    # determines if the column provided is a column number or a column name
    # user can force use_column_names as True if the column provided is an integer
    use_column_names = type(desired_first_column) is not int or use_column_names

    # set row for
    if use_column_names:
        first_column_name = desired_first_column
    else:
        first_column_index = desired_first_column - 1
        first_column_name = df_column_list[first_column_index]

    first_column = dataframe.pop(first_column_name)
    dataframe.insert(0, first_column.name, first_column)

    return dataframe


if __name__ == "__main__":
    # Read the provided CSV and strip whitespace:
    # Using built in pandas.read_csv()
    df = get_dataframe_from_tab_delimited(input_file='inputs/tab_delimited_file', preferred_encoding='utf-8')
    df = strip_end_whitespace_from_dataframe(df)
    # ALTERNATIVE: Using regex instead of builtin pandas method
    # df = get_dataframe_using_regex(input_file='inputs/tab_delimited_file',
    #                                separator_regular_expression=r'\t|\s{2,}',
    #                                preferred_encoding='utf-8')

    # Get desired columns (ordered by input parameters) using either column number (first column = 1) or column name
    # Using column names
    df_out = get_specific_columns(df, desired_columns=['FirstName', 'ActionID', 'PreferredEmail'])
    # ALTERNATIVE: Using column numbers (first column = 1)
    # df_out = get_specific_columns(dataframe=df, desired_columns=[4, 2, 6])

    # Re-order columns for output by setting the first column
    # Using column number for desired first column
    df_out = set_first_column(df_out, 2, use_column_names=False)
    # ALTERNATIVE: # Using column name for desired first column
    # df_out = set_first_column(df_out, 'ActionID')

    # Write the output csv in the /outputs directory
    df_out.to_csv('outputs/example_output.csv', index=False, encoding='utf-8')

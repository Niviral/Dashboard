# Dashboard
#Python 3.8.2<br>
Simple dashboard created with [Dash](https://plotly.com/dash/)<br>
To set up dashboard install requirements:<br>
    `pip3 install -r requirements.txt`<br>
and set up enviromental variable to provide app with file name: <br>
    For linux `export DASH_FILE_NAME='filename.csv'`<br>
    For Windows Power Shell `Set-Variable -Name DASH_FILE_NAME -value 'filename.csv'`<br>
Data fille reqirements:
| DATE       | TIME     | QUERY_RAW_PHRASE | LOG_TIME |
|------------|----------|------------------|----------|
| 2020-07-27 | 10:30:03 | FOO              | 20       |
| 2020-07-27 | 10:15:02 | FOO              | 15       |
| 2020-07-26 | 10:30:03 | FOO              | 17       |
| 2020-07-26 | 10:15:02 | FOO              | 22       |
| 2020-07-27 | 08:30:02 | BAR              | 22       |
| 2020-07-27 | 08:15:02 | BAR              | 17       |
| 2020-07-26 | 08:30:02 | BAR              | 15       |
| 2020-07-26 | 08:15:02 | BAR              | 20       |

To start app just simply call index file <br>
    `python3 index.py`<br>

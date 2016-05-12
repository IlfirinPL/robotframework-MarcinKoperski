| *** Settings *** |
| Documentation  | Base resource use it as common import place |
| ...            |
| ...            | Author: Marcin Koperski |
| Library        | TestToolsMK |
| Library        | Dialogs |
| Library        | Screenshot |
| Library        | ImapLibrary |
| Library        | XML |
| Library        | Process |
| Library        | ArchiveLibrary |
| Library        | Selenium2Library |
| Library        | OperatingSystem |
| Library        | Collections |
| Library        | DatabaseLibrary |

| *** Variables *** |
| &{selenium config} | selenium_timeout=65 s | width=1366 | height=1200 | x=1872 | y=-82 |

| *** Test Cases *** |
| Logger |
|    | Set Log Level Restore |

| File list |
|    | ${list} | List Files In Directory | ${EXECDIR} |
|    | ${info} | Get File Lines Count | ${list[0]} |
|    | Should Be Equal As Strings | .gitignore / 57 | ${list[0]} / ${info} |

| Using Timer Example |
|    | Timer Start |
|    | Timer Start | small |
|    | Sleep | 0.5 |
|    | Timer Log | small | INFO |
|    | Timer Stop | small | compact |
|    | Timer Should Be Lesser Then | 1 |

| List Sort By Number |
|    | ${to sort} | Create List | 6234 | 723 | 82 | 9 |
|    | Sort List By Number | ${to sort} |
|    | Should Be Equal | ${to sort[0]} | 9 |

| Jquery2 Example |
|    | #PLUGIN CHROME | https://chrome.google.com/webstore/detail/jquery-unique-selector/cmdmlphjbobhblimniofbnlfkmpcjlgd?utm_source=chrome-app-launcher-info-dialog |
|    | Open Browser Extension | http://codylindley.com/jqueryselectors/ |
|    | Import JQuery |
|    | Input Text | jquery=textarea.left | edit JQUERY |
|    | Click Element | jquery=input#radio2 |
|    | Input Text | jquery=div.domtree>form>div:nth-child(1)>div:nth-child(1)>input | test2 |
|    | Click Element | jquery=div.domtree>form>div:nth-child(3)>select>option:nth-child(3) |
|    | [Teardown] | Close All Browsers |

| Compare images |
|    | [Tags] | WIN |
|    | Open Browser Extension | http://www.google.pl |
|    | ${name a} | Capture Page Screenshot Extension |
|    | Go To | http://www.google.com |
|    | ${name b} | Capture Page Screenshot Extension |
|    | ${status} | Run Keyword And Return Status | Image Should Be Difference Less Then | ${name a} | ${name b} | 1 |
|    | Should Be Equal As Strings | ${status} | False |
|    | [Teardown] | Close All Browsers |

| Download To Folder GC |
|    | ${path} | Set Variable | ${TEMPDIR}/Artifacts/download |
|    | Create Directory | ${path} |
|    | ${path} | Normalize Path | ${path} |
|    | ${capabilities} | Create Download Dir Capabilities For Chrome | ${path} |
|    | Log | ${capabilities} |
|    | Remove File | ${path}/menuexcel.xls |
|    | Open Browser Extension | http://www.lancsngfl.ac.uk/cmsmanual/index.php?category_id=14 | gc | desired_capabilities=${capabilities} | remote_url=http://127.0.0.1:4444/wd/hub |
|    | Click Element | //a[contains(.,'.xls - an Excel spreadsheet file')] |
|    | Wait Until Keyword Succeeds | 10 | 1 | File Should Not Change | ${path}/menuexcel.xls |
|    | File Should Not Be Empty | ${path}/menuexcel.xls |
|    | [Teardown] | Close All Browsers |

| Download To Folder FF |
|    | ${path} | Set Variable | ${TEMPDIR}/Artifacts/download |
|    | Create Directory | ${path} |
|    | ${path} | Normalize Path | ${path} |
|    | ${capabilities} | Create Download Dir Profile For Firefox | ${path} | ${EXECDIR}/resources/mimeTypes.rdf |
|    | Log | ${capabilities} |
|    | Remove File | ${path}/menuexcel.xls |
|    | Open Browser Extension | http://www.lancsngfl.ac.uk/cmsmanual/index.php?category_id=14 | ff | ff_profile_dir=${capabilities} |
|    | Click Element | //a[contains(.,'.xls - an Excel spreadsheet file')] |
|    | Wait Until Keyword Succeeds | 10 | 1 | File Should Not Change | ${path}/menuexcel.xls |
|    | File Should Not Be Empty | ${path}/menuexcel.xls |
|    | [Teardown] | Close All Browsers |

| DataBase Extenions |
|    | ${ db file} | Set Variable | ./example.db |
|    | Remove File | ${ db file} |
|    | Connect To Database Using Custom Params | sqlite3 | database='${db file}' |
|    | Execute Sql String With Logs | CREATE TABLE [test_data] ( [id] INTEGER \ NOT NULL PRIMARY KEY, [string] VARCHAR(100) \ NULL, [time] TIMESTAMP \ NULL ) |
|    | ${time} | Get Time |
|    | Repeat Keyword | 4 | Execute Sql String With Logs | Insert Into test_data (string,time) values ("RF","${time}") |
|    | ${resutls} | Query Cell | select count(*) from test_data |
|    | Should Be Equal As Strings | ${resutls} | 4 |
|    | ${table} | Query Row | select * from test_data where id = 2 |
|    | List Should Contain Value | ${table} | ${time} |
|    | ${single value} | Query Cell | select time from test_data where id = 3 |
|    | Should Be Equal As Strings | ${single value} | ${time} |
|    | ${resutls} | Query Many Rows | select * from test_data |
|    | Length Should Be | ${resutls} | 4 |
|    | Disconnect From Database |
|    | [Teardown] | Remove File | ${ db file} |

| CSV |
|    | Remove File | ${EXECDIR}/Artifacts/output.csv |
|    | Csv Writer | test11 | test12 |
|    | Csv Writer | test22 | test22 |
|    | ${table} | Csv Read File | ${EXECDIR}/Artifacts/output.csv |
|    | Should Be Equal As Strings | test11 | ${table[0][0]} |
|    | Should Be Equal As Strings | test22 | ${table[1][1]} |

| Create Table From Array |
|    | Remove File | ${EXECDIR}/Artifacts/output.csv |
|    | Csv Writer | test11 | test12 |
|    | Csv Writer | test22 | test22 |
|    | ${table} | Csv Read File | ${EXECDIR}/Artifacts/output.csv |
|    | Connect To Database Using Custom Params | sqlite3 | database=':memory:' |
|    | ${table name} | Insert Data To Generated Table | ${table} |
|    | ${unque} | Query | select * from ${table name} |
|    | Length Should Be | ${unque} | 2 |

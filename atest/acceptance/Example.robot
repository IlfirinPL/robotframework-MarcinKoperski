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
| Library        | Selenium2Library |
| Library        | OperatingSystem |
| Library        | Collections |
| Library        | DatabaseLibrary |
| Library        | String |

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
|    | [Tags] | TODO |
|    | #PLUGIN CHROME | https://chrome.google.com/webstore/detail/jquery-unique-selector/cmdmlphjbobhblimniofbnlfkmpcjlgd?utm_source=chrome-app-launcher-info-dialog |
|    | Open Browser Extension | http://codylindley.com/jqueryselectors/ |
|    | Import JQuery |
|    | Input Text | jquery=textarea.left | edit JQUERY |
|    | Click Element | jquery=input#radio2 |
|    | Input Text | jquery=div.domtree>form>div:nth-child(1)>div:nth-child(1)>input | test2 |
|    | Click Element | jquery=div.domtree>form>div:nth-child(3)>select>option:nth-child(3) |
|    | [Teardown] | Close All Browsers |

| Compare images |
|    | [Tags] | WIN | TODO |
|    | Open Browser Extension | http://www.google.pl |
|    | ${name a} | Capture Page Screenshot Extension |
|    | Go To | http://www.google.com |
|    | ${name b} | Capture Page Screenshot Extension |
|    | ${status} | Run Keyword And Return Status | Image Should Be Difference Less Then | ${name a} | ${name b} | 0 |
|    | Should Be Equal As Strings | ${status} | False |
|    | [Teardown] | Close All Browsers |

| Download To Folder GC |
|    | [Tags] | WIN |
|    | [Setup] |
|    | Comment | get all binaries |
|    | Get Selenium Server |
|    | Start Selenium Server |
|    | Get Chrome Driver Latest |
|    | Open Browser | http://127.0.0.1:4444/wd/hub | gc |
|    | Capture Page Screenshot Extension |
|    | Comment |
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
|    | [Teardown] | Run Keywords | Close All Browsers |
|    | ... | AND | Shutdown Selenium Server |

| Download To Folder FF |
|    | [Tags] | WIN |
|    | Get Selenium Server |
|    | Start Selenium Server |
|    | Get Firefox Driver Latest |
|    | Open Browser | http://127.0.0.1:4444/wd/hub | gc |
|    | Capture Page Screenshot Extension |
|    | ${path} | Set Variable | Artifacts/download |
|    | ${capabilities} | Create Download Dir Profile For Firefox | ${path} | C:/Cutting Edge QA/robotframework-MarcinKoperski/atest/acceptance/mimeTypes.rdf |
|    | Log | ${capabilities} |
|    | Remove File | ${path}/menuexcel.xls |
|    | Open Browser Extension | http://www.lancsngfl.ac.uk/cmsmanual/index.php?category_id=14 | ff | ff_profile_dir=${capabilities} | remote_url=http://127.0.0.1:4444/wd/hub |
|    | Click Element | //a[contains(.,'.xls - an Excel spreadsheet file')] |
|    | Wait Until Keyword Succeeds | 10 | 1 | File Should Not Change | ${path}/menuexcel.xls |
|    | File Should Not Be Empty | ${path}/menuexcel.xls |
|    | [Teardown] | Run Keywords | Close All Browsers |
|    | ... | AND | Shutdown Selenium Server |

| DataBase Extensions |
|    | ${ db file} | Set Variable | Artifacts/example.db |
|    | Remove File | ${ db file} |
|    | Create File | ${ db file} |
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
|    | File Should Exist | Artifacts/log_of_sql_execution.sql |
|    | [Teardown] | Remove Directory | Artifacts | ${True} |

| CSV |
|    | Remove File | ${TEMPDIR}/Artifacts/output.csv |
|    | Csv Set Output File | ${TEMPDIR}/Artifacts/output.csv |
|    | Csv Writer | test11 | test12 |
|    | Csv Writer | test22 | test22 |
|    | ${table} | Csv Read File | ${TEMPDIR}/Artifacts/output.csv |
|    | Should Be Equal As Strings | test11 | ${table[0][0]} |
|    | Should Be Equal As Strings | test22 | ${table[1][1]} |
|    | [Teardown] | Remove Directory | ${TEMPDIR}/Artifacts/ | ${true} |

| Create Table From Array |
|    | [Setup] | Remove File | ${TEMPDIR}/Artifacts/output.csv |
|    | Csv Set Output File | ${TEMPDIR}/Artifacts/output.csv |
|    | Csv Writer | test11 | test12 |
|    | Csv Writer | test22 | test22 |
|    | ${table} | Csv Read File | ${TEMPDIR}/Artifacts/output.csv |
|    | Connect To Database Using Custom Params | sqlite3 | database=':memory:' |
|    | ${table name} | Insert Data To Generated Table | ${table} |
|    | ${unque} | Query | select * from ${table name} |
|    | Length Should Be | ${unque} | 2 |

| Image Operations |
|    | Image Self Check |

| Log Variable To file |
|    | [Setup] | Remove Files | test1.txt | ${TEMPDIR}/temp1.txt |
|    | ${test} | Generate Random String |
|    | Log Variable To File | ${test} | test1 | test1.txt |
|    | File Should Exist | test1.txt |
|    | Log Variable To File | ${test} | test2 | ${TEMPDIR}/temp1.txt |
|    | File Should Exist | ${TEMPDIR}/temp1.txt |
|    | [Teardown] | Remove Files | test1.txt | ${TEMPDIR}/temp1.txt |

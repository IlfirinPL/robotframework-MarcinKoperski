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

| *** Variables *** |
| &{selenium config} | selenium_timeout=65 s | width=1366 | height=1200 | x=1872 | y=-82 |

| *** Test Cases *** |
| Logger |
|    | Set Log Level Restore |

| File list |
|    | ${list} | List Files In Directory | ${EXECDIR} |
|    | ${info} | Get File Lines Count | ${list[0]} |
|    | Should Be Equal As Strings | env.py / 16 | ${list[0]} / ${info} |


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

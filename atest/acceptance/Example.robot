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
|    | ${list}	| List Files In Directory	| ${EXECDIR} |
|    | ${info}	| get_file_lines_count |	${list[0]} |
|    | Log To Console    | ${list[0]} / ${info}              |


| Using Timer Example |
|    | Timer Start |
|    | Timer Start |
|    | Timer Start | small |
|    | Sleep | 0.5 |
|    | Timer Log | small | WARN |
|    | Timer Stop | small | compact |


| List Sort By Number |
|    | ${to sort} | Create List | 6234 | 723 | 82 | 9 |
|    | Sort List By Number | ${to sort} |
|    | Should Be Equal | ${to sort[0]} | 9 |




| Jquery2 Example |
|    | #PLUGIN CHROME | https://chrome.google.com/webstore/detail/jquery-unique-selector/cmdmlphjbobhblimniofbnlfkmpcjlgd?utm_source=chrome-app-launcher-info-dialog |
|    | Open Browser Extension | http://codylindley.com/jqueryselectors/ |
|    | Import JQuery |
|    | Set Selenium Speed | 0 s |
|    | Input Text | jquery=textarea.left | edit JQUERY |
|    | Click Element | jquery=input#radio2 |
|    | Input Text | jquery=div.domtree>form>div:nth-child(1)>div:nth-child(1)>input | test2 |
|    | Click Element | jquery=div.domtree>form>div:nth-child(3)>select>option:nth-child(3) |
|    | [Teardown] | Close All Browsers |


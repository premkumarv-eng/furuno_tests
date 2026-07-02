*** Keywords ***
Add Two Numbers
    [Arguments]    ${a}    ${b}
    ${result}=    add_numbers    ${a}    ${b}
    RETURN    ${result}
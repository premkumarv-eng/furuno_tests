*** Keywords ***
Add Two Numbers
    [Arguments]    ${a}    ${b}
    ${result}=    add_numbers    ${a}    ${b}
    RETURN    ${result}
    
Sub Two Numbers
    [Arguments]    ${a}    ${b}
    ${result}=    sub_numbers    ${a}    ${b}
    RETURN    ${result}
*** Settings ***
Library     ../../Furuno_Framework/libraries/Calculator.py
Resource    ../Keywords/cal_keyword.robot

*** Tasks ***
TC-1
    [Tags]    TC-1
    [Documentation]    Verify Addition
        ${result}=    Add Two Numbers    15    10
        Log To Console    Result is ${result}
        Should Be Equal As Integers    ${result}    25
TC-2
    [Tags]    TC-2
    [Documentation]    Verify Subtraction
        ${result}=    Sub Two Numbers    15    10
        Log To Console    Result is ${result}
        Should Be Equal As Integers    ${result}    5
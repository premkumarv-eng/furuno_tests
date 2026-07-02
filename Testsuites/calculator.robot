*** Settings ***
Library     ../../Furuno_framework/libraries/Calculator.py
Resource    ../Keywords/cal_keyword.robot


*** Tasks ***
Verify Addition
    ${result}=    Add Two Numbers    10    20
    Log To Console    Result is ${result}
    Should Be Equal As Integers    ${result}    30
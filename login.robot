*** Settings ***
Library           SeleniumLibrary

*** Variables ***
${URL}            https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
${BROWSER}        Chrome

${VALID_USERNAME}    Admin
${VALID_PASSWORD}    admin123

${INVALID_USERNAME}  vodinhnguu
${INVALID_PASSWORD}  vodinhnguu...

*** Test Cases ***

Valid Login Test
    [Documentation]    
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Wait Until Element Is Visible    name=username
    Input Text    name=username    ${VALID_USERNAME}
    Input Text    name=password    ${VALID_PASSWORD}
    Click Button    xpath=//button[@type='submit']
    Wait Until Page Contains Element    xpath=//h6[text()='Dashboard']    timeout=10s
    Capture Page Screenshot
    Sleep    10s
    Close Browser

Invalid Login Test
    [Documentation]    
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Wait Until Element Is Visible    name=username
    Input Text    name=username    ${INVALID_USERNAME}
    Input Text    name=password    ${INVALID_PASSWORD}
    Click Button    xpath=//button[@type='submit']
    Wait Until Page Contains    Invalid credentials    timeout=10s
    Capture Page Screenshot
    Sleep    10s
    Close Browser

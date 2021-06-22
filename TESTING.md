# Testing

Testing was done throughout site development, with branches created for each feature before it was merged into the master file. 

Usability was tested with the below workflow, sent to new users to ensure testing from different users, on different devices and browsers.

|         | User Action                                                                              | Expected result                                                                                                                                                                       | Y/N |
| ------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --- |
| Sign Up |
| 1       | Click on Sign-up from navbar                                                             | Blank sign-up page                                                                                                                                                                    | Y   |
| 2       | Enter new username                                                                       | Field will only accept email address format                                                                                                                                           | Y   |
| 3       | Enter new password                                                                       | Field will only accept min 8 characters: 1 upper, 1 lower, 1 number at least                                                                                                          | Y   |
| 4       | Click create account                                                                     | \* Opens account page with "Welcome Please update your details"<br>\* ADMIN: a new account has been created in MongoDB                                                                | Y   |
| 5       | Campaign overview table                                                                  | All 0 or blank                                                                                                                                                                        | Y   |
| 6       | Action: edit account info                                                                | \* Update information<br>\* Currency is read only                                                                                                                                     | Y   |
| 7       | Select save                                                                              | Account information is update                                                                                                                                                         | Y   |
| 8       | Action: create new campaign                                                              | Opens blank Campaign Profile page                                                                                                                                                     | Y   |
| 9       | Fill in fields                                                                           | Campaign name, campaign type, communication platform and start date are all required fields                                                                                           | Y   |
| 10      | Click save                                                                               | \* Back to account page with the added campaign.<br>\* Campaign overview now updated with relevant data.<br>\* ADMIN: a new campaign and calculation have been created within MongoDB | Y   |
| 11      | Open campaign dropdown                                                                   | \* Contains the info you input<br>\* Are the calculations correct?                                                                                                                    | Y   |
| 12      | Click edit icon                                                                          | \* Takes you to Update Campaign Profile page<br>\* Does it display the information you previously entered?                                                                            | Y   |
| 13      | Update campaign profile and select save & close                                          | \* Takes you back to the account page<br>\* Has the campaign information and campaign overview table been updated with the new information?                                           | Y   |
| 14      | Action: create new campaign                                                              | Opens blank Campaign Profile page                                                                                                                                                     | Y   |
| 15      | Action: create campaign with same name as existing campaign, (not case sensitive)        | Does not allow you to create a campaign                                                                                                                                               | Y   |
| 16      | Fill in fields                                                                           | Campaign name, campaign type, communication platform and start date are all required fields                                                                                           | Y   |
| 17      | Click save                                                                               | \* Back to account page with the added campaign.<br>\* Campaign overview now updated with relevant data.                                                                              | Y   |
| 18      | Action: create new campaign                                                              | Opens blank Campaign Profile page                                                                                                                                                     | Y   |
| 19      | Click cancel                                                                             | Back to account page without an added campaign                                                                                                                                        | Y   |
| 20      | Open a campaign dropdown and select delete icon                                          | Pop-up: are you sure you want to delete "campaign name"                                                                                                                               | Y   |
| 21      | Select "No"                                                                              | Back to account profile page                                                                                                                                                          | Y   |
| 22      | Open a campaign dropdown and select delete icon                                          | Pop-up: are you sure you want to delete "campaign name"                                                                                                                               | Y   |
| 23      | Select "Yes"                                                                             | Deletes campaign and updates account overview table                                                                                                                                   | Y   |
| 24      | Action: looking for comparative data                                                     | Redirects to Becnhmark data page and table                                                                                                                                            | Y   |
| 25      | Navigate back to My Account                                                              |                                                                                                                                                                                       | Y   |
| 26      | Create a new campaign with a very high total campaign cost to create a very high average |                                                                                                                                                                                       | Y   |
| 27      | Navigate back to Benchmark data                                                          | Is your additional data represented in the graphs?                                                                                                                                    | Y   |
| 28      | Click "Log out" in the top navigation                                                    | \* Redirects you to Log in page<br>\* Navbar no longer says "My Account" but rather Log in and Sign up                                                                                | Y   |
| 29      | Click browser back button                                                                | You are still logged out                                                                                                                                                              | Y   |
| Log In  |
|         | Navigate to Log In page                                                                  | Blank log in page                                                                                                                                                                     | Y   |
| 1       | Log In using your existing username and password                                         | Redirects you to account profile page with all you pre-entered campaigns and information                                                                                              | Y   |
| 2       | Click "Log out" in the top navigation                                                    | \* Redirects you to Log in page<br>\* Navbar no longer says "My Account" but rather Log in and Sign up                                                                                | Y   |
| Sign Up |
| 1       | Click on Sign-up from navbar                                                             | Blank sign-up page                                                                                                                                                                    | Y   |
| 2       | Sign up using the same email address as before                                           | Should not allow you to create an account                                                                                                                                             | Y   |
| Admin   |
| 1       | Navigate to Log In page                                                                  | Blank log in page                                                                                                                                                                     | Y   |
| 2       | Username: admin@admin.com<br>Password: Admi1n!Ct                                         | \* Redirects you to administration page for Lead Generation Calculator<br>\* Navbar has My Account and Category Management options                                                    | Y   |
| 3       | Select Category Management from navbar                                                   |                                                                                                                                                                                       | Y   |
| 4       | Select create new category and complete information                                      | \* Select category type from: Campaign type, Communication platform, Industry<br>\* Enter category name                                                                               | Y   |
| 5       | Click save                                                                               | Redirect back to Category Management, which is now displaying the additional option                                                                                                   | Y   |
| 6       | Navigate to My Account (still logged into admin)                                         |                                                                                                                                                                                       | Y   |
| 7       | Create a new campaign                                                                    | \* Does the new category option display?                                                                                                                                              | Y   |
| 8       | Navigate back to Category Management                                                     |                                                                                                                                                                                       | Y   |
| 9       | Select a category to edit                                                                | \* Category type is read only<br>\* Change category name                                                                                                                              | Y   |
| 10      | Save                                                                                     | The updated category is displayed                                                                                                                                                     | Y   |
| 11      | Delete a category                                                                        | It is no longer available                                                                                                                                                             | Y   |

Testing conducted outside of the Chrome development tool on the following;

iPhone SE2020
iPhone 12
iPad Pro 9.7"
All on iOS 14.3.
Testing conducted on the following browsers;

Safari
Chrome
Microsoft Edge
Firefox

## User story testing

**First-time visitors**

| User story | Requirement met 
|-----|----|
| a. As a first-time visitor I want to quickly understand the purpose of the site | a |
| b. As a first-time visitor I want to easily register an account | b |
| c. As a first-time visitor I want to feel confident that the data I enter is secure | c |
| d. As a first-time visitor I want to understand any cost associated with registration | d|
| e. As a first-time visitor I want to quickly create a new campaign | e |
| f. As a first-time visitor I want to easily obtain comparative benchmark data | f |

**Returning visitors**

| User story | Requirement met 
|-----|----|
| a. As a returning visitor I want to quickly and easily log into my account profile | a |
| b. As a returning visitor I want to see all open campaigns | a |
| c. As a returning visitor I want to quickly create a new campaign | a |
| d. As a returning visitor I want to read existing campaign data | a |
| e. As a returning visitor I want to easily update existing campaign and / or the account profile information | a |
| f. As a returning visitor I want to delete campaign information with confidence | a |

**Site administrator**

| User story | Requirement met 
|-----|----|
| a. As a site administrator I want to quickly and easily log into the admin area | a |
| b. As a site administrator I want to create a new industry / communications platform / campaign type category | a |
| c. As a site administrator I want to read information about existing categories | a |
| d. As a site administrator I want to easily update existing category information | a |
| e. As a site administrator I want to delete category information with ease | a |
| f. As a site administrator I want to create, edit and delete campaigns, the same as a "normal" user | a |

## Lighthouse report

## Issues

## Code validators


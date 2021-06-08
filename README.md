# Lead Generator Calculator

<div align="center">
    <img src="" width="500"> IMAGE
</div>

[View the live site here](#)

# Contents

* [Project Overview](#project-overview)
* [User Experience Design](#user-experience-design)
   * [Strategy](#strategy)
   * [Scope](#scope)
   * [Structure](#structure)
   * [Skeleton](#skeleton)
   * [Surface](#surface)
* [Technologies Used](#technologies-used)
* [Testing](#testing)
* [Deployment](#deployment)
* [Credits](#credits)


<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


# Project Overview

A site to assist people involved in strategic marketing decisions. Manage core marketing campaign data and the subsequent number of leads generated to obtain information about the cost per lead. This data provides invaluable insight into the value provided by marketing campaigns.

Site users also have access to average cost per lead information from other companies using the site.

# User Experience Design

## Strategy

Developed for those involved in strategic marketing decisions, the site allows for better-informed decisions about the cost per marketing lead, and cost per converted sales lead per marketing activity / campaign that they conduct.

Companies open an account and create a campaign profile, which includes the cost of the campaign, number of Marketing Qualified Leads (MQL) and number of converted or Sales Qualified Leads (SQL). They are then presented with the cost per MQL and SQL, as well as a conversion hit rate to understand which activities provide converted leads. This information gives the foundation for better-informed decisions for marketing strategies and budget planning.

Site users will have access to anonymous comparable data, so they have a benchmark.

### Target audience

Small-Medium Enterprises (SMEs) that may not have a Customer Relationship Management (CRM) tool, or are relying on spreadsheets to manage this information. The site will be a source of information that can be updated as a campaign continues to run and then presented to stakeholders as needed.

### User stories

**First-time visitors**

    a. As a first-time visitor I want to quickly understand the purpose of the site
    b. As a first-time visitor I want to easily register an account
    c. As a first-time visitor I want to feel confident that the data I enter is secure
    d. As a first-time visitor I want to understand any cost associated with registration
    e. As a first-time visitor I want to quickly create a new campaign 
    f. As a first-time visitor I want to easily obtain comparative benchmark data

**Returning visitors**

    a. As a returning visitor I want to quickly and easily log into my account profile
    b. As a returning visitor I want to see all open / live and closed campaigns
    c. As a returning visitor I want to quickly create a new campaign
    d. As a returning visitor I want to read existing campaign data
    e. As a returning visitor I want to easily update existing campaign and / or account profile data
    f. As a returning visitor I want to delete campaign information with confidence

**Site administrator**

    a. As a site administrator I want to quickly and easily log into the admin area
    b. As a site administrator I want to create a new industry / communications platform category
    c. As a site administrator I want to read information about existing categories
    d. As a site administrator I want to easily update existing category information
    e. As a site administrator I want to delete category information with ease

## Scope

### Features

| Feature  | Details  | Internal Links |
|---|---|---|
| Nav bar | Consistent on each file using Jinga templating | Home - About - Benchmark data - Log In - Sign Up |
| Favicon | Consistent on each file using Jinga templating | Home |
| Footer | Consistent on each file using Jinga templating. Copyright info | N/A |
| Contact form | Pop-up form accessible at the bottom of every page. Floating action button. | N/A |
| About | General site info and FAQs | Log In / Sign Up links |
| Benchmark Data | Graphs to display data from companies using the site, including helpful links from external sources about lead generation and cost | Log In / Sign up links |
| Log In page | Email address and password required. Also used for Admin log in  | Sign up page link |
| Sign Up page | Email address and password only required  | Log in page link |
| Administration profile | Category management: create, read, edit and delete | Create new category link |
| Create a new category | Save new category listing or edit existing listing   | N/A |
| Account profile | Campaign management: create, read, edit and delete | Create new campaign link |
| Create a new campaign | Save new category listing or edit existing listing  | N/A |
| Currency exchange | For comparison purposes, data displayed on benchmark-data.html will be converted into Euros using an API. It will therefore be converted in the back-end before displayed in the front-end  | N/A |

## Structure

### Site map

![sitemap](https://user-images.githubusercontent.com/76033080/119633678-474f4c00-be12-11eb-8d83-54129e340f32.jpg)

## Skeleton

For wireframes see separate [SKELETON.md file](SKELETON.md).

**Database schema**

Using [Creately](https://creately.com/) to generate a database schema, few company details are required. Industry and country are dropdown fields to reduce the risk of misspellings - this data is required to populate graphs displayed on benchmark-data.html, so they must be uniform. The Industry listing will be managed by Administration who will have access to create, edit and delete the industry options.

The Country field is dropdown using the [Exchange Rate API](https://www.exchangerate-api.com/docs/supported-currencies) who maintain country and currency code listings. Again the importance of pre-defined fields for these options must be stressed, so the countries can be used for data comparison in benchmark-data.html. Free text fields will not allow for such data comparison (for example Sweden, Sverige, SWE or SE are all common terms, but cannot be grouped as the same country so the risk is they are appear as four different countries where the data should be displayed as one).

[Exchange Rate API](https://www.exchangerate-api.com/docs/supported-currencies) also provides currency exchange. At present the site is focused on European businesses, therefore all data for comparison purposes will be converted into Euros.

![database_schema](https://user-images.githubusercontent.com/76033080/119633631-3b638a00-be12-11eb-8377-2c917a91c63f.jpg)

## Surface

### Typography

### Imagery

**Background Image 1**

Image by <a href="https://pixabay.com/users/geralt-9301/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=1087845">Gerd Altmann</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=1087845">Pixabay</a>

**Background Image 2**

Image by <a href="https://pixabay.com/users/tumisu-148124/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=4168483">Tumisu</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=4168483">Pixabay</a>

**Background Image 3**

Image by <a href="https://pixabay.com/users/thedigitalartist-202249/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=3400789">Pete Linforth</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=3400789">Pixabay</a>


Image by <a href="https://pixabay.com/users/manuchi-1728328/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=2462436">Денис Марчук</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=2462436">Pixabay</a>

**Background Image 6**

Image by <a href="https://pixabay.com/users/geralt-9301/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=3539317">Gerd Altmann</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=3539317">Pixabay</a>


**Background Image 7**

Image by <a href="https://pixabay.com/users/kiquebg-5133331/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=4256272">kiquebg</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=4256272">Pixabay</a>

**Background image**

Image by <a href="https://pixabay.com/users/geralt-9301/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=2910663">Gerd Altmann</a> from <a href="https://pixabay.com/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=2910663">Pixabay</a>

### Color Scheme

# Technologies Used

The project uses the following languages;

* HTML5
* CSS
* JavaScript
* jQuery
* Python

The project was created 

# Testing

# Deployment

# Credits

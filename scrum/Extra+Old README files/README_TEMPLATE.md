# Overview

Use this section to outline the vision for the product, including a **use case diagram** that illustrates the main user interactions. This will provide readers with a comprehensive overview of the project.

# Design

## User Stories

US#1: Story Points: 3
    The website lists all items curently available by store on the homepage with no log in required
 
US#2: Story Points: 3
    The restaurant has an Admin account able to add new items and delete old items on the menu through the back end.
   
US#3: Story Points: 5
    The restaurant has an Admin account able to update items on the menu through the back end.      
 
US#4:  Story Points: 10
    Restaurant customers should be able to add and remove items from their purchase cart. The purchase screen will total all added items.
 
US#5:  Story Points: 5
    Restaurant customers should be able to browse and sort the menu by categories: appetizers, entrees, desserts, beverages, and sides.
 
US#6 (optional):  Story Points: 13
    Restaurant customers should be able to save their favorite items/ previous orders to order again.


## Sequence Diagram

At least one **user story**, unrelated to user creation or authentication, must be detailed using a **sequence diagram**.

## Model 

Include a class diagram that clearly describes the model classes used in the project and their associations.

# Development Process 

This section should describe, in general terms, how Scrum was used in this project. Include a table summarizing the division of the project into sprints, the user story goals planned for each sprint, the user stories actually completed, and the start and end dates of each sprint. You may also add any relevant observations about the sprints as you see fit.

|Sprint#|Goals|Start|End|Done|Observations|
|---|---|---|---|---|---|
|1|US#1, US#2, ...|mm/dd/23|mm/dd/23|US#1|...|

As in Project 2, you should take notes on the major sprint meetings: planning, daily scrums, review, and retrospective. Use the scrum folder and the shared templates to record your notes.

# Testing 

In this section, share the results of the tests performed to verify the quality of the developed product, including the test coverage in relation to the written code. There is no minimum code coverage requirement, but ensure there is at least some coverage through one white-box test and one black-box test.

# Deployment 

The final product must demonstrate the integrity of at least 5 out of the 6 planned user stories. It should be packaged as a Docker image and be deployable using:

```
docker compose up
```

Challenge
---------
Have you ever heard of Hacker News? It's a great source of tech-related news. They provide a public API at https://hackernews.api-docs.io.

The goal is to make a web app to make it easier to navigate the news:

Choose a web framework of your choice. Django, Flask, use what you like. 
1. Make a new virtualenv and pip install it;
2. Make a scheduled job to sync the published news to a DB every 5 minutes. 

    _You can start with the latest 100 items, and sync every new item from there._

    __Note__: here are several types of news (items), with relations between them.

3. Implement a view to list the latest news
4. Allow filtering by the type of item
5. Implement a search box for filtering by text

__As there are hundreds of news you probably want to use pagination or lazy loading when you display them.__
It is also important to expose an API so that our data can be consumed:

__GET__ : List the items, allowing filters to be specified;

__POST__ : Add new items to the database (not present in Hacker News);

Bonus
-----
Only display top-level items in the list, and display their children (comments, for example) on a detail page;
In the API, allow updating and deleting items if they were created in the API (but never data that was retrieved from Hacker News);\nBe creative! :)

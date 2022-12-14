Django-Reddit
---------------------

A django app to get latest posts from reddit and multiple other things.



Quickstart
----------
1. Build the images and run the containers:
  ```
    docker-compose up -d --build
  ```

### USAGE From CLI
    
    docker-compose exec -T web python manage.py get_new_posts "name_of_subreddit"
    
   -  for example
    ```
    docker-compose exec -T web python manage.py get_new_posts popular
    ```

    docker-compose exec -T web python manage.py get_new_posts "name_of_subreddit"  [optional-count-of-top-posts]

   -  for example
    ```
    docker-compose exec -T web python manage.py get_new_posts popular -i 16
    ```

### Summary,Limitations,bugs,future work
  The api only fetches the top posts from the subreddit, reddit has different query params for (types,limit and time) of the
  posts.Hot,New,Top etc are the post types.The code only fetches the top 75 posts (a limitation) over a month and calculates the new 
  top posts based on ups (as stated by reddit). The new top posts are not calculated for every subreddit separately but all post together
  in the database. This is also a limitation of the system
  If the project was broader, I would have gone with django rest framework and swagger for a better frontend of the api and given features of filtering, selecting what category of post you want,the time of post and maximum post. Calculating top post for every subreddit separately.
  you want. The project also lacks extensive testing or any test cases.Requires proper exception handling and logging. The exceptions are generalized for now, should change it to what type of exceptions.


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
  The exceptions are generalized for now, should change it to what type of exceptions.
  The api only fetches the new posts, reddit has different query params for post types,limit and time.
  Hot,New,Top etc are the post types. The code only fetches the new post and calculates the top posts based on
  score. If the project was broader, I would have gone with django rest framework and swagger for a better frontend of
  the api.Would've given features of filtering, selecting what category of post you want and the time of post. The project
  also lacks extensive testing or any test cases.Requires proper exception handling and logging.


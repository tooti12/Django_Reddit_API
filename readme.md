Django-Reddit
---------------------

A django app to get latest posts from reddit and multiple other things.



Quickstart
----------
docker compose up -d

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
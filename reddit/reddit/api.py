import requests
import pandas as pd
import json
from reddit.models import Post
class Reddit():

    def __init__(self,subreddit:str,post_type:str='new.json',top_posts_count:int = 15) -> None:
        """Initialize all the required variables.
        We also keep the previous execution ids.
        """
        self.HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/90.0.4430.212 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
        self.base_url = f'https://www.reddit.com/r/{subreddit}'
        self.post_type = post_type
        self.top_posts_count = top_posts_count
        self.post_df = None
        # Fetch the previous post_ids ordered by score.Essentially means ordered by TOP post
        self.previous_execution_post_ids = list(Post.objects.all().order_by('-score').values_list('post_id',flat=True))
        self._load_all_posts_to_df()


    def _get_reddit_request(self)->json:
        """Send a get request to the reddit api.We add the 'new.json'
        to our subreddit to get the latests post only.
        Raises:
            Exception: Api get call failed

        Returns:
            json: Json response from the reddit api
        """
        try:
            url = f'{self.base_url}/{self.post_type}'
            resp = requests.get(url, headers=self.HEADERS)
        except Exception:
            print('Something Went Wrong')
            # Should have proper exception messages and types
            raise Exception('Something went wrong')
        return resp.json()

    def _load_all_posts_to_df(self):
        """Load the json into a pandas dataframe
        """
        results = self._get_reddit_request()
        myDict = {}
        for post in results['data']['children']:
            myDict[post['data']['id']] = {'post_id':post['data']['name'],'title':post['data']['title'],'score':post['data']['score']}
        self.post_df = pd.DataFrame.from_dict(myDict, orient='index')
       
        
    def print_new_post(self):
        """We compare our existing post_ids with the latest ones,
        if there is a different id, we have a new post.
        """
        # New Posts From Previous Execution
        print("-------------------------------------")
        new_posts_from_previous_execution = self.post_df[~self.post_df['post_id'].isin(self.previous_execution_post_ids)]
        if new_posts_from_previous_execution.empty:
            print("Sorry there are no new posts from Last Execution\n")
        else:
            # Add new posts in the db
            print('New posts from the last program execution \n')
            print(f'{new_posts_from_previous_execution}\n')
            model_instances = [Post(post_id=data.post_id,title=data.title,score=data.score) for data in  new_posts_from_previous_execution.itertuples()]
            Post.objects.bulk_create(model_instances)
        print("-------------------------------------")
    def print_updated_vote_count(self):
        """We find all the similar id's from our post_df.
        If the id is similar,we check if the new score is different.
        The new score helps in telling if there was a vote count change.
        """
        # Posts which we already have in our database
        similar_posts_from_new_request = self.post_df[self.post_df['post_id'].isin(self.previous_execution_post_ids)]
        print('Posts that had a vote count change:\n')
        for post_id in similar_posts_from_new_request['post_id']:
            current_post = Post.objects.get(post_id=post_id) # The one in our database
            repeating_post_score = similar_posts_from_new_request[similar_posts_from_new_request['post_id']==post_id].score.iloc[0]
            if current_post.score!= repeating_post_score:
                # Vote count was changed, the post was same but the votes have changed.
                # Score is the sum of (Upvotes - DownVotes)
                if current_post.score<repeating_post_score:
                    print(f'-> {current_post.post_id} - {current_post.title} had a vote count change of {repeating_post_score-current_post.score}\n') 
                else:
                    print(f'-> {current_post.post_id} - {current_post.title} had a vote count change of {current_post.score - repeating_post_score}\n') 
                #Update the new score in the DB
                current_post.score = repeating_post_score
                current_post.save()
        print("-------------------------------------")
    def print_posts_not_in_top(self):
        """ Since score might have been updated or new posts were
        added we again fetch the latest id's order by score.This gives 
        us or new top posts. We compare our new top posts with previous execution
        top posts which we had saved when initializing the class
        """
        top_n_posts = list(Post.objects.all().order_by('-score').values_list('post_id',flat=True))
        n = self.top_posts_count # Number of post we consider to be top
        # Slicing, no check on length since slicing does not give you an error on non-existent values
        print(f'Posts No longer within top {n} posts:\n')
        if set(top_n_posts[:n])!=set(self.previous_execution_post_ids[:n]):
            #Top Posts has changed
            not_top_n_anymore = [id for id in self.previous_execution_post_ids[:n] if id not in top_n_posts[:n] ]
            for id in not_top_n_anymore:  
                post = Post.objects.get(post_id=id)
                print(f'-> {post.post_id} - {post.title}\n')
        print("-------------------------------------")

        
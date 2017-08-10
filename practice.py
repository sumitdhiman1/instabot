import requests
import urllib
from textblob import TextBlob

from textblob.sentiments import NaiveBayesAnalyzer


ACCESS_TOKEN = "4085586844.3191c20.6a3ad10bbcfd45e4899d750e89c81047"
BASE_URL = "https://api.instagram.com/v1/"

''' 
Function declaration to get your own info 
'''


def self_info():
    '''
    1.get self information.....................................
    2.https://api.instagram.com/v1/users/self/?access_token=ACCESS_TOKEN
    '''
    url = BASE_URL + "users/self/?access_token=%s"%ACCESS_TOKEN
    print 'GET request url : %s' % (url)
    user_info = requests.get(url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print "User does not exist!"
    else:
        print "Status code other than 200 received!"

''' 
 Function declaration to get the ID of a user by username 
 '''

def get_user_id(intagram_username):
    '''
    1.Make the url
    2.print url
    '''
    url = BASE_URL + "users/search?q=%s&access_token=%s"%(intagram_username,ACCESS_TOKEN)
    print "GET request url : %s" % (url)
    user_info = requests.get(url).json()['data'][0]['id']
    return user_info


''' 
 Function declaration to get the info of a user by username 
 '''

def get_user_info(instagram_username):
    user_id = get_user_id(instagram_username)
    if user_id == None:
       print 'User does not exist!'
       exit()
    url = BASE_URL + 'users/%s?access_token=%s' % (user_id, ACCESS_TOKEN)
    print "GET request url : %s" % (url)
    user_info = requests.get(url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print "There is no data for this user!"
    else:
        print "Status code other than 200 received!"

''' 
 Function declaration to get your recent post 
'''

def get_own_post():
    url = BASE_URL + 'users/self/media/recent/?access_token=%s'% (ACCESS_TOKEN)
    print 'GET request url : %s' % (url)
    own_media = requests.get(url).json()
    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'

''' 
 Function declaration to get the recent post of a user by username 
'''

def get_user_post(instagram_username):
    user_id = get_user_id(instagram_username)
    if user_id == None:
        print 'User does not exist!'
        exit()

    url = BASE_URL + 'users/%s/media/recent/?access_token=%s'% (user_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (url)
    user_media = requests.get(url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print "Your image has been downloaded!"
        else:
            print "Post does not exist!"
    else:
        print "Status code other than 200 received!"
    return user_media['data'][0]['id']

''' 
 Function declaration to get the ID of the recent post of a user by username 
'''

def get_post_id(instagram_username):
    user_id = get_user_id(instagram_username)
    if user_id == None:
        print 'User does not exist!'
        exit()

    request_url = BASE_URL + 'users/%s/media/recent/?access_token=%s' % (user_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()

''' 
 Function declaration to like the recent post of a user 
 '''




def like_a_post(instagram_username):
    media_id = get_post_id(instagram_username)
    url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": ACCESS_TOKEN}
    print 'POST request url : %s' % (url)
    post_a_like = requests.post(url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'


def get_comment_list(instagram_username):
    media_id = get_user_post(instagram_username)
    url = BASE_URL + "media/%s/comments?access_token=%s" % (media_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (url)
    get_comments = requests.get(url).json()
    if get_comments['meta']['code'] == 200:
        if len(get_comments['data']):
            print "List of comments"
            number = 1
            for text in get_comments['data']:
                print "%s from %s\n comment= %s"%(number,text['from']['username'], text['text'])
                number = number +1
        else:
            print "No comments found"
    else:
        "Status code other than 200 received!"






''' 
 Function declaration to make a comment on the recent post of the user 
'''

def post_a_comment(instagram_username):
    media_id = get_post_id(instagram_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)
    make_comment = requests.post(request_url, payload).json()
    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"


def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, ACCESS_TOKEN)
    print 'GET request url : %s' % (url)
    comment_info = requests.get(url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
        # Here's a naive implementation of how to delete the negative comments :)
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())

                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
         print 'Status code other than 200 received!'



def start_bot():
    while True:
        print '\n'
        print "Hey! Welcome to instaBot!"
        print "Here are your menu options:\n"
        print "a.Get your own details"
        print "b.Get details of a user by username"
        print "c.Get your own recent post"
        print "d.Get the recent post of a user by username"
        print "e.Like the recent post of a user"
        print "f.Get a list of comments on the recent post of a user"
        print "g.Make a comment on the recent post of a user"
        print "h.Delete negative comments from the recent post of a user"
        print "i.Exit"

        choice = raw_input("Enter you choice: ")
        if choice == "a":
            self_info()
        elif choice == "b":
            instagram_username = raw_input("Enter the username of the user: ")
            get_user_info(instagram_username)
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            instagram_username = raw_input("Enter the username of the user: ")
            get_user_post(instagram_username)
        elif choice == "e":
            insta_username = raw_input("Enter the username of b the user: ")
            like_a_post(insta_username)
        elif choice == "f":
            insta_username = raw_input("Enter the username of the user: ")
            get_comment_list(insta_username)
        elif choice == "g":
            insta_username = raw_input("Enter the username of the user: ")
            post_a_comment(insta_username)
        elif choice == "h":
            instagram_username = raw_input("Enter the username of the user: ")
            delete_negative_comment(instagram_username)
        elif choice == "i":
           exit()
        else:
            print "wrong choice"
start_bot()













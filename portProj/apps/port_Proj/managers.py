from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import datetime

NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
# Managers
class UserManager(models.Manager):
    def validate_registration(self, post_data):
        errors = []
        if len(post_data['first_name']) < 2 or len(post_data['last_name']) < 2 or len(post_data['username']) < 2:
            errors.append("All name fields must be at least three characters")
        if len(post_data['password']) < 8 and len(post_data['password']) < 35:
            errors.append("this password should be more than 8 characters and less than 35 characters")
        if not re.match(NAME_REGEX, post_data['first_name']) or not re.match(NAME_REGEX, post_data['last_name']) or not re.match(NAME_REGEX, post_data['username']):
            errors.append("All name fields must be letters only")
        if post_data['password'] != post_data['password_confirm']:
            errors.append("passwords do not match")

        if not errors:
            hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))
            
            new_user = self.create(
                first_name=post_data['first_name'],
                last_name=post_data['last_name'],
                username=post_data['username'],
                password=hashed,
                post_level="Irrelevant"
            )
            return new_user
        return errors
    def validate_login(self, post_data):
        errors = []
        if len(self.filter(username=post_data['username'])) > 0:
            user = self.filter(username=post_data['username'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append("Invalid Login Information")
        else:
            errors.append("Invalid Login Information")
        if errors:
            return errors
        return user
    def validate_edit(self, post_data, said_id):
        errors = []
        if len(post_data['first_name']) < 2 or len(post_data['last_name']) < 2 or len(post_data['username']) < 2:
            errors.append("All name fields must be at least three characters")
        if len(post_data['password']) < 8 and len(post_data['password']) < 35:
                errors.append("this password should be more than 8 characters and less than 35 characters")
        if not re.match(NAME_REGEX, post_data['first_name']) or not re.match(NAME_REGEX, post_data['last_name']) or not re.match(NAME_REGEX, post_data['username']):
            errors.append("All name fields must be letters only")
        if not errors:
            hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))
            edited_user = models.Users.objects.filter(id=said_id).update(first_name = post_data['first_name'], last_name = post_data['last_name'], username = post_data['username'], password = hashed)
            return edited_user
        return errors
    def delete_user(self, user_id):
        errors = []
        if len(self.filter(id=user_id)) > 0:
            user = models.Users.objects.get(id = user_id)
            user.delete()
        elif len(self.filter(id=user_id)) == 0:
            errors.append("There's no user here!")
            return errors

class PostManager(models.Manager):
    def validate_post(self, post_data, user_id):
        errors = []
        if len(post_data['content']) < 5:
            errors.append("Please do something more than five characters. Come on, dude.")
        else:
            words_check = post_data('content').split()
            for a in range(0, words_check.length):
                if re.match(EMAIL_REGEX, a):
                    errors.append("Please do not put email addresses in posts. we're better than that guys")
            if not errors:
                new_post = self.create(
                    page=user_id,
                    content=post_data['content']
                )
                return new_post
        return errors
    def delete_post(self, post_id):
        post = models.Posts.objects.get(id = post_id)
        post.delete()
        print("post deleted")
        return True

class CommentManager(models.Manager):
    def validate_comment(self, post_data, user_id):
        errors = []
        if len(post_data['comment']) < 5:
            errors.append("Please do something more than five characters. Come on, dude.")
        else:
            words_check = post_data('comment').split()
            for a in range(0, words_check.length):
                if re.match(EMAIL_REGEX, a):
                    errors.append("Please do not put email addresses in posts. we're better than that guys")
            if not errors:
                new_comment = self.create(
                    post_id=post_data['post_id'],
                    comment=post_data['comment'],
                    user = user_id
                )
                return new_comment
        return errors
    def delete_comment(self, comment_id):
        comment = models.Comments.objects.get(id=comment_id)
        comment.delete()
        print("comment deleted")
        return True
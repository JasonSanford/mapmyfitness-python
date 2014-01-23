from .base import BaseValidator


class UserValidator(BaseValidator):
    def validate_search(self):
        search_kwargs = self.search_kwargs

        if 'friends_with' not in search_kwargs and 'requested_friendship_with' not in search_kwargs and 'suggested_friends_for' not in search_kwargs:
            self.add_error('Either a friends_with, requested_friendship_with or suggested_friends_for argument must be passed to search for users.')
            return

        if 'friends_with' in search_kwargs:
            if not isinstance(search_kwargs['friends_with'], int):
                self.add_error('User friends_with must be of type int.')
        elif 'requested_friendship_with' in search_kwargs:
            if not isinstance(search_kwargs['requested_friendship_with'], int):
                self.add_error('User requested_friendship_with must be of type int.')
        else:  # suggested_friends_for
            if 'suggested_friends_source' not in search_kwargs and 'suggested_friends_emails' not in search_kwargs:
                self.add_error('User suggested_friends_source or suggested_friends_emails must exist when searching users via suggested_friends_for.')
                return
            if 'suggested_friends_source' in search_kwargs:
                if search_kwargs['suggested_friends_source'] != 'facebook':
                    self.add_error('User suggested_friends_source must be "facebook".')
            else:  # suggested_friends_emails
                if not search_kwargs['suggested_friends_emails']:
                    self.add_error('User suggested_friends_emails must not be empty.')

import numpy as np
import pandas as pd
import hashlib
import datetime
from werkzeug import generate_password_hash, check_password_hash
import re
from helpers import hash_password

class User:
    """
    User class. Has methods that inserts to and reads from the User table.
    """
    def __init__(self, first_name, last_name, email, phone, credit_card, type_of_user):
        df = pd.read_csv('database/User.csv')

        df.loc[len(df)] = pd.Series(data=[' ', ' ', first_name, last_name, email, phone, credit_card, type_of_user,'','','',''],
                           index=['username', 'password', 'first_name', 'last_name', 'email', 'phone', 'credit_card', 'type_of_user','portfolio', 'about', 'resume', 'interests'])
        df.to_csv('database/User.csv', index=False)

    @staticmethod
    def has_user_id(username):
        """
        Returns True if the username exists in the User table.
        Returns False otherwise.
        """
        df = pd.read_csv('database/User.csv')
        tmp = df.loc[df['username'] == username]

        return not tmp.empty

    @staticmethod
    def set_credentials(username, password, email):
        """
        After a user is approved, the user can set his/her official username and password.
        This method stores this information in the User table.
        """
        # Change the login credentials in Applicant database
        df = pd.read_csv('database/Applicant.csv')
        df.loc[df.email == email, 'username'] = username
        df.loc[df.email == email, 'password'] = hash_password(password)
        df.to_csv('database/Applicant.csv', index=False)
        # Change the login credentials in User database
        df = pd.read_csv('database/User.csv')
        df.loc[df.email == email, 'username'] = username
        df.loc[df.email == email, 'password'] = hash_password(password)
        df.to_csv('database/User.csv', index=False)

    
    @staticmethod
    def use_old_credentials(username, email):
        """
        After a user is approved, the user can keep their old username and password.
        This method stores this information in the User table.
        """
        df = pd.read_csv('database/Applicant.csv')
        password = df.loc[df.user_id == username, 'password']
        df = pd.read_csv('database/User.csv')
        df.loc[df.email == email, 'username'] = username
        df.loc[df.email == email, 'password'] = password
        df.to_csv('database/User.csv', index=False)

    @staticmethod
    def check_password(username, password):
        """
        Checks if the password of a username match. 
        Returns true if password given matches the password for username 
        given and false if the password does not match.
        """
        df = pd.read_csv('database/User.csv')
        user = df.loc[df['username'] == username]
        if not user.empty:
            pwhash = user['password'].item()
            return pwhash == hash_password(password)  

    @staticmethod
    def get_user_info(username):
        """
        Returns a dictionary of the user's information.
        """
        df = pd.read_csv('database/User.csv')
        user = df.loc[df['username'] == username]

        if not user.empty:
            return {'username': username,
                    'first_name': user['first_name'].item(),
                    'last_name': user['last_name'].item(),
                    'email': user['email'].item(),
                    'phone': user['phone'].item(),
                    'type_of_user': user['type_of_user'].item(),
                    'credit_card': user['credit_card'].item(),
                    'about': user['about'].item(),
                    'link_to_user': '/user/' + username,
                    'portfolio': user['portfolio'].item(),
                    'interests': user['interests'].item(),
                    'resume': user['resume'].item()}

    @staticmethod
    def get_number_of_users():
        """
        Returns the number of users stored in the database. Excludes NaNs.
        """
        df = pd.read_csv('database/User.csv')
        return df['username'].count() # does not count NaNs

    @staticmethod
    def does_user_have_enough_money(username,amount):
        """
        Returns whether [username] has enough balance in their account to afford a transaction of 
        [amount] dollars.
        """
        df = pd.read_csv('database/User.csv')
        user = df.loc[df.username == username]
        type_of_user = user['type_of_user'].item()
        balance = 0
        if type_of_user == 'client':
            df = pd.read_csv('database/Client.csv')
            user = df.loc[df.username == username]
            balance = user['balance'].item()
        elif type_of_user == 'developer':
            df = pd.read_csv('database/Developer.csv')
            user = df.loc[df.username == username]
            balance = user['balance'].item()
        return balance >= amount

    @staticmethod
    def delete_user(username):
        """
        Deletes [username]'s account
        """
        if User.has_user_id(username):
            df = pd.read_csv('database/User.csv')
            type_of_user = df.loc[df.username == username]['type_of_user'].item()
            df = df.loc[df.username != username]
            df.to_csv('database/User.csv', index=False)

            if type_of_user == 'client':
                df = pd.read_csv('database/Client.csv')
                df = df.loc[df.username != username]
                df.to_csv('database/Client.csv', index=False)

            elif type_of_user == 'developer':
                df = pd.read_csv('database/Developer.csv')
                df = df.loc[df.username != username]
                df.to_csv('database/Developer.csv', index=False)

    @staticmethod
    def set_username(username,new_username):
        """
        Modifies the user's username.
        """
        df = pd.read_csv('database/User.csv')
        user = df.loc[df['username'] == username]
        if not user.empty:
            df.loc[df.username == username, 'username'] = new_username
            df.to_csv('database/User.csv', index=False)

    @staticmethod
    def set_password(username,password):
        """
        Modifies the user's password.
        """
        df = pd.read_csv('database/User.csv')
        user = df.loc[df['username'] == username]
        if not user.empty:
            df.loc[df.username == username, 'password'] = hash_password(password)
            df.to_csv('database/User.csv', index=False)

    @staticmethod
    def set_first_name(username,first_name):
        """
        Modifies the user's first name.
        """
        df = pd.read_csv('database/User.csv')
        user = df.loc[df['username'] == username]
        if not user.empty:
            df.loc[df.username == username, 'first_name'] = first_name
            df.to_csv('database/User.csv', index=False)

    @staticmethod
    def set_last_name(username,last_name):
        """
        Modifies the user's last name.
        """
        df = pd.read_csv('database/User.csv')
        user = df.loc[df['username'] == username]
        if not user.empty:
            df.loc[df.username == username, 'last_name'] = last_name
            df.to_csv('database/User.csv', index=False)

    @staticmethod
    def set_email(username,email):
        """
        Modifies the user's email.
        """
        df = pd.read_csv('database/User.csv')
        user = df.loc[df['username'] == username]
        if not user.empty:
            df.loc[df.username == username, 'email'] = email
            df.to_csv('database/User.csv', index=False)


    @staticmethod
    def set_phone(username,phone):
        """
        Modifies the user's phone.
        """
        df = pd.read_csv('database/User.csv')
        user = df.loc[df['username'] == username]
        if not user.empty:
            df.loc[df.username == username, 'phone'] = phone
            df.to_csv('database/User.csv', index=False)

    @staticmethod
    def set_about(username, about):
        """
        Modifies the user's about/info.
        """
        df = pd.read_csv('database/User.csv')
        user = df.loc[df['username'] == username]

        if not user.empty:
            df.loc[df.username == username, 'about'] = about
            df.to_csv('database/User.csv', index=False)

    @staticmethod
    def set_resume(username,resume):
        """
        Modifies the user's resume.
        """
        df = pd.read_csv('database/User.csv')
        user = df.loc[df['username'] == username]
        if not user.empty:
            df.loc[df.username == username, 'resume'] = resume
            df.to_csv('database/User.csv', index=False)

    @staticmethod
    def set_portfolio(username,portfolio):
        """
        Modifies the user's portfolio.
        """
        df = pd.read_csv('database/User.csv')
        user = df.loc[df['username'] == username]
        if not user.empty:
            df.loc[df.username == username, 'portfolio'] = portfolio
            df.to_csv('database/User.csv', index=False)

    @staticmethod
    def set_interests(username,interests):
        """
        Modifies the user's interests.
        """
        df = pd.read_csv('database/User.csv')
        user = df.loc[df['username'] == username]
        if not user.empty:
            df.loc[df.username == username, 'interests'] = interests
            df.to_csv('database/User.csv', index=False)

class Client:
    """
    Client class. Has methods that inserts to and reads from the Client table.
    """
    def __init__(self, username):
        df = pd.read_csv('database/Client.csv')

        df.loc[len(df)] = pd.Series(data=[username, 0, 0, 0, 0, 100],
            index=['username', 'avg_rating', 'avg_given_rating', 'num_of_completed_projects', 'num_of_warnings', 'balance'])
        df.to_csv('database/Client.csv', index=False)

    @staticmethod
    def get_info(username):
        """
        Returns a dictionary of information for the given developer.
        """
        df = pd.read_csv('database/Client.csv')
        client = df.loc[df.username == username]

        return {'username': username,
                'avg_rating': client['avg_rating'].item(),
                'avg_given_rating': client['avg_given_rating'].item(),
                'num_of_completed_projects': client['num_of_completed_projects'].item(),
                'num_of_warnings': client['num_of_warnings'].item(),
                'balance': client['balance'].item()}

    @staticmethod
    def get_projects_posted(username):
        """
        Returns a list of all demands that the client posted.
        """
        df = pd.read_csv('database/Demand.csv')
        projects = df.loc[df.client_username == username]

        return projects.index.tolist()
    
    @staticmethod
    def get_past_projects(username):
        """
        Returns a list of all demands that the client posted.
        """
        df = pd.read_csv('database/Demand.csv')
        projects = df.loc[(df.client_username == username) & (df.is_completed)]

        return projects.index.tolist()

    @staticmethod
    def get_number_of_clients():
        """
        Returns the number of clients in the client database. Excludes NaNs.
        """
        df = pd.read_csv('database/Client.csv')
        return df['username'].count() # does not count NaNs

    @staticmethod
    def get_most_active_clients():
        """
        Returns the top 3 clients with the most projects completed.
        """
        df = pd.read_csv('database/Client.csv')
        sorted_df = df.sort_values(by='num_of_completed_projects', ascending=False)
        sorted_df = sorted_df.iloc[:3]

        usernames = []
        for index, row in sorted_df.iterrows():
            if not BlacklistedUser.is_blacklisted(row['username']):
                usernames.append(User.get_user_info(row['username']))

        return usernames

    @staticmethod
    def get_clients_with_most_projects():
        """
        Returns the top 3 clients with the most projects, completed or not.
        This is used on the index page.
        """
        df = pd.read_csv('database/Demand.csv')
        projects = df.groupby(['client_username']).size()
        projects = projects.sort_values(ascending=False)

        usernames = []
        for index, value in projects.iteritems():
            if len(usernames) == 3:
                break;
            usernames.append(index)

        return usernames

    @staticmethod
    def get_similar_clients(username):
        """
        Returns three clients with similar interests as the specified user, based
        on tags of the user's most recent completed projects.
        """
        projects = []
        user_type = User.get_user_info(username)['type_of_user']
        if user_type == 'client':
            projects = Client.get_projects_posted(username)
        else: #is developer
            projects = Developer.get_past_projects(username)
        
        tags = ""
        for index in projects:
            demand = Demand.get_info(index)
            tags += str(demand['tags']) + " "
        print("tag", tags)
        similar_projects = Demand.get_filtered_demands(None, None, None, None, tags, None, None)
        print(similar_projects)
        similar_clients = []
        similar_clients_usernames=[]

        for index in similar_projects:
            if len(similar_clients) == 3:
                break
            demand = Demand.get_info(index)
            if not (demand['client_username'] == username) and not (demand['chosen_developer_username'] == username):
                if demand['client_username'] not in similar_clients_usernames and not BlacklistedUser.is_blacklisted(demand['client_username']) and not DeleteRequest.is_account_deleted(demand['client_username']):
                    similar_clients_usernames.append(demand['client_username'])
                    similar_clients.append(User.get_user_info(demand['client_username']))

        return similar_clients

    @staticmethod
    def add_to_balance(username, amount):
        """
        Adds amount of funds to balance.
        """
        df = pd.read_csv('database/Client.csv')
        client = df.loc[df.username == username]
        df.loc[df.username == username, 'balance'] = amount + client['balance'].item()
        df.to_csv('database/Client.csv', index=False)


class Developer:
    """
    Developer class. Has methods that inserts to and reads from the Developer table.
    """
    def __init__(self, username):
        df = pd.read_csv('database/Developer.csv')

        df.loc[len(df)] = pd.Series(data=[username, 0, 0, 0, 0, 0, 0],
            index=['username', 'avg_rating', 'avg_given_rating', 'num_of_completed_projects', 'num_of_warnings', 'balance', 'earnings'])
        df.to_csv('database/Developer.csv', index=False)

    @staticmethod
    def get_info(username):
        """
        Returns a dictionary of information for the given developer.
        """
        df = pd.read_csv('database/Developer.csv')
        developer = df.loc[df.username == username]

        return {'username': username,
                'avg_rating': developer['avg_rating'].item(),
                'avg_given_rating': developer['avg_given_rating'].item(),
                'num_of_completed_projects': developer['num_of_completed_projects'].item(),
                'num_of_warnings': developer['num_of_warnings'].item(),
                'balance': developer['balance'].item()}

    @staticmethod
    def get_past_projects(username):
        """
        Returns a list of past demands that the developer worked on.
        These past demands are ones that are completed.
        """
        df = pd.read_csv('database/Demand.csv')
        projects = df.loc[(df.chosen_developer_username == username) & (df.is_completed)]

        return projects.index.tolist()

    @staticmethod
    def get_number_of_developers():
        """
        Returns the number of developers in the developer database. Excludes NaNs.
        """
        df = pd.read_csv('database/Developer.csv')
        return df['username'].count() # does not count NaNs

    @staticmethod
    def get_most_active_developers():
        """
        Returns the top 3 developers with the most projects completed.
        """
        df = pd.read_csv('database/Developer.csv')
        sorted_df = df.sort_values(by='num_of_completed_projects', ascending=False)
        sorted_df = sorted_df.iloc[:3]

        usernames = []
        for index, row in sorted_df.iterrows():
            if not BlacklistedUser.is_blacklisted(row['username']):
                usernames.append(User.get_user_info(row['username']))

        return usernames

    @staticmethod
    def get_similar_developers(username):
        """
        Returns three developers with similar interests as the specified user, based
        on tags of the user's most recent completed projects.
        """
        projects = []
        user_type = User.get_user_info(username)['type_of_user']
        if user_type == 'client':
            projects = Client.get_projects_posted(username)
        else: #is developer
            projects = Developer.get_past_projects(username)
        
        tags = ""
        for index in projects:
            demand = Demand.get_info(index)
            tags += str(demand['tags']) + " "
        print("tag", tags)
        similar_projects = Demand.get_filtered_demands(None, None, None, None, tags, None, None)
        similar_developers = []
        similar_developers_usernames = []

        for index in similar_projects:
            if len(similar_developers) == 3:
                break
            demand = Demand.get_info(index)
            if not (demand['client_username'] == username) and not (demand['chosen_developer_username'] == username):
                if demand['chosen_developer_username'] not in similar_developers_usernames and not BlacklistedUser.is_blacklisted(demand['chosen_developer_username']) and not DeleteRequest.is_account_deleted(demand['chosen_developer_username']):
                    similar_developers_usernames.append(demand['chosen_developer_username'])
                    similar_developers.append(User.get_user_info(demand['chosen_developer_username']))

        return similar_developers

    @staticmethod
    def get_top_earners():
        """
        Returns a list of usernames belonging to the three developers with the most earnings.
        """
        df = pd.read_csv('database/Developer.csv')
        df = df.loc[df.earnings > 0]
        sorted_df = df.sort_values(by='earnings', ascending=False)

        if (len(sorted_df) > 3):
            return sorted_df.username.tolist()[:3]
        else:
            return sorted_df.username.tolist()

    @staticmethod
    def submit_system(demand_id, username):
        """
        Updates the Demand table so that the project is complete.
        Also notifies the client that the project is complete.
        """
        df = pd.read_csv('database/Demand.csv')
        df.loc[int(demand_id), 'is_completed'] = True

        demand_info = Demand.get_info(demand_id)

        message = 'The system for the {} demand has been uploaded. Please rate {} <a href="/bid/{}/rating/{}">here</a>.'.format(demand_info['title'], username, demand_id, username)
        Notification(demand_info['client_username'], username, message)
        df.to_csv('database/Demand.csv', index=False)

    @staticmethod
    def add_earnings(username, amount):
        """
        Updates the Developer table.
        Adds amount to the developer's current amount of earnings.
        """
        df = pd.read_csv('database/Developer.csv')
        df.loc[df['username'] == username, 'earnings'] += amount
        df.to_csv('database/Developer.csv', index=False)

class Applicant:
    """
    Applicant class. Has methods that inserts to and reads from the Applicant table.
    """
    def __init__(self, type_of_user, first_name, last_name, email, phone,
                 card_info, temp_user_id, password):
        """
        Create a new applicant and store the information in the database.
        """
        df = pd.read_csv('database/Applicant.csv')

        hashed = hash_password(password)

        df.loc[len(df)] = pd.Series(data=[first_name, last_name, email,
                            phone, card_info, temp_user_id, hashed, type_of_user, 'pending'],
                           index=['first_name', 'last_name',
                           'email', 'phone', 'credit_card', 'user_id',
                           'password', 'type_of_user', 'status'])
        df.to_csv('database/Applicant.csv', index=False)

    def validate_email(self, email):
        """
        Validates the email, which should be unique from other emails.
        The email should also be in the correc format.
        Returns True if the email is valid. Returns False otherwise.
        """
        df = pd.read_csv('database/Applicant.csv')
        tmp = df.loc[df['email'] == email]

        return tmp.empty

    def has_user_id(self, user_id):
        """
        Validates the temporary user id, which should be unique from other user IDs.
        Returns True if the user ID already exists in the Applicant table.
        Returns False if the user ID does not already exist.
        """
        df = pd.read_csv('database/Applicant.csv')
        tmp = df.loc[df['temp_user_id'] == user_id]

        return not tmp.empty

    @staticmethod
    def get_applicant_info(user_id):
        """
        Returns a dictionary of the applicant's information.
        """
        df = pd.read_csv('database/Applicant.csv')
        user = df.loc[df['user_id'] == user_id]

        if not user.empty:
            return {'user_id': user_id,
                    'first_name': user['first_name'].item(),
                    'last_name': user['last_name'].item(),
                    'email': user['email'].item(),
                    'phone': user['phone'].item(),
                    'credit_card': int(user['credit_card'].item()),
                    'type_of_user': user['type_of_user'].item(),
                    'status': user['status'].item(),
                    'reason': user['reason'].item()}

    @staticmethod
    def is_unique_user_id(user_id):
        """
        Checks whether user_id is unique.
        Returns True if user_id is unique and False if user_id is not unique.
        """
        df0 = pd.read_csv('database/Applicant.csv')
        tmp0 = df0.loc[df0['user_id'] == user_id]

        df1 = pd.read_csv('database/User.csv')
        tmp1 = df1.loc[df1['username'] == user_id]

        df2 = pd.read_csv('database/SuperUser.csv')
        tmp2 = df2.loc[df2['username'] == user_id]

        return tmp0.empty and tmp1.empty and tmp2.empty

    @staticmethod
    def is_unique_email(email):
        """
        Checks whether email is unique.
        Returns True if email is unique and False if email is not unique.
        """
        df0 = pd.read_csv('database/Applicant.csv')
        tmp0 = df0.loc[df0['email'] == email]

        df1 = pd.read_csv('database/User.csv')
        tmp1 = df1.loc[df1['email'] == email]

        df2 = pd.read_csv('database/SuperUser.csv')
        tmp2 = df2.loc[df2['email'] == email]

        return tmp0.empty and tmp1.empty and tmp2.empty

    @staticmethod
    def check_password(user_id, password):
        """
        Checks if the password of a user_id match. 
        Returns true if password given matches the password for user_id 
        given and false if the password does not match.
        """
        df = pd.read_csv('database/Applicant.csv')
        user = df.loc[df['user_id'] == user_id]
        if not user.empty:
            pwhash = user['password'].item()
            return pwhash == hash_password(password) 

    @staticmethod
    def approve(user_id):
        """
        Approves the applicant and adds the user to the User table.
        After adding to the User table, the applicant's status is changed to approved.
        """
        # get the applicant's information from the table
        df = pd.read_csv('database/Applicant.csv')
        user = df.loc[df.user_id == user_id]

        if not user.empty:
            if user['status'].item() == 'pending':
                # create a new row in the User table
                User(user['first_name'].item(), user['last_name'].item(), user['email'].item(), user['phone'].item(),
                    user['credit_card'].item(), user['type_of_user'].item())

                # update status
                df.loc[df.user_id == user_id, 'status'] = 'approved'
                df.to_csv('database/Applicant.csv', index=False)


    @staticmethod
    def reject(user_id, reason):
        """
        Reject the applicant. The applicant's status is changed to rejected.
        """
        df = pd.read_csv('database/Applicant.csv')
        user = df.loc[df.user_id == user_id]

        if user['status'].item() == 'pending':
            # update status
            df.loc[df.user_id == user_id, 'status'] = 'rejected'
            df.loc[df.user_id == user_id, 'reason'] = reason
            df.to_csv('database/Applicant.csv', index=False)

    @staticmethod
    def get_pending_applicants():
        """
        Gets all applicants with a status of 'pending'
        """
        df = pd.read_csv('database/Applicant.csv')
        get_apps = df.loc[df['status'] == 'pending']
        pending_applicants = get_apps.T.to_dict().values()
        return pending_applicants

class Demand:
    """
    Demand class. Has methods that inserts to, reads from, and modifies Demand table.
    """
    def __init__(self, client_username, title, tags, specifications, bidding_deadline, submission_deadline):
        """
        Create a new demand by adding a row with the information to the Demand table.
        Returns the demand_id, which is the index of the row that was just added.
        """
        df = pd.read_csv('database/Demand.csv')

        now = datetime.datetime.now()
        format = '%m-%d-%Y %I:%M %p'
        date_posted = now.strftime(format)

        df.loc[len(df)] = pd.Series(data=[client_username, date_posted, title, tags, specifications, bidding_deadline, submission_deadline, False, False, False, False],
            index=['client_username', 'date_posted', 'title', 'tags', 'specifications', 'bidding_deadline', 'submission_deadline', 'is_completed', 'bidding_deadline_approaching_notif_sent', 'is_expired', 'submission_deadline_approaching_notif_sent'])

        df.to_csv('database/Demand.csv', index=False)

    @staticmethod
    def get_most_recent_demand_id():
        df = pd.read_csv('database/Demand.csv')
        return df.index.values.tolist()[-1]

    @staticmethod
    def get_info(demand_id):
        """
        Returns a dictionary of information for the specified demand.
        """
        df = pd.read_csv('database/Demand.csv')
        demand = df.loc[int(demand_id)]

        now = datetime.datetime.now()
        deadline_passed = datetime.datetime.strptime(demand['bidding_deadline'], '%m-%d-%Y %I:%M %p') < now

        bids = Bid.get_bids_for_demand(demand_id)
        if len(bids) > 0:
            lowest_bid = Bid.get_info(bids[0])['bid_amount']
        else:
            lowest_bid = None

        if not demand.empty:
            return {'client_username': demand['client_username'],
                    'date_posted': demand['date_posted'],
                    'title': demand['title'],
                    'tags': demand['tags'],
                    'specifications': demand['specifications'],
                    'bidding_deadline': demand['bidding_deadline'],
                    'submission_deadline': demand['submission_deadline'],
                    'is_completed': demand['is_completed'],
                    'is_expired': demand['is_expired'],
                    'bidding_deadline_passed': deadline_passed,
                    'chosen_developer_username' : demand['chosen_developer_username'],
                    'chosen_bid_amount': demand['bid_amount'],
                    'developer_was_chosen': not pd.isnull(demand['chosen_developer_username']),
                    'min_bid': lowest_bid,
                    'link_to_client': '/user/' + demand['client_username'],
                    'link_to_demand': '/bid/' + str(demand_id)}

    @staticmethod
    def get_all_demands():
        """
        Returns a list of all demands.
        The demands are ordered from most recent to least recent.
        """
        df = pd.read_csv('database/Demand.csv')
        return df.index.tolist()[::-1]

    @staticmethod
    def get_filtered_demands(start_date, end_date, client, client_rating, tags, min_bid, active):
        """
        Returns a list of demands that are filtered.
        The demands are ordered from most recent to least recent.
        """
        filtered = pd.read_csv('database/Demand.csv')
        now = datetime.datetime.now()
        filtered['date_posted'] = pd.to_datetime(filtered['date_posted'])
        filtered['bidding_deadline'] = pd.to_datetime(filtered['bidding_deadline'])

        # filter by date posted
        if start_date is not None and start_date != '':
            filtered = filtered.loc[filtered.date_posted >= start_date]

        if end_date is not None and end_date != '':
            filtered = filtered.loc[filtered.date_posted <= end_date]

        # filter by client's username
        if client is not None and client != '':
            filtered = filtered.loc[filtered.client_username == client]

        # filter by active status
        if active != False:
            filtered = filtered.loc[(filtered.bidding_deadline > now) & (filtered.is_completed == False)]

        # filter by client_rating
        if client_rating is not None:
            client_df = pd.read_csv('database/Client.csv')
            merged = pd.merge(filtered, client_df, how='left', left_on=['client_username'], right_on=['username'])
            filtered = merged.loc[merged.avg_rating >= client_rating]

        # filter by the minimum bid amount
        if min_bid is not None:
            def lowest_bid(demand_id):
                bids = Bid.get_bids_for_demand(demand_id)
                return float(Bid.get_info(bids[0])['bid_amount']) if len(bids) > 0 else None

            filtered['lowest_bid'] = pd.Series(filtered.index.map(lowest_bid))
            filtered = filtered.loc[(filtered.lowest_bid >= min_bid) | (filtered.lowest_bid.isnull())]

        # filter by tags
        if tags is not None and tags != '':
            # remove punctuation, change words to lowercase
            tags = map(lambda x: x.lower(), re.findall(r'[^\s!,.?":;0-9]+', tags))
            tags = set(tags)

            def has_tag(demand_id):
                demand_tags = map(lambda x: x.lower(), re.findall(r'[^\s!,.?":;0-9]+', Demand.get_info(demand_id)['tags']))
                demand_tags = set(demand_tags)

                # if there is an intersection between the sets, there are matching tags
                return len(tags & demand_tags) > 0

            filtered['has_tag'] = pd.Series(filtered.index.map(has_tag))
            filtered = filtered.loc[filtered.has_tag == True]

        return filtered.sort_values(['date_posted'], ascending=[True]).index.tolist()[::-1]

    @staticmethod
    def get_current_projects(username):
        """
        Returns index of projects related to username.
        """
        df = pd.read_csv('database/Demand.csv')
        projects = df.loc[((df.chosen_developer_username == username) | (df.client_username == username)) 
                    & (df.is_completed == False) & (df.chosen_developer_username.notnull())]
        
        return projects.index.tolist()

    
    @staticmethod
    def choose_developer(demand_id, developer_username, client_username, bid_amount, reason=None):
        """
        Update the Demand table when a client chooses a developer for a certain demand.
        Also half of the bid amount is transferred from the client to the developer.
        """
        df = pd.read_csv('database/Demand.csv')
        df.loc[int(demand_id), 'chosen_developer_username'] = developer_username
        df.loc[int(demand_id), 'bid_amount'] = bid_amount
        df.to_csv('database/Demand.csv', index=False)

        # notify the developer that he/she was chosen to implement the system
        demand_title = Demand.get_info(demand_id)['title']
        message = 'Congratulations! You were chosen by {} for the {} demand.'.format(client_username, demand_title)
        Notification(developer_username, client_username, message)

        # transfer money from client to developer
        Transaction(developer_username, client_username, float(bid_amount) / 2, reason)

    @staticmethod
    def check_approaching_bidding_deadlines():
        """
        Checks for any approaching bidding deadlines for all of the demands.
        If the deadline is within 24 hours, a notification will be sent to the client
        who created the demand. Only one notification will be sent.
        """
        df = pd.read_csv('database/Demand.csv')
        now = datetime.datetime.now()

        for index, row in df.iterrows():
            dt = datetime.datetime.strptime(row['bidding_deadline'], '%m-%d-%Y %I:%M %p')
            time_diff = (dt - now).days
            if time_diff <= 1 and (not row['bidding_deadline_approaching_notif_sent']):
                message = 'The deadline for your {} demand is approaching.'.format(row['title'])
                Notification(row['client_username'], 'superuser0', message)
                df.loc[index, 'bidding_deadline_approaching_notif_sent'] = True

        df.to_csv('database/Demand.csv', index=False)

    @staticmethod
    def check_approaching_submission_deadlines():
        """
        Checks for any approaching submission deadlines for all of the demands.
        if the deadline is within 24 hours, a notification will be sent to the
        developer who is assigned the demand. Only one notification will be sent.
        """
        df = pd.read_csv('database/Demand.csv')
        now = datetime.datetime.now()

        for index, row in df.iterrows():
            if (not row['is_expired']) and (row['chosen_developer_username'] is not None):
                dt = datetime.datetime.strptime(row['submission_deadline'], '%m-%d-%Y %I:%M %p')
                time_diff = (dt - now).days
                if time_diff <= 1 and (not row['submission_deadline_approaching_notif_sent']):
                    message = 'The deadline for submitting your system for the {} demand is approaching.'.format(row['title'])
                    Notification(row['chosen_developer_username'], 'superuser0', message)
                    df.loc[index, 'submission_deadline_approaching_notif_sent'] = True

        df.to_csv('database/Demand.csv', index=False)

    @staticmethod
    def check_expired_demands():
        """
        Checks for any demands that are passed their bidding deadlines
        and have no bidders. These systems are marked as expired, and
        the client who posted the demand pays a $10 fee.
        """
        df = pd.read_csv('database/Demand.csv')
        now = datetime.datetime.now()

        for index, row in df.iterrows():
            if not row['is_expired']:
                dt = datetime.datetime.strptime(row['bidding_deadline'], '%m-%d-%Y %I:%M %p')
                num_bids = len(Bid.get_bids_for_demand(index))

                # if the bidding deadline passed and there are no bids for this demand,
                # make it expired
                if (now > dt) and (num_bids == 0):
                    df.loc[index, 'is_expired'] = True
                    message = 'Your {} demand expired at {}. $10 is taken off of your balance.'.format(row['title'], row['bidding_deadline'])
                    Notification(row['client_username'], 'superuser0', message)
                    Transaction('superuser0', row['client_username'], 10)

        df.to_csv('database/Demand.csv', index=False)

    @staticmethod
    def check_overdue_demands():
        """
        Checks for any demands that are passed their submission deadlines and are
        not already completed by the chosen developers. These systems are arked as expired,
        and the chosen developer has to pay back the amount of money that was originally
        given to them at the beginning, along with a fee of $10.
        """
        df = pd.read_csv('database/Demand.csv')
        now = datetime.datetime.now()

        for index, row in df.iterrows():
            if not row['is_expired']:
                dt = datetime.datetime.strptime(row['submission_deadline'], '%m-%d-%Y %I:%M %p')
                chosen_developer = row['chosen_developer_username']

                # the chosen developer did not complete the system in time
                if (now > dt) and (chosen_developer is not None) and not row['is_completed']:
                    df.loc[index, 'is_expired'] = True
                    fee = round(row['bid_amount'] + 10, 2)
                    message = 'The deadline for submitting the system demand {} is over. ${} is taken off your balance as a penalty fee.'.format(Demand.get_info(index)['title'], fee)
                    Notification(chosen_developer, 'superuser0', message)
                    Transaction(chosen_developer, row['client_username'], fee)

                    # automatically give this developer a rating of 1
                    df2 = pd.read_csv('database/Rating.csv')
                    df2.loc[len(df)] = pd.Series(data=[index, chosen_developer, row['client_username'], 1, 'System demand overdue.'],
                        index=['demand_id', 'recipient', 'rater', 'rating', 'message'])
                    df2.to_csv('database/Rating.csv')

        df.to_csv('database/Demand.csv', index=False)

class Bid:
    """
    Bid class. Has methods that inserts to Bid table.
    """
    def __init__(self, demand_id, developer_username, bid_amount):
        df = pd.read_csv('database/Bid.csv')
        now = datetime.datetime.now()
        format = '%m-%d-%Y %I:%M %p'
        date_bidded = now.strftime(format)
        bid_amount = round(bid_amount, 2)

        df.loc[len(df)] = pd.Series(data=[demand_id, developer_username, bid_amount, date_bidded],
            index=['demand_id', 'developer_username', 'bid_amount', 'date_bidded'])
        df.to_csv('database/Bid.csv', index=False)

        # send notification to client who made the demand stating that a bid was made
        demand_info = Demand.get_info(demand_id)
        client_username = demand_info['client_username']
        demand_title = demand_info['title']
        message = '{} made a bid of ${} on your {} demand'.format(developer_username, bid_amount, demand_title) 
        Notification(client_username, developer_username, message)

    @staticmethod
    def get_info(bid_id):
        """
        Returns a dictionary of information for the bid specified by the given index.
        Argument bid_id is the index of the row for the bid in the Bid table.
        """
        df = pd.read_csv('database/Bid.csv')
        bid = df.loc[int(bid_id)]

        # get time since bid was made
        now = datetime.datetime.now()
        bid_made = datetime.datetime.strptime(bid['date_bidded'], '%m-%d-%Y %I:%M %p')
        time_diff = now - bid_made

        if time_diff.days > 0:
            td = str(time_diff.days) + 'd'
        else:
            seconds = time_diff.seconds

            if seconds // 3600 > 0:
                td = str(seconds // 3600) + 'h'
            else:
                td = str(seconds // 60) + 'm'

        return {'demand_id': bid['demand_id'],
                'developer_username': bid['developer_username'],
                'bid_amount': format(bid['bid_amount'], '.2f'),
                'time_diff': td}

    @staticmethod
    def get_bids_for_demand(demand_id):
        """
        Returns a list of bid_ids or indexes where the bids are located in the Bid table.
        The list is sorted from lowest bid to highest bid.
        """
        df = pd.read_csv('database/Bid.csv')
        bids = df.loc[df['demand_id'] == int(demand_id)].sort_values(['bid_amount'], ascending=[True])

        return bids.index.tolist()

    @staticmethod
    def get_bids_by_username(username):
        """
        Returns bid index by username, ordered in latest to oldest.
        """
        df = pd.read_csv('database/Bid.csv')
        bids = df.loc[df.developer_username == username]
        bids_sorted = bids.sort_values(['date_bidded'], ascending=[False])

        return bids_sorted.index.tolist()

class BlacklistedUser:
    """
    BlacklistedUser class. Has methods that inserts to and reads from BlacklistedUser table.
    """
    def __init__(self, user_id):
        df = pd.read_csv('database/BlacklistedUser.csv')

        # get date for when the user can be taken off of blacklist
        # it is a year from the day when the user is put on the blacklist
        now = datetime.datetime.now()
        date = "{}-{}-{}".format(now.year + 1, now.month, now.day)

        df.loc[len(df)] = pd.Series(data=[user_id, date],
            index=['user_id', 'blacklisted_until'])
        df.to_csv('database/BlacklistedUser.csv', index=False)

    @staticmethod
    def is_blacklisted(username):
        """
        Checks if a user is on the blacklist.
        """
        df = pd.read_csv('database/BlacklistedUser.csv')
        return len(df.loc[df['user_id'] == username]) > 0

    @staticmethod
    def get_info(username):
        """
        Returns a dictionary of information for the given developer.
        """
        df = pd.read_csv('database/BlacklistedUser.csv')
        blacklisteduser = df.loc[df.user_id == username]

        return {'username': username,
                'blacklisted_until': blacklisteduser['blacklisted_until'].item()}


class SuperUser:
    """
    SuperUser class.
    """
    def __init__(self, username, password, first_name, last_name):
        df = pd.read_csv('database/SuperUser.csv')

        hashed = hash_password(password)
        df.loc[len(df)] = pdf.Series(data=[username, hashed],
            index=['username', 'password'])

    @staticmethod
    def get_superuser_info(username):
        """
        Returns a dictionary of the superuser's information.
        """
        df = pd.read_csv('database/SuperUser.csv')
        user = df.loc[df['username'] == username]

        if not user.empty:
            return {'id': user['id'],
                    'username': username,
                    'first_name': user['first_name'].item(),
                    'last_name': user['last_name'].item(),
                    'email': user['email'].item()}
    
    @staticmethod
    def check_password(username, password):
        """
        Checks if the password of a user_id match. 
        Returns true if password given matches the password for user_id 
        given and false if the password does not match.
        """
        df = pd.read_csv('database/SuperUser.csv')
        user = df.loc[df['username'] == username]
        if not user.empty:
            pwhash = user['password'].item()
            return pwhash == hash_password(password) 


class Notification:
    """
    Notifications that show up on dashboard.
    """
    def __init__(self,recipient,sender,message):
        df = pd.read_csv('database/Notification.csv')

        now = datetime.datetime.now()
        format = '%m-%d-%Y %I:%M %p'
        date_sent = now.strftime(format)
        
        df.loc[len(df)] = pd.Series(data=[len(df), recipient, sender, date_sent, message, False],
            index=['message_id','recipient', 'sender','date_sent', 'message', 'read_status'])

        df.to_csv('database/Notification.csv', index=False)

    @staticmethod
    def get_number_of_unread(recipient):
        """
        Gets the number of unread messages the recipient username has.
        """
        df = pd.read_csv('database/Notification.csv')
        msgs = df.loc[(df['recipient'] == recipient) & (df.read_status == False)]

        return len(msgs)

    @staticmethod
    def get_notif_to_recipient(recipient, number):
        """
        Get messages to a certain recipient. The amount that is returned is number.
        The most recent notifications are returned.
        """
        df = pd.read_csv('database/Notification.csv')
        msgs = df.loc[df['recipient'] == recipient]
        msgs_sorted = msgs.sort_values(by="message_id", ascending=False) # latest notif first

        notifs = []
        for index, row in msgs_sorted.iterrows():
            if len(notifs) == number :
                break
            temp = { 'sender': row['sender'],
                    'message': row['message'],
                    'date_sent': row['date_sent'],
                    'read_status': row['read_status']}
            notifs.append(temp)
        return notifs

    @staticmethod
    def get_all_notif_to_recipient(recipient):
        """
        Get all notifications to a user
        """
        df = pd.read_csv('database/Notification.csv')
        msgs = df.loc[df['recipient'] == recipient]
        msgs_sorted = msgs.sort_values(by="message_id", ascending=False) # latest notif first

        df.loc[df['recipient'] == recipient, ['read_status']] = True
        df.to_csv('database/Notification.csv', index=False)

        notifs = []
        for index, row in msgs_sorted.iterrows():
            temp = {'sender': row['sender'],
                    'message': row['message'],
                    'date_sent': row['date_sent'],
                    'read_status': row['read_status']}
            notifs.append(temp)
        return notifs

class SystemWarning:
    """
    A warning that is issued to a user

    The status of a warning may be:
        active
        protested
        inactive
    """
    def __init__(self,recipient,status):
        df = pd.read_csv('database/Warning.csv')
        # Create a new row in table for warning
        df.loc[len(df)] = pd.Series(data=[len(df), recipient, status],
            index=['warning_id','warned_user','status'])
        df.to_csv('database/Warning.csv', index=False)

    @staticmethod
    def protest_warning(warning_id,reason):
        """
        Allow user to protest a warning
        """
        df = pd.read_csv('database/Warning.csv')
        # Set warning back to active and give reason
        df.loc[df.warning_id == warning_id, 'status'] = 'pending'
        df.loc[df.warning_id == warning_id, 'reason'] = reason

        df.to_csv('database/Warning.csv', index=False)

    @staticmethod
    def remove_warning(warning_id):
        """
        Remove warning that user has protested
        """
        df = pd.read_csv('database/Warning.csv')
        # Set warning back to active and give reason
        df.loc[df.warning_id == warning_id, 'status'] = 'inactive'
        df.to_csv('database/Warning.csv', index=False)

    @staticmethod
    def keep_warning(warning_id):
        """
        Keep the warning that user has protested and provide reason for doing so
        """
        df = pd.read_csv('database/Warning.csv')
        # Set warning back to active and give reason
        df.loc[df.warning_id == warning_id, 'status'] = 'active_and_denied'
        df.to_csv('database/Warning.csv', index=False)

    @staticmethod
    def get_warned_user(warning_id):
        """
        Get the recipient of a particular warning's username
        """
        df = pd.read_csv('database/Warning.csv')
        if len(df.loc[df.warning_id == warning_id]) > 0:
            df = pd.read_csv('database/Warning.csv')
            return df.loc[df.warning_id == warning_id, 'warned_user'][warning_id]

    @staticmethod
    def get_warning_status(warning_id):
        """
        Get the recipient of a particular warning's username
        """
        df = pd.read_csv('database/Warning.csv')
        if len(df.loc[df.warning_id == warning_id]) > 0:
            df = pd.read_csv('database/Warning.csv')
            return df.loc[df.warning_id == warning_id, 'status'][warning_id]

    @staticmethod
    def get_warning_info(warning_id):
        """
        Returns a dictionary of the warning's information.
        """
        df = pd.read_csv('database/Warning.csv')
        warning = df.loc[df['warning_id'] == warning_id]

        if not warning.empty:
            return {'warning_id': warning['warning_id'].item(),
                    'warned_user': warning['warned_user'].item(),
                    'status': warning['status'].item(),
                    'reason': warning['reason'].item()}

    @staticmethod
    def get_protests():
        """
        Gets all pending protest requests.
        """
        df = pd.read_csv('database/Warning.csv')
        get_protests = df.loc[df['status'] == 'pending']
        protests = get_protests.T.to_dict().values()
        return protests

    @staticmethod
    def get_user_warnings(username):
        """
        Gets a dictionary of all the warnings given to [username]
        """
        df = pd.read_csv('database/Warning.csv')
        get_warnings = df.loc[df['warned_user'] == username]
        warnings = get_warnings.T.to_dict().values()
        return warnings

    @staticmethod
    def should_be_blacklisted(username):
        """
        Returns whether [username] should be blacklisted (if they have more than 2 active warnings)
        """
        df = pd.read_csv('database/Warning.csv')
        get_warnings = df.loc[df['warned_user'] == username]
        warnings = get_warnings.T.to_dict().values()
        num_of_warnings = 0
        for warning in warnings:
            if warning['status'] == 'active' or warning['status'] == 'active_and_denied':
                num_of_warnings+=1
            if num_of_warnings >=2:
                return True
        return False 

class Transaction:
    """
    Transactions between users (sender and recipient).
    """
    def __init__(self, recipient, sender, amount, message=None):
        df = pd.read_csv('database/Transaction.csv')
        df.loc[len(df)] = pd.Series(data=[len(df), recipient, sender, amount, 'pending', message],
            index=['transaction_id', 'recipient','sender','amount','status', 'optional_message'])
        df.to_csv('database/Transaction.csv', index=False)

    @staticmethod
    def get_transaction_info(transaction_id):
        """
        Returns a dictionary of the transaction's information.
        """
        df = pd.read_csv('database/Transaction.csv')
        transaction = df.loc[df['transaction_id'] == int(transaction_id)]

        if not transaction.empty:
            return {'transaction_id': transaction['transaction_id'].item(),
                    'recipient': transaction['recipient'].item(),
                    'sender': transaction['sender'].item(),
                    'amount': transaction['amount'].item(),
                    'optional_message': transaction['optional_message'].item()}

    @staticmethod
    def approve_transaction(transaction_id):
        """
        Approves a transaction
        """
        df = pd.read_csv('database/Transaction.csv')
        transaction = df.loc[df['transaction_id'] == transaction_id]
        df.loc[df.transaction_id == transaction_id, 'status'] = 'approved'
        df.to_csv('database/Transaction.csv', index=False)

    @staticmethod
    def deny_transaction(transaction_id):
        """
        Denies a transaction
        """
        df = pd.read_csv('database/Transaction.csv')
        transaction = df.loc[df['transaction_id'] == transaction_id]
        df.loc[df.transaction_id == transaction_id, 'status'] = 'denied'
        df.to_csv('database/Transaction.csv', index=False)
        # Issues a warning to the sender
        sender = transaction['sender'].item()
        SystemWarning(sender,'active')

    @staticmethod
    def get_pending_transactions():
        """
        Gets all pending transactions that are waiting on approval from the superuser.
        """
        df = pd.read_csv('database/Transaction.csv')
        get_pending_transactions = df.loc[df['status'] == 'pending']
        pending_transactions = get_pending_transactions.T.to_dict().values()
        return pending_transactions

    @staticmethod
    def get_transactions_by_recipient(username):
        """
        Get all transactions where username is recipient.
        """
        df = pd.read_csv("database/Transaction.csv")
        transactions = df.loc[(df.recipient == username)]
        dict_transactions = transactions.T.to_dict().values()

        print(dict_transactions)

        return dict_transactions

    @staticmethod
    def get_transactions_by_sender(username):
        """
        Get all transactions where username is sender.
        """
        df = pd.read_csv("database/Transaction.csv")
        transactions = df.loc[(df.sender == username)]
        dict_transactions = transactions.T.to_dict().values()

        print(dict_transactions)

        return dict_transactions

class Rating:
    """
    Ratings between developers and clients.
    """
    def __init__(self, demand_id, recipient, rater, rating, message=None):
        df = pd.read_csv('database/Rating.csv')
        df.loc[len(df)] = pd.Series(data=[demand_id, recipient, rater, rating, message],
            index=['demand_id', 'recipient', 'rater', 'rating', 'message'])
        df.to_csv('database/Rating.csv', index=False)

    @staticmethod
    def get_avg_rating(username):
        """
        Gets the average rating of [username]
        """
        df = pd.read_csv('database/Rating.csv')
        ratings = df.loc[df.recipient == username]
        average = ratings["rating"].mean()

        return average

    @staticmethod
    def get_ratings_by_demand_id(demand_id):
        """
        Returns dataframe of ratings corresponding to a demand_id.
        """
        df = pd.read_csv('database/Rating.csv')
        ratings = df.loc[df.demand_id == demand_id]

        return ratings

    @staticmethod
    def check_if_valid_rating_form(demand_id, recipient, rater):
        """
        Checks if the URL for a rating is legitimate.
        """
        demand = Demand.get_info(demand_id)
        if (demand['client_username'] == recipient and demand['chosen_developer_username'] == rater) or (demand['client_username'] == rater and demand['chosen_developer_username'] == recipient):
        # exists a demand where recipient/rater is a dev/client
            if demand['is_completed']:
            # if the demand has finished and can have ratings
                ratings = Rating.get_ratings_by_demand_id(demand_id)
                if len(ratings.loc[ratings.recipient == recipient]) == 0:
                    # there has not yet been a rating for this recipient
                    return True
        return False

class DeleteRequest:
    """
    Delete requests created by users
    """
    def __init__(self, username):
        df = pd.read_csv('database/DeleteRequest.csv')
        df.loc[len(df)] = pd.Series(data=[len(df), username, 'pending'],
            index=['delete_request_id', 'username', 'status'])

    @staticmethod
    def get_delete_request_status(delete_request_id):
        """
        Gets the status of the delete request with the id of [delete_request_id]
        """
        df = pd.read_csv('database/DeleteRequest.csv')
        status = df.loc[df.delete_request_id == delete_request_id, 'status'] 
        return status

    @staticmethod
    def set_delete_request_status(delete_request_id, status):
        """
        Sets the status of the delete request with the id of [delete_request_id] to [status]
        """
        df = pd.read_csv('database/DeleteRequest.csv')
        df.loc[df.delete_request_id == delete_request_id, 'status'] = status
        df.to_csv('database/DeleteRequest.csv', index=False)

    @staticmethod
    def is_account_deleted(username):
        """
        Checks if [username]'s account is deleted
        """
        df = pd.read_csv('database/DeleteRequest.csv')
        # Check if user has requested a deletion.
        df = df.loc[df.username == username]
        # If they have, check if that request has been approved
        if len(df) > 0:
            df = df.loc[df.status == 'approved']
            if len(df) > 0:
                return True
        return False

    @staticmethod
    def get_pending_delete_requests():
        """
        Gets a dictionary of all pending delete requests that are waiting on approval from the superuser.
        """
        df = pd.read_csv('database/DeleteRequest.csv')
        pending_delete_requests = df.loc[df['status']=='pending'].T.to_dict().values()
        return pending_delete_requests

        df = pd.read_csv('database/Warning.csv')
        get_warnings = df.loc[df['warned_user'] == username]
        warnings = get_warnings.T.to_dict().values()
        return warnings

    @staticmethod
    def get_delete_request_info(delete_request_id):
        """
        Returns a dictionary of the delete request's information.
        """
        df = pd.read_csv('database/DeleteRequest.csv')
        delete_request = df.loc[df.delete_request_id == delete_request_id]

        if not delete_request.empty:
            return {'delete_request_id': delete_request_id,
                    'username': delete_request['username'].item(),
                    'status': delete_request['status'].item()}

    @staticmethod
    def approve_delete_request(delete_request_id):
        """
        Deletes the account of the user that requested their account to be deleted and changes the status
        of the delete request.
        """
        info = DeleteRequest.get_delete_request_info(delete_request_id)
        print(info['username'])
        User.delete_user(info['username'])
        DeleteRequest.set_delete_request_status(delete_request_id,'approved')


    @staticmethod
    def deny_delete_request(delete_request_id):
        DeleteRequest.set_delete_request_status(delete_request_id,'denied')


# run these checks here (not as good as real triggers, but good enough)
Demand.check_approaching_bidding_deadlines()
Demand.check_approaching_submission_deadlines()
Demand.check_expired_demands()
Demand.check_overdue_demands()

#-------------------------------------------------------------------------------#
#
#                         --- p y C o l d S t r e a m ---
#
#-------------------------------------------------------------------------------#

import logging
from .rest_api import ColdStreamRestClient, ColdStreamDataObject

log = logging.getLogger(__name__)

                 #-----------------------------------------------#
                 #                    UserManager
                 #-----------------------------------------------#

## Main case data class
class UserManager(ColdStreamRestClient):

                 #------------------- Attributes ----------------#

    ## @start_attributes

    ## Get the current user
    @property
    def current_user(self):
        return self.__cuser

    ## @end_attributes

                 #------------------- Constructor ---------------#

    ## Constructor
    #
    # @param token (str): the api token
    def __init__(self, token):
        super().__init__(token=token)

        self.__cuser = User(self.token, self.request_get(self.URL["identity"] + "/users/me"))

                 #-------------------- Selector -----------------#

                 #--------------------- Methods -----------------#

    ## Retrieves the user the given user ID
    #
    # @param user_ID (int): user ID
    def get_user(self, user_ID):
        url = self.URL["identity"] + "/users/" + str(user_ID)
        return User(self.token, self.request_get(url))

    ## Retrieves the user list for a specific organization
    #
    # @param organization_ID (int): the organization ID
    #
    # @return (list of User)
    def get_organization_users(self, organization_ID):
        url = self.URL["identity"] + "/organizations/" + str(organization_ID) + "/members"
        data = self.request_get(url)
        return [User(self.token, d) for d in data["items"]]

    ## Retrieves the user list for a specific project
    #
    # @param project_ID (int): the project Id
    #
    # @return (list of User)
    def get_project_users(self, project_ID):
        url = self.URL["identity"] + "/projects/" + str(project_ID)
        data = self.request_get(url)
        return [User(self.token, d) for d in data["items"]]

#-------------------------------------------------------------------------------#

                 #-----------------------------------------------#
                 #                    User
                 #-----------------------------------------------#

## Manage the user data
class User(ColdStreamDataObject):


                 #------------------- Attributes ----------------#

    ## @start_attributes

    ## Return the current organization
    @property
    def organization(self):
        if self.__org_index >= 0:
            return self.__orgs[self.__org_index]

        return None

    ## Return the organizations the user is enrolled in
    @property
    def organizations(self):
        return self.__orgs

    ## @end_attributes

                 #------------------- Constructor ---------------#

    ## Constructor
    #
    # @param token (str): the api token
    # @param data (dict): user data
    def __init__(self, token, data):
        super().__init__(token, data, "users")
        self.__orgs = [Organization(self.token, d) for d in data.get("organizations", [])]
        
        # By default, always take the first organization
        self.__org_index = 0

                 #--------------------- Methods -----------------#

    ## Select the proper organization
    #
    # @param organization_ID (int): the organization ID
    def select_organization(self, organization_ID):
        for idx, org in enumerate(self.organizations):
            if org.ID == organization_ID:
                self.__org_index = idx
                break

    ## Update the user data
    #
    # @param first_name (str): the first name of the user
    # @param last_name (str): the second name of the user
    # @param phone (str): the phone number of the user
    def update(self, first_name, last_name, phone=None):
        payload = {"firstName" : first_name, "secondName" : last_name}
        if phone is not None:
            payload["phone"] = phone

        super().update(payload)

#-------------------------------------------------------------------------------#

                 #-----------------------------------------------#
                 #                    Organization
                 #-----------------------------------------------#

## Main case data class
class Organization(ColdStreamDataObject):

                 #------------------- Attributes ----------------#

    ## @start_attributes

    ## @end_attributes

                 #------------------- Constructor ---------------#

    ## Constructor
    #
    # @param token (str): the api token
    # @param data (dict): user data
    def __init__(self, token, data):
        super().__init__(token, data, "organizations")

                 #--------------------- Methods -----------------#

    ## Returns a history on the activities for a given organization
    #
    # @return (list of dict)
    def get_activity_log(self):
        url = self.instance_url + "/logs"
        return self.request_get(url)["items"]

    ## Return the submission queue of cases for the organization
    #
    # @return (list of dict)
    def get_queue_items(self):
        url = self.instance_url + "/queue/items"
        return self.request_get(url)["items"]

    ## Reorders the case submission queue.  An item can be moved to a different position or it
    # can be given a different priority
    #
    # Possible priority values are '0 = Low', '1 = Medium', '2 = High'
    #
    # @param moveable_item_ID (int): ID of the queue item
    # @param target_position (int): the new position of the queue item, defaults to None
    # @param target_priority (int): the new priority of the queue item, defaults to None
    def modify_queue_item(self, moveable_item_ID, target_position=None, target_priority=None):
        url = self.instance_url + "/queue/items"
        payload = {"moveableItemId" : moveable_item_ID}
        if target_position is not None:
            payload["targetPosition"] = target_position
        if target_priority is not None:
            payload["targetPriority"] = target_priority

        self.request_post(url, payload)

    ## Removes the given item from the case submission queue
    #
    # @param item_ID (int): ID of the queue item
    def remove_queue_item(self, item_ID):
        url = self.instance_url + "/queue/item/" + str(item_ID)
        self.request_del(url)

#-------------------------------------------------------------------------------#

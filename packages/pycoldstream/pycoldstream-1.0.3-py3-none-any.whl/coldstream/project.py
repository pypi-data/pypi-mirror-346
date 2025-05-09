#-------------------------------------------------------------------------------#
#
#                         --- p y C o l d S t r e a m ---
#
#-------------------------------------------------------------------------------#

import logging
from .rest_api import ColdStreamRestClient, ColdStreamDataObject
from .user import User
from .case import Case

log = logging.getLogger(__name__)

                 #-----------------------------------------------#
                 #                    ProjectManager
                 #-----------------------------------------------#

## Main case data class
class ProjectManager(ColdStreamRestClient):


                 #------------------- Attributes ----------------#


    ## @start_attributes

    ## @end_attributes

                 #------------------- Constructor ---------------#

    ## Constructor
    #
    # @param token (str): the api token
    # @param user (User): the current user
    def __init__(self, token, user):
        super().__init__(token=token)

        self.__user = user

                 #-------------------- Selector -----------------#

                 #--------------------- Methods -----------------#

    ## Get the projects for a given user within the active organization
    #
    # @param status (int): project status label, defaults to None
    def get_user_projects(self, status=None):
        organization_ID = self.__user.organization.ID
        url = self.URL["projects"] + "/organizations/" + str(organization_ID) + "/projects/all"

        if status is not None:
            url += f"?Status={status}"

        data = self.request_get(url)
        return [Project(self.token, d, self.__user) for d in data]

    ## Get the projects for a given organization
    #
    # @param organization_ID (int): ID of the organization
    # @param status (int): project status label, defaults to None
    def get_organization_projects(self, organization_ID, status=None):
        url = self.URL["projects"] + "/organizations/" + str(organization_ID) + "/projects"

        if status is not None:
            url += f"?Status={status}"

        data = self.request_get(url)
        return [Project(self.token, d, self.__user) for d in data]

    ## Get a specific project
    #
    # @param project_ID (int): id of the project to retrieve
    def get_project(self, project_ID):
        url = self.URL["projects"] + "/projects/" + str(project_ID)
        return Project(self.token, self.request_get(url), self.__user)

    ## Create a new project
    #
    # @param name (str): the project name
    # @param descr (str): the project description
    def create_project(self, name, descr):
        url = self.URL["projects"] + "/projects"
        payload = {"name" : name,
                   "description" : descr,
                   "organizationId" : self.__user.organization.ID}
        return Project(self.token, self.request_post(url, payload), self.__user)

#-------------------------------------------------------------------------------#

                 #-----------------------------------------------#
                 #                    Project
                 #-----------------------------------------------#

## Main Project class
class Project(ColdStreamDataObject):

                 #------------------- Attributes ----------------#

    ACCESS = {"viewer" : 0,
              "user" : 1,
              "owner" : 2}

    ## @start_attributes

    ## Return the project members
    #
    # @param (list of User)
    @property
    def members(self):
        return [User(self.token, d) for d in self.data["members"]]

    ## Return the project cases
    @property
    def cases(self):
        url = self.URL["cases"] + "/projects/" + str(self.ID) + "/cases"
        data = self.request_get(url)
        all_cases = [Case(self.token, d, self.__user) for d in data["items"]]
        return [c for c in all_cases if c.project_ID == self.ID]

    ## @end_attributes

                 #------------------- Constructor ---------------#

    ## Constructor
    #
    # @param token (str): the api token
    # @param data (dict): project data
    # @param user (User): the current user
    def __init__(self, token, data, user):
        super().__init__(token, data, "projects")
        self.__user = user

                 #--------------------- Methods -----------------#

    ## Update the project data
    #
    # @param name (str): the project name
    # @param descr (str): the project description
    def update(self, name, descr):
        super().update({"name" : name, "description" : descr})

    ## Open the project if it is closed
    def close(self):
        url = self.instance_url + "/status?isProjectClosed=true"
        self.request_patch(url)

    ## Re-open the project if it is closed
    def reopen(self):
        url = self.instance_url + "/status?isProjectClosed=false"
        self.request_patch(url)

    ## Add project member
    #
    # @param user (User): the user to be granted project access
    # @param access_level (str): the desired access level
    def add_member(self, user, access_level):
        url = self.instance_url + "/members"
        payload = {"accessLevel" : self.ACCESS[access_level],
                   "memberId" : user.ID}
        self.request_post(url, payload)

    ## Remove a project member
    #
    # @param user (User): the user to be removed from project access
    def delete_member(self, user):
        url = self.instance_url + "/members/" + str(user.ID)
        self.request_del(url)

    ## Retrieve a case from the project
    def get_case(self, case_ID):
        url = self.URL["cases"] + "/cases/" + str(case_ID)
        return Case(self.token, self.request_get(url), self.__user)

    ## Create a new project case
    #
    # @param case_type (int): case type
    # @param name (str): case name
    def create_case(self, case_type, name):
        url = self.URL["cases"] + "/cases"
        payload = {"type" : case_type,
                   "name" : name,
                   "projectId" : self.ID}
        return Case(self.token, self.request_post(url, payload), self.__user)

#-------------------------------------------------------------------------------#

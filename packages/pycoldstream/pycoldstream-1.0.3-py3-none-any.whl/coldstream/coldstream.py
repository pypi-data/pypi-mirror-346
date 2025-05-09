#-------------------------------------------------------------------------------#
#
#                         --- p y C o l d S t r e a m ---
#
#-------------------------------------------------------------------------------#

import logging
from .rest_api import ColdStreamRestClient, set_hosting
from .user import UserManager
from .project import ProjectManager
from .library import LibraryManager

log = logging.getLogger(__name__)

                 #-----------------------------------------------#
                 #                    ColdstreamSession
                 #-----------------------------------------------#

## Main case data class
class ColdstreamSession:


                 #------------------- Attributes ----------------#


    ## @start_attributes

    ## Return the project manager
    @property
    def projects(self):
        return self.__projects

    ## Return the user manager
    @property
    def users(self):
        return self.__users

    ## Return the library manager
    @property
    def library(self):
        return self.__library

    ## @end_attributes

                 #------------------- Constructor ---------------#

    ## Constructor
    #
    # @param client (ColdStreamRestClient): the session rest client
    def __init__(self, client):
        self.__client = client

        self.__users = UserManager(self.__client.token)
        self.__projects = ProjectManager(self.__client.token,
                                         self.__users.current_user)
        self.__library = LibraryManager(self.__client.token,
                                        self.__users.current_user)

                 #-------------------- Selector -----------------#

    ## Create a coldstream session
    #
    # @param host (str): the hosting location
    # @param user (str): user name
    # @param password (str): the password
    @classmethod
    def create_from_login(cls, user, password, host):
        set_hosting(host)
        connection = ColdStreamRestClient(user=user, password=password)
        return cls(connection)

                 #--------------------- Methods -----------------#

#-------------------------------------------------------------------------------#

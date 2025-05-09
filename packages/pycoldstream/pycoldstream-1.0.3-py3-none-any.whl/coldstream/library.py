#-------------------------------------------------------------------------------#
#
#                         --- p y C o l d S t r e a m ---
#
#-------------------------------------------------------------------------------#

import logging
from .rest_api import ColdStreamRestClient, ColdStreamDataObject

log = logging.getLogger(__name__)

                 #-----------------------------------------------#
                 #                    LibraryManager
                 #-----------------------------------------------#

## Main case data class
class LibraryManager(ColdStreamRestClient):

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

    ## Retrieves the library item the given the library item ID
    #
    # @param library_item_ID (int): the library item ID
    #
    # @return (LibraryItem)
    def get_item(self, library_item_ID):
        organization_ID = self.__user.organization.ID

        url = self.URL["cases"] + "/organizations/" + str(organization_ID) + "/library-items/" + str(library_item_ID)
        return LibraryItem(self.token, self.request_get(url), organization_ID)

    ## Retrieves the library items of a given type
    #
    # @param item_type (int): library item type
    # @param name (str): optional name filter, defaults to None
    #
    # @return (list of LibraryItem)
    def get_items_by_type(self, item_type, name=None):
        organization_ID = self.__user.organization.ID

        url = self.URL["cases"] + "/organizations/" + str(organization_ID) + "/library-items?Type=" + str(item_type)

        if name is not None:
            url += "&Name=" + name

        library_data = self.request_get(url)
        return [LibraryItem(self.token, data_i, organization_ID) for data_i in library_data["items"]]

    ## Create a new library item
    #
    # @param name (str): name of the item
    # @param item_type (int): library item type
    # @param properties (dict): the library item properties
    # @param description (str): optional description, defaults to None
    def create_item(self, name, item_type, properties, description=None):
        organization_ID = self.__user.organization.ID

        url = self.URL["cases"] + "/organizations/" + str(organization_ID) + "/library-items"
        payload = {"name": name,
                   "type" : item_type,
                   "properties" : properties}
        if description is not None:
            payload["description"] = description

        return LibraryItem(self.token, self.request_put(url, payload), organization_ID)

#-------------------------------------------------------------------------------#
                 #-----------------------------------------------#
                 #                    LibraryItem
                 #-----------------------------------------------#

## Manage the library item
class LibraryItem(ColdStreamDataObject):


                 #------------------- Attributes ----------------#

    TYPES = {"0" : "solid",
             "1" : "fluid",
             "2" : "fan",
             "3" : "pump",
             "4" : "thermal interface",
             "5" : "3D printing",
             "6" : "die casting",
             "7" : "sheet metal",
             "8" : "cnc milling",
             "9" : "electric wire"}

    ## @start_attributes

    ## Return the instance url
    @property
    def instance_url(self):
        return self.URL["cases"] + f"/organizations/{self.__organization_ID}/library-items/{self.ID}"

    ## @end_attributes

                 #------------------- Constructor ---------------#

    ## Constructor
    #
    # @param token (str): the api token
    # @param data (dict): user data
    # @param organization_ID (int): the organization ID
    def __init__(self, token, data, organization_ID):
        super().__init__(token, data, "cases")

        self.__organization_ID = organization_ID
        
                 #--------------------- Methods -----------------#

    ## Update the library item with the given info
    #
    # @param name (str): the item name
    # @param properties (dict): the item properties
    # @param description (str): optional description, defaults to None
    def update(self, name, properties, description=None):
        payload = {"name" : name,
                   "properties" : properties}

        if description is not None:
            payload["description"] = description

        super().update(payload)

    ## Returns the activity history for the requested library item
    #
    # @return (list of dict)
    def get_history(self):
        url = self.instance_url + "/logs"
        return self.request_get(url)["items"]

#-------------------------------------------------------------------------------#

#-------------------------------------------------------------------------------#
#
#                         --- C O L D S T R E A M api ---
#
#-------------------------------------------------------------------------------#

import os
import json
import logging
from .rest_api import ColdStreamDataObject, ApiError

log = logging.getLogger(__name__)

                 #-----------------------------------------------#
                 #                    Case
                 #-----------------------------------------------#

## Manage the user data
class Case(ColdStreamDataObject):


                 #------------------- Attributes ----------------#

    CASE_TYPES = {"Custom design" : 0,
                  "Simulation" : 1,
                  "Standard design" : 2}

    CASE_STATUSES = {"Created" : 0,
                     "Running" : 1,
                     "Finished" : 2,
                     "Stalled" : 3,
                     "Queued" : 4}

    ## @start_attributes

    ## Return the case type
    @property
    def case_type(self):
        return self.data["type"]

    ## Return the case status
    @property
    def case_status(self):
        return self.data["status"]

    ## Return the project ID
    @property
    def project_ID(self):
        return self.data["projectId"]

    ## Get the case setup
    #
    # @return (dict)
    @property
    def setup(self):
        url = self.URL["cases"] + "/cases/setup/" + str(self.ID)
        return self.request_get(url)

    ## Validates the given case to determine if the case is ready for submission or not
    #
    # @return (dict)
    @property
    def ready_to_submit(self):
        url = self.URL["cases"] + "/cases/validate"
        payload = {"caseId": self.ID}

        try:
            validation = self.request_post(url, payload)
            return validation["status"] == 1
        except:
            return False

	## Return the regions
    #
    # @return (list of Region)
    @property
    def regions(self):
        return [Region(self.token, region_data, self.ID) for region_data in self.setup["regions"]]

    ## Return the interfaces
    #
    # @return (list of Interface)
    @property
    def interfaces(self):
        return [Interface(self.token, region_data) for region_data in self.setup["interfaces"]]

    ## @end_attributes

                 #------------------- Constructor ---------------#

    ## Constructor
    #
    # @param token (str): the api token
    # @param data (dict): region data
    # @param user (User): the current user
    def __init__(self, token, data, user):
        super().__init__(token, data, "cases")

        self.__user = user

                 #--------------------- Methods -----------------#

    ## Create a new region with the given info
    #
    # Returns a json object with meta data for the created region
    #
    # @param name (str): name of the region
    # 
    # @return (Region)
    def create_region(self, name):
        url = self.URL["cases"] + "/regions"
        payload = {"name" : name, "caseId": self.ID}
        return Region(self.token, self.request_post(url, payload), self.ID)

    ## Retrieves the region for the given region ID
    #
    # @param region_ID (int): the region ID
	#
	# @return (Region)
    def get_region(self, region_ID):
        url = self.URL["cases"] + "/regions/" + str(region_ID)
        return Region(self.token, self.request_get(url), self.ID)

    ## Create a new target
    #
    # @param component_ID (int): id of the component for which you want to create a target
    def create_target(self, component_ID):
        url = self.URL["targets"] + "/targets"
        payload = {"caseId" : self.ID, "caseComponentId" : component_ID}

        t = Target(self.token, self.request_post(url, payload))
        return t

    ## Retrieves the target for the given target ID
    #
    # @param target_ID (int): the target Id
    #
    # @return (Target)
    def get_target(self, target_ID):
        url = self.URL["targets"] + "/targets/" + str(target_ID)
        return Target(self.token, self.request_get(url))

    ## Create a new interface between two regions
    #
    # @param region1_ID (int): ID of the first region
    # @param region2_ID (int): ID of the second region
    #
    # @return (Interface)
    def create_interface(self, region1_ID, region2_ID):
        url = self.URL["cases"] + "/interfaces"
        payload = {"caseId" : self.ID,
                   "firstRegionId" : region1_ID,
                   "secondRegionId" : region2_ID}
        return Interface(self.token, self.request_post(url, payload))

    ## Retrieves the interfaces for the given interface ID
    #
    # @param interface_ID (int): the interface ID
    #
    # @return (Interface)
    def get_interface(self, interface_ID):
        url = self.URL["cases"] + "/interfaces/" + str(interface_ID)
        return Interface(self.token, self.request_get(url))

    ## Retrieves the case validation results
    #
    # @return (dict)
    def get_validation_result(self):
        if not self.ready_to_submit:
            return None

        url = self.instance_url + "/validation/result"
        return CaseValidationResult(self.request_get(url))

    ## Submit the case for estimation
    def estimate(self):
        url = self.instance_url + "/estimation"
        self.request_post(url)

    ## Submit the case
    #
    # Resolution level: possible values are: '0 = conceptual' -- '1 = detailed' -- '2 = draft'
    # Processing method: possible values are '0 = correlation' -- '1 = cfd' -- '2 = cfd reinforced'
    # Priority level: possible values are: '0 = low' -- '1 = medium' -- '2 = high'
    #
    # @param resolution (int): resolution level
    # @param credits (int): the amount of credits you want to use
    # @param processing_method (int): proecessing method, defaults to None
    # @param priority_level (int): the priority level, defaults to None
    def submit_case(self, resolution, credits, processing_method=None, priority_level=None):
        if not self.ready_to_submit:
            log.warning("Not ready to submit!")
            return

        if not resolution in [0, 1, 2]:
            raise ApiError("incorrect input 'resolution'")
        if not processing_method in [None, 0, 1, 2]:
            raise ApiError("incorrect input 'processing_method'")
        if not priority_level in [None, 0, 1, 2]:
            raise ApiError("incorrect input 'priority_level'")

        url = self.URL["cases"] + "/cases/submit"
        payload = {"resolution" : resolution,
                   "caseId" : self.ID,
                   "credits" : credits}
        if processing_method is not None:
            payload["processingMethod"] = processing_method
        if priority_level is not None:
            payload["priorityLevel"] = priority_level

        self.request_post(url, payload)

    ## Retrieves the case results for the given case
    #
    # @param iteration (int): optional parameter to select a certain iteration of the case
    def get_results(self, iteration=None):
        url = self.URL["cases"] + "/cases/result/" + str(self.ID)

        if iteration is not None and self.case_type != 1:
            url += "?iteration=" + str(iteration)

        return CaseResults(self.request_get(url))

    ## Retrieves the case results summary for the given case
    #
    # @param iteration (int): optional parameter to select a certain iteration of the case
    def get_results_summary(self, iteration=None):
        url = self.URL["cases"] + "/cases/summary/" + str(self.ID)

        if iteration is not None and self.case_type != 1:
            url += "?iteration=" + str(iteration)

        return CaseResults(self.request_get(url))

    ## Retrieves the case estimation results for a given case. If no results are available yet, then this method returns None
    #
    # @param iteration (int): optional parameter to select a certain iteration of the case
    def get_estimation_results(self, iteration=None):
        if self.case_status != 2:
            return None

        url = self.instance_url + "/estimation/result"

        if iteration is not None and self.case_type != 1:
            url += "?iteration=" + str(iteration)

        return CaseResults(self.request_get(url))

    ## Retrieves the case results evolution graph for a given case
    def get_results_evolution_graph(self):
        url = self.instance_url + "/results/evolution-graph"

        return CaseResults(self.request_get(url))

    ## Return the case history
    #
    # @return (list of dict)
    def get_history(self):
        organization_ID = self.__user.organization.ID
        url = self.URL["cases"] + "/organizations/" + str(organization_ID) + "/cases/" + str(self.ID) + "/logs"

        return self.request_get(url)["items"]

    ## Get the case notes
    #
    # @return (list of dict)
    def get_notes(self):
        url = self.instance_url + "/notes"
        return self.request_get(url)

    ## Post a new case note
    #
    # Valid note types are 'Information', 'Warning' and 'Error'
    #
    # @param note_type (str): message time
    # @param message (str): the message body
    def post_note(self, note_type, message):
        url = self.instance_url + "/notes"
        payload = {"type": note_type,
                   "message": message}
        self.request_post(url, payload)

    ## Upload the component geometry file
    #
    # @param filepath: path to the file
    def upload_geometry_file(self, filepath):
        url_data = self.get_signed_url(filepath, self.ID, self.ID)
        self.upload_file(filepath, url_data.get("preSignedUrl"))

        url = self.URL["cases"] + "/jobs/initialize"
        payload = {"caseId": self.ID,
                   "fileId": url_data.get("id"),
                   "fileURL": url_data.get("fileUrl")}
        self.request_post(url, payload)

    ## Retrieves a download link for the given file.
    #
    # @param file_ID (int, optional): id of the file you want a download link for, None by default
    # @param key (str, optional): name of the file you want a download link for, None by default
    def get_file_download_link(self, file_ID=None, key=None):
        if file_ID is None and key is None:
            raise ApiError("file_ID and key cannot be simultaneously None")

        url = self.URL["fileserver"] + "/cases/" + str(self.ID) + "/files/"

        if file_ID is not None:
            url += str(file_ID)
        if key is not None:
            url += key

        return self.request_get(url)

    ## Returns a list of links for setup files
    #
    ## @return (list of dict)
    def get_setup_file_links(self):
        url = self.URL["fileserver"] + "/cases/" + str(self.ID) + "/files"
        return self.request_get(url)

    ## Duplicate the case
    #
    ## @param name (str): the new case name
    ## @return (Case)
    def duplicate_case(self, name):
        url = self.URL["cases"] + "/cases/duplicate"

        payload = {"caseId": self.ID,
                   "caseName": name,
                   "linkCopy": True,
                   "ImproveDesignIteration": 0}
        return Case(self.token, self.request_post(url, payload), self.__user)

    ## Move the case to another project
    #
    ## @param project_ID (int): the ID of the project you want to move the case to
    ## @return (Case)
    def move_case(self, project_ID):
        url = self.URL["cases"] + "/cases/move"
        payload = {"caseId": self.ID,
                   "projectId": project_ID}
        return Case(self.token, self.request_post(url, payload), self.__user)


#-------------------------------------------------------------------------------#

                 #-----------------------------------------------#
                 #                    Region
                 #-----------------------------------------------#

## Manage the user data
class Region(ColdStreamDataObject):

                 #------------------- Attributes ----------------#

    ## @start_attributes

    ## Return the region boundaries
    #
    # @return (list of Boundary)
    @property
    def boundaries(self):
        return [Boundary(self.token, b_data, self.__case_ID) for b_data in self.data["boundaries"]]

    ## Return the subregions
    #
    # @return (list of Subregoin)
    @property
    def subregions(self):
        return [SubRegion(self.token, s_data, self.__case_ID) for s_data in self.data["subregions"]]

    ## @end_attributes

                 #------------------- Constructor ---------------#
    ## Constructor
    #
    # @param token (str): the api token
    # @param data (dict): region data
    # @param case_ID (int): the case ID
    def __init__(self, token, data, case_ID):
        super().__init__(token, data, "regions")
        self.__case_ID = case_ID

                 #--------------------- Methods -----------------#

    ## Update the region with the given info
    #
    # @param name (str): the (new) region name you want to assign to the region
    # @param region_type (str): the region type you want the region to be, this can be 'solid' or 'fluid'
    # @param data (dict, optional): all data concerning the region
    #
    # @return (dict)
    def update(self, name, region_type, data=None):
        details = self.data
        super().update({"name": name,
                        "RegionType": region_type,
                        "data": json.dumps(data) if data is not None else "{}"
                        })
        self.data.clear()
        self.data.update(details)
        self.data.update({"name": name})


    ## Create a new subregion for the given region
    #
    # Returns a json object with meta data for the created subregion
    #
    # @param name (str): name of the subregion
    #
    # @return (Subregion)
    def create_subregion(self, name):
        url = self.URL["cases"] + "/subregions"

        payload = {"name" : name,
                   "regionId" : self.ID,
                   "caseId": self.__case_ID}
        return SubRegion(self.token, self.request_post(url, payload), self.__case_ID)

    ## Retrieves the subregion for the given subregion ID
    #
    # @param region_ID (int): the subregion ID
    def get_subregion(self, subregion_ID):
        url = self.URL["cases"] + "/subregions/" + str(subregion_ID)
        return SubRegion(self.token, self.request_get(url), self.__case_ID)

    ## Create a new boundary for the given region
    #
    # Returns a json object with meta data for the created boundary
    #
    # @param name (str): name of the boundary
    #
    # @return (dict)
    def create_boundary(self, name):
        url = self.URL["cases"] + "/boundaries"
        payload = {"name" : name,
                   "regionId" : self.ID,
                   "caseId": self.__case_ID}
        return Boundary(self.token, self.request_post(url, payload), self.__case_ID)

    ## Retrieves the boundary for the given boundary ID
    #
    # @param boundary_ID (int): the boundary ID
	#
	# @return (Boundary)
    def get_boundary(self, boundary_ID):
        url = self.URL["cases"] + "/boundaries/" + str(boundary_ID)
        return Boundary(self.token, self.request_get(url), self.__case_ID)


    ## Upload the component geometry file
    #
    # @param filepath: path to the file
    def upload_geometry_file(self, filepath):
        url_data = self.get_signed_url(filepath, self.__case_ID, self.ID)
        self.upload_file(filepath, url_data.get("preSignedUrl"))

        if os.path.splitext(filepath)[1] != ".stl":
            self.create_visualization(self.__case_ID, url_data.get("id"), url_data.get("fileUrl"))

#-------------------------------------------------------------------------------#

                 #-----------------------------------------------#
                 #                    Region
                 #-----------------------------------------------#

## Manage the SubRegion data
class SubRegion(ColdStreamDataObject):

                 #------------------- Attributes ----------------#

    ## @start_attributes

    ## @end_attributes

                 #------------------- Constructor ---------------#

    ## Constructor
    #
    # @param token (str): the api token
    # @param data (dict): case data
    # @param case_ID (int): the case ID
    def __init__(self, token, data, case_ID):
        super().__init__(token, data, "subregions")

        self.__case_ID = case_ID

                 #--------------------- Methods -----------------#

    ## Update the subregion with the given info
    #
    # @param name (str): the (new) subregion name you want to assign to the subregion
    # @param subregion_type (str): the subregion type, options are 'general' and 'design'
    # @param data (dict, optional): all data concerning the region
    #
    # @return (dict)
    def update(self, name, subregion_type, data=None):
        details = self.data
        super().update({"name" : name,
                        "subregionType" : subregion_type,
                        "data" : json.dumps(data) if data is not None else "{}"})
        self.data.clear()
        self.data.update(details)
        self.data.update({"name": name})

    ## Upload the component geometry file
    #
    # @param filepath: path to the file
    def upload_geometry_file(self, filepath):
        url_data = self.get_signed_url(filepath, self.__case_ID, self.ID)
        self.upload_file(filepath, url_data.get("preSignedUrl"))

        if os.path.splitext(filepath)[1] != ".stl":
            self.create_visualization(self.__case_ID, url_data.get("id"), url_data.get("fileUrl"))

#-------------------------------------------------------------------------------#

                 #-----------------------------------------------#
                 #                    Boundary
                 #-----------------------------------------------#

## Manage the Boundary data
class Boundary(ColdStreamDataObject):

                 #------------------- Attributes ----------------#

    ## @start_attributes

    ## @end_attributes

                 #------------------- Constructor ---------------#

    ## Constructor
    #
    # @param token (str): the api token
    # @param data (dict): case data
    # @param case_ID (int): the case ID
    def __init__(self, token, data, case_ID):
        super().__init__(token, data, "boundaries")

        self.__case_ID = case_ID

                 #--------------------- Methods -----------------#

    ## Update the boundary with the given info.
    #
    # @param name (str): the (new) boundary name you want to assign to the boundary
    # @param boundary_type (str): the boundary type, options are 'fixedTemperatureWall', 'heatedWall', ...
    # @param data (dict, optional): all data concerning the region
    def update(self, name, boundary_type, data=None):
        details = self.data
        super().update({"name" : name,
                        "boundaryType" : boundary_type,
                        "data" : json.dumps(data) if data is not None else "{}"})
        self.data.clear()
        self.data.update(details)
        self.data.update({"name": name})

    ## Upload the component geometry file
    #
    # @param filepath: path to the file
    def upload_geometry_file(self, filepath):
        url_data = self.get_signed_url(filepath, self.__case_ID, self.ID)
        self.upload_file(filepath, url_data.get("preSignedUrl"))

        if os.path.splitext(filepath)[1] != ".stl":
            self.create_visualization(self.__case_ID, url_data.get("id"), url_data.get("fileUrl"))

#-------------------------------------------------------------------------------#

                 #-----------------------------------------------#
                 #                    Interface
                 #-----------------------------------------------#

## Manage the user data
class Interface(ColdStreamDataObject):

                 #------------------- Attributes ----------------#

    ## @start_attributes

    ## @end_attributes

                 #------------------- Constructor ---------------#

    ## Constructor
    #
    # @param token (str): the api token
    # @param data (dict): case data
    def __init__(self, token, data):
        super().__init__(token, data, "interfaces")

                 #--------------------- Methods -----------------#

    ## Update the interface with the given information
    #
    # @param region1_ID (int): ID of the first region
    # @param region2_ID (int): ID of the second region
    # @param reset (bool): true if you want to reset the interface side's data
    # @param interface_type (str): type you want the updated interface to have
    # @param data (dict): interface data
    def update(self, region1_ID, region2_ID, reset, interface_type=None, data=None):
        interface_ID = self.ID
        payload = {"resetInterfaceSidesData": reset,
                   "firstRegionId": region1_ID,
                   "secondRegionId": region2_ID,
                   "data":json.dumps(data) if data is not None else "{}"}
        if interface_type is not None:
            payload["interfaceType"] = interface_type
        super().update(payload)
        interfaces = self.data.get("interfaces", [])
        for interface in interfaces:
            if interface["id"] == interface_ID:
                self.data.clear()
                self.data.update(interface)
                break

#-------------------------------------------------------------------------------#
                 #-----------------------------------------------#
                 #                    Target
                 #-----------------------------------------------#

## Manage the Target data
class Target(ColdStreamDataObject):

                 #------------------- Attributes ----------------#

    ## @start_attributes

    ## @end_attributes

                 #------------------- Constructor ---------------#

    ## Constructor
    #
    # @param token (str): the api token
    # @param data (dict): case data
    def __init__(self, token, data):
        super().__init__(token, data, "targets")


                 #--------------------- Methods -----------------#

    ## Update the target with the given info.
    #
    # @param target_type (str): the target type
    # @param data (dict, optional): all data concerning the target
    def update(self, target_type, data=None):
        details = self.data
        super().update({"targetType" : target_type,
                        "data" : json.dumps(data) if data is not None else '{}'})
        self.data = details



#-------------------------------------------------------------------------------#

                 #-----------------------------------------------#
                 #                    CaseResults
                 #-----------------------------------------------#

## Manage the case result data
class CaseResults:

                 #------------------- Attributes ----------------#

    ## @start_attributes

    ## Return the raw data
    #
    # @return (dict)
    @property
    def data(self):
        return self.__data

    ## @end_attributes

                 #------------------- Constructor ---------------#

    ## Constructor
    #
    # @param data (dict): case data
    def __init__(self, data):
        self.__data = data

                 #--------------------- Methods -----------------#

#-------------------------------------------------------------------------------#

                 #-----------------------------------------------#
                 #                    CaseValidationResult
                 #-----------------------------------------------#

## Manage the case validation result
class CaseValidationResult:

                 #------------------- Attributes ----------------#

    ## @start_attributes

    ## Return the raw data
    #
    # @return (dict)
    @property
    def data(self):
        return self.__data

    ## Return True if valid to submit
    @property
    def valid(self):
        return self.status == 1

    ## Return the validation status
    @property
    def status(self):
        return self.__data["status"]

    ## @end_attributes

                 #------------------- Constructor ---------------#

    ## Constructor
    #
    # @param data (dict): case data
    def __init__(self, data):
        self.__data = data

                 #--------------------- Methods -----------------#

    ## Print the validation messages
    def print_messages(self):
        for message in self.data.get("validationMessages", []):
            log.info(message["severity"])
            log.info(message["message"])
            log.info("")

#-------------------------------------------------------------------------------#

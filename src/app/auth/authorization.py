from fastapi import Request
import faster_than_requests as requests
from enum import Enum
import urllib


# defining resource type variants - these will be used for type checking throughout the entire authZ workflow
class ResourceType:
    def __init__(self, id):
        self.id = id
        
class Organization(ResourceType):
    pass

class Application(ResourceType):
    pass

class Service(ResourceType):
    pass


def get_resource_type(url):
    parsed_url = urllib.parse.urlparse(url)
    path = parsed_url.path
    resource_level = path.count("/") - 1
    resource_id = 121
    
    if resource_level == 1:
        Organization(resource_id)
    if resource_level == 2:
        Application(resource_id)
    if resource_level == 3:
        Service(resource_id)


def get_user_permissions_json():
    # todo: check cache before making api call
    requests_service_url = "https://0.0.0.0/8000/api/v1/permissions/<user_uuid>"
    response = requests.get(requests_service_url)
    return response.body


def extract_resource_permissions(user_permissions_json: json, resource: ResourceType):
    # case match against all resource type variants
    match resource:
        case Organization(resource):
            allowed_organizations = []
            for organization in user_permissions_json["organizations"]:
                allowed_organizations.append(organization.id)
                return allowed_organizations
            
        case Application(resource):
            allowed_applications = []
            for organization in user_permissions_json["organizations"]:
                for application in organization["applications"]:
                    allowed_applications.append(application.id)
                return allowed_applications
            
        case Service(resource):
            allowed_services = []
            for organization in user_permissions_json["organizations"]:
                for application in organization["applications"]:
                    for service in application["services"]:
                        allowed_services.append(service.id)
                return allowed_services
            
        case _:
            return False


def is_authorized(resource: ResourceType, allowed_resources: list) -> bool:
    if resource.id in allowed_resources:
        return True
    return False


def check_cache():
    # read_from_cache()
    # write_to_cache()
    pass

def read_from_cache():
    pass

def write_to_cache():
    pass
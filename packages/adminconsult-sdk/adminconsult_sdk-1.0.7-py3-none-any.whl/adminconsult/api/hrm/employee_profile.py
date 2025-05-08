from typing import Iterator
from adminconsult.api.clientcredentials import ClientCredentials
from adminconsult.api.entity import Entity
from adminconsult.api.entity_collection import EntityCollection

class EmployeeProfile(Entity):

    profile_id: int = None
    profile_name = None
    is_functional = None
    is_operational = None
    is_relational = None
    is_skill = None
    is_fixed = None
    is_public = None
            
    _property_mapping = dict({
        "profile_id": {
            "GET": "ProfileId",
            "POST": None,
            "PUT": None
        },
        "profile_name": {
            "GET": "ProfileName",
            "POST": None,
            "PUT": None
        },
        "is_functional": {
            "GET": "IsFunctional",
            "POST": None,
            "PUT": None
        },
        "is_operational": {
            "GET": "IsOperational",
            "POST": None,
            "PUT": None
        },
        "is_relational": {
            "GET": "IsRelational",
            "POST": None,
            "PUT": None
        },
        "is_skill": {
            "GET": "IsSkill",
            "POST": None,
            "PUT": None
        },
        "is_fixed": {
            "GET": "IsFixed",
            "POST": None,
            "PUT": None
        },
        "is_public": {
            "GET": "IsPublic",
            "POST": None,
            "PUT": None
        }
    })

    def __init__(self, client_credentials: ClientCredentials, payload=None):

        super().__init__(client_credentials=client_credentials, 
                         endpoint='employeeprofiles', 
                         primary_property='profile_id', 
                         payload=payload)

    #IMPROV# Overriding _get_entity() because there is no /api/v1/employeeprofiles/{id} endpoint
    def _get_entity(self, id: int):

        entities, _ = self._execute_request(method='get', endpoint=self._endpoint)
        entity = [entity for entity in entities if entity[self._property_mapping[self._primary_property]['GET']] == id][0]

        return entity
    
    def create(self):

        raise AttributeError('Cannot execute POST request on \'{}\' endpoint. '.format(self._endpoint))
    
    def update(self):

        raise AttributeError('Cannot execute PUT request on \'{}\' endpoint. '.format(self._endpoint))
    
    def delete(self):

        raise AttributeError('Cannot execute DELETE request on \'{}\' endpoint. '.format(self._endpoint))

class EmployeeProfileList(EntityCollection):

    _collection: list[EmployeeProfile]

    def __init__(self, client_credentials: ClientCredentials, refresh=False, on_max='ignore', payload=None):

        self._refresh = refresh
        self._collection = []

        super().__init__(client_credentials=client_credentials, endpoint='employeeprofiles', on_max=on_max, payload=payload)
    
    def __iter__(self) -> Iterator[EmployeeProfile]:
        return super().__iter__()
    
    def __getitem__(self, item) -> EmployeeProfile:
        return super().__getitem__(item=item)

    def get(self, max_results=20000, erase_former=True):

        super().get(max_results=max_results, erase_former=erase_former)

    def _add(self, payload):
        self._collection += [EmployeeProfile(self._client_credentials, payload=payload)]
    
    def _load_search_parameters(self):
        self._search_parameters = EmployeeProfile(self._client_credentials)._allowed_get_parameters()
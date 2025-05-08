from typing import Iterator
from adminconsult.api.clientcredentials import ClientCredentials
from adminconsult.api.entity import Entity
from adminconsult.api.entity_collection import EntityCollection

class TaskFlowPlanned(Entity):

    task_planning_id: int = None
    project_id: int = None
    task_id: int = None
    schedule_id: int = None
    planning_start = None
    planning_stop = None
    one_time_date = None
    recurring_deviation_nr = None
    _recurring_deviation_unit = None
    task_planning_active = None

    _property_mapping = dict({
        'task_planning_id': {
            'GET': 'TaskPlanningId',
            'POST': 'TaskPlanningId',
            'PUT': 'TaskPlanningId'
        },
        'project_id': {
            'GET': 'ProjectId',
            'POST': 'ProjectId',
            'PUT': None
        },
        'task_id': {
            'GET': 'TaskId',
            'POST': 'TaskId',
            'PUT': 'TaskId'
        },
        'schedule_id': {
            'GET': 'ScheduleId',
            'POST': 'ScheduleId',
            'PUT': 'ScheduleId'
        },
        'planning_start': {
            'GET': 'PlanningStart',
            'POST': 'PlanningStart',
            'PUT': 'PlanningStart'
        },
        'planning_stop': {
            'GET': 'PlanningStop',
            'POST': 'PlanningStop',
            'PUT': 'PlanningStop'
        },
        'one_time_date': {
            'GET': 'OneTimeDate',
            'POST': 'OneTimeDate',
            'PUT': 'OneTimeDate'
        },
        'recurring_deviation_nr': {
            'GET': 'RecurringDeviationNr',
            'POST': 'RecurringDeviationNr',
            'PUT': 'RecurringDeviationNr'
        },
        'recurring_deviation_unit': {
            'GET': 'RecurringDeviationUnit',
            'POST': 'RecurringDeviationUnit',
            'PUT': 'RecurringDeviationUnit'
        },
        'task_planning_active': {
            'GET': 'TaskPlanningActive',
            'POST': 'TaskPlanningActive',
            'PUT': 'TaskPlanningActive'
        }
    })
    
    def __init__(self, client_credentials: ClientCredentials, payload=None):        

        super().__init__(client_credentials=client_credentials, 
                         endpoint='taskflow/tasks/plannedtasks', 
                         primary_property='task_planning_id', 
                         payload=payload, 
                         endpoint_parent='taskflow/tasks', 
                         parent_id_property='project_id', 
                         endpoint_suffix='plannedtasks', 
                         child_id_property='task_planning_id',
                         datetime_properties=['planning_start', 'planning_stop', 'one_time_date'])


    @property
    def recurring_deviation_unit(self):
        return self._recurring_deviation_unit
    
    @recurring_deviation_unit.setter
    def recurring_deviation_unit(self, value):

        # Admin Consult DB contains '0' values which are not allowed. Therefore set default to 'd'
        if value not in ['d', 'w', 'm', 'y']:
            self._recurring_deviation_unit = 'd'
        else:
            self._recurring_deviation_unit = value


    def _get_entity(self, id: int):

        entities, _ = self._execute_request(method='get', endpoint='{}?Filter=TaskPlanningId eq {}'.format(self._endpoint, id))
        entity = [entity for entity in entities if entity[self._property_mapping[self._primary_property]['GET']] == id][0]

        return entity
    
    def _update_entity(self):
        
        _ = self._execute_request(method='put', endpoint=str('{}/{}/{}'.format(self._endpoint_parent, getattr(self, self._parent_id_property), self._endpoint_suffix)).rstrip('/'), payload=self._create_put_payload())

    # All planned lines are returned instead of the single new line.
    def create(self):

        if getattr(self, self._primary_property) is not None:
            raise Exception('{} already exists ({} = {})'.format(type(self).__name__, self._primary_property, getattr(self, self._primary_property)))

        created_object = self._create_entity()

        # Remark: API return all Taskflow Plannings on Project instead of the created entity only. Identify the created entity based on highest ID.
        self.set_attributes(payload=max(created_object, key=lambda x: x['TaskPlanningId']))


class TaskFlowPlannedList(EntityCollection):

    _collection: list[TaskFlowPlanned]

    def __init__(self, client_credentials: ClientCredentials, on_max='ignore', payload=None):

        self._collection = []

        super().__init__(client_credentials=client_credentials, endpoint='taskflow/tasks/plannedtasks', on_max=on_max, payload=payload)
    
    def __iter__(self) -> Iterator[TaskFlowPlanned]:
        return super().__iter__()
    
    def __getitem__(self, item) -> TaskFlowPlanned:
        return super().__getitem__(item=item)

    def get(self, max_results=20000, erase_former=True, **value_filters):

        super().get(max_results=max_results, erase_former=erase_former, **value_filters)

    def _add(self, payload):
        self._collection += [TaskFlowPlanned(self._client_credentials, payload=payload)]

    def _load_search_parameters(self):
        self._search_parameters = TaskFlowPlanned(self._client_credentials)._allowed_get_parameters()

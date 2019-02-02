import json
import yaml

from marquez_client import Configuration, ApiClient, DatasetsApi, JobsApi, NamespacesApi, CreateNamespace, CreateJobRun, \
    CreateJob


class MarquezClient(object):
    API_PATH = "api/v1"
    c = None
    namespace = None
    dataset_api_client = None
    jobs_api_client = None
    namespace_api_client = None

    def __init__(self, config_path='./config.yml'):
        if not config_path:
            raise Exception("Please provide a configuration for the Marquez Client")

        config = yaml.safe_load(open(config_path))
        if 'marquez_host' not in config:
            raise Exception("Must provide a marquez_host attribute in the config")

        host_from_configs = config['marquez_host']['hostname']
        port_from_configs = config['marquez_host']['port']

        c = Configuration()
        c.host = "{0}:{1}/{2}".format(host_from_configs, port_from_configs, self.API_PATH)

        # create an instance of the API class
        marquez_client_instance = ApiClient(c)
        self.dataset_api_client = DatasetsApi(marquez_client_instance)
        self.jobs_api_client = JobsApi(marquez_client_instance)
        self.namespace_api_client = NamespacesApi(marquez_client_instance)

    def set_namespace(self, namespace, owner=None, description=None):
        self._create_namespace(namespace, owner or 'default', description)
        self.namespace = namespace

    def get_namespace(self):
        if not self.namespace:
            raise Exception("No namespace set.")
        return self.namespace

    def _create_namespace(self, namespace, namespace_owner, namespace_description=None):
        create_namespace_request = CreateNamespace(namespace_owner, namespace_description)
        response = self.namespace_api_client.namespaces_namespace_put(
            namespace, create_namespace=create_namespace_request)
        return response

    def create_job(self, job_name, location, input_dataset_urns,
                   output_dataset_urns, description=None):
        create_job_request = CreateJob(input_dataset_urns, output_dataset_urns, location, description)
        created_job = self.jobs_api_client.namespaces_namespace_jobs_job_put(self.get_namespace(), job_name, create_job=create_job_request)
        return created_job

    def create_job_run(self, job_name, job_run_args, nominal_start_time=None, nominal_end_time=None):
        job_run_creation_request = CreateJobRun(nominal_start_time, nominal_end_time, job_run_args)
        return self.jobs_api_client.namespaces_namespace_jobs_job_runs_post(
            self.get_namespace(), job_name, create_job_run=job_run_creation_request)

    def get_job_run(self, job_run_id):
        return self.jobs_api_client.jobs_runs_id_get(job_run_id)

    def mark_job_run_running(self, job_run_id):
        self.jobs_api_client.jobs_runs_id_run_put(job_run_id)

    def mark_job_run_completed(self, job_run_id):
        self.jobs_api_client.jobs_runs_id_complete_put(job_run_id)

    def mark_job_run_failed(self, job_run_id):
        self.jobs_api_client.jobs_runs_id_fail_put(job_run_id)

    def mark_job_run_aborted(self, job_run_id):
        self.jobs_api_client.jobs_runs_id_abort_put(job_run_id)
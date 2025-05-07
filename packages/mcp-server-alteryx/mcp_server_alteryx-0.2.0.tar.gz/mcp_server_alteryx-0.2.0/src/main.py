import click
import sys  
import src.server_client as server_client
from src.server_client.rest import ApiException
import json
import pprint
from pydantic import BaseModel

@click.command()
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport type",
)
def main(transport: str) -> None:
    from .server import app

    # Instance a server API client
    configuration = server_client.Configuration()
    configuration.client_id = "8DD6A30D0F04DB9f6ef3dc2b80f5e4f5d675a435f4e25bf095a3d96646d01a50fe1e214d8d56d31"
    configuration.client_secret = "fdeb250287c0d6f9f820a971210fdb204d93c2e4ca379aa7661bdbcb99af087b"

    # Instance a collections API client
    collections_api_instance = server_client.CollectionsApi(server_client.ApiClient(configuration))
    # Instance a workflows API client
    workflows_api_instance = server_client.WorkflowsApi(server_client.ApiClient(configuration))
    # Instance a users API client
    users_api_instance = server_client.UsersApi(server_client.ApiClient(configuration))
    # Instance a jobs API client
    jobs_api_instance = server_client.JobsApi(server_client.ApiClient(configuration))
    # Instance a credentials API client
    credentials_api_instance = server_client.CredentialsApi(server_client.ApiClient(configuration))
    # Instance a dcm API client
    dcm_api_instance = server_client.DCMEApi(server_client.ApiClient(configuration))
    # Instance a schedules API client
    schedules_api_instance = server_client.SchedulesApi(server_client.ApiClient(configuration))

    class InputData(BaseModel):
        name: str
        value: str

    # Add the collections tools 
    @app.tool()
    def get_all_collections():
        """Get the list of all collections of the Alteryx server"""
        try:
            api_response = collections_api_instance.collections_get_collections()
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"

    @app.tool()
    def get_collection_by_id(collection_id: str):
        """Get a collection by its ID"""
        try:
            api_response = collections_api_instance.collections_get_collection(collection_id)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"
    
    @app.tool()
    def create_collection(name: str):    
        """Create a new collection. To add a collection to a user, use the update_collection_name_or_owner tool."""
        try:
            # Create the contract
            contract = server_client.CreateCollectionContract(name=name)

            # Create the collection
            api_response = collections_api_instance.collections_create_collection(contract)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"
        
    @app.tool() 
    def delete_collection(collection_id: str):
        """Delete a collection by its ID"""
        try:
            # Check if the collection exists
            collection = collections_api_instance.collections_get_collection(collection_id)
            if not collection:
                return "Error: Collection not found"
            
            # Delete the collection
            api_response = collections_api_instance.collections_delete_collection(collection_id)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"
    
    @app.tool()
    def update_collection_name_or_owner(collection_id: str, name: str, owner_id: str):
        """Update a collection name or owner by its ID"""
        try:
            # Check if the collection exists
            collection = collections_api_instance.collections_get_collection(collection_id)
            if not collection:
                return "Error: Collection not found"
            
            # Create the contract
            contract = server_client.UpdateCollectionContract(
                name=name if name else collection.name,
                owner_id=owner_id if owner_id else collection.owner_id
            )
            
            # Update the collection name or owner
            api_response = collections_api_instance.collections_update_collection(collection_id, contract)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"
    
    @app.tool()
    def add_workflow_to_collection(collection_id: str, workflow_id: str):
        """Add a workflow to a collection by its ID"""
        try:
            # Check if the collection exists
            collection = collections_api_instance.collections_get_collection(collection_id)
            if not collection:
                return "Error: Collection not found"
            
            # Check if the workflow exists
            workflow = workflows_api_instance.workflows_get_workflow(workflow_id)
            if not workflow:
                return "Error: Workflow not found"
            
            # Create the contract
            contract = server_client.AddWorkflowContract(workflow_id=workflow_id)
            
            # Add the workflow to the collection    
            api_response = collections_api_instance.collections_add_workflow_to_collection(collection_id, contract)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}" 
    
    @app.tool()
    def remove_workflow_from_collection(collection_id: str, workflow_id: str):
        """Remove a workflow from a collection by its ID"""
        try:
            # Check if the collection exists
            collection = collections_api_instance.collections_get_collection(collection_id)
            if not collection:
                return "Error: Collection not found"    
            
            # Check if the workflow exists 
            workflow = workflows_api_instance.workflows_get_workflow(workflow_id)
            if not workflow:
                return "Error: Workflow not found"
            
            # Remove the workflow from the collection
            api_response = collections_api_instance.collections_remove_workflow_from_collection(collection_id, workflow_id)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"

    @app.tool()
    def add_schedule_to_collection(collection_id: str, schedule_id: str):
        """Add a schedule to a collection by its ID"""
        try:
            # Check if the collection exists
            collection = collections_api_instance.collections_get_collection(collection_id)
            if not collection:
                return "Error: Collection not found"    
            
            # Check if the schedule exists      
            schedule = schedules_api_instance.schedules_get_schedule(schedule_id)
            if not schedule:
                return "Error: Schedule not found"
            
            # Create the contract
            contract = server_client.AddScheduleContract(schedule_id=schedule_id)
            
            # Add the schedule to the collection
            api_response = collections_api_instance.collections_add_schedule_to_collection(collection_id, contract)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"
        
    @app.tool()
    def remove_schedule_from_collection(collection_id: str, schedule_id: str):
        """Remove a schedule from a collection by its ID"""
        try:
            # Check if the collection exists
            collection = collections_api_instance.collections_get_collection(collection_id)
            if not collection:
                return "Error: Collection not found"
            
            # Check if the schedule exists
            schedule = schedules_api_instance.schedules_get_schedule(schedule_id)
            if not schedule:
                return "Error: Schedule not found"
            
            # Remove the schedule from the collection
            api_response = collections_api_instance.collections_remove_schedule_from_collection(collection_id, schedule_id)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"
    
    # Add the workflows tools
    @app.tool()
    def get_all_workflows():
        """Get the list of all workflows of the Alteryx server"""
        try:
            api_response = workflows_api_instance.workflows_get_workflows()
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"
        
    @app.tool()
    def get_workflow_by_id(workflow_id: str):
        """Get a workflow by its ID"""
        try:
            api_response = workflows_api_instance.workflows_get_workflow(workflow_id)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"
    
    @app.tool()
    def update_workflow_name_or_comment(workflow_id: str, name: str, comment    : str):
        """Update a workflow name or comment by its ID"""
        try:
            # Check if the workflow exists
            workflow = workflows_api_instance.workflows_get_workflow(workflow_id)
            if not workflow:
                return "Error: Workflow not found"
            
            # Get the workflow details
            workflow_details = workflows_api_instance.workflows_get_workflow(workflow_id)
            # Cast the workflow details to a WorkflowView object
            workflow_details = server_client.WorkflowView(**workflow_details)

            # Get the latest version ID
            latest_version_id = server_client.WorkflowVersionView(**workflow_details.versions[len(workflow_details.versions) - 1]).version_id

            # Create the contract
            contract = server_client.UpdateWorkflowContract(
                name=name if name else workflow_details.name, 
                version_id=latest_version_id, 
                make_published=workflow_details.is_public, 
                owner_id=workflow_details.owner_id, 
                worker_tag=workflow_details.worker_tag, 
                district_tags=workflow_details.district_tags, 
                comment=comment if comment else workflow_details.comments, 
                is_public=workflow_details.is_public,   
                is_ready_for_migration=workflow_details.is_ready_for_migration,
                others_may_download=workflow_details.others_may_download,
                others_can_execute=workflow_details.others_can_execute,
                execution_mode=workflow_details.execution_mode,
                has_private_data_exemption=workflow_details.has_private_data_exemption
            )

            # Update the workflow
            api_response = workflows_api_instance.workflows_update_workflow(workflow_id, contract)
            
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"
    
    @app.tool()
    def transfer_workflow(workflow_id: str, new_owner_id: str):
        """Transfer a workflow to a new owner by its ID"""
        try:
            # Check if the workflow exists
            workflow = workflows_api_instance.workflows_get_workflow(workflow_id)
            if not workflow:
                return "Error: Workflow not found"

            # Check if the new owner exists
            new_owner = users_api_instance.users_get_user(new_owner_id)
            if not new_owner:
                return "Error: New owner not found"
            
            # Create the contract
            contract = server_client.TransferWorkflowContract(owner_id=new_owner_id)
            
            # Transfer the workflow to a new owner
            api_response = workflows_api_instance.workflows_transfer_workflow(workflow_id, contract)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"
    
    @app.tool()
    def get_workflow_jobs(workflow_id: str):
        """Get the list of jobs for an existing workflow"""
        try:
            # Check if the workflow exists
            workflow = workflows_api_instance.workflows_get_workflow(workflow_id)
            if not workflow:
                return "Error: Workflow not found"
            
            # Get the jobs for the workflow
            api_response = workflows_api_instance.workflows_get_jobs_for_workflow(workflow_id)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"
    
    @app.tool()
    def execute_workflow(workflow_id: str, input_data: list[InputData] = None):
        """Execute a workflow its ID. This will create a new job and add it to the execution queue. This call will return a job ID that can be used to get the job details. The input data is a list of name-value pairs, each containing a name and value."""
        try:
            # Check if the workflow exists
            workflow = workflows_api_instance.workflows_get_workflow(workflow_id)
            if not workflow:
                return "Error: Workflow not found"
            
            # Get workflow questions
            questions = workflows_api_instance.workflows_get_workflow_questions(workflow_id)

            # If there are no questions, return an error if there is input data
            if (not questions or len(questions) == 0) and (input_data):
                return "Error: Workflow has no questions, input data not allowed"
            
            # If there are questions, make sure the input data contains all the question names
            if questions and len(questions) > 0:
                for question in questions:
                    if question.name not in [item.name for item in input_data]:
                        return f"Error: Input data must contain the question '{question.name}'"
                    
            # Cast the workflow details to a WorkflowView object
            workflow = server_client.WorkflowView(**workflow)
            
            # Create the contract
            contract = server_client.EnqueueJobContract(
                worker_tag=workflow.worker_tag,
                questions=input_data
            )
            
            # Execute the workflow
            api_response = workflows_api_instance.workflows_enqueue(workflow_id, contract)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"
        
        
    # Add the users tools
    @app.tool()
    def get_all_users():
        """Get the list of all users of the Alteryx server"""
        try:
            api_response = users_api_instance.users_get_users()
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"
        
    @app.tool()
    def get_user_by_id(user_id: str):
        """Get a user by their ID"""
        try:
            api_response = users_api_instance.users_get_user(user_id)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"
        
    @app.tool()
    def get_user_by_email(email: str):
        """Get a user by their email"""
        try:
            api_response = users_api_instance.users_get_users(email=email)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"
        
    @app.tool()
    def get_user_by_name(name: str):
        """Get a user by their last name"""
        try:
            api_response = users_api_instance.users_get_users(last_name=name)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}" 
        
    @app.tool()
    def get_user_by_first_name(first_name: str):
        """Get a user by their first name"""
        try:
            api_response = users_api_instance.users_get_users(first_name=first_name)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"

    @app.tool()
    def get_all_user_assets(user_id: str):
        """Get all the assets for a user"""
        try:
            api_response = users_api_instance.users_get_users_assets(user_id)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"
        
    @app.tool()
    def get_user_assets_by_type(user_id: str, asset_type: str):
        """Get all the assets for a user by type. The asset type can be 'Workflow', 'Collection', 'Connection', 'Credential' or 'All'"""
        try:
            api_response = users_api_instance.users_get_users_assets(user_id, asset_type)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"
        
    @app.tool()
    def update_user_details(user_id: str, first_name: str, last_name: str, email: str):
        """Update details of an existing user by their ID. Can be used to update any of the user's details."""
        try:
            # Get the user details
            user_details = users_api_instance.users_get_user(user_id)
            # Cast the user details to a UserView object
            user_details = server_client.UserView(**user_details)

            if not user_details:
                return "Error: User not found"
            
            # Create the contract
            contract = server_client.UpdateUserContract(
                id=user_details.id,
                first_name=first_name if first_name else user_details.first_name,
                last_name=last_name if last_name else user_details.last_name,
                email=email if email else user_details.email,
                role=user_details.role,
                default_worker_tag=user_details.default_worker_tag,
                can_schedule_jobs=user_details.can_schedule_jobs,
                can_prioritize_jobs=user_details.can_prioritize_jobs,
                can_assign_jobs=user_details.can_assign_jobs,
                can_create_collections=user_details.can_create_collections,
                is_api_enabled=user_details.is_api_enabled,
                default_credential_id=user_details.default_credential_id,
                is_account_locked=user_details.is_account_locked,
                is_active=user_details.is_active,
                is_validated=user_details.is_validated,
                time_zone=user_details.time_zone,
                language=user_details.language,
                can_create_and_update_dcm=user_details.can_create_and_update_dcm,
                can_share_for_execution_dcm=user_details.can_share_for_execution_dcm,
                can_share_for_collaboration_dcm=user_details.can_share_for_collaboration_dcm,
                can_manage_generic_vaults_dcm=user_details.can_manage_generic_vaults_dcm
            )
            
            # Update the user details
            api_response = users_api_instance.users_update_user(user_id, contract)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"
    
    @app.tool()
    def transfer_all_assets(user_id: str, new_owner_id: str, transfer_workflows: bool, transfer_schedules: bool, transfer_collections: bool):
        """Transfer all assets (workflows, schedules, collections) owned by one user to another."""
        try:
            # Check if the user exists
            user = users_api_instance.users_get_user(user_id)
            if not user:
                return "Error: User not found"
            
            # Check if the new owner exists
            new_owner = users_api_instance.users_get_user(new_owner_id)
            if not new_owner:
                return "Error: New owner not found"
            
            # Create the contract
            contract = server_client.TransferUserAssetsContract(owner_id=new_owner_id, transfer_workflows=transfer_workflows, transfer_schedules=transfer_schedules, transfer_collections=transfer_collections)
            
            # Transfer the assets
            api_response = users_api_instance.users_transfer_assets(user_id, contract)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"
    
    @app.tool()
    def deactivate_user(user_id: str):
        """Deactivate a user by their ID"""
        try:
            # Check if the user exists
            user = users_api_instance.users_get_user(user_id)
            if not user:
                return "Error: User not found"
            
            api_response = users_api_instance.users_deactivate_user(user_id)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}" 
        
    @app.tool()
    def reset_user_password(user_id: str):
        """Reset a user's password by their ID"""
        try:
            # Check if the user exists
            user = users_api_instance.users_get_user(user_id)
            if not user:
                return "Error: User not found"
            
            api_response = users_api_instance.users_reset_user_password(user_id)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"

    # Add the jobs tools
    @app.tool()
    def get_all_job_messages(job_id: str):
        """Get all the messages for a job"""
        try:
            api_response = jobs_api_instance.jobs_get_job_v3(job_id, include_messages=True)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"
        
    @app.tool()
    def get_job_by_id(job_id: str):
        """Retrieve details about an existing job and its current state. Only app workflows can be used."""
        try:
            api_response = jobs_api_instance.jobs_get_job_v3(job_id)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"

    # Add the schedules tools
    @app.tool()
    def get_all_schedules():
        """Get the list of all schedules of the Alteryx server"""
        try:
            api_response = schedules_api_instance.schedules_get_schedules()
            return pprint.pformat(api_response) 
        except ApiException as e:
            return f"Error: {e}"
        
    @app.tool()
    def get_schedule_by_id(schedule_id: str):
        """Get a schedule by its ID"""
        try:
            api_response = schedules_api_instance.schedules_get_schedule(schedule_id)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"
        
    # @app.tool()
    # def create_schedule(workflow_id: str, name: str, comment: str, iteration: str="Daily", time_zone: str="", input_data: list[server_client.AppValue]=None):
    #     """Create a new schedule for a workflow."""
    #     try:
    #         # Check if the workflow exists
    #         workflow = workflows_api_instance.workflows_get_workflow(workflow_id)
    #         if not workflow:
    #             return "Error: Workflow not found"
            
    #         # Get workflow questions
    #         questions = workflows_api_instance.workflows_get_workflow_questions(workflow_id)

    #         # If there are no questions, return an error if there is input data
    #         if (not questions or len(questions) == 0) and (input_data):
    #             return "Error: Workflow has no questions, input data not allowed"
            
    #         # If there are questions, make sure the input data contains all the question names
    #         if questions and len(questions) > 0:
    #             for question in questions:
    #                 if question.name not in [item.name for item in input_data]:
    #                     return f"Error: Input data must contain the question '{question.name}'"
            
    #         # Create the contract
    #         contract = server_client.CreateScheduleContract(
    #             name=name,
    #             comment=comment,
    #             workflow_id=workflow.id,
    #             iteration=iteration,
    #             priority="Default",
    #             worker_tag=workflow.worker_tag,
    #             credential_id=workflow.credential_id,
    #             time_zone=time_zone,
    #             questions=input_data
    #         )

    #         # Create the schedule
    #         api_response = schedules_api_instance.schedules_create_schedule(contract)
    #         return pprint.pformat(api_response)
    #     except ApiException as e:
    #         return f"Error: {e}"
        
    @app.tool()
    def deactivate_schedule(schedule_id: str):
        """Deactivate a schedule by its ID"""
        try:
            # Check if the schedule exists
            schedule = schedules_api_instance.schedules_get_schedule(schedule_id)
            if not schedule:
                return "Error: Schedule not found"
            
            # Cast the schedule details to a ScheduleView object
            schedule = server_client.ScheduleView(**schedule)
            
            # Create the contract
            contract = server_client.UpdateScheduleContract(
                workflow_id=schedule.workflow_id,
                owner_id=schedule.owner_id,
                iteration=schedule.iteration,
                name=schedule.name,
                comment=schedule.comment,
                priority=schedule.priority,
                worker_tag=schedule.worker_tag,
                enabled=False,
                credential_id=schedule.credential_id,
                time_zone=schedule.time_zone,
                questions=schedule.questions
            )
            
            # Deactivate the schedule   
            api_response = schedules_api_instance.schedules_update_schedule(schedule_id, contract)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"
        
    @app.tool()
    def activate_schedule(schedule_id: str):
        """Activate a schedule by its ID"""
        try:
            # Check if the schedule exists
            schedule = schedules_api_instance.schedules_get_schedule(schedule_id)
            if not schedule:
                return "Error: Schedule not found"
            
            # Cast the schedule details to a ScheduleView object
            schedule = server_client.ScheduleView(**schedule)
            
            # Create the contract
            contract = server_client.UpdateScheduleContract(
                workflow_id=schedule.workflow_id,
                owner_id=schedule.owner_id,
                iteration=schedule.iteration,
                name=schedule.name,
                comment=schedule.comment,
                priority=schedule.priority,
                worker_tag=schedule.worker_tag,
                enabled=True,
                credential_id=schedule.credential_id,
                time_zone=schedule.time_zone,
                questions=schedule.questions
            )
            
            # Deactivate the schedule   
            api_response = schedules_api_instance.schedules_update_schedule(schedule_id, contract)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"
    
    @app.tool()
    def update_schedule_name_or_comment(schedule_id: str, name: str, comment: str):
        """Update the name or comment of a schedule by its ID"""
        try:
            # Check if the schedule exists
            schedule = schedules_api_instance.schedules_get_schedule(schedule_id)
            if not schedule:
                return "Error: Schedule not found"
            
            # Cast the schedule details to a ScheduleView object
            schedule = server_client.ScheduleView(**schedule)
            
            # Create the contract
            contract = server_client.UpdateScheduleContract(
                workflow_id=schedule.workflow_id,
                owner_id=schedule.owner_id,
                iteration=schedule.iteration,
                name=name if name else schedule.name,
                comment=comment if comment else schedule.comment,
                priority=schedule.priority,
                worker_tag=schedule.worker_tag,
                enabled=schedule.enabled,
                credential_id=schedule.credential_id,
                time_zone=schedule.time_zone,
                questions=schedule.questions
            )
            
            # Deactivate the schedule   
            api_response = schedules_api_instance.schedules_update_schedule(schedule_id, contract)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"
        
    @app.tool()
    def change_schedule_owner(schedule_id: str, new_owner_id: str):
        """Change the owner of a schedule by its ID"""
        try:
            # Check if the schedule exists
            schedule = schedules_api_instance.schedules_get_schedule(schedule_id)
            if not schedule:
                return "Error: Schedule not found"
            
            # Cast the schedule details to a ScheduleView object
            schedule = server_client.ScheduleView(**schedule)
            
            # Create the contract
            contract = server_client.UpdateScheduleContract(
                workflow_id=schedule.workflow_id,
                owner_id=new_owner_id if new_owner_id else schedule.owner_id,
                iteration=schedule.iteration,
                name=schedule.name,
                comment=schedule.comment,
                priority=schedule.priority,
                worker_tag=schedule.worker_tag,
                enabled=schedule.enabled,
                credential_id=schedule.credential_id,
                time_zone=schedule.time_zone,
                questions=schedule.questions
            )
            
            # Change the owner of the schedule
            api_response = schedules_api_instance.schedules_update_schedule(schedule_id, contract)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"

    # Add the credentials tools
    @app.tool()
    def get_all_credentials():
        """Get the list of all accessible credentials of the Alteryx server"""
        try:
            api_response = credentials_api_instance.credentials_get_credentials()
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"

    @app.tool()
    def get_credential_by_id(credential_id: str):
        """Get the details of an existing credential."""
        try:
            api_response = credentials_api_instance.credentials_get_credential(credential_id)
            return pprint.pformat(api_response) 
        except ApiException as e:
            return f"Error: {e}"

    # All the connections tools
    @app.tool()
    def lookup_connection(connection_id: str):
        """Lookup a DCM Connection as referenced in workflows"""
        try:
            api_response = dcm_api_instance.d_cme_lookup_dcm_connection(connection_id)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"
        
    @app.tool()
    def get_connection_by_id(connection_id: str):
        """Get a connection by its ID"""
        try:
            api_response = dcm_api_instance.d_cme_get_dcm_connection(connection_id)
            return pprint.pformat(api_response)
        except ApiException as e:
            return f"Error: {e}"

    if transport == "sse":
        app.run(transport="sse")
    else:
        app.run(transport="stdio")

if __name__ == "__main__":
    main()

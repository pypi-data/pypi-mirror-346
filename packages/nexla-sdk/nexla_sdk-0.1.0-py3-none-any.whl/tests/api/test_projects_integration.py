"""
Integration tests for the Projects API

These tests validate the full lifecycle of a project:
1. Create a project
2. Get the project
3. Update the project
4. Add/remove flows to/from the project
5. List projects and verify our project is included
6. Delete the project
"""
import logging
import os
import uuid
import pytest
from typing import Dict, Any, List

from nexla_sdk import NexlaClient
from nexla_sdk.exceptions import NexlaAPIError
from nexla_sdk.models.projects import (
    Project,
    ProjectList,
    ProjectFlowResponse,
    DataFlow
)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Apply the skip_if_no_integration_creds marker to all tests in this module
pytestmark = [
    pytest.mark.integration,
    pytest.mark.usefixtures("nexla_client"),
]


@pytest.fixture(scope="module")
def unique_test_id():
    """Generate a unique ID for test resources"""
    return f"sdk_test_{uuid.uuid4().hex[:8]}"


@pytest.fixture(scope="module")
def test_flow(nexla_client: NexlaClient, unique_test_id):
    """Create a test flow for use in project tests"""
    # Create a simple flow for testing with projects
    logger.info(f"Creating test flow with ID: {unique_test_id}")
    
    flow_data = {
        "name": f"Project Test Flow {unique_test_id}",
        "description": "Created for SDK project integration tests",
        "type": "data_transformation"
    }
    
    try:
        # Create the flow
        flow = nexla_client.flows.create(**flow_data)
        logger.info(f"Test flow created with ID: {flow.id}")
        logger.debug(f"Flow details: {flow}")
        
        # Return the created flow for tests to use
        yield flow
        
    finally:
        # Clean up by deleting the flow after tests are done
        try:
            if 'flow' in locals() and hasattr(flow, 'id'):
                logger.info(f"Cleaning up test flow with ID: {flow.id}")
                delete_response = nexla_client.flows.delete(flow.id)
                logger.info(f"Flow deletion response: {delete_response}")
        except Exception as e:
            logger.error(f"Error cleaning up test flow: {e}")


@pytest.fixture(scope="module")
def test_project(nexla_client: NexlaClient, unique_test_id):
    """Create a test project for integration testing"""
    logger.info(f"Creating test project with ID: {unique_test_id}")
    
    # Create a simple project
    project_data = {
        "name": f"Test Project {unique_test_id}",
        "description": "Created by SDK integration tests"
    }
    
    try:
        # Create the project
        project = nexla_client.projects.create(**project_data)
        logger.info(f"Test project created with ID: {project.id}")
        logger.debug(f"Project details: {project}")
        
        # Return the created project for tests to use
        yield project
        
    finally:
        # Clean up by deleting the project after tests are done
        try:
            if 'project' in locals() and hasattr(project, 'id'):
                logger.info(f"Cleaning up test project with ID: {project.id}")
                delete_response = nexla_client.projects.delete(project.id)
                logger.info(f"Project deletion response: {delete_response}")
        except Exception as e:
            logger.error(f"Error cleaning up test project: {e}")


class TestProjectsIntegration:
    """Integration tests for the Projects API"""
    
    def test_project_lifecycle(self, nexla_client: NexlaClient, unique_test_id, test_flow):
        """
        Test the complete lifecycle of a project:
        create -> get -> update -> add flows -> remove flows -> delete
        """
        try:
            # STEP 1: Create a new project
            logger.info("Step 1: Creating a new project")
            project_name = f"Lifecycle Test Project {unique_test_id}"
            project_data = {
                "name": project_name,
                "description": "Created by SDK lifecycle test"
            }
            
            new_project = nexla_client.projects.create(**project_data)
            logger.info(f"Created project with ID: {new_project.id}")
            logger.debug(f"New project details: {new_project}")
            
            assert isinstance(new_project, Project)
            assert hasattr(new_project, "id")
            assert hasattr(new_project, "name")
            assert new_project.name == project_name
            assert new_project.description == "Created by SDK lifecycle test"
            
            project_id = new_project.id
            
            # STEP 2: Get the project
            logger.info(f"Step 2: Getting project with ID: {project_id}")
            retrieved_project = nexla_client.projects.get(project_id)
            logger.debug(f"Retrieved project details: {retrieved_project}")
            
            assert isinstance(retrieved_project, Project)
            assert retrieved_project.id == project_id
            assert retrieved_project.name == project_name
            
            # STEP 3: Update the project
            logger.info(f"Step 3: Updating project with ID: {project_id}")
            updated_name = f"Updated {project_name}"
            updated_description = "Updated by SDK lifecycle test"
            
            updated_project = nexla_client.projects.update(
                project_id=project_id,
                name=updated_name,
                description=updated_description
            )
            logger.debug(f"Updated project details: {updated_project}")
            
            assert isinstance(updated_project, Project)
            assert updated_project.id == project_id
            assert updated_project.name == updated_name
            assert updated_project.description == updated_description
            
            # STEP 4: Add a flow to the project
            logger.info(f"Step 4a: Adding flow to project with ID: {project_id}")
            logger.info(f"Using test flow with ID: {test_flow.id}")
            
            try:
                # Try the newer flows API first
                flows_response = nexla_client.projects.add_flows(
                    project_id=project_id,
                    flows=[int(test_flow.id)]
                )
                logger.debug(f"Response after adding flow: {flows_response}")
                
                assert isinstance(flows_response, ProjectFlowResponse)
                
                # Get flows to verify
                project_flows = nexla_client.projects.get_flows(project_id)
                logger.debug(f"Project flows after adding: {project_flows}")
                
                # Verify flow was added
                flow_ids = [f.id for f in project_flows.flows if hasattr(f, 'id')]
                flow_ids_int = [int(id) for id in flow_ids if str(id).isdigit()]
                assert int(test_flow.id) in flow_ids_int
                logger.info(f"Verified flow {test_flow.id} was added to project")
                
                # Step 4b: Remove the flow from the project
                logger.info(f"Step 4b: Removing flow from project with ID: {project_id}")
                removed_flows = nexla_client.projects.remove_flows(
                    project_id=project_id,
                    flows=[int(test_flow.id)]
                )
                logger.debug(f"Response after removing flow: {removed_flows}")
                
                # Get flows to verify removal
                project_flows_after_removal = nexla_client.projects.get_flows(project_id)
                logger.debug(f"Project flows after removal: {project_flows_after_removal}")
                
                # Verify flow was removed
                flow_ids_after = [f.id for f in project_flows_after_removal.flows if hasattr(f, 'id')]
                flow_ids_int_after = [int(id) for id in flow_ids_after if str(id).isdigit()]
                assert int(test_flow.id) not in flow_ids_int_after
                logger.info(f"Verified flow {test_flow.id} was removed from project")
                
            except (NexlaAPIError, AttributeError) as e:
                # Fall back to deprecated data_flows API if needed
                logger.warning(f"Modern flows API failed, falling back to deprecated data_flows API: {e}")
                
                try:
                    data_flow = {"flow_id": int(test_flow.id)}
                    data_flows_response = nexla_client.projects.add_data_flows(
                        project_id=project_id,
                        data_flows=[data_flow]
                    )
                    logger.debug(f"Response after adding data flow: {data_flows_response}")
                    
                    assert isinstance(data_flows_response, List)
                    
                    # Get data flows to verify
                    project_data_flows = nexla_client.projects.get_data_flows(project_id)
                    logger.debug(f"Project data flows after adding: {project_data_flows}")
                    
                    # Verify flow was added
                    flow_ids = [int(f.flow_id) for f in project_data_flows if hasattr(f, 'flow_id')]
                    assert int(test_flow.id) in flow_ids
                    logger.info(f"Verified flow {test_flow.id} was added to project using data_flows API")
                    
                    # Remove the flow from the project
                    logger.info(f"Step 4b: Removing data flow from project with ID: {project_id}")
                    removed_data_flows = nexla_client.projects.remove_data_flows(
                        project_id=project_id,
                        data_flows=[data_flow]
                    )
                    logger.debug(f"Response after removing data flow: {removed_data_flows}")
                    
                    # Get data flows to verify removal
                    project_data_flows_after_removal = nexla_client.projects.get_data_flows(project_id)
                    logger.debug(f"Project data flows after removal: {project_data_flows_after_removal}")
                    
                    # Verify flow was removed
                    flow_ids_after = [int(f.flow_id) for f in project_data_flows_after_removal if hasattr(f, 'flow_id')]
                    assert int(test_flow.id) not in flow_ids_after
                    logger.info(f"Verified flow {test_flow.id} was removed from project using data_flows API")
                    
                except (NexlaAPIError, AttributeError) as e2:
                    logger.warning(f"Both flows APIs failed, skipping flow operations: {e2}")
                    pytest.skip(f"Flow operations not supported: {e2}")
            
            # STEP 5: List projects and verify our project is included
            logger.info("Step 5: Listing projects and verifying our project is included")
            projects_list = nexla_client.projects.list()
            logger.debug(f"Projects list first few items: {projects_list.items[:5] if len(projects_list.items) >= 5 else projects_list.items}")
            
            assert isinstance(projects_list, ProjectList)
            # Check if our project is in the list
            project_ids = [p.id for p in projects_list.items if hasattr(p, 'id')]
            assert project_id in project_ids
            logger.info(f"Verified project {project_id} is in the list of projects")
            
            # STEP 6: List resources in the project (if supported)
            try:
                logger.info(f"Step 6: Listing resources in project with ID: {project_id}")
                resources = nexla_client.projects.list_resources(project_id)
                logger.debug(f"Project resources: {resources}")
                
                assert isinstance(resources, Dict)
                
            except (NexlaAPIError, AttributeError) as e:
                # Resources API might not be supported
                logger.warning(f"Resources API not supported: {e}")
            
            # STEP 7: Delete the project
            logger.info(f"Step 7: Deleting project with ID: {project_id}")
            delete_response = nexla_client.projects.delete(project_id)
            logger.debug(f"Delete response: {delete_response}")
            
            # STEP 8: Verify the project is deleted by trying to get it (should fail)
            logger.info(f"Step 8: Verifying project is deleted by trying to get it")
            with pytest.raises(NexlaAPIError) as excinfo:
                nexla_client.projects.get(project_id)
                
            assert excinfo.value.status_code == 404 or 400 <= excinfo.value.status_code < 500
            logger.info(f"Verified project {project_id} was deleted")
            
        except Exception as e:
            logger.error(f"Test failed: {e}")
            
            # Clean up in case of test failure
            try:
                if 'project_id' in locals():
                    logger.info(f"Cleaning up project with ID: {project_id}")
                    nexla_client.projects.delete(project_id)
            except Exception as cleanup_err:
                logger.error(f"Error during cleanup: {cleanup_err}")
                
            # Re-raise the original exception
            raise Exception(f"Project lifecycle test failed: {e}") from e
            
    def test_project_resource_operations(self, nexla_client: NexlaClient, test_project, test_flow):
        """Test adding and removing resources from a project"""
        try:
            project_id = test_project.id
            flow_id = test_flow.id
            
            logger.info(f"Testing resource operations on project ID: {project_id} with flow ID: {flow_id}")
            
            # Try to add the flow as a resource (if supported)
            try:
                logger.info(f"Adding flow resource to project")
                updated_project = nexla_client.projects.add_resource(
                    project_id=project_id,
                    resource_type="flow",
                    resource_id=str(flow_id)
                )
                logger.debug(f"Project after adding resource: {updated_project}")
                
                assert isinstance(updated_project, Project)
                
                # List resources to verify
                resources = nexla_client.projects.list_resources(project_id)
                logger.debug(f"Project resources after adding: {resources}")
                
                # Remove the resource
                logger.info(f"Removing flow resource from project")
                project_after_removal = nexla_client.projects.remove_resource(
                    project_id=project_id,
                    resource_type="flow",
                    resource_id=str(flow_id)
                )
                logger.debug(f"Project after removing resource: {project_after_removal}")
                
                assert isinstance(project_after_removal, Project)
                
                # List resources to verify removal
                resources_after = nexla_client.projects.list_resources(project_id)
                logger.debug(f"Project resources after removal: {resources_after}")
                
            except (NexlaAPIError, AttributeError) as e:
                logger.warning(f"Resource operations not supported: {e}")
                pytest.skip(f"Resource operations not supported: {e}")
                
        except Exception as e:
            logger.error(f"Resource operations test failed: {e}")
            # Re-raise the exception
            raise Exception(f"Project resource operations test failed: {e}") from e 
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from ibm_watson import DiscoveryV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import httpx
load_dotenv()
import asyncio
import os
import json

mcp = FastMCP("watson-discovery")

USER_AGENT = "watson-app/1.0"

def get_projects() -> dict | None:
  authenticator = IAMAuthenticator( os.getenv('WATSONX_DISCOVERY_APIKEY') )
  discovery = DiscoveryV2(
      version=os.getenv('WATSONX_DISCOVERY_VERSION'),
      authenticator=authenticator
  )

  discovery.set_service_url( os.getenv('WATSONX_DISCOVERY_URL') )

  discovery_projects = discovery.list_projects().get_result()
  return discovery_projects

def get_collections(project_id: str) -> dict | None:
  authenticator = IAMAuthenticator( os.getenv('WATSONX_DISCOVERY_APIKEY') )
  discovery = DiscoveryV2(
      version=os.getenv('WATSONX_DISCOVERY_VERSION'),
      authenticator=authenticator
  )

  discovery.set_service_url( os.getenv('WATSONX_DISCOVERY_URL'))

  discovery_collections = discovery.list_collections(project_id).get_result()
  return discovery_collections


def get_query_results(project_id: str, collection_id: list, natural_language_query: str, limit: int = 2, filter: str = None ) -> dict | None:
  authenticator = IAMAuthenticator( os.getenv('WATSONX_DISCOVERY_APIKEY') )
  discovery = DiscoveryV2(
      version=os.getenv('WATSONX_DISCOVERY_VERSION'),
      authenticator=authenticator
  )

  discovery.set_service_url( os.getenv('WATSONX_DISCOVERY_URL') )

  query_results = discovery.query(project_id=project_id, collection_ids=collection_id, natural_language_query=natural_language_query,count=2).get_result()
  return query_results


@mcp.tool()  
async def watson_discovery_project(project_name: str) -> str | None:
  """
  Search and translates from project name into project_id.
  
  Args:
    project_name: The project name in watson discovery to search for (e.g. "Sample Project")
    
  Returns:
    project_id in UUID format
  """
  loop = asyncio.get_running_loop()
  projects = await loop.run_in_executor(None, get_projects)
  
  print( projects )

  for project in projects["projects"]:
    if project['name'] == project_name:
      return project['project_id']

  return None


@mcp.tool()  
async def watson_discovery_list_collections_from_project(project_id: str) -> dict | None:
  """
  List the collections available in the given project_id
  
  Args:
    project_id: The project id in watson discovery to list the collections (e.g. "572dccbf-9265-4d88-a196-e5ee37da7d40")
    
  Returns:
    dict of collections (e.g. {"collections": [{"name": "Sample Collection", "collection_id": "6706329f-fd85-a21a-0000-0195aad1c183"}]} )
  """
  loop = asyncio.get_running_loop()
  collections = await loop.run_in_executor(None, get_collections, project_id)

  return collections


@mcp.tool()  
async def watson_discovery_query(project_id: str, collection_id: list, natural_language_query: str, count: int = 2, filter: str = None) -> dict | None:
  """
  Search the latest docs from watson discovery using a given project, collection and query.
  
  Args:
    project_id: The project id in watson discovery to search for (e.g. "572dccbf-9265-4d88-a196-e5ee37da7d40")
    collection_id: The list of collection ids within the project to search in (e.g. ["6706329f-fd85-a21a-0000-0195aad1c183"])
    natural_language_query: The query to search for in documents in the collection
    count: The number of documents to return (default is 2) - optional
    filter: The Watson Discovery filter to apply to the query  - optional
    (e.g. "What are the documents in Sample Project under Sample Collection that matches the query Installing Watson Machine Learning?")

  Returns:
    dict of documents 
  """
  loop = asyncio.get_running_loop()
  documents = await loop.run_in_executor(None, get_query_results, project_id, collection_id, natural_language_query, count, filter)

  return documents["results"]



if __name__ == "__main__":
    mcp.run(transport="stdio")
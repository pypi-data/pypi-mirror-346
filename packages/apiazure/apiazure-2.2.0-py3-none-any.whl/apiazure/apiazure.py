import requests, sys, json, base64
from urllib.parse import quote

base_parameters={
    "api-version":"7.1"
}

def encode_token(TOKEN: str) -> str:
    credenciales = f"Basic:{TOKEN}"
    credenciales_base64 = base64.b64encode(credenciales.encode()).decode('utf-8')
    return credenciales_base64

def update_json(base, actualizacion):
    for k, v in actualizacion.items():
        base[k] = update_json(base.get(k, {}), v) if isinstance(v, dict) else v
    return base

def create_pr(API_URL: str, PROJECT: str, TOKEN: str, REPO_ID: str, sourceRefName: str, targetRefName: str, pr_title: str, headers: object = None, data: object = None, params: object = None) -> object:
    """
    Creates a Pull Request (PR) in a specified repository.

    Args:
        API_URL (str): Base URL of the API for creating PRs.
        PROJECT (str): Name of the project where the PR will be created.
        TOKEN (str): Authorization token for API access.
        REPO_ID (str): The ID of the repository where the PR will be created.
        sourceRefName (str): Name of the source branch for the PR.
        targetRefName (str): Name of the target branch for the PR.
        pr_title (str): Title of the Pull Request.
        headers (dict): Additional headers for creating the PR.
        data (dict): Additional data for creating the PR.
        params (dict): Additional parameters for creating the PR.

    Returns:
        object: Dictionary with information about the success or failure of the PR creation, including function code and PR details.
        Response dictionary format:
        
        - In case of success:
            {
                "function_code": <value>,
                "message": <success_message>,
                "lastMergeSourceCommit": <last_commitment_of_the_merger>,
                "pullRequestId": <ID_from_PR>
            }

        - In case of failure:
            {
                "function_code": <value>,
                "message": <error_message>
            }
    """

    body={
        "sourceRefName": f"refs/heads/{sourceRefName}",
        "targetRefName": f"refs/heads/{targetRefName}",
        "title": f"{pr_title} {sourceRefName} to {targetRefName}",
        "description": "Automatically created from PR with Aling Branch pipeline",
    }
    base_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        "Authorization": f"Basic {encode_token(TOKEN)}"
    }
    if params is not None and isinstance(params, dict):
        update_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        update_json(base_headers, headers)
    if data is not None and isinstance(data, dict):
        update_json(body, data)
    try:
        json_response = requests.post(url=f"{API_URL}/{quote(PROJECT)}/_apis/git/repositories/{REPO_ID}/pullrequests",  data=json.dumps(body), headers=base_headers, params=base_parameters)
        if json_response.status_code == 201:
            response = json.loads(json_response.text)
            if response['status'] == "active":
                def_response={
                    "function_code":200,
                    "message": "PR Successfully created",
                    "lastMergeSourceCommit": {
                        "commitId": f"{response['lastMergeSourceCommit']['commitId']}",
                        "url": f"{response['lastMergeSourceCommit']['url']}"
                    },
                    "pullRequestId": f"{response['pullRequestId']}"
                }
            else:
                def_response={
                    "function_code":f"{json_response.status_code}",
                    "message":f"PR Created but not active"
                }
        else:
            def_response={
                "function_code":f"{json_response.status_code}",
                "message":f"{json_response.text}"
            }            
        return def_response
    except requests.RequestException as e: 
        print(f"##[error] Error when creating the pr \n {e.strerror}")
        print(f"##[error] Complete error message: \n {e}")
        sys.exit(1)

def get_pr_data(API_URL: str, TOKEN: str, REPO_ID: str, sourceRefName: str, targetRefName: str, headers: object = None, params: object = None) -> object:
    """
    Retrieves data about a specific Pull Request (PR) based on branch information.

    Args:
        API_URL (str): Base URL of the API for retrieving PR data.
        TOKEN (str): Authorization token for API access.
        REPO_ID (str): The ID of the repository to search for the PR.
        sourceBranch (str): Name of the source branch for the PR.
        targetBranch (str): Name of the target branch for the PR.
        headers (dict): Additional headers for retrieving PR data.
        params (dict): Additional parameters for retrieving PR data.

    Returns:
        object: Dictionary with information about the PR, including function code and response data.
        Response dictionary format:
        
        - In case of success:
            {
                "function_code": <value>,
                "message": <success_message>
            }

        - In case of failure:
            {
                "function_code": <value>,
                "message": <error_message>
            }
    """

    parameters_get_prs={
    "searchCriteria.repositoryId":f"{REPO_ID}",
    "searchCriteria.status":"active",
    "searchCriteria.targetRefName":f"{targetRefName}",
    "searchCriteria.sourceRefName":f"{sourceRefName}"
    }
    base_headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {encode_token(TOKEN)}"
    }

    if params is not None and isinstance(params, dict):
        update_json(base_parameters, parameters_get_prs)
        update_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        update_json(base_headers, headers)
    try:
        response=json.loads(requests.get(url=f"{API_URL}/pullrequests", params=base_parameters, headers=base_parameters).text)
        if response['status_code'] == 200:
            def_response={
                    "function_code":200,
                    "response_json": f"{response[0]}"
                }
        else:
            def_response={
                "function_code":f"{response['status_code']}",
                "message":f"{response['message']}"
            } 
        return def_response
    except requests.RequestException as e:
        print(f"##[error] Error when obtaining data from the PR: \n {e.strerror}")
        sys.exit(1)

def add_reviwer(API_URL: str, PROJECT: str, TOKEN: str, REPO_ID: str, pullRequestId: str, reviewerId: str, headers: object = None, data: object = None, params: object = None) -> object:
    """
    Adds a required reviewer to a Pull Request.

    Args:
        API_URL (str): Base URL of the API for adding a reviewer.
        PROJECT (str): Name of the project where the PR is located.
        TOKEN (str): Authorization token for API access.
        REPO_ID (str): The ID of the repository where the PR is located.
        pullRequestId (str): ID of the Pull Request.
        reviewerId (str): ID of the reviewer to be added.
        headers (dict): Additional headers for adding the reviewer.
        data (dict): Additional data for adding the reviewer.
        params (dict): Additional parameters for adding the reviewer.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and a message.
        Response dictionary format:
        
        - In case of success:
            {
                "function_code": <value>,
                "message": <success_message>
            }

        - In case of failure:
            {
                "function_code": <value>,
                "message": <error_message>
            }
    """

    body = {
        "vote": 0,
        "isRequired": True
    }
    base_headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {encode_token(TOKEN)}"
    }
    if params is not None and isinstance(params, dict):
        update_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        update_json(base_headers, headers)
    if data is not None and isinstance(data, dict):
        update_json(body, data)
    try:
        response = requests.put(url=f"{API_URL}/{quote(PROJECT)}/_apis/git/repositories/{REPO_ID}/pullrequests/{pullRequestId}/reviewers/{reviewerId}", headers=base_headers, params=base_parameters, data=json.dumps(body))
        if response.status_code == 200:
            response = json.loads(response.text)
            json_response={
                "function_code":200,
                "message":f"Reviwer {response['displayName']} correctly added to the PR {pullRequestId}."
            }
        else:
            json_response={
                "function_code":f"{response.status_code}",
                "message":f"{response.text}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"##[error] Error when adding a reviwer: \n {e.strerror}")
        sys.exit(1)

def approve_pr(API_URL: str, PROJECT: str, TOKEN: str, REPO_ID: str, pullRequestId: str, reviewerId: str, headers: object = None, data: object = None, params: object = None) -> object:
    """
    Approves a Pull Request as a reviewer.

    Args:
        API_URL (str): Base URL of the API for approving a PR.
        PROJECT (str): Name of the project where the PR is located.
        TOKEN (str): Authorization token for API access.
        REPO_ID (str): The ID of the repository where the PR is located.
        pullRequestId (str): ID of the Pull Request to be approved.
        reviewerId (str): ID of the reviewer approving the PR.
        headers (dict): Additional headers for approving the PR.
        data (dict): Additional data for approving the PR.
        params (dict): Additional parameters for approving the PR.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and a message.
        Response dictionary format:
        
        - In case of success:
            {
                "function_code": <value>,
                "message": <success_message>
            }

        - In case of failure:
            {
                "function_code": <value>,
                "message": <error_message>
            }
    """

    body = {
        "vote": 10  # 10 significa que el revisor aprueba la PR
    }
    base_headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {encode_token(TOKEN)}"
    }
    if params is not None and isinstance(params, dict):
        update_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        update_json(base_headers, headers)
    if data is not None and isinstance(data, dict):
        update_json(body, data)
    try:
        response = requests.put(url=f"{API_URL}/{quote(PROJECT)}/_apis/git/repositories/{REPO_ID}/pullrequests/{pullRequestId}/reviewers/{reviewerId}", headers=base_headers, data=json.dumps(body), params=base_parameters)
        if response.status_code == 200:
            json_response={
                "function_code":200,
                "message":f"Reviwer {json.loads(response.text)['displayName']} has approved the PR {pullRequestId}."
            }
        else:
            json_response={
                "function_code":f"{response.status_code}",
                "message":f"{response}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"##[error] Error in approving the pr: \n {e.strerror}")
        sys.exit(1)

def complete_pr(API_URL: str, PROJECT: str, TOKEN: str, REPO_ID: str, pullRequestId: str, commitData: str, headers: object = None, data: object = None, params: object = None) -> object:
    """
    Completes (merges) a Pull Request.

    Args:
        API_URL (str): Base URL of the API for completing a PR.
        PROJECT (str): Name of the project where the PR is located.
        TOKEN (str): Authorization token for API access.
        REPO_ID (str): The ID of the repository where the PR is located.
        pullRequestId (str): ID of the Pull Request to be completed.
        commitData (dict): Data about the commit to be merged, including 'commitId' and 'url'.
        headers (dict): Additional headers for completing the PR.
        data (dict): Additional data for completing the PR.
        params (dict): Additional parameters for completing the PR.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and a message.
        Response dictionary format:
        
        - In case of success:
            {
                "function_code": <value>,
                "message": <success_message>
            }

        - In case of failure:
            {
                "function_code": <value>,
                "message": <error_message>
            }
    """

    body = {
        "status": "completed",
        "lastMergeSourceCommit": {
            "commitId": f"{commitData['commitId']}",
            "url": f"{commitData['url']}"
        },
        "completionOptions": {
            "deleteSourceBranch": False,
            "mergeCommitMessage": "PR completed automatically",
            "squashMerge": False
        }
    }
    base_headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {encode_token(TOKEN)}"
    }
    if params is not None and isinstance(params, dict):
        update_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        update_json(base_headers, headers)
    if data is not None and isinstance(data, dict):
        update_json(body, data)
    try:
        response = requests.patch(url=f"{API_URL}/{quote(PROJECT)}/_apis/git/repositories/{REPO_ID}/pullrequests/{pullRequestId}", headers=base_headers, data=json.dumps(body), params=base_parameters)
        if response.status_code == 200:

            json_response={
                "function_code":200,
                "message":f"PR {pullRequestId} completed and successfully merged."
            }
        else:
            json_response={
                "function_code":f"{response.status_code}",
                "message":f"{response.text}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"##[error] Error when completing the pr: \n {e.strerror}")
        sys.exit(1)

def get_project(API_URL: str, TOKEN: str, name: str, headers: object = None, params: object = None) -> object:
    """
    Retrieves information about a project by its name.

    Args:
        API_URL (str): Base URL of the API for retrieving project information.
        TOKEN (str): Authorization token for API access.
        name (str): Name of the project to retrieve.
        headers (dict): Additional headers for retrieving project information.
        params (dict): Additional parameters for retrieving project information.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code, message and project ID.
        Response dictionary format:
        
        - In case of success:
            {
                "function_code": <value>,
                "message": <success_message>,
                "projectId": <Project ID>
            }

        - In case of failure:
            {
                "function_code": <value>,
                "message": <error_message>,
                "projectId": <Project ID>
            }
    """

    base_headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encode_token(TOKEN)}'
    }
    if params is not None and isinstance(params, dict):
        update_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        update_json(base_headers, headers)
    try:
        response = requests.get(url=f"{API_URL}/_apis/projects", headers=base_headers, params=base_parameters)
        if response.status_code == 200:
            for project in json.loads(response.text)['value']:
                if name in project['name']:
                    json_response={
                        "function_code":200,
                        "projectId": f"{project['id']}",
                        "message":f"Obtaining correct projects"
                    }
                    break
                else:
                    json_response={
                        "function_code": 204,
                        "projectId": 0,
                        "message":f"##[error] Project not found, verify project name"
                    }
        else:
            json_response={
                "function_code":f"{response.status_code}",
                "projectId": "0",
                "message":f"{response.text}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"##[error] Error when obtaining projects: \n {e.strerror}")
        sys.exit(1)

def get_teams_by_projectId(API_URL: str, TOKEN: str, project_id: str, team_name: str, headers: object = None, params: object = None) -> object:
    """
    Retrieves information about a specific team in a project by its name.

    Args:
        API_URL (str): Base URL of the API for retrieving team information.
        TOKEN (str): Authorization token for API access.
        project_id (str): ID of the project.
        team_name (str): Name of the team to retrieve.
        headers (dict): Additional headers for retrieving team information.
        params (dict): Additional parameters for retrieving team information.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and team ID.
        Response dictionary format:
        
        - In case of success:
            {
                "function_code": <value>,
                "message": <success_message>,
                "teamId": <Team ID>
            }

        - In case of failure:
            {
                "function_code": <value>,
                "message": <error_message>,
                "teamId": <Team ID>
            }
    """

    base_headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encode_token(TOKEN)}'
    }
    if params is not None and isinstance(params, dict):
        update_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        update_json(base_headers, headers)
    try:
        response = requests.get(url=f"{API_URL}/_apis/projects/{project_id}/teams", headers=base_headers, params=base_parameters)
        if response.status_code == 200:
            for team in json.loads(response.text)['value']:
                if team_name in team['name']:
                    json_response={
                        "function_code":200,
                        "teamId": f"{team['id']}",
                        "message":f"Obtaining the correct equipment"
                    }
                    break
                else:
                    json_response={
                        "function_code": 204,
                        "teamId": 0,
                        "message":f"##[error] Team not found, check team or project name"
                    }
        else:
            json_response={
                "function_code":f"{response.status_code}",
                "teamId": "0",
                "message":f"{response.text}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"##[error] Error obtaining teams: \n {e.strerror}")
        sys.exit(1)

def get_reviewer_id_by_team_id(API_URL: str, TOKEN: str, project_id: str, team_id: str, user_email: str, headers: object = None, params: object = None) -> object:
    """
    Retrieves the reviewer ID by team ID and user email.

    Args:
        API_URL (str): Base URL of the API for retrieving reviewer information.
        TOKEN (str): Authorization token for API access.
        project_id (str): ID of the project.
        team_id (str): ID of the team.
        user_email (str): Email of the user whose reviewer ID is needed.
        headers (dict): Additional headers for retrieving reviewer information.
        params (dict): Additional parameters for retrieving reviewer information.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and reviewer ID.
        Response dictionary format:
        
        - In case of success:
            {
                "function_code": <value>,
                "message": <success_message>,
                "reviwerId": <Reviwer_ID>
            }

        - In case of failure:
            {
                "function_code": <value>,
                "message": <error_message>,
                "reviwerId": <Reviwer_ID>
            }
    """

    base_headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encode_token(TOKEN)}'
    }
    if params is not None and isinstance(params, dict):
        update_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        update_json(base_headers, headers)
    try:
        response = requests.get(url=f"{API_URL}/_apis/projects/{project_id}/teams/{team_id}/members", headers=base_headers, params=base_parameters)
        if response.status_code == 200:
            for user in json.loads(response.text)['value']:
                if user['identity']['uniqueName'] == user_email:
                    json_response={
                        "function_code":200,
                        "reviwerId": f"{user['identity']['id']}",
                        "message":f"Reviewer ID successfully obtained"
                    }
                    break
                else:
                    json_response={
                        "function_code": 204,
                        "reviwerId": 0,
                        "message":f"##[error] User not found, verify the email, the team, the project or that the user belongs to the team."
                    }
            
        else:
            json_response={
                "function_code": response.status_code,
                "reviwerId": 0,
                "message":f"##[error] User not found, verify the email, the team, the project or that the user belongs to the team."
            }
        return json_response
    except requests.RequestException as e:
        print(f"##[error] Error obtaining reviwer id: \n {e.strerror}")
        sys.exit(1)

def get_repo_id(API_URL: str, PROJECT: str, TOKEN: str, repo_name: str, headers: object = None, params: object = None) -> object:
    """
    Retrieves the reviewer ID by team ID and user email.

    Args:
        API_URL (str): Base URL of the API for retrieving reviewer information.
        PROJECT (str): Name of the project to retrieve.
        TOKEN (str): Authorization token for API access.
        repo_name (str): Repo name to obtain.
        headers (dict): Additional headers for retrieving reviewer information.
        params (dict): Additional parameters for retrieving reviewer information.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and repo ID.
        Response dictionary format:
        
        - In case of success:
            {
                "function_code": <value>,
                "message": <success_message>,
                "repoId": <Reviwer Id>
            }

        - In case of failure:
            {
                "function_code": <value>,
                "message": <error_message>,
                "repoId": <Reviwer Id>
            }
    """

    base_headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encode_token(TOKEN)}'
    }
    if params is not None and isinstance(params, dict):
        update_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        update_json(base_headers, headers)
    try:
        response = requests.get(url=f"{API_URL}/{quote(PROJECT)}/_apis/git/repositories", headers=base_headers, params=base_parameters)
        if response.status_code == 200:
            for repos in json.loads(response.text)['value']:
                if repos['name'] == repo_name:
                    json_response={
                        "function_code":200,
                        "repoId": f"{repos['id']}",
                        "message":f"Repository ID obtained correctly"
                    }
                    break
        else:
            json_response={
                "function_code":f"{response.status_code}",
                "repoId": "0",
                "message":f"{response.text}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"##[error] Error obtaining repo id: \n {e.strerror}")
        sys.exit(1)

def list_policies_type(API_URL: str, PROJECT: str, TOKEN: str, headers: object = None, params: object = None) -> object:
    """
    Retrieves the list of policies Types of the project selected.

    Args:
        API_URL (str): Base URL of the API for retrieving reviewer information.
        PROJECT (str): Name of the project to retrieve.
        TOKEN (str): Authorization token for API access.
        headers (dict): Additional headers for retrieving policies type information.
        params (dict): Additional parameters for retrieving policies type information.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and policies type list.
        Response dictionary format:
        
        - In case of success:
            {
                "function_code": <value>,
                "message": <success_message>,
                "policie_types": {
                    "id": <Id of the type of policy>,
                    "name": <Name of policy type>
                }
            }

        - In case of failure:
            {
                "function_code": <value>,
                "message": <error_message>
            }
    """

    base_headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encode_token(TOKEN)}'
    }
    if params is not None and isinstance(params, dict):
        update_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        update_json(base_headers, headers)
    try:
        response = requests.get(url=f"{API_URL}/{quote(PROJECT)}/_apis/policy/types", headers=base_headers, params=base_parameters)
        if response.status_code == 200:
            json_response={
                        "function_code":200,
                        "message": "Types correctly obtained",
                        "policies": []
                }
            for policie_type in json.loads(response.text)['value']:
                json_response['policies'].append({
                    "id": policie_type['id'],
                    "name": policie_type['displayName']
                })
        else:
            json_response={
                "function_code":f"{response.status_code}",
                "message":f"{response.text}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"##[error] Error obtaining policy types: \n {e.strerror}")
        sys.exit(1)

def list_pipelines(API_URL: str, PROJECT: str, TOKEN: str, headers: object = None, params: object = None) -> object:
    """
    Retrieves the list of pipelines of the project selected.

    Args:
        API_URL (str): Base URL of the API for retrieving reviewer information.
        PROJECT (str): Name of the project to retrieve.
        TOKEN (str): Authorization token for API access.
        headers (dict): Additional headers for retrieving pipelines information.
        params (dict): Additional parameters for retrieving pipelines information.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and pipeline list ID.
        Response dictionary format:
        
        - In case of success:
            {
                "function_code": <value>,
                "pipelines": {
                    "id": <Id>,
                    "name": <Pipeline Name>
                }
            }

        - In case of failure:
            {
                "function_code": <value>,
                "message": <error_message>
            }
    """

    base_headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encode_token(TOKEN)}'
    }
    if params is not None and isinstance(params, dict):
        update_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        update_json(base_headers, headers)
    try:
        response = requests.get(url=f"{API_URL}/{quote(PROJECT)}/_apis/pipelines", headers=base_headers, params=base_parameters)
        if response.status_code == 200:
            json_response={
                        "function_code":200,
                        "message": "Correctly obtained pipelines",
                        "pipelines": []
            }
            for pipeline_list in json.loads(response.text)['value']:
                json_response['pipelines'].append({
                    "id": pipeline_list['id'],
                    "name": pipeline_list['name']
                })
        else:
            json_response={
                "pipelines": [],
                "function_code":f"{response.status_code}",
                "message":f"{response.text}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"##[error] Error obtaining the pipeline list: \n {e.strerror}")
        sys.exit(1)

def find_pipeline_by_name(API_URL: str, PROJECT: str, TOKEN: str, PIPELINE_NAME: str, headers: object = None, params: object = None) -> object:
    """
    Retrieves the pipeline filtered by name.

    Args:
        API_URL (str): Base URL of the API for retrieving reviewer information.
        PROJECT (str): Name of the project to retrieve.
        TOKEN (str): Authorization token for API access.
        PIPELINE_NAME (str): Name of the pipeline to retrieve.
        headers (dict): Additional headers for retrieving pipeline information.
        params (dict): Additional parameters for retrieving pipeline information.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and pipeline.
        Response dictionary format:
        
        - In case of success:
            {
                "function_code": <value>,
                "pipelines": {
                    "id": <Id>,
                    "name": <Name>
                }
            }

        - In case of failure:
            {
                "function_code": <value>,
                "message": <error_message>
            }
    """

    base_headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encode_token(TOKEN)}'
    }
    if params is not None and isinstance(params, dict):
        update_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        update_json(base_headers, headers)
    try:
        response = list_pipelines(API_URL=API_URL, PROJECT=PROJECT, TOKEN=TOKEN, headers=None, params=None)
        for pipeline in response['pipelines']:
            if pipeline['name'] == PIPELINE_NAME:
                json_response={
                    "function_code":200,
                    "pipeline": {
                        "id": pipeline['id'],
                        "name": pipeline['name']
                    }
                }
                break
            else:
                json_response={
                    "function_code":404,
                    "message":f"##[error] Pipeline not found: {PIPELINE_NAME}"
                }
        return json_response
    except requests.RequestException as e:
        print(f"##[error] Error obtaining the pipeline: \n {e.strerror}")
        sys.exit(1)

def list_pipelines_runs(API_URL: str, PROJECT: str, TOKEN: str, PIPELINE_ID: int, headers: object = None, params: object = None) -> object:
    """
    Retrieves the list of pipelines of the project selected.

    Args:
        API_URL (str): Base URL of the API for retrieving reviewer information.
        PROJECT (str): Name of the project to retrieve.
        TOKEN (str): Authorization token for API access.
        PIPELINE_ID (int): Id of the pipeline to retrieve.
        headers (dict): Additional headers for retrieving pipelines information.
        params (dict): Additional parameters for retrieving pipelines information.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and pipeline runs list.
        Response dictionary format:
        
        - In case of success:
            {
                "function_code": <value>,
                "pipelines_runs": {
                    "id": <Id>,
                    "build_name": <Build name>,
                    "status": <Build status>,
                    "result": <Build result>,
                    "variables": <Build Variables>
                }
            }

        - In case of failure:
            {
                "function_code": <value>,
                "message": <error_message>
            }
    """

    base_headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encode_token(TOKEN)}'
    }
    if params is not None and isinstance(params, dict):
        update_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        update_json(base_headers, headers)
    try:
        response = requests.get(url=f"{API_URL}/{quote(PROJECT)}/_apis/pipelines/{PIPELINE_ID}/runs", headers=base_headers, params=base_parameters)
        if response.status_code == 200:
            json_response={
                        "function_code":200,
                        "message": "Correctly obtained runs",
                        "pipelines_runs": []
            }
            for pipeline_run in json.loads(response.text)['value']:
                json_response['pipelines_runs'].append({
                    "id": pipeline_run['id'],
                    "build_name": pipeline_run['name'],
                    "state": pipeline_run['state'],
                    "result": pipeline_run['result'] if pipeline_run['state'] != "inProgress" else None,
                    "variables": pipeline_run['variables'] if "variables" in pipeline_run.keys() else None
                })
        else:
            json_response={
                "function_code":f"{response.status_code}",
                "message":f"{response.text}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"##[error] Error obtaining pipeline runs list: \n {e.strerror}")
        sys.exit(1)

def get_build_status_by_build_id(API_URL: str, PROJECT: str, TOKEN: str, BUILD_NAME: str, PIPELINE_NAME: str = None, headers: object = None, params: object = None) -> object:
    """
    Retrieves the status of a pipeline run.

    Args:
        API_URL (str): Base URL of the API for retrieving reviewer information.
        PROJECT (str): Name of the project to retrieve.
        TOKEN (str): Authorization token for API access.
        BUILD_NAME (str): Name of the build to retrieve.
        PIPELINE_NAME (str): Name of the pipeline to retrieve.
        headers (dict): Additional headers for retrieving build status.
        params (dict): Additional parameters for retrieving build status.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and status of build.
        Response dictionary format:
        
        - In case of success:
            {
                "function_code": 200,
                "build": {
                    "id": <Id>,
                    "build_name": <Build name>,
                    "state": <Build status>,
                    "result": <Build result>
                }
            }

        - In case of failure:
            {
                "function_code": 400,
                "message": <error_message>
            }
    """

    base_headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encode_token(TOKEN)}'
    }
    if params is not None and isinstance(params, dict):
        update_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        update_json(base_headers, headers)
    try:
        if PIPELINE_NAME is None:
            pipelines_response = list_pipelines(API_URL=API_URL, PROJECT=PROJECT, TOKEN=TOKEN, headers=None, params=None)
            list_pipelines_runs_response={
                "pipeline_runs":[]
            }
            for pipeline in pipelines_response['pipelines']:
                list_pipelines_runs_by_pipeline_id_response = list_pipelines_runs(API_URL=API_URL, PROJECT=PROJECT, TOKEN=TOKEN, PIPELINE_ID=pipeline['id'], headers=None, params=None)
                for pipeline_run in list_pipelines_runs_by_pipeline_id_response['pipelines_runs']:
                    list_pipelines_runs_response['pipeline_runs'].append(pipeline_run)
        else:
            pipelines_response = find_pipeline_by_name(API_URL=API_URL, PROJECT=PROJECT, TOKEN=TOKEN, PIPELINE_NAME=PIPELINE_NAME, headers=None, params=None)
            list_pipelines_runs_response = list_pipelines_runs(API_URL=API_URL, PROJECT=PROJECT, TOKEN=TOKEN, PIPELINE_ID=pipelines_response['pipeline']['id'], headers=None, params=None)

        for pipeline_run in list_pipelines_runs_response['pipeline_runs']:
            if pipeline_run['build_name'] == BUILD_NAME:
                json_response={
                    "function_code":200,
                    "build": {
                        "id": pipeline_run['id'],
                        "build_name": pipeline_run['build_name'],
                        "state": pipeline_run['state'],
                        "result": pipeline_run['result']
                    }
                }
                find=True
                break
            else:
                find=False
        if find==False:
            json_response={
                "function_code":404,
                "message":f"##[error] Build not found: {BUILD_NAME}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"##[error] Error obtaining status of the build: \n {e.strerror}")
        sys.exit(1)

def get_build_status_by_source_branch(API_URL: str, PROJECT: str, TOKEN: str, SOURCE_BRANCH: str, PIPELINE_NAME: str = None, headers: object = None, params: object = None) -> object:
    """
    Retrieves the status of a pipeline run.

    Args:
        API_URL (str): Base URL of the API for retrieving reviewer information.
        PROJECT (str): Name of the project to retrieve.
        TOKEN (str): Authorization token for API access.
        SOURCE_BRANCH (str): Name of the source branch to retrieve.
        PIPELINE_NAME (str): Name of the pipeline to retrieve.
        headers (dict): Additional headers for retrieving build status.
        params (dict): Additional parameters for retrieving build status.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and status of build.
        Response dictionary format:
        
        - In case of success:
            {
                "function_code": 200,
                "build": {
                    "id": <Id>,
                    "build_name": <Build name>,
                    "state": <Build status>,
                    "result": <Build result>
                }
            }

        - In case of failure:
            {
                "function_code": 400,
                "message": <error_message>
            }
    """

    base_headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encode_token(TOKEN)}'
    }
    if params is not None and isinstance(params, dict):
        update_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        update_json(base_headers, headers)
    try:
        if PIPELINE_NAME is not None:
            pipelines_response = find_pipeline_by_name(API_URL=API_URL, PROJECT=PROJECT, TOKEN=TOKEN, PIPELINE_NAME=PIPELINE_NAME, headers=None, params=None)
            list_pipelines_runs_response = list_pipelines_runs(API_URL=API_URL, PROJECT=PROJECT, TOKEN=TOKEN, PIPELINE_ID=pipelines_response['pipeline']['id'], headers=None, params=None)
        else:
            pipelines_response = list_pipelines(API_URL=API_URL, PROJECT=PROJECT, TOKEN=TOKEN, headers=None, params=None)
            list_pipelines_runs_response={
                "pipeline_runs":[]
            }
            if pipelines_response['function_code'] == 200:
                for pipeline in pipelines_response['pipelines']:
                    list_pipelines_runs_by_pipeline_id_response = list_pipelines_runs(API_URL=API_URL, PROJECT=PROJECT, TOKEN=TOKEN, PIPELINE_ID=pipeline['id'], headers=None, params=None)
                    for pipeline_run in list_pipelines_runs_by_pipeline_id_response['pipelines_runs']:
                        list_pipelines_runs_response['pipeline_runs'].append(pipeline_run)
            else:
                json_response={
                    "function_code":404,
                    "message":f"##[error] Pipeline not found: {PIPELINE_NAME}, {pipelines_response['message']}"
                }
                return json_response

        for pipeline_run in list_pipelines_runs_response['pipeline_runs']:
            if pipeline_run['variables'] is not None:
                if "system.pullRequest.sourceBranch" in pipeline_run['variables'].keys():
                    if pipeline_run['variables']['system.pullRequest.sourceBranch']['value'].split('/')[2] == SOURCE_BRANCH:
                        json_response={
                            "function_code":200,
                            "build": {
                                "id": pipeline_run['id'],
                                "build_name": pipeline_run['build_name'],
                                "state": pipeline_run['state'],
                                "result": pipeline_run['result']
                            }
                        }
                        find=True
                        break
                    else:
                        find=False
        if find==False:
            json_response={
                "function_code":404,
                "message":f"##[error] Build not found by branch filter: {SOURCE_BRANCH}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"##[error] Error obtaining status of the build: \n {e.strerror}")
        sys.exit(1)

def get_branches_from_repo(API_URL: str, PROJECT: str, TOKEN: str, repo_name: str, headers: object = None, data: object = None, params: object = None):
    """
    Retrieves the status of a pipeline run.

    Args:
        API_URL (str): Base URL of the API for retrieving reviewer information.
        PROJECT (str): Name of the project to retrieve.
        TOKEN (str): Authorization token for API access.
        repo_name (str): Name of the repository to retrieve branches from.
        headers (dict): Additional headers for retrieving build status.
        data (dict): Additional data for retrieving build status.
        params (dict): Additional parameters for retrieving build status.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and status of build.
        Response dictionary format:
        
        - In case of success:
            {
                "function_code": 200,
                "build": {
                    "id": <Id>,
                    "build_name": <Build name>,
                    "state": <Build status>,
                    "result": <Build result>
                }
            }

        - In case of failure:
            {
                "function_code": 400,
                "message": <error_message>
            }
    """

    base_headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encode_token(TOKEN)}'
    }
    if params is not None and isinstance(params, dict):
        update_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        update_json(base_headers, headers)
    try:
        repositoryId = get_repo_id(API_URL=API_URL, PROJECT=PROJECT, TOKEN=TOKEN, repo_name=repo_name, headers=None, params=None)
        if repositoryId['function_code'] == 200:
            response = requests.get(url=f"{API_URL}/{quote(PROJECT)}/_apis/git/repositories/{repositoryId['repoId']}/refs", headers=base_headers, params=base_parameters)
            if response.status_code == 200:
                json_response={
                            "function_code": 200,
                            "message": "Correctly obtained branches",
                            "branches": []
                }
                for branch in json.loads(response.text)['value']:
                    json_response['branches'].append({
                        "name": branch['name'],
                    })
            else:
                json_response={
                    "function_code":f"{response.status_code}",
                    "message":f"##[error] Error obtaining branches from the repo, message: {response.text}"
                }
        else:
            json_response={
                "function_code":f"{repositoryId['function_code']}",
                "message":f"##[error] Error obtaining repo id, message: {repositoryId['message']}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"##[error] Error obtaining the branches: \n {e.strerror}")
        sys.exit(1)

import requests, sys, json, base64
from urllib.parse import quote

base_parameters={
    "api-version":"7.1"
}

def encode_token(TOKEN: str) -> str:
    credenciales = f"Basic:{TOKEN}"
    credenciales_base64 = base64.b64encode(credenciales.encode()).decode('utf-8')
    return credenciales_base64

def actualizar_json(base, actualizacion):
    for k, v in actualizacion.items():
        base[k] = actualizar_json(base.get(k, {}), v) if isinstance(v, dict) else v
    return base

def create_pr(API_URL: str, PROJECT: str, TOKEN: str, REPO_ID: str, sourceRefName: str, targetRefName: str, pr_title: str, headers: object = None, data: object = None, params: object = None) -> object:
    """
    Creates a Pull Request (PR) in a specified repository.

    Args:
        API_URL (str): Base URL of the API for creating PRs.
        PROJECT (str): Name of the project where the PR will be created.
        TOKEN (str): Authorization token for API access.
        REPO_ID (str): The ID of the repository where the PR will be created.
        data (dict): Additional data for creating the PR.
        headers (dict): Additional headers for creating the PR.
        params (dict): Additional parameters for creating the PR.
        sourceRefName (str): Name of the source branch for the PR.
        targetRefName (str): Name of the target branch for the PR.
        pr_title (str): Title of the Pull Request.

    Returns:
        object: Dictionary with information about the success or failure of the PR creation, including function code and PR details.
        Formato del diccionario de respuesta:
        
        - En caso de éxito:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>,
                "lastMergeSourceCommit": <último_commit_de_la_fusión>,
                "pullRequestId": <ID_del_PR>
            }

        - En caso de fallo:
            {
                "function_code": <valor>,
                "message": <mensaje_de_error>
            }
    """

    body={
        "sourceRefName": f"refs/heads/{sourceRefName}",
        "targetRefName": f"refs/heads/{targetRefName}",
        "title": f"{pr_title} {sourceRefName} to {targetRefName}",
        "description": "Creado de PR de forma automática con pipeline Aling Branch",
    }
    base_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        "Authorization": f"Basic {encode_token(TOKEN)}"
    }
    if params is not None and isinstance(params, dict):
        actualizar_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        actualizar_json(base_headers, headers)
    if data is not None and isinstance(data, dict):
        actualizar_json(body, data)
    try:
        json_response = requests.post(url=f"{API_URL}/{quote(PROJECT)}/_apis/git/repositories/{REPO_ID}/pullrequests",  data=json.dumps(body), headers=base_headers, params=base_parameters)
        if json_response.status_code == 201:
            response = json.loads(json_response.text)
            if response['status'] == "active":
                def_response={
                    "function_code":200,
                    "message": "PR Creada correctamente",
                    "lastMergeSourceCommit": {
                        "commitId": f"{response['lastMergeSourceCommit']['commitId']}",
                        "url": f"{response['lastMergeSourceCommit']['url']}"
                    },
                    "pullRequestId": f"{response['pullRequestId']}"
                }
            else:
                def_response={
                    "function_code":f"{json_response.status_code}",
                    "message":f"PR Creada pero no activa"
                }
        else:
            def_response={
                "function_code":f"{json_response.status_code}",
                "message":f"{json_response.text}"
            }            
        return def_response
    except requests.RequestException as e: 
        print(f"Error al crear la pr \n {e.strerror}")
        print(f"Mensaje de error completo: \n {e}")
        sys.exit(1)

def get_pr_data(API_URL: str, TOKEN: str, REPO_ID: str, sourceRefName: str, targetRefName: str, headers: object = None, params: object = None) -> object:
    """
    Retrieves data about a specific Pull Request (PR) based on branch information.

    Args:
        API_URL (str): Base URL of the API for retrieving PR data.
        TOKEN (str): Authorization token for API access.
        REPO_ID (str): The ID of the repository to search for the PR.
        params (dict): Additional parameters for retrieving PR data.
        sourceBranch (str): Name of the source branch for the PR.
        targetBranch (str): Name of the target branch for the PR.

    Returns:
        object: Dictionary with information about the PR, including function code and response data.
        Formato del diccionario de respuesta:
        
        - En caso de éxito:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>
            }

        - En caso de fallo:
            {
                "function_code": <valor>,
                "message": <mensaje_de_error>
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
        actualizar_json(base_parameters, parameters_get_prs)
        actualizar_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        actualizar_json(base_headers, headers)
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
        print(f"Error al obtener datos de la PR: \n {e.strerror}")
        sys.exit(1)

def add_reviwer(API_URL: str, PROJECT: str, TOKEN: str, REPO_ID: str, pullRequestId: str, reviewerId: str, headers: object = None, data: object = None, params: object = None) -> object:
    """
    Adds a required reviewer to a Pull Request.

    Args:
        API_URL (str): Base URL of the API for adding a reviewer.
        TOKEN (str): Authorization token for API access.
        REPO_ID (str): The ID of the repository where the PR is located.
        params (dict): Additional parameters for adding the reviewer.
        pullRequestId (str): ID of the Pull Request.
        reviewerId (str): ID of the reviewer to be added.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and a message.
        Formato del diccionario de respuesta:
        
        - En caso de éxito:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>
            }

        - En caso de fallo:
            {
                "function_code": <valor>,
                "message": <mensaje_de_error>
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
        actualizar_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        actualizar_json(base_headers, headers)
    if data is not None and isinstance(data, dict):
        actualizar_json(body, data)
    try:
        response = requests.put(url=f"{API_URL}/{quote(PROJECT)}/_apis/git/repositories/{REPO_ID}/pullrequests/{pullRequestId}/reviewers/{reviewerId}", headers=base_headers, params=base_parameters, data=json.dumps(body))
        if response.status_code == 200:
            response = json.loads(response.text)
            json_response={
                "function_code":200,
                "message":f"Revisor {response['displayName']} agregado correctamente a la PR {pullRequestId}."
            }
        else:
            json_response={
                "function_code":f"{response.status_code}",
                "message":f"{response.text}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"Error al añadir un reviwer: \n {e.strerror}")
        sys.exit(1)

def approve_pr(API_URL: str, PROJECT: str, TOKEN: str, REPO_ID: str, pullRequestId: str, reviewerId: str, headers: object = None, data: object = None, params: object = None) -> object:
    """
    Approves a Pull Request as a reviewer.

    Args:
        API_URL (str): Base URL of the API for approving a PR.
        TOKEN (str): Authorization token for API access.
        REPO_ID (str): The ID of the repository where the PR is located.
        params (dict): Additional parameters for approving the PR.
        pullRequestId (str): ID of the Pull Request to be approved.
        reviewerId (str): ID of the reviewer approving the PR.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and a message.
        Formato del diccionario de respuesta:
        
        - En caso de éxito:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>
            }

        - En caso de fallo:
            {
                "function_code": <valor>,
                "message": <mensaje_de_error>
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
        actualizar_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        actualizar_json(base_headers, headers)
    if data is not None and isinstance(data, dict):
        actualizar_json(body, data)
    try:
        response = requests.put(url=f"{API_URL}/{quote(PROJECT)}/_apis/git/repositories/{REPO_ID}/pullrequests/{pullRequestId}/reviewers/{reviewerId}", headers=base_headers, data=json.dumps(body), params=base_parameters)
        if response.status_code == 200:
            json_response={
                "function_code":200,
                "message":f"Revisor {json.loads(response.text)['displayName']} ha aprobado la PR {pullRequestId}."
            }
        else:
            json_response={
                "function_code":f"{response.status_code}",
                "message":f"{response}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"Error al aprobar la pr: \n {e.strerror}")
        sys.exit(1)

def complete_pr(API_URL: str, PROJECT: str, TOKEN: str, REPO_ID: str, pullRequestId: str, commitData: str, headers: object = None, data: object = None, params: object = None) -> object:
    """
    Completes (merges) a Pull Request.

    Args:
        API_URL (str): Base URL of the API for completing a PR.
        TOKEN (str): Authorization token for API access.
        REPO_ID (str): The ID of the repository where the PR is located.
        params (dict): Additional parameters for completing the PR.
        pullRequestId (str): ID of the Pull Request to be completed.
        commitData (dict): Data about the commit to be merged, including 'commitId' and 'url'.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and a message.
        Formato del diccionario de respuesta:
        
        - En caso de éxito:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>
            }

        - En caso de fallo:
            {
                "function_code": <valor>,
                "message": <mensaje_de_error>
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
            "mergeCommitMessage": "[skip ci] PR completada automáticamente",
            "squashMerge": False
        }
    }
    base_headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {encode_token(TOKEN)}"
    }
    if params is not None and isinstance(params, dict):
        actualizar_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        actualizar_json(base_headers, headers)
    if data is not None and isinstance(data, dict):
        actualizar_json(body, data)
    try:
        response = requests.patch(url=f"{API_URL}/{quote(PROJECT)}/_apis/git/repositories/{REPO_ID}/pullrequests/{pullRequestId}", headers=base_headers, data=json.dumps(body), params=base_parameters)
        if response.status_code == 200:

            json_response={
                "function_code":200,
                "message":f"PR {pullRequestId} completada y mergeada correctamente."
            }
        else:
            json_response={
                "function_code":f"{response.status_code}",
                "message":f"{response.text}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"Error al completar la pr: \n {e.strerror}")
        sys.exit(1)

def get_project(API_URL: str, TOKEN: str, name: str, headers: object = None, params: object = None) -> object:
    """
    Retrieves information about a project by its name.

    Args:
        API_URL (str): Base URL of the API for retrieving project information.
        TOKEN (str): Authorization token for API access.
        name (str): Name of the project to retrieve.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and project ID.
        Formato del diccionario de respuesta:
        
        - En caso de éxito:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>,
                "projectId": <Id del proyecto>
            }

        - En caso de fallo:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>,
                "projectId": <Id del proyecto>
            }
    """

    base_headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encode_token(TOKEN)}'
    }
    if params is not None and isinstance(params, dict):
        actualizar_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        actualizar_json(base_headers, headers)
    try:
        response = requests.get(url=f"{API_URL}/_apis/projects", headers=base_headers, params=base_parameters)
        if response.status_code == 200:
            for project in json.loads(response.text)['value']:
                if name in project['name']:
                    json_response={
                        "function_code":200,
                        "projectId": f"{project['id']}",
                        "message":f"Obtencion de projectos correcto"
                    }
                    break
                else:
                    json_response={
                        "function_code": 204,
                        "projectId": 0,
                        "message":f"Proyecto no encontrado, verifique el nombre del proyecto"
                    }
        else:
            json_response={
                "function_code":f"{response.status_code}",
                "projectId": "0",
                "message":f"{response.text}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"Error al obtener los proyectos: \n {e.strerror}")
        sys.exit(1)

def get_teams_by_projectId(API_URL: str, TOKEN: str, project_id: str, team_name: str, headers: object = None, params: object = None) -> object:
    """
    Retrieves information about a specific team in a project by its name.

    Args:
        API_URL (str): Base URL of the API for retrieving team information.
        TOKEN (str): Authorization token for API access.
        project_id (str): ID of the project.
        team_name (str): Name of the team to retrieve.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and team ID.
        Formato del diccionario de respuesta:
        
        - En caso de éxito:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>,
                "teamId": <Id del team>
            }

        - En caso de fallo:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>,
                "teamId": <Id del team>
            }
    """

    base_headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encode_token(TOKEN)}'
    }
    if params is not None and isinstance(params, dict):
        actualizar_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        actualizar_json(base_headers, headers)
    try:
        response = requests.get(url=f"{API_URL}/_apis/projects/{project_id}/teams", headers=base_headers, params=base_parameters)
        if response.status_code == 200:
            for team in json.loads(response.text)['value']:
                if team_name in team['name']:
                    json_response={
                        "function_code":200,
                        "teamId": f"{team['id']}",
                        "message":f"Obtencion de equipos correcto"
                    }
                    break
                else:
                    json_response={
                        "function_code": 204,
                        "teamId": 0,
                        "message":f"Equipo no encontrado, verifique el nombre del equipo o el proyecto"
                    }
        else:
            json_response={
                "function_code":f"{response.status_code}",
                "teamId": "0",
                "message":f"{response.text}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"Error al obtener los equipos: \n {e.strerror}")
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

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and reviewer ID.
        Formato del diccionario de respuesta:
        
        - En caso de éxito:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>,
                "reviwerId": <Id del reviwer>
            }

        - En caso de fallo:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>,
                "reviwerId": <Id del reviwer>
            }
    """

    base_headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encode_token(TOKEN)}'
    }
    if params is not None and isinstance(params, dict):
        actualizar_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        actualizar_json(base_headers, headers)
    try:
        response = requests.get(url=f"{API_URL}/_apis/projects/{project_id}/teams/{team_id}/members", headers=base_headers, params=base_parameters)
        if response.status_code == 200:
            for user in json.loads(response.text)['value']:
                if user['identity']['uniqueName'] == user_email:
                    json_response={
                        "function_code":200,
                        "reviwerId": f"{user['identity']['id']}",
                        "message":f"Obtencion de Id de usuario correcto"
                    }
                    break
                else:
                    json_response={
                        "function_code": 204,
                        "reviwerId": 0,
                        "message":f"Usuario no encontrado, verifique el email, el equipo, el proyecto o que el usuario pertenezca al equipo"
                    }
            
        else:
            json_response={
                "function_code": response.status_code,
                "reviwerId": 0,
                "message":f"Usuario no encontrado, verifique el email, el equipo, el proyecto o que el usuario pertenezca al equipo"
            }
        return json_response
    except requests.RequestException as e:
        print(f"Error al obtener los miembros del equipo: \n {e.strerror}")
        sys.exit(1)

def get_repo_id(API_URL: str, PROJECT: str, TOKEN: str, repo_name: str, headers: object = None, params: object = None) -> object:
    """
    Retrieves the reviewer ID by team ID and user email.

    Args:
        API_URL (str): Base URL of the API for retrieving reviewer information.
        TOKEN (str): Authorization token for API access.
        repo_name (str): Repo name to obtain.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and repo ID.
        Formato del diccionario de respuesta:
        
        - En caso de éxito:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>,
                "repoId": <Id del reviwer>
            }

        - En caso de fallo:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>,
                "repoId": <Id del reviwer>
            }
    """

    base_headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encode_token(TOKEN)}'
    }
    if params is not None and isinstance(params, dict):
        actualizar_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        actualizar_json(base_headers, headers)
    try:
        response = requests.get(url=f"{API_URL}/{quote(PROJECT)}/_apis/git/repositories", headers=base_headers, params=base_parameters)
        if response.status_code == 200:
            for repos in json.loads(response.text)['value']:
                if repos['name'] == repo_name:
                    json_response={
                        "function_code":200,
                        "repoId": f"{repos['id']}",
                        "message":f"Obtencion de Id de repositorio correcto"
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
        print(f"Error al obtener los miembros del equipo: \n {e.strerror}")
        sys.exit(1)

def list_policies_type(API_URL: str, PROJECT: str, TOKEN: str, headers: object = None, params: object = None) -> object:
    """
    Retrieves the list of policies Types of the project selected.

    Args:
        API_URL (str): Base URL of the API for retrieving reviewer information.
        TOKEN (str): Authorization token for API access.
        PROJECT (str): Name of the project to retrieve.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and policies type list.
        Formato del diccionario de respuesta:
        
        - En caso de éxito:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>,
                "policie_types": {
                    "id": <Id del tipo de politica>,
                    "name": <Nombre del tipo de politica>
                }
            }

        - En caso de fallo:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>
            }
    """

    base_headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encode_token(TOKEN)}'
    }
    if params is not None and isinstance(params, dict):
        actualizar_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        actualizar_json(base_headers, headers)
    try:
        response = requests.get(url=f"{API_URL}/{quote(PROJECT)}/_apis/policy/types", headers=base_headers, params=base_parameters)
        if response.status_code == 200:
            json_response={
                        "function_code":200,
                        "message": "Obtencion de tipos correcto",
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
        print(f"Error al obtener los tipos de politica: \n {e.strerror}")
        sys.exit(1)

def list_pipelines(API_URL: str, PROJECT: str, TOKEN: str, headers: object = None, params: object = None) -> object:
    """
    Retrieves the list of pipelines of the project selected.

    Args:
        API_URL (str): Base URL of the API for retrieving reviewer information.
        TOKEN (str): Authorization token for API access.
        PROJECT (str): Name of the project to retrieve.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and pipeline list ID.
        Formato del diccionario de respuesta:
        
        - En caso de éxito:
            {
                "function_code": <valor>,
                "pipelines": {
                    "id": <Id>,
                    "name": <Nombre>
                }
            }

        - En caso de fallo:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>
            }
    """

    base_headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encode_token(TOKEN)}'
    }
    if params is not None and isinstance(params, dict):
        actualizar_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        actualizar_json(base_headers, headers)
    try:
        response = requests.get(url=f"{API_URL}/{quote(PROJECT)}/_apis/pipelines", headers=base_headers, params=base_parameters)
        if response.status_code == 200:
            json_response={
                        "function_code":200,
                        "message": "Obtencion de pipelines correcto",
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
        print(f"Error al obtener la lista de pipelines: \n {e.strerror}")
        sys.exit(1)

def find_pipeline_by_name(API_URL: str, PROJECT: str, TOKEN: str, PIPELINE_NAME: str, headers: object = None, params: object = None) -> object:
    """
    Retrieves the pipeline filtered by name.

    Args:
        API_URL (str): Base URL of the API for retrieving reviewer information.
        TOKEN (str): Authorization token for API access.
        PROJECT (str): Name of the project to retrieve.
        PIPELINE_NAME (str): Name of the pipeline to retrieve.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and pipeline.
        Formato del diccionario de respuesta:
        
        - En caso de éxito:
            {
                "function_code": <valor>,
                "pipelines": {
                    "id": <Id>,
                    "name": <Nombre>
                }
            }

        - En caso de fallo:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>
            }
    """

    base_headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encode_token(TOKEN)}'
    }
    if params is not None and isinstance(params, dict):
        actualizar_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        actualizar_json(base_headers, headers)
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
                    "message":f"Pipeline no encontrado: {PIPELINE_NAME}"
                }
        return json_response
    except requests.RequestException as e:
        print(f"Error al obtener la lista de pipelines: \n {e.strerror}")
        sys.exit(1)

def list_pipelines_runs(API_URL: str, PROJECT: str, TOKEN: str, PIPELINE_ID: int, headers: object = None, params: object = None) -> object:
    """
    Retrieves the list of pipelines of the project selected.

    Args:
        API_URL (str): Base URL of the API for retrieving reviewer information.
        TOKEN (str): Authorization token for API access.
        PROJECT (str): Name of the project to retrieve.
        PIPELINE_ID (int): Id of the pipeline to retrieve.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and pipeline runs list.
        Formato del diccionario de respuesta:
        
        - En caso de éxito:
            {
                "function_code": <valor>,
                "pipelines_runs": {
                    "id": <Id>,
                    "build_name": <Build name>,
                    "status": <Estado del build>,
                    "result": <Resultado del build>,
                    "variables": <Variables del build>
                }
            }

        - En caso de fallo:
            {
                "function_code": <valor>,
                "message": <mensaje_de_éxito>
            }
    """

    base_headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encode_token(TOKEN)}'
    }
    if params is not None and isinstance(params, dict):
        actualizar_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        actualizar_json(base_headers, headers)
    try:
        response = requests.get(url=f"{API_URL}/{quote(PROJECT)}/_apis/pipelines/{PIPELINE_ID}/runs", headers=base_headers, params=base_parameters)
        if response.status_code == 200:
            json_response={
                        "function_code":200,
                        "message": "Obtencion de runs correcta",
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
        print(f"Error al obtener los miembros del equipo: \n {e.strerror}")
        sys.exit(1)

def get_build_status_by_build_id(API_URL: str, PROJECT: str, TOKEN: str, BUILD_NAME: int, PIPELINE_NAME: str = None, headers: object = None, params: object = None) -> object:
    """
    Retrieves the status of a pipeline run.

    Args:
        API_URL (str): Base URL of the API for retrieving reviewer information.
        TOKEN (str): Authorization token for API access.
        PROJECT (str): Name of the project to retrieve.
        BUILD_ID (int): Id of the build to retrieve.
        PIPELINE_NAME (str): Name of the pipeline to retrieve.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and status of build.
        Formato del diccionario de respuesta:
        
        - En caso de éxito:
            {
                "function_code": 200,
                "build": {
                    "id": <Id>,
                    "build_name": <Build name>,
                    "state": <Estado del build>,
                    "result": <Resultado del build>
                }
            }

        - En caso de fallo:
            {
                "function_code": 400,
                "message": <mensaje_de_éxito>
            }
    """

    base_headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encode_token(TOKEN)}'
    }
    if params is not None and isinstance(params, dict):
        actualizar_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        actualizar_json(base_headers, headers)
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
                "message":f"Build no encontrado: {BUILD_NAME}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"Error al obtener los miembros del equipo: \n {e.strerror}")
        sys.exit(1)

def get_build_status_by_source_branch(API_URL: str, PROJECT: str, TOKEN: str, SOURCE_BRANCH: str, PIPELINE_NAME: str = None, headers: object = None, params: object = None) -> object:
    """
    Retrieves the status of a pipeline run.

    Args:
        API_URL (str): Base URL of the API for retrieving reviewer information.
        TOKEN (str): Authorization token for API access.
        PROJECT (str): Name of the project to retrieve.
        SOURCE_BRANCH (str): Name of the source branch to retrieve.
        PIPELINE_NAME (str): Name of the pipeline to retrieve.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and status of build.
        Formato del diccionario de respuesta:
        
        - En caso de éxito:
            {
                "function_code": 200,
                "build": {
                    "id": <Id>,
                    "build_name": <Build name>,
                    "state": <Estado del build>,
                    "result": <Resultado del build>
                }
            }

        - En caso de fallo:
            {
                "function_code": 400,
                "message": <mensaje_de_éxito>
            }
    """

    base_headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encode_token(TOKEN)}'
    }
    if params is not None and isinstance(params, dict):
        actualizar_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        actualizar_json(base_headers, headers)
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
                    "message":f"Pipeline no encontrado: {PIPELINE_NAME}, {pipelines_response['message']}"
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
                "message":f"Build no encontrado por filtro de branch: {SOURCE_BRANCH}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"Error al obtener los miembros del equipo: \n {e.strerror}")
        sys.exit(1)

def get_branches_from_repo(API_URL: str, PROJECT: str, TOKEN: str, repo_name: str, headers: object = None, data: object = None, params: object = None):
    """
    Retrieves the status of a pipeline run.

    Args:
        API_URL (str): Base URL of the API for retrieving reviewer information.
        TOKEN (str): Authorization token for API access.
        PROJECT (str): Name of the project to retrieve.
        SOURCE_BRANCH (str): Name of the source branch to retrieve.
        PIPELINE_NAME (str): Name of the pipeline to retrieve.

    Returns:
        object: Dictionary with information about the success or failure of the operation, including function code and status of build.
        Formato del diccionario de respuesta:
        
        - En caso de éxito:
            {
                "function_code": 200,
                "build": {
                    "id": <Id>,
                    "build_name": <Build name>,
                    "state": <Estado del build>,
                    "result": <Resultado del build>
                }
            }

        - En caso de fallo:
            {
                "function_code": 400,
                "message": <mensaje_de_éxito>
            }
    """

    base_headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encode_token(TOKEN)}'
    }
    if params is not None and isinstance(params, dict):
        actualizar_json(base_parameters, params)
    if headers is not None and isinstance(headers, dict):
        actualizar_json(base_headers, headers)
    try:
        repositoryId = get_repo_id(API_URL=API_URL, PROJECT=PROJECT, TOKEN=TOKEN, repo_name=repo_name, headers=None, params=None)
        if repositoryId['function_code'] == 200:
            response = requests.get(url=f"{API_URL}/{quote(PROJECT)}/_apis/git/repositories/{repositoryId['repoId']}/refs", headers=base_headers, params=base_parameters)
            if response.status_code == 200:
                json_response={
                            "function_code": 200,
                            "message": "Obtencion de ramas correcta",
                            "branches": []
                }
                for branch in json.loads(response.text)['value']:
                    json_response['branches'].append({
                        "name": branch['name'],
                    })
            else:
                json_response={
                    "function_code":f"{response.status_code}",
                    "message":f"Error en la obtencion de las ramas del repo, mensaje: {response.text}"
                }
        else:
            json_response={
                "function_code":f"{repositoryId['function_code']}",
                "message":f"Error en la obtencion de repo id, mensaje: {repositoryId['message']}"
            }
        return json_response
    except requests.RequestException as e:
        print(f"Error al obtener los miembros del equipo: \n {e.strerror}")
        sys.exit(1)



# generar una funcion para recorer la lista y llamar a la descarga del repo y al crud_prs


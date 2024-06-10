import azure.functions as func
import logging
import os
import json
from github import Github, GithubIntegration, Auth

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="createGitHubAppToken")
def createGitHubAppToken(req: func.HttpRequest) -> func.HttpResponse:
    # Auth with JWT
    with open(os.getenv("PEM_PATH"), "r") as pem_file:
        auth = Auth.AppAuth(os.getenv("APP_ID"), pem_file.read())

    with GithubIntegration(auth=auth) as gi:
        # Get installation ID
        installation_id = gi.get_repo_installation(os.getenv("GITHUB_OWNER"), os.getenv("GITHUB_REPO")).id

        # Get access token
        access_token = gi.get_access_token(installation_id).token

    return func.HttpResponse(
        body=json.dumps({"access_token": access_token}),
        mimetype="application/json"
    )


@app.route(route="createManifestPR")
def createManifestPR(req: func.HttpRequest) -> func.HttpResponse:
    access_token = req.params.get("access_token")

    # Auth with access token
    auth = Auth.Token(access_token)

    with Github(auth=auth) as g:
        # Get repository
        repo = g.get_repo("{owner}/{repo}".format(owner=os.getenv("GITHUB_OWNER"), repo=os.getenv("GITHUB_REPO")))
        print(f"repo_name: {repo.name}")

        # Get pull request
        pr = repo.get_pull(pr_number)

        # Add pull request comment
        comment = pr.create_comment("")

    return func.HttpResponse(
        "Succeed"
    )

from github_auth import GitHubAuth, GitHubDeviceFlow


def main():
    # 1. Create a Device Flow instance with your OAuth App client ID
    device_flow = GitHubDeviceFlow(client_id="Iv23lifLGFWDfqa8h8VY")

    # 2. Authenticate (opens browser automatically)
    token = device_flow.authenticate(scopes="repo user")

    # 3. Use the token
    if token:
        gh = GitHubAuth(token=token)
        result = gh.verify_auth()
        print(result)


if __name__ == "__main__":
    main()

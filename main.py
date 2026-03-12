import requests


def get_owner():
    while True:
        owner = input("Enter a GitHub owner: ")
        own_url = f"https://api.github.com/users/{owner}/repos"
        res = requests.get(own_url).json()

        if len(res) != 0:
            break
        print("Wrong name")

    return owner


def get_repo(owner,repo_list):
    while True:
        repo = input(f"Enter {owner}'s repo: ")

        if repo not in repo_list:
            break
        print("Wrong name")

    return repo

def main():

    owner = get_owner()

    while True:
        # Print choises 0 = exit, 1 = search user
        print("Owner is " + owner)
        print("0. Exit")
        print("1. Switch user")
        print("2. List repos")
        print("3. Look into repo")

        choice = input("What do you want to do? : ")

        own_url = f"https://api.github.com/users/{owner}/repos"

        if choice == "0":
            break
        elif choice == "1":
            owner = get_owner()
        elif choice == "2":
            res = requests.get(own_url).json()
            if len(res) != 0:
                print([x["name"] for x in res])
        elif choice == "3":
            res = requests.get(own_url).json()
            if len(res) != 0:
                print([x["name"] for x in res])
                repo = get_repo(owner, res)
            while True:
                print("Repo is: " + repo)

                url = f"https://api.github.com/repos/{owner}/{repo}"

                if requests.get(url).status_code != 200:
                    print("Wrong repo")
                    break

                print("0. Exit")
                print("1. List commits")
                print("2. List contributors")
                print("3. List authors")
                choice = input("What do you want to do? : ")
                if choice == "0":
                    break
                elif choice == "1":
                    commits = requests.get(url+ "/commits").json()
                    print(commits[0]["commit"]["author"].keys())
                    print("\n".join([x["commit"]["author"]["date"] + " " + x["commit"]["author"]["name"] + " " + x["commit"]["message"].split('\n')[0] for x in commits[:5]]))
                elif choice == "2":
                    contributors = requests.get(url+ "/contributors").json()
                    print(contributors[0].keys())
                    print("\n".join([x["login"] for x in contributors[:5]]))
        else:
            print("Wrong choice")


    repo = input("Enter a GitHub repository: ")

    url = f"https://api.github.com/repos/{owner}/{repo}"

    print(requests.get(url).json())

    # 1. Get List of Contributors (Authors)
    contributors_url = f"{url}/contributors"
    authors_res = requests.get(contributors_url)

    if authors_res.status_code == 200:
        authors = authors_res.json()
        print(f"Top Author: {authors[0]['login']} with {authors[0]['contributions']} commits")

    # 2. Get Commit History
    commits_url = f"{url}/commits"
    commits_res = requests.get(commits_url)

    if commits_res.status_code == 200:
        latest_commits = commits_res.json()
        for commit in latest_commits[:5]:  # Show first 5
            message = commit['commit']['message'].split('\n')[0]
            date = commit['commit']['author']['date']
            print(f"[{date}] {message}")


if __name__ == "__main__":
    main()
    print("done")

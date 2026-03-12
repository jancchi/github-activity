import requests
import plotly.graph_objects as go
from collections import Counter
from datetime import datetime


def visualize_commits(commits):
    dates = [x["commit"]["author"]["date"][:10] for x in commits]
    counts = Counter(dates)

    sorted_dates = sorted(counts.keys())
    sorted_counts = [counts[d] for d in sorted_dates]

    fig = go.Figure(go.Bar(x=sorted_dates, y=sorted_counts))
    fig.update_layout(
        title="Commit activity",
        xaxis_title="Date",
        yaxis_title="Commits",
        xaxis_tickangle=-45
    )
    fig.show()


def visualize_contributors(contributors):
    logins = [x["login"] for x in contributors[:10]]
    contribs = [x["contributions"] for x in contributors[:10]]

    fig = go.Figure(go.Bar(
        x=contribs,
        y=logins,
        orientation="h"
    ))
    fig.update_layout(
        title="Top contributors",
        xaxis_title="Commits",
        yaxis=dict(autorange="reversed")
    )
    fig.show()

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
                    visualize_commits(commits)
                    #print(commits[0]["commit"]["author"].keys())
                    #print("\n".join([x["commit"]["author"]["date"] + " " + x["commit"]["author"]["name"] + " " + x["commit"]["message"].split('\n')[0] for x in commits[:5]]))
                elif choice == "2":
                    contributors = requests.get(url+ "/contributors").json()
                    visualize_contributors(contributors)
                    #print(contributors[0].keys())
                    #print("\n".join([x["login"] for x in contributors[:5]]))
        else:
            print("Wrong choice")

if __name__ == "__main__":
    main()
    print("done")

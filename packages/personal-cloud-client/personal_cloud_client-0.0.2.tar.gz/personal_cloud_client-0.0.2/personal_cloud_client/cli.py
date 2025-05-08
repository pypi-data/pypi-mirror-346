import argparse
import requests


def deploy_app(args):
    with open(args.image, "rb") as f:
        headers = {"Access-Token": args.token}

        response = requests.post(
            f"{args.host}/app/deploy",
            files={"image": f},
            data={ "name": args.name },
            headers=headers
        )

    print(f"[{response.status_code}] {response.text}")


def main():
    parser = argparse.ArgumentParser(description="Personal Cloud Client")
    parser.add_argument("--host", default="http://localhost:3000", help="Server URL")
    parser.add_argument("--token", required=True, help="Auth token")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Command: deploy
    deploy_parser = subparsers.add_parser("deploy", help="Deploy the application's docker image")
    deploy_parser.add_argument("--name", required=True, help="App name")
    deploy_parser.add_argument("--image", required=True, help="App image path")
    deploy_parser.set_defaults(func=deploy_app)

    # Execute command
    args = parser.parse_args()
    args.func(args)

import argparse

import playlists
import tokens

parser = argparse.ArgumentParser("Spotify most recent playlist")
subparsers = parser.add_subparsers(help="Available commands")
subparsers.required = True

generate_playlist_subparser = subparsers.add_parser("generate-playlists")
generate_playlist_subparser.set_defaults(command="generate-playlists")

list_users_subparser = subparsers.add_parser("list-users")
list_users_subparser.set_defaults(command="list-users")

args = parser.parse_args()


if args.command == "generate-playlists":
    playlists.generate_playlists()

elif args.command == "list-users":
    playlists.list_users()


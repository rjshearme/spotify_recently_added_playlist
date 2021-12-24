import argparse

import playlists
import tokens

parser = argparse.ArgumentParser("Spotify most recent playlist")
subparsers = parser.add_subparsers(help="Available commands")
subparsers.required = True

generate_playlist_subparser = subparsers.add_parser("generate-playlists")
generate_playlist_subparser.set_defaults(command="generate-playlists")

refresh_token_subparser = subparsers.add_parser("refresh-token")
refresh_token_subparser.set_defaults(command="refresh-token")

args = parser.parse_args()


if args.command == "generate-playlists":
    playlists.generate_playlists()

elif args.command == "refresh-token":
    tokens.get_refresh_token()

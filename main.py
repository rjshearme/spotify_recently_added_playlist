import argparse

import playlists
import tokens

parser = argparse.ArgumentParser("Spotify most recent playlist")
subparsers = parser.add_subparsers(help="Available commands")
subparsers.required = True

generate_playlist_subparser = subparsers.add_parser("generate-playlist")
generate_playlist_subparser.add_argument("--days-limit", required=True, type=int, help="The last N days of songs to include in the playlist")
generate_playlist_subparser.set_defaults(command="generate-playlist")

refresh_token_subparser = subparsers.add_parser("refresh-token")
refresh_token_subparser.set_defaults(command="refresh-token")

args = parser.parse_args()


if args.command == "generate-playlist":
    playlists.generate_playlist(days_limit=args.days_limit)

elif args.command == "refresh-token":
    tokens.get_refresh_token()

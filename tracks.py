import datetime

class Track:

    def __init__(self, spotify_dict):
        self.name = spotify_dict["track"]["name"]
        self.day_added = datetime.datetime.strptime(spotify_dict["added_at"], "%Y-%m-%dT%H:%M:%SZ").date()
        self.track_id = spotify_dict["track"]["id"]

    def __repr__(self):
        return f"<Track(name='{self.name}', track_id='{self.track_id}', day_added={self.day_added})>"


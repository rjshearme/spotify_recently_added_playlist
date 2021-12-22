import tokens


def make_api_call(url, method, *, data=None, params=None):
    response = method(
        url=url,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {tokens.get_access_token()}",
        },
        params=params if params is not None else {},
        data=data if data is not None else {},
    )
    if not response.ok:
        raise RuntimeError(f"Error making request to {url}: ", r.content)
    return response
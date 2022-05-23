# Description

A simple application which connects to the spotify api and allows for doing various things against it.

# How To Use

You will need to set up a Spotify dev account at <https://developer.spotify.com>

Once you have done that, you will need to create a new application to associate with the app. This can be done here: <https://developer.spotify.com/dashboard/applications>

Then, you will need to collect some information from the application to feed into the app. On the application, you will need to collect the Client ID and the Client Secret.

Finally before running, you will need to place the information in a file in the root of the directory called credentials.json with the below information:

```json
{
    "client_id": "<CLIENT_ID_HERE>",
    "client_secret": "<CLIENT_SECRET_HERE>",
    "redirect_uri": "<YOUR_PUBLIC_IP_HERE>:8000/auth",
    "scope": "user-read-currently-playing user-read-recently-played playlist-read-private user-library-read"
}
```
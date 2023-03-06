# oidc-python
A POC to learn about using OIDC from [here](https://realpython.com/flask-google-login/)

This uses Google as the OIDC provider. A set of OAuth credentials can be generated [here](https://console.developers.google.com/apis/credentials)

1. You need a `Client ID` and `Client Secret` from the provider (in this case, Google)
1. It's here you need to add the authorised origins (the URL for your app) and the redirect URI (the callback endpoint for your app). Because this app is a demo and only ever going to run locally, these are set to `https://127.0.0.1:5000` and `https://127.0.0.1:5000/login/callback`, respectively. 

When you login, the app does the following:

1. Sends a request to the provider's authorization URL (this is fetched using the `./well-known/openid-configuration` endpoint)
1. Provider ask's the user to login
1. Provider asks th user to consent to the app acting on thier behalf
1. Provider sends a unique authorisation code to the app
1. App sends the authorisation code to the providers token endpoint (this is fetched using the same endpoint above)
1. Provider sends back tokens (one of which, `id_token` is a JWT) which can be used with other URLs "as" the user

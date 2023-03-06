# oidc-python
A POC to learn about using OIDC from [here](https://realpython.com/flask-google-login/)

This uses Google as the OIDC provider. A set of OAuth credentials can be generated [here](https://console.developers.google.com/apis/credentials)

1. You need a `Client ID` and `Client Secret` from the provider (in this case, Google)
1. It's here you need to add the authorised origins (the URL for your app) and the redirect URI (the callback endpoint for your app). Because this app is a demo and only ever going to run locally, these are set to `https://127.0.0.1:5000` and `https://127.0.0.1:5000/login/callback`, respectively. 
1. 

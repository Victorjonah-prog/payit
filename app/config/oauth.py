import os
from authlib.integrations.starlette_client import OAuth


#get env

AUTH0_DOMAIN=os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID=os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET=os.getenv("AUTH0_CLIENT_SECRET")



oauth = OAuth()

oauth.register(
    name= "auth0",
    client_id = AUTH0_CLIENT_ID,
    client_secret= AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",

    },
    server_metadata_url=f"https://{AUTH0_DOMAIN}/.well-known/openid-configuration"
    
)

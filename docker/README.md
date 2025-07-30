Create an .env file with following items:
```
DB_CONN_STRING=<connection string for sqlalchemy>
LOBBIES_DIR=<directory to save existing lobbies when app stops>
ACCESS_TOKEN_SECRET=<see how to generate below>
REFRESH_TOKEN_SECRET=<see how to generate below>
```

The dev compose file installs the core game logic in editable mode to prevent rebuilds
import cognitojwt

def verifyToken(id_token):
    REGION = 'us-east-1'
    USERPOOL_ID = 'us-east-1_Xn6o2B9bL'
    APP_CLIENT_ID = '6dr4s3bnourm4h78lnikpf2ajp'
    try:
        verified_claims: dict = cognitojwt.decode(
            id_token,
            REGION,
            USERPOOL_ID,
            app_client_id=APP_CLIENT_ID,  # Optional
            testmode=True  # Disable token expiration check for testing purposes
        )

        return verified_claims
    except:
        return None
    

print(verifyToken("eyJraWQiOiJoUUtRMXlXRWNmaFBzWFFMSzdrU0FaNEtSaEJmYUJQYVlyTzIySWNSMG5rPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI0NGU4MjQzOC0yMGExLTcwNTEtMmZjOS1mMTgwZTZhMjBhYTMiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX1huNm8yQjliTCIsImNvZ25pdG86dXNlcm5hbWUiOiI0NGU4MjQzOC0yMGExLTcwNTEtMmZjOS1mMTgwZTZhMjBhYTMiLCJvcmlnaW5fanRpIjoiYjFiYmJjMjYtZmIzYi00OTFjLWI3Y2QtNzRmMzdmZDUwYWE5IiwiYXVkIjoiNmRyNHMzYm5vdXJtNGg3OGxuaWtwZjJhanAiLCJldmVudF9pZCI6IjYwYjRmMjNkLTIxODgtNGU1ZC04ZjQ5LTk3ZjA4MDBkZGJjYyIsInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNzE2ODg2MDczLCJuYW1lIjoidXNlciIsImV4cCI6MTcxNjg4OTY3MywiaWF0IjoxNzE2ODg2MDczLCJqdGkiOiJjMGU2MDAwNS03OWY1LTQ5YzMtODk3My05ZTc5YzA1NTZjYzUiLCJlbWFpbCI6InZla25venVnbm9AZ3VmdW0uY29tIn0.Of056x8vectMhgsnDs_2C60VflGtD5oCZ7Q_ZUoLZqa6bfWtrxIXQuRxTuefZdranVO2Q-EJFsr7-oZy8JJShIIrh_wzK3ww2cSozVqVJIUQVDlL1ugBmYvssbEIYCSxAPRZMIMz1SybQAnBqNAITz-JuzVdglWKvi7XwBlAq8ru5jyvl4TMtnQUnBboK9C7w43ijZXT4sFdR-u2NMG1NypMxr7TQYDjnPjQrwZaCAb9939ErqbpEpJW2pl78qWK2PePbe_A7E_1hJ1HweHrDkTz83gV2Pznqc64tBlReVmo5pvX-t565_2vqczgYluW30OOO2Fr-fGWDvP2B_rAFw"))
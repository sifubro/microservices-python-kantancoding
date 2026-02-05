# AUTH SERVICE
# For AUTH we will use JWT (JSON web tokens), datetime to set expiration date on token and os for enviroment variables to configure MySQL connection
import jwt, datetime, os
# We are going to use flask to create our server
from flask import Flask, request
# to query SQL DB
from flask_mysqldb import MySQL

# create our server (Flask object)
server = Flask(__name__)
mysql = MySQL(server)

# dictionary to store config variables
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT"))


@server.route("/login", methods=["POST"])
def login():
    # The `request.authorization` attribute provides the credentials from a Basic Authentication Header.
    # When we send a request to this \login route we need to provide basic auth header which will contains the username and password
    # This request obj has an attribute that gives us access  to that. Once we instantiate this obj we can do auth.username and auth.password to get the username and password
    auth = request.authorization
    
    # If we don't provide that header within the request, the auth will be None
    if not auth:  #if the header doesn't exist within the request
        return "missing credentials", 401

    # This Auth service is going to have its own MySQL DB
    # check `user` table within the DB for username and password for the users trying to log in or trying to access the API
    cur = mysql.connection.cursor()

    # check the DB for the username and the password that we pass in our basic Auth header in out request to this login endpoint `auth = request.authorization`
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username,)
    )

    if res > 0: # user exists within the database
        user_row = cur.fetchone() # tuple (email, password)
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        else:
            # return a JSON Web Token
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "invalid credentials", 401


@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "missing credentials", 401

    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithms=["HS256"]
        )
    except:
        return "not authorized", 403

    return decoded, 200


def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": authz,
        },
        secret,
        algorithm="HS256",
    )


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)

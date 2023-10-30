from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

router_security = APIRouter()

secret_key = "75362b26268895ecc7549c2c7931609bd23f3d1d6758054260ecdfce9ca151b1"
algorithm = "HS256"

# Definimos una función que crea un token JWT con una fecha de expiración
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

# Middleware para validar el token JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Ruta para obtener un token JWT
@router_security.get("/token")
def get_access_token():
    access_token_expires = timedelta(hours=7)  # Token de acceso expira en 7 horas
    access_token = create_access_token(data={"sub": "user"}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer", "refresh_token_expiration_hours": 60}

# Ruta protegida que requiere un token JWT válido
#@app.get("/secure-data")
#def get_secure_data(token: str = Depends(oauth2_scheme)):
#    try:
#        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
#        return {"message": "This is secure data!", "user": payload["sub"]}
#    except JWTError:
#        raise HTTPException(status_code=401, detail="Invalid token")


# Ceci est le projet DjangoTp1 de Antoine Delalande

Afin de configurer l'envoie des mails, veuillez ajouter ces variables a vos variables d'environnement :

EMAIL_HOST
EMAIL_PORT
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD
DEFAULT_FROM_EMAIL
RAVIOLI_KEY

Toutes les dates s'écrivent au format AAAA-MM-JJ HH:mm:ss.


# API Exemples:
    GET: curl http://localhost:8000/api/vehicle/ -H 'API-KEY: fd2ns6z5g6541gn3sd2g1ns'
    
    POST: curl -X POST http://localhost:8000/api/vehicle/ -H 'API-KEY:  fd2ns6z5g6541gn3sd2g1ns' -H 'Content-Type: application/json' -d '{"description": "test", "number": "TE-111-ST", "vehicle_type": "ESSENCE", "location": "2"}'
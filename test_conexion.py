from db.connection import get_client

client = get_client()
response = client.table("postulaciones").select("*").execute()
print("✅ Conexión exitosa. Filas en tabla:", len(response.data))
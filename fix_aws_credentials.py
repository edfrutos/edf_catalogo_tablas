#!/usr/bin/env python3
import os
import boto3
import botocore
from dotenv import load_dotenv
import sys

def check_credentials():
    # Cargar variables de entorno desde .env
    load_dotenv()

    # Obtener credenciales de AWS desde variables de entorno
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_REGION', 'us-east-1')
    bucket_name = os.getenv('S3_BUCKET_NAME')

    if not all([aws_access_key, aws_secret_key, bucket_name]):
        print("❌ Faltan variables de entorno necesarias:")
        print(f"AWS_ACCESS_KEY_ID: {'✅ Configurado' if aws_access_key else '❌ No configurado'}")
        print(f"AWS_SECRET_ACCESS_KEY: {'✅ Configurado' if aws_secret_key else '❌ No configurado'}")
        print(f"S3_BUCKET_NAME: {'✅ Configurado' if bucket_name else '❌ No configurado'}")
        print(f"AWS_REGION: {'✅ Configurado' if aws_region else '❌ No configurado (usando us-east-1 por defecto)'}")
        return False

    try:
        # Crear cliente S3
        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region
        )
        
        # Verificar que podemos listar el bucket
        print(f"Intentando acceder al bucket {bucket_name}...")
        s3.head_bucket(Bucket=bucket_name)
        print("✅ Acceso al bucket exitoso.")
        
        return True
        
    except botocore.exceptions.ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        if error_code == 'InvalidAccessKeyId':
            print("❌ Error: Las credenciales de AWS no son válidas.")
            print("El ID de clave de acceso proporcionado no existe en los registros de AWS.")
        elif error_code == 'SignatureDoesNotMatch':
            print("❌ Error: La firma no coincide. Posiblemente la clave secreta sea incorrecta.")
        elif error_code == 'NoSuchBucket':
            print(f"❌ Error: El bucket '{bucket_name}' no existe.")
        elif error_code == '403':
            print("❌ Error: Acceso denegado al bucket. Verifica los permisos de la IAM.")
        else:
            print(f"❌ Error al conectar con S3: {e}")
        
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def print_next_steps():
    print("\n📋 PASOS PARA SOLUCIONAR EL PROBLEMA")
    print("=====================================")
    print("1️⃣ Verifica que las credenciales de AWS actuales sean correctas en AWS Management Console")
    print("2️⃣ Si las credenciales son inválidas, debes crear un nuevo par de claves de acceso:")
    print("   a. Inicia sesión en la consola AWS")
    print("   b. Ve a IAM > Users > [tu usuario]")
    print("   c. En la pestaña 'Security credentials', crea una nueva clave de acceso")
    print("   d. Guarda el ID y la clave secreta de forma segura")
    print("3️⃣ Actualiza el archivo .env con las nuevas credenciales:")
    print("   AWS_ACCESS_KEY_ID=nueva_clave_id")
    print("   AWS_SECRET_ACCESS_KEY=nueva_clave_secreta")
    print("4️⃣ Asegúrate de que el bucket existe y el usuario tiene permisos sobre él")
    print("5️⃣ Verifica que la configuración CORS del bucket permita las solicitudes desde tu dominio")
    print("6️⃣ Reinicia Apache después de actualizar las credenciales:")
    print("   sudo systemctl restart apache2")

if __name__ == "__main__":
    print("🔍 DIAGNÓSTICO DE CREDENCIALES AWS S3")
    print("=====================================")
    success = check_credentials()
    
    if not success:
        print_next_steps()
    else:
        print("\n✅ Las credenciales AWS parecen estar funcionando correctamente.")
        print("Si sigue habiendo problemas con las imágenes, verifica la configuración CORS del bucket S3.")

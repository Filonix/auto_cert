import os
import datetime
import OpenSSL.crypto

def check_certificates(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            try:
                path = os.path.join(root, file)
                if os.path.splitext(file)[1].lower() == '.cer': # проверка расширения файла
                    with open(path, 'rb') as f:
                        cert_data = f.read()
                    cert = OpenSSL.crypto.load_certificate(
                        OpenSSL.crypto.FILETYPE_ASN1, cert_data)
                    not_after = datetime.datetime.strptime(
                        cert.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')
                    time_left = not_after - datetime.datetime.utcnow()
                    if time_left > datetime.timedelta(days=0) and time_left < datetime.timedelta(days=30):
                        print(f'Сертификат {path} истекает {time_left}')
            except Exception as e:
                print(f'Error processing {path}: {e}')

check_certificates(os.getcwd())

input("Нажмите любую клавишу для выхода...")

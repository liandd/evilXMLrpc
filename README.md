# evilXMLrpc
Herramienta para la explotación de xmlrpc.php por método POST en un CMS WordPress

![imagen](https://github.com/user-attachments/assets/1c983353-99b5-436e-b7e0-8e32951e01f4)

Al estar habilitado el xmlrpc.php nos dirá que solo acepta POST:

![Imagen2](https://github.com/user-attachments/assets/c363724c-e353-43bc-822f-1053da834f5b)

Una petición cualquiera por POST genera el error:

![imagen3](https://github.com/user-attachments/assets/2fb7c82d-a2a6-4153-959b-e0a61254660e)

Pero aprovechandonos del xmlrpc podemos listar los métodos configurados en el CMS WordPress:
```xml
<?xml version="1.0" encoding="utf-8"?>
<methodCall>
<methodName>system.listMethods</methodName>
<params></params>
</methodCall>
```

Generando la siguiente respuesta de lado del servidor:

```xml
HTTP/1.1 200 OK
Date: Mon, 30 Jun 2025 11:54:30 UTC
Server: Apache
Strict-Transport-Security: max-age=63072000; includeSubdomains; preload
Connection: close
Vary: Accept-Encoding
Referrer-Policy: no-referrer-when-downgrade
Content-Length: 4272
Content-Type: text/xml; charset=UTF-8

<?xml version="1.0" encoding="UTF-8"?>
<methodResponse>
  <params>
    <param>
      <value>
      <array><data>
  <value><string>system.multicall</string></value>
  <value><string>system.listMethods</string></value>
  <value><string>system.getCapabilities</string></value>
  <value><string>demo.addTwoNumbers</string></value>
  .........
</data></array>
      </value>
    </param>
  </params>
</methodResponse>
```
Implementación óptima para el problema con concurrencia aplicada. La arquitectura del código está alineada con las limitaciones del entorno CMS WordPress Local (latencia de red, volumen de datos de rockyou.txt), y se refleja una alta eficiencia bajo las restricciones:
- O(n) en tiempo: recorre cada palabra al menos una vez.
- El peor caso es O(n) 14mil millones, pero se espera terminar antes O(k) k << n.
- CPU usage bajo: 9% confirma que el cuello está en latencia de red, no en cómputo.
- Memoria constante O(1) por el uso de descriptores de archivos y hilos activos.
- Cada hilo mantiene contexto mínimo: una palabra, la conexión, y el control de flujo.

![Eficiencia](https://github.com/user-attachments/assets/677a18a5-d0cc-4ba5-879f-cd24555b7003)



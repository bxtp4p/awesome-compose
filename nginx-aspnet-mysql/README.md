## Compose sample application

### Splunk Observability Steps

Perform these steps to configure this to work with Splunk Observability.

1. Download the [OpenTelemetry NGINX module](https://github.com/open-telemetry/opentelemetry-cpp-contrib/suites/4593268145/artifacts/123907654) to this project directory. Unzip it and rename as `0tel_ngx_module.so` if necessary.
1. Create a `.env` file and reference it in the [docker-compose.yaml](docker-compose.yaml) file. Reference it in the `otel-collector` service's `env_file` section. It should include the following:

   ```
   SPLUNK_ACCESS_TOKEN=<your_token>
   SPLUNK_REALM=<your_realm>
   SPLUNK_API_URL=https://api.<your_realm>.signalfx.com
   SPLUNK_HEC_TOKEN=<your_token>
   SPLUNK_HEC_URL=https://ingest.<your_realm>.signalfx.com/v1/log
   SPLUNK_INGEST_URL=https://ingest.<your_realm>.signalfx.com
   SPLUNK_TRACE_URL=https://ingest.<your_realm>.signalfx.com/v2/trace
   SPLUNK_CONFIG=/etc/otel/collector/gateway_config.yaml
   ```
### ASP.NET server with an Nginx proxy and a MySQL database

Project structure:
```
.
├── backend
│   ├── Dockerfile
│   ├── aspnet.csproj
│   └── Program.cs
├── db
│   └── password.txt
├── docker-compose.yaml
├── proxy
│   ├── conf
│   └── Dockerfile
└── README.md
```

[_docker-compose.yaml_](docker-compose.yaml)
```
services:
  backend:
    build: backend
    ...
  db:
    # We use a mariadb image which supports both amd64 & arm64 architecture
    image: mariadb:10.6.4-focal
    # If you really want to use MySQL, uncomment the following line
    #image: mysql:8.0.27
    ...
  proxy:
    build: proxy
    ports:
    - 80:80
    ...
```
The compose file defines an application with three services `proxy`, `backend` and `db`.
When deploying the application, docker-compose maps port 80 of the proxy service container to port 80 of the host as specified in the file.
Make sure port 80 on the host is not already being in use.

> ℹ️ **_INFO_**  
> For compatibility purpose between `AMD64` and `ARM64` architecture, we use a MariaDB as database instead of MySQL.  
> You still can use the MySQL image by uncommenting the following line in the Compose file   
> `#image: mysql:8.0.27`

## Deploy with docker-compose

```
$ docker-compose up -d
```

## Expected result

Listing containers must show three containers running and the port mapping as below:
```
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                  NAMES
8906b14c5ad1        nginx-aspnet-mysql_proxy     "nginx -g 'daemon of…"   2 minutes ago       Up 2 minutes        0.0.0.0:80->80/tcp    nginx-aspnet-mysql
l_proxy_1
13e0e0a7715a        nginx-aspnet-mysql_backend   "/server"                2 minutes ago       Up 2 minutes        8000/tcp              nginx-aspnet-mysq
l_backend_1
ca8c5975d205        mysql:5.7                    "docker-entrypoint.s…"   2 minutes ago       Up 2 minutes        3306/tcp, 33060/tcp   nginx-aspnet-mysql
l_db_1
```

After the application starts, navigate to `http://localhost:80` in your web browser or run:
```
$ curl localhost:80
["Blog post #0","Blog post #1","Blog post #2","Blog post #3","Blog post #4"]
```

Stop and remove the containers
```
$ docker-compose down
```

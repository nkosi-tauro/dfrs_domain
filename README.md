
## Enviroments
- [Production](https://dfrsdomain-production.up.railway.app/)  
- [Development](https://dfrsdomain-dev.up.railway.app/)

## :checkered_flag: Starting ##

```bash
# Clone this project
$ git clone https://github.com/nkosi-tauro/dfrs_domain

# Access directory
$ cd dfrs_domain

# build docker container
$ docker build --tag dfrs_domain .

# Run the project
$ docker run --publish 8000:8000 dfrs_domain

# The server will initialize in the <http://localhost:8000>
```

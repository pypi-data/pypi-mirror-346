aioclient
===

Installation
---

```sh
python3 -m pip install aioclient
```

Usage
---

```python
import aioclient
import asyncio

async def get_example():
    status, headers, body = await aioclient.get('https://www.example.com/')
    print(body)

asyncio.run(get_example())
```

Changelog
---

### v0.1.0

* GET requests return `status, headers, body` tuples


### v0.2.0

* Support `OPTIONS`, `HEAD`, `POST`, `PUT`, `PATCH`, and `DELETE` requests
* Deserialize `text/xml` responses as XML `ElementTree`

### v0.2.1

* Fix project description

### v0.2.2

* Remove `cchardet` dependency

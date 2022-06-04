## Before
### install module
```bash
$ pip3 install -r requirements.txt
```

### .env file
```
NAVER_CLIENT_ID=
NAVER_CLIENT_SECRET=

KAKAO_MAP_API_KEY=

KOFIC_KEY=

SECRET_KEY=

DEBUG_MODE=
```

## After
### Run
```bash
$ python3 manage.py runserver {yourport}
```

## Deploy
* local (login required)

```bash
$ ./deploy local
```

* aws (pem key required)

```bash
$ ./deploy
```
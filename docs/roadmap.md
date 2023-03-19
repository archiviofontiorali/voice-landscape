# Roadmap

## Django
- [x] Enable jazzmin
- [x] Create superuser command
- [x] Delete old scripts folder
- [x] Create Models
  - [x] Share
  - [x] Frequency
  - [x] Place
- [x] Install SpatiaLite and GeoDjango 
  [tutorial](https://docs.djangoproject.com/en/4.1/ref/contrib/gis/tutorial/), [installation](https://docs.djangoproject.com/en/4.1/ref/contrib/gis/install/)
- [x] Delete old templates folder
- [x] Delete old www static folder
- [x] Uninstall sqladmin
- [x] remove starlette commands
- [x] Uninstall SQLModel and fastapi
- [x] Remove api, db amd settings module
- [x] use name resolution for links
- [x] Uninstall pydantic
- [x] Remove repos, handlers, cases (merged in apps)
- [x] Move SpeechToText to django
- [x] Remove old app
- [x] Add signal to save frequencies on Share save
- [x] Complete share template

- [ ] Move test to django
- [ ] Add support to PostgreSQL and PostGIS
- [ ] Unistall starlette, Pydantic, ...
- [ ] Privacy and cookies page
- [ ] Improve how axios show messages in SharePage

- [ ] Check why auto location is so slow
- [ ] Check why frequencies are not updated correctly

### Code to generate grid of places
```python
import numpy as np
a = np.array([44.647728027899625, 10.88466746283678])
b = np.array([44.64159324683118, 10.902033051497972])
c = np.array([44.65583248401956, 10.903694945558476])
v1, v2 = b - a, c - a

N = 6
points = np.empty(((N + 1) * (N + 2) // 2, 2))
count = 0
for i in range(N + 1):
    for j in range(N - i + 1):
        points[count, :] = a + (i / N) * v1 + (j / N) * v2
        count += 1


for i, p in enumerate(points):
    PLACES[(p[0], p[1])] = f"place #{i}"
```
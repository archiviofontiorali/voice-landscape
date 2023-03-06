import numpy as np
from starlette.testclient import TestClient

import voices.app
import voices.constants as c

app = voices.app.App().app()
client = TestClient(app)


def test_app():
    for x, y in np.random.rand(100, 2):
        coord = c.a + x * c.v1 + y * c.v2
        response = client.post(
            url="/share",
            data={"loc-x": coord[0], "loc-y": coord[1], "text": "Paesaggio di Voci"},
        )
        assert response.status_code == 200, response

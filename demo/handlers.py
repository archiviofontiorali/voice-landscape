class PageHandler:
    def __init__(self, case):
        self._case = case

    async def __call__(self, request):
        return await self._case.execute(request)


class ShareHandler:
    def __init__(self, case):
        self._case = case

    async def __call__(self, request):
        data = await request.form()

        latitude = float(data.get("loc-x", None)) if request.method == "POST" else None
        longitude = float(data.get("loc-y", None)) if request.method == "POST" else None
        text = data.get("text", None) if request.method == "POST" else None

        return await self._case.execute((latitude, longitude), text, request)

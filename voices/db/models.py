import sqlmodel


class Voice(sqlmodel.SQLModel, table=True):
    id: int | None = sqlmodel.Field(default=True, primary_key=True)
    word: str

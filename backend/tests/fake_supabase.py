class _Result:
    def __init__(self, data):
        self.data = data


class FakeTable:
    """Just enough of the Supabase query builder for the project store."""

    def __init__(self, rows: list[dict]):
        self._rows = rows
        self._op = None
        self._payload = None
        self._filter = None

    def insert(self, payload):
        self._op, self._payload = "insert", payload
        return self

    def select(self, _columns):
        self._op = "select"
        return self

    def update(self, payload):
        self._op, self._payload = "update", payload
        return self

    def delete(self):
        self._op = "delete"
        return self

    def eq(self, column, value):
        self._filter = (column, value)
        return self

    def execute(self):
        if self._op == "insert":
            # Mirror the real database: reject non-JSON values
            import json

            json.dumps(self._payload)
            self._rows.append(dict(self._payload))
            return _Result([dict(self._payload)])

        matches = [
            r for r in self._rows
            if self._filter is None or r.get(self._filter[0]) == self._filter[1]
        ]
        if self._op == "update":
            for row in matches:
                row.update(self._payload)
            return _Result([dict(r) for r in matches])
        if self._op == "delete":
            for row in matches:
                self._rows.remove(row)
            return _Result([])
        return _Result([dict(r) for r in matches])


class FakeSupabase:
    def __init__(self):
        self.tables: dict[str, list[dict]] = {}

    def table(self, name: str) -> FakeTable:
        return FakeTable(self.tables.setdefault(name, []))
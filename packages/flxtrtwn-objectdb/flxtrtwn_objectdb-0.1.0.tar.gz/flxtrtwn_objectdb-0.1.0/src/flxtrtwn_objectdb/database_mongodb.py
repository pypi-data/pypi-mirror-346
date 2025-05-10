"""Redis Database implementation."""

from typing import Any, Dict, Mapping, Type

import pymongo

# import redis.commands.search.aggregation as aggregations
# import redis.commands.search.reducers as reducers
import pymongo.database

# from redis.commands.search.query import Query
from flxtrtwn_objectdb.database import Database, DatabaseItem, T, UnknownEntityError


class MongoDBDatabase(Database):
    """MongoDB database implementation."""

    def __init__(self, mongodb_client: pymongo.MongoClient, name: str) -> None:
        self.connection: pymongo.MongoClient[Mapping[str, dict[str, Any]]] = mongodb_client
        self.database: pymongo.database.Database[Mapping[str, dict[str, Any]]] = self.connection[name]

    def update(self, item: DatabaseItem) -> None:
        """Update data."""
        item_type = type(item)
        # rs = self.connection.ft(f"idx:{item_type.__name__}")
        # schema = (TextField(f"$.{field}", as_name=field) for field in item.model_fields.keys())
        # try:
        #     rs.create_index(
        #         schema, definition=IndexDefinition(prefix=[f"{item_type.__name__}:"], index_type=IndexType.JSON)
        #     )
        # except:
        #     pass
        collection = self.database[item_type.__name__]
        if collection.find_one():
            collection.update_one(filter={"identifier": item.identifier}, update=item.model_dump())
        else:
            collection.insert_one(item.model_dump())

    def get(self, schema: Type[T], identifier: str) -> T:
        collection = self.database[schema.__name__]
        if res := collection.find_one(filter={"identifier": identifier}):
            return schema(**res)
        raise UnknownEntityError(f"Unknown identifier: {identifier}")

        # res = rs.search(Query("Paul @age:[30 40]"))
        # rs.search(Query("Paul").return_field("$.city", as_field="city")).docs
        # req = aggregations.AggregateRequest("*").group_by("@city", reducers.count().alias("count"))
        # print(rs.aggregate(req).rows)

    def get_all(self, schema: Type[T]) -> Dict[str, T]:
        raise NotImplementedError

import graphene
from address.schema import Query as address_query

class Query(address_query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)

import graphene
from address.schema import Query as address_query
from address.schema import Mutation as address_mutation

class Query(address_query, graphene.ObjectType):
    pass

class Mutation(address_mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

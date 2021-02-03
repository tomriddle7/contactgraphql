import graphene
from graphene_django.types import DjangoObjectType
from .models import Contact

class ContactType(DjangoObjectType):
  class Meta:
    model = Contact
  
class Query(object):
    all_contact = graphene.List(ContactType)

    def resolve_all_contact(self, info, **kwargs):
    	return Contact.objects.all()

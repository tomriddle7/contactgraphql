import graphene
from graphene_django.types import DjangoObjectType
from .models import Contact

class ContactType(DjangoObjectType):
  class Meta:
    model = Contact
  
class Query(object):
    contact = graphene.Field(ContactType,
                              id=graphene.Int(),
                              name=graphene.String(),
                              tel=graphene.String(),
                              address=graphene.String(),
                              photo=graphene.String())

    all_contact = graphene.List(ContactType)

    def resolve_contact(self, info, **kwargs):
      id = kwargs.get('id')
      name = kwargs.get('name')
      tel = kwargs.get('tel')
      address = kwargs.get('address')
      photo = kwargs.get('photo')
      
      if id is not None:
        return Contact.objects.get(pk=id)
      
      if name is not None:
        return Contact.objects.get(name=name)

      if tel is not None:
        return Contact.objects.get(tel=tel)
        
      if address is not None:
        return Contact.objects.get(address=address)
      
      if photo is not None:
        return Contact.objects.get(photo=photo)

      return None

    def resolve_all_contact(self, info, **kwargs):
    	return Contact.objects.all()

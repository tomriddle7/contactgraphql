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


class CreateContact(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    tel = graphene.String()
    address = graphene.String()
    photo = graphene.String()

    class Arguments:
        # The input arguments for this mutation
        name = graphene.String(required=True)
        tel = graphene.String(required=True)
        address = graphene.String(required=True)
        photo = graphene.String(required=True)


    def mutate(self, info, name, tel, address, photo):
        contact = Contact(name=name, tel=tel, address=address, photo=photo)
        contact.save()

        # Notice we return an instance of this mutation
        return CreateContact(id=contact.id,
            name=contact.name,
            tel=contact.tel,
            address=contact.address,
            photo=contact.photo
        )


class UpdateContact(graphene.Mutation):
    contact = graphene.Field(ContactType)
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        tel = graphene.String()
        address = graphene.String()
        photo = graphene.String()

    @staticmethod
    def mutate(root, info, **kwargs):
      contact_instance = Contact.objects.get(pk=kwargs["id"])
      if contact_instance:
        for k, v in kwargs.items():
            setattr(contact_instance, k, v)
        contact_instance.full_clean()
        contact_instance.save()

        return UpdateContact(contact=contact_instance, ok=True)
      else:
        return UpdateContact(contact=None, ok=False)


class DeleteContact(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        contact = Contact.objects.get(pk=kwargs["id"])
        contact.delete()
        return cls(ok=True)

class Mutation(graphene.ObjectType):
    create_contact = CreateContact.Field()
    update_contact = UpdateContact.Field()
    delete_contact = DeleteContact.Field()
    

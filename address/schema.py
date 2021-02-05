import graphene
from graphene_django.types import DjangoObjectType
from .models import Contact
from django.db.models import Q

class ContactType(DjangoObjectType):
  class Meta:
    model = Contact
  
class Query(object):
    contact = graphene.List(ContactType,
                              id=graphene.Int(),
                              gte_id=graphene.Int(),
                              lte_id=graphene.Int(),
                              name=graphene.String(),
                              tel=graphene.String(),
                              address=graphene.String(),
                              photo=graphene.String())

    all_contact = graphene.List(ContactType)

    def resolve_contact(self, info, id=None, gte_id=None, lte_id=None, name=None, tel=None, address=None, photo=None, **kwargs):
      if id:
        filter = (
          Q(id__exact=id)
        )
        return Contact.objects.filter(filter)

      if gte_id and lte_id:
        filter = (
          Q(id__range=(gte_id, lte_id))
        )
        return Contact.objects.filter(filter)

      if gte_id:
        filter = (
          Q(id__gte=gte_id)
        )
        return Contact.objects.filter(filter)

      if lte_id:
        filter = (
          Q(id__lte=lte_id)
        )
        return Contact.objects.filter(filter)

      if name:
        filter = (
          Q(name__contains=name)
        )
        return Contact.objects.filter(filter)

      if tel:
        filter = (
          Q(tel__contains=tel)
        )
        return Contact.objects.filter(filter)

      if address:
        filter = (
          Q(address__contains=address)
        )
        return Contact.objects.filter(filter)

      if photo:
        filter = (
          Q(photo__contains=photo)
        )
        return Contact.objects.filter(filter)

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
    

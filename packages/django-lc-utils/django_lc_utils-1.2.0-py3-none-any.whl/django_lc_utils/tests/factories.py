from django.contrib.auth import get_user_model
from factory import Faker, LazyAttribute, fuzzy, post_generation
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    username = LazyAttribute(
        lambda obj: "{}_{}".format(obj.name.lower().replace(" ", ""), fuzzy.FuzzyInteger(0, 99999).fuzz())
    )
    email = LazyAttribute(lambda obj: "%s@gmail.com" % (obj.username))
    name = Faker("name")

    @post_generation
    def password(self, create, extracted, **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

    @post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]

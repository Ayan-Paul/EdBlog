from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from Institute.models import Institute
import uuid

class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)

		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

class Account(AbstractBaseUser):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(max_length=30)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name="accounts",null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_institute_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class UserAccount(Account):
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    contact_no = models.CharField(max_length=15, null=True, blank=True)
    short_intro = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(max_length=255, upload_to='profile_images', null=True, blank=True, default='profile_images/default_image.jpg')
    department = models.CharField(max_length=30)

    class Types(models.TextChoices):
        STUDENT = "Student", "STUDENT"
        TEACHER = "Teacher", "TEACHER"

    default_type = Types.STUDENT

    type = models.CharField(max_length=30, choices=Types.choices, default=default_type)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

# class InstituteAdminAccountManager(models.Manager):
#     def get_queryset(self, *args, **kwargs):
#         return self.filter(is_institute_admin=True)

class InstituteAdminAccount(Account):
    pass

    # objects = InstituteAdminAccountManager

class StudentAccountManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=UserAccount.Types.STUDENT)

class TeacherAccountManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=UserAccount.Types.TEACHER)

class StudentAccount(UserAccount):
    roll_no = models.CharField(max_length=30, null=True, blank=True)

    # objects = StudentAccountManager()

class TeacherAccount(UserAccount):
    employment_id = models.CharField(max_length=30, null=True, blank=True)

    # objects = TeacherAccountManager()

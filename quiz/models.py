from django.db import models
from django.shortcuts import reverse
# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.template.defaultfilters import slugify
class Usermanager(BaseUserManager):

    def create_user(self, nickname, password=None):
        
        if not nickname:
            raise ValueError('A user must have a nickname')

        user = self.model(
            nickname = nickname,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname, password=None):
        user = self.create_user(nickname = nickname, password=password)
        user.is_admin = True
        user.is_staff =True 
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    nickname = models.CharField(("nickname"), max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    objects = Usermanager()
    USERNAME_FIELD = 'nickname'

    def __str__(self):
        return self.nickname

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, quiz):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Quiz(models.Model):
    title = models.CharField(("title"), max_length=50)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    time_created = models.DateTimeField(("time created"), auto_now_add=False, auto_now=True)


    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

    def generate_slug(self):
        self.slug = slugify(self.title)
        return self.slug


    def save(self, *args, **kwargs):
        self.generate_slug()
        return super(Quiz, self).save(*args, **kwargs)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("show_quiz", kwargs={"slug": self.slug})


class Question(models.Model):
    question_text = models.CharField(("question text"), max_length=500)
    quiz = models.ForeignKey("Quiz", verbose_name=("quiz"), on_delete=models.CASCADE)
    slug = models.SlugField(("slug"), max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = ("Question")
        verbose_name_plural = ("Questions")

    def __str__(self):
        return self.question_text

    def get_absolute_url(self):
        return reverse("Question_detail", kwargs={"slug": self.slug})
        
    def generate_slug(self):
        self.slug = slugify(self.question_text)
        return self.slug


    def save(self, *args, **kwargs):
        self.generate_slug()
        return super(Question, self).save(*args, **kwargs)

class Choice(models.Model):
    choice_text = models.CharField(("choice text"), max_length=200)
    question = models.ForeignKey("Question", verbose_name=("question"), on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = ("Choice")
        verbose_name_plural = ("Choices")

    def __str__(self):
        return self.choice_text

class Quiz_Answer(models.Model):
    quiz = models.ForeignKey("Quiz", verbose_name=("quiz"), on_delete=models.CASCADE)
    timestamp = models.DateTimeField(("timestamp"), auto_now=True)
    slug = models.SlugField(("slug"), max_length=500)


    class Meta:
        verbose_name = ("Quiz_Answer")
        verbose_name_plural = ("Quiz_Answers")

    def __str__(self):
        return self.quiz.title

    def get_absolute_url(self):
        return reverse("Quiz_Answer_detail", kwargs={"pk": self.pk})

        
    def generate_slug(self):
        self.slug = slugify(self.slug)
        return self.slug


    def save(self, *args, **kwargs):
        self.generate_slug()
        return super(Quiz_Answer, self).save(*args, **kwargs)


class Question_Answer(models.Model):
    answer = models.ForeignKey("Choice", verbose_name=("answer"), on_delete=models.CASCADE)
    quiz_answer = models.ForeignKey("Quiz_Answer", verbose_name=("quiz answer"), on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = ("Question_Answer")
        verbose_name_plural = ("Question_Answers")

    def __str__(self):
        return self.answer.question.question_text

    def get_absolute_url(self):
        return reverse("Question_Answer_detail", kwargs={"pk": self.pk})



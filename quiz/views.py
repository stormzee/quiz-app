from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .forms import QuizForm, QuestionForm, ChoiceForm
from .models import Quiz, Question, Choice

def show_quizzes(request):
    quiz_list = Quiz.objects.all()
    context = {'quiz_list':quiz_list}

    return render(request, 'quizzes.html', context=context)
    

def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST or None)
        if form.is_valid:
            form.save()
        return redirect('show_quizzes')
    else:
        form = QuizForm

    context = {
        'form':form
    }
    return render(request, 'create_quiz.html', context=context)


def add_questions(request, quiz_slug):
    quiz = get_object_or_404(Quiz, slug=quiz_slug)

    if request.method == 'POST':
        question = QuestionForm(request.POST or None)
        if question.is_valid():
            Question.objects.create(
                question_text = request.POST['question_text'], quiz = quiz
            )

        return redirect('show_quizzes')

    else:
        question = QuestionForm
    context = {
        'form': question,
        'quiz': quiz,
    }

    return render(request, 'add_questions.html', context=context)


def add_choices(request, question_slug):
    question = Question.objects.get(slug=question_slug)

    if request.method == 'POST':
        choice = ChoiceForm(request.POST or None)
        if choice.is_valid():
            Choice.objects.create(
                choice_text = request.POST['choice_text'], question = question
            )
        return redirect('show_quizzes')
    else:
        choice = ChoiceForm
    context = {
        'form':choice,
        'question':question,
    }            

    return render(request, 'add_choices.html', context=context)


def GetQuestions(request, quiz_slug):

    quiz = get_object_or_404(Quiz, slug=quiz_slug)
    question_list = []

    for question in quiz.question_set.all():
        question_list.append(question)
    # print(question_list[0].question_text)
    context = {
        'quiz':quiz,
        'question_list':question_list,
    }

    return render(request, 'questions.html', context=context)
    

    ...


def QuizAnsweringView(request, quiz_slug):
    """for every question:
    1. display the question
    2. display the choices.

    if choices are selected and request is POST:
        3. create a question answer object for every question
        4. create a quiz answer object for all the question answer objects
        5. save selected choice, question answer, quiz answer objects


    Args:
        request ([http request]): [description]
        quiz_slug ([slug]): [arg to get a specific object from the models]
    """
    quiz = Quiz.objects.get(slug=quiz_slug)
    context = {
        'quiz':quiz,
    }
    return render(request, 'quizzes.html', context=context)

def QuizAnsweringView(request):
    ...
    """for every question:
    get the selected choice(answer)
    """

    
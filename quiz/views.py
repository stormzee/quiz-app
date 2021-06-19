from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .forms import QuizForm, QuestionForm, ChoiceForm
from .models import Quiz, Question, Choice, Question_Answer, Quiz_Answer

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
    questions = quiz.question_set.all()
    answered_quiz = Quiz_Answer(quiz=quiz)
    answered_quiz.save()
    
    for question in questions:

        if request.method == 'POST':
            selected_choice = Choice.objects.get(id=request.POST['choice'])
            answered_question = Question_Answer()
            answered_question.answer = selected_choice
            answered_question.quiz_answer = answered_quiz

    answered_quiz.save()



    context = {
        'quiz':quiz,
        'questions':questions,
    }

    return render(request, 'questions.html', context=context)



# Todo==> create a different view to handle answering of questions.
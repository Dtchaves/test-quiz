import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct


def test_add_multiple_choices_assigns_incremental_ids():
    question = Question(title='q1')

    first = question.add_choice('a')
    second = question.add_choice('b')

    assert first.id == 1
    assert second.id == 2


def test_add_choice_with_empty_text_raises_error():
    question = Question(title='q1')

    with pytest.raises(Exception):
        question.add_choice('')


def test_add_choice_with_text_longer_than_100_chars_raises_error():
    question = Question(title='q1')

    with pytest.raises(Exception):
        question.add_choice('a' * 101)


def test_remove_choice_by_id_removes_only_target_choice():
    question = Question(title='q1')
    first = question.add_choice('a')
    second = question.add_choice('b')

    question.remove_choice_by_id(first.id)

    assert len(question.choices) == 1
    assert question.choices[0].id == second.id


def test_remove_choice_by_id_with_invalid_id_raises_error():
    question = Question(title='q1')
    question.add_choice('a')

    with pytest.raises(Exception):
        question.remove_choice_by_id(999)


def test_remove_all_choices_clears_all_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')

    question.remove_all_choices()

    assert question.choices == []


def test_set_correct_choices_marks_only_selected_choices_as_correct():
    question = Question(title='q1')
    first = question.add_choice('a')
    second = question.add_choice('b')

    question.set_correct_choices([second.id])

    assert not first.is_correct
    assert second.is_correct


def test_set_correct_choices_with_invalid_id_raises_error():
    question = Question(title='q1')
    question.add_choice('a')

    with pytest.raises(Exception):
        question.set_correct_choices([999])


def test_correct_selected_choices_returns_only_selected_correct_ids():
    question = Question(title='q1', max_selections=2)
    first = question.add_choice('a', is_correct=True)
    second = question.add_choice('b', is_correct=False)
    third = question.add_choice('c', is_correct=True)

    corrected = question.correct_selected_choices([first.id, second.id])

    assert corrected == [first.id]
    assert third.id not in corrected


def test_correct_selected_choices_above_max_selections_raises_error():
    question = Question(title='q1', max_selections=1)
    first = question.add_choice('a', is_correct=True)
    second = question.add_choice('b', is_correct=False)

    with pytest.raises(Exception):
        question.correct_selected_choices([first.id, second.id])


@pytest.fixture
def question_with_multiple_choices():
    question = Question(title='q1', max_selections=2)
    first = question.add_choice('a', is_correct=True)
    second = question.add_choice('b', is_correct=False)
    third = question.add_choice('c', is_correct=False)
    return question, first, second, third


def test_fixture_based_correction_with_no_selection_returns_empty_list(question_with_multiple_choices):
    question, _, _, _ = question_with_multiple_choices

    corrected = question.correct_selected_choices([])

    assert corrected == []


def test_fixture_based_set_correct_choices_accumulates_correct_answers(question_with_multiple_choices):
    question, first, second, _ = question_with_multiple_choices

    question.set_correct_choices([second.id])
    corrected = question.correct_selected_choices([first.id, second.id])

    assert corrected == [first.id, second.id]
import React, { useState, useEffect } from 'react';
import './QuizView.scss';
import $ from 'jquery';

const questionsPerPlay = 5;

const QuizView = () => {
  const [ quizViewState, setQuizViewState ] = useState({
    quizCategory: null,
    previousQuestions: [],
    showAnswer: false,
    categories: {},
    numCorrect: 0,
    currentQuestion: {},
    guess: '',
    forceEnd: false
  })

  useEffect(() => {
    $.ajax({
      url: `http://localhost:5000/categories`,
      type: 'GET',
      success: (result) => {
        setQuizViewState({ ...quizViewState, categories: result.categories })
        return;
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again')
        return;
      }
    })
  }, []) //eslint-disable-line

  
  const selectCategory = ({ type, id=0 }) => {
    setQuizViewState({ ...quizViewState, quizCategory: {type, id}})
  }

  const handleChange = (e) => {
    setQuizViewState({ ...quizViewState, guess: e.target.value})
  }

  const getNextQuestion = () => {
    const previousQuestions = [...quizViewState.previousQuestions]
    if (quizViewState.currentQuestion.id) { previousQuestions.push(quizViewState.currentQuestion.id) }  

    $.ajax({
      url: 'http://localhost:5000/quizzes',
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        previous_questions: previousQuestions,
        quiz_category: quizViewState.quizCategory
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        setQuizViewState({...quizViewState,
          showAnswer: false,
          previousQuestions: previousQuestions,
          currentQuestion: result.question,
          guess: '',
          forceEnd: result.question ? false : true
        })
        return;
      },
      error: (error) => {
        alert('Unable to load question. Please try your request again')
        return;
      }
    })
  }
  
  useEffect(() => {
    if (quizViewState.quizCategory) {
      getNextQuestion()
    }
  }, [quizViewState.quizCategory]) //eslint-disable-line


  const evaluateAnswer = () => {
    const formatGuess = quizViewState.guess.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").toLowerCase() //eslint-disable-line
    if (formatGuess === quizViewState.currentQuestion.answer.toLowerCase()) {
      return true
    } else {
      const answerArray = quizViewState.currentQuestion.answer.toLowerCase().split(' ');
      return answerArray.includes(formatGuess)
    }
  }

  const submitGuess = (e) => {
    e.preventDefault()
    const formatGuess = quizViewState.guess.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").toLowerCase() //eslint-disable-line
    let evaluate = evaluateAnswer();
    setQuizViewState({
      ...quizViewState,
      numCorrect: !evaluate ? quizViewState.numCorrect : quizViewState.numCorrect + 1,
      showAnswer: true
    })
  }

  const restartGame = () => {
    setQuizViewState({
      ...quizViewState,
      quizCategory: null,
      previousQuestions: [],
      showAnswer: false,
      numCorrect: 0,
      currentQuestion: {},
      guess: '',
      forceEnd: false
    })
  }

  const renderPrePlay = () => {
    return (
      <div className='quiz-play-holder'>
        <div className="choose-header">Choose Category</div>
        <div className="category-holder">
          <div className="play-category" onClick={selectCategory}>ALL</div>
          {Object.keys(quizViewState.categories).map(id => {
          return (
            <div
              key={id}
              value={id}
              className="play-category"
              onClick={() => selectCategory({type: quizViewState.categories[id], id})}>
              {quizViewState.categories[id]}
            </div>)
          })}
        </div>
      </div>
    )
  }

  const renderFinalScore = () => {
    return(
      <div className="quiz-play-holder">
        <div className="final-header"> Your Final Score is {quizViewState.numCorrect}</div>
        <div className="play-again button" onClick={() => restartGame()}> Play Again? </div>
      </div>
    )
  }

  const renderCorrectAnswer = () => {
    const formatGuess = quizViewState.guess.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").toLowerCase() //eslint-disable-line
    let evaluate =  evaluateAnswer()
    return(
      <div className="quiz-play-holder">
        <div className="quiz-question">{quizViewState.currentQuestion.question}</div>
        <div className={`${evaluate ? 'correct' : 'wrong'}`}>{evaluate ? "You were correct!" : "You were incorrect"}</div>
        <div className="quiz-answer">{quizViewState.currentQuestion.answer}</div>
        <div className="next-question button" onClick={() => getNextQuestion()}> Next Question </div>
      </div>
    )
  }

  const renderPlay = () => {
    return quizViewState.previousQuestions.length === questionsPerPlay || quizViewState.forceEnd
      ? renderFinalScore()
      : quizViewState.showAnswer 
        ? renderCorrectAnswer()
        : (
          <div className="quiz-play-holder">
            <div className="quiz-question">{quizViewState.currentQuestion.question}</div>
            <form onSubmit={submitGuess}>
              <input type="text" name="guess" value={quizViewState.guess} onChange={handleChange}/>
              <input className="submit-guess button" type="submit" value="Submit Answer" />
            </form>
          </div>
        )
  }


  return ( 
    quizViewState.quizCategory
    ? renderPlay()
    : renderPrePlay()
  )
}

export default QuizView;
import React, { useState, useEffect } from 'react';
import './QuestionView.css';
import Search from '../Search/Search';
import $ from jquery;

const QuestionView = () => {
  const [ questionViewState, setQuestionViewState ] = useState({
    questions: [],
    page: 1,
    totalQuestions: 0,
    categories: {},
    currentCategory: null,
  })

  const getQuestions = () => {
    $.ajax({
      url: `/questions?page=${questionViewState.page}`, //TODO: update request url
      type: 'GET',
      success: (result) => {
        setQuestionViewState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          categories: result.categories,
          currentCategory: result.current_category
        })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  useEffect(() => {
    getQuestions();
  }, [])

  const selectPage(num) => {
    setQuestionViewState({...questionViewState, {page:num}}, () => getQuestions())
  }

  const createPagination = () => {
    let pageNumbers = [];
    let maxPage = Math.ceil(questionViewState.totalQuestions / 10)
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === questionViewState.page ? 'active' : ''}`}
          onClick={selectPage}>{i}
        </span>)
    }
    return pageNumbers;
  }

  const getByCategory = (id) => {
    $.ajax({
      url: `/categories/${id}/questions`, //TODO: update request URL
      type: 'GET',
      success: (result) => {
        setQuestionViewState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category
        })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  const submitSearch = () => {
    $.ajax({
      url: `/questions`, //TODO: update request URL
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({ searchTerm: searchTerm }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        setQuestionViewState({
          questions: result.questions,
          totalQuestion: result.total_questions,
          currentCategory: result.current_category
        })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  const questionAction = (id) => (action) => {
    if (action === 'DELETE') {
      if(window.confirm('Are you sure you want to delete the question?')) {
        $.ajax({
          url: `/questions/${id}`, //TODO: update request URL
          type: 'DELETE',
          success: (result) => {
            getQuestions();
          },
          error: (error) => {
            alert('Unable to load questions. Please try your request again')
            return;
          }
        })
      }
    }
  }

  return ( 
    <div className='question-view'>
      <div className='categories-list'>
        <h2 onClick={getQuestions}>Categories</h2>
        <ul>
          {}
        </ul>
      </div>
    </div>
  );
}

export default QuestionView;
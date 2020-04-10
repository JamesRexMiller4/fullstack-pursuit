import React, { useState, useEffect } from 'react';
import $ from 'jquery';
import './FormView.css';

const FormView = () => {
  const [ form, setForm ] = useState({
    questions: '',
    answer: '',
    difficulty: 1,
    category: 1,
    categories: {}
  })

  useEffect(() => {
    $.ajax({
      url: '/categories', //TODO: update request URL
      type: 'GET',
      success: (result) => {
        setForm({ ...form, categories: result.categories})
        return;
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again')
        return;
      }
    })
  }, [])

  const submitQuestion = (e) => {
    $.ajax({
      url: '/questions', //TODO: update request URL
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        question: form.question,
        answer: form.answer,
        difficulty: form.difficulty,
        category: form.category
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        document.getElementById('add-question-form').reset();
        return;
      },
      error: (error) => {
        alert('Unable to add question. Please try your request again')
        return;
      }
    })
  }

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  return (
    <div id="add-form">
      <h2>Add a New Trivia Question</h2>
      <form className="form-view" id='add-question-form' onSubmit={submitQuestion}>
        <label>
          Question
          <input type='text' name='question' onChange={handleChange} />
        </label>
        <label>
          Answer
          <input type='text' name='answer' onChange={handleChane} />
        </label>
        <label>
          Difficulty
          <select name='difficulty' onChange={handleChange}>
            <option value='1'>1</option>
            <option value='2'>2</option>
            <option value='3'>3</option>
            <option value='4'>4</option>
            <option value='5'>5</option>
          </select>
        </label>
        <label>
          Category
          <select name='category' onChange={handleChange}>
            {Object.keys(form.categories).map(id => {
              return (
                <option key={id} value={id}>{form.categories[id]}</option>
              )
            })}
          </select>
        </label>
        <input type="submit" className='button' value='Submit' />
      </form>
    </div>
  );
}

export default FormView;

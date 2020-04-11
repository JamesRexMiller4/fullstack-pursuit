import React, { useState } from 'react';
import './Question.css';

const Question = ({ question, questionAction, answer, category, difficulty }) => {
  const [ visibleAnswer, setVisibleAnswer ] = useState(false)

  const flipVisibility = () => {
    setVisibleAnswer({ visibleAnswer: !visibleAnswer})
  }

  return ( 
    <div className='Question-holder'>
      <div className='Question'>{question}</div>
      <div className='Question-status'>
        <img className='category' src={`${category}.svg`}/>
        <div className='difficulty'>Difficulty: {difficulty}</div>
        <img src='delete.png' className='delete' onClick={() => questionAction('DELETE')}/>
      </div>
      <div className='show-answer button' onClick={flipVisibility}>
        {visibleAnswer ? 'Hide' : 'Show'} Answer
      </div>
      <div className='answer-holder'>
        <span style={{"visibility": visibleAnswer ? 'visible': 'hidden'}}>Answer: {answer}</span>
      </div>
    </div>
  );
}

export default Question;
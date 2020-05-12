import React, {} from 'react';
import './Header.scss';

const Header = () => {
  const navTo = (uri) => {
    window.location.href = window.location.origin + uri;
  }

  return ( 
    <div className='App-header'>
      <h1 onClick={() => navTo('')}>FullStack-Trivia</h1>
      <h2 onClick={() => navTo('')}>List</h2>
      <h2 onClick={() => navTo('/add')}>Add</h2>
      <h2 onClick={() => navTo('/play')}>Play</h2>
    </div>
  );
}

export default Header;
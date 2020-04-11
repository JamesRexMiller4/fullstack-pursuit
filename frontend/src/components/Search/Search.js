import React, { useState, useRef } from 'react';
import './Search';

const Search = ({ submitSearch }) => {
  const [ search, setSearch ] = useState({
    query: ''
  });
  const inputEl = useRef(null);

  const getInfo = (e) => {
    submitSearch(search.query)
  }

  const handleInputChange = () => {
    setSearch({query: inputEl})
  }

  return ( 
    <form onSubmit={getInfo}>
      <input 
        placeholder="Search questions..."
        ref={inputEl}
        onChange={handleInputChange}/>
      <input type="submit" value='Submit' className='button' />
    </form>
  );
}

export default Search;
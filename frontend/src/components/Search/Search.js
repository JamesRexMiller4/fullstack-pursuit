import React, { useState, useRef } from 'react';
import './Search';

const Search = ({ submitSearch }) => {
  const [ search, setSearch ] = useState({
    searchTerm: ''
  });
  const inputEl = useRef(null);

  const getInfo = (e) => {
    e.preventDefault()
    submitSearch(search)
  }

  const handleInputChange = () => {
    setSearch({searchTerm: inputEl.current.value})
  }

  return ( 
    <form onSubmit={getInfo}>
      <input 
        placeholder="Search questions..."
        ref={inputEl}
        value={search.searchTerm}
        onChange={handleInputChange}/>
      <input type="submit" value='Submit' className='button' />
    </form>
  );
}

export default Search;
import React from 'react';
import { Header } from './component/layout/header';
import { SearchBar } from './component/search/searchbar';
import { SearchResults } from './component/search/searchres';
import { useState } from 'react';


const App= () => {
  const [searchResults, setSearchResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <SearchBar 
          setSearchResults={setSearchResults}
          setIsLoading={setIsLoading}
          setError={setError}
        />
        <SearchResults 
          results={searchResults}
          isLoading={isLoading}
          error={error}
        />
      </main>
    </div>
  );
};

export default App;

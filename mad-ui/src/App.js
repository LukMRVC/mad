import React from 'react';
import RandomGraphFrom from './RandomGraphForm';
import GraphAnalytics from './GraphAnalytics';

function App() {

  return (
    <div className="App">
      <h1>Analytické nástroje</h1>
      <main className="forms-wrapper">
        <div>
          <RandomGraphFrom />
        </div>
          <GraphAnalytics />
      </main>
    </div>
  );
}

export default App;

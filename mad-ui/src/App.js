import React, { useState } from 'react';

function App() {

  const [isFetching, setFetching] = useState(false);
  const [result, setResult] = useState('');


  async function handleSubmit(event) {
    event.preventDefault();
    const formValues = Object.fromEntries(new FormData(event.target));
    const endpoint = new URL(`http://localhost:8000/${formValues['graph-model']}`);
    endpoint.searchParams.append('nodes', formValues['nodes']);
    endpoint.searchParams.append('connection', formValues['connection']);
    endpoint.searchParams.append('steps', formValues['steps']);

    setFetching(true);
    try {
      const result = await fetch(endpoint.toString(), {
        timeout: 5000,
      });
      const jsonData = await result.json();
      if ('download' in formValues) {
        const edges = jsonData.edges.map((edge) => `${edge[0]},${edge[1]}`);
        const url = URL.createObjectURL(new Blob([edges.join('\n')]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'graph.txt');
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }

      setResult(jsonData);
    } catch (error) {
      console.error(error);
    } finally {
      setFetching(false);
    }
  }

  return (
    <div className="App">
      <h1>Generátor náhodného grafu</h1>
      <form onSubmit={handleSubmit} action="http://localhost:8000/ba">
        <label htmlFor="graph-model">Model grafu</label>
        <select required id="graph-model" name="graph-model">
          <option value="ba">Barabási–Albert</option>
        </select>

        <label htmlFor="nodes">Počáteční počet hran</label>
        <input required name="nodes" id="nodes" placeholder="5" type="number" />

        <label htmlFor="connection">Počer hran pro nový vrchol</label>
        <input required name="connection" id="connection" placeholder="5" type="number" />

        <label htmlFor="steps">Počer kroků</label>
        <input required name="steps" id="steps" placeholder="5" type="number" />

        <label htmlFor="download">
          <input name="download" id="download" placeholder="5" type="checkbox" value="true" />
          Stáhnout
        </label>

        <button disabled={isFetching} name="generate" value="gen" type="submit">Vygenerovat</button>
      </form>

      {result && 
        <pre>
          {JSON.stringify(result)}
        </pre>
      }
    </div>
  );
}

export default App;

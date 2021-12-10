import React, { useState } from 'react';
import { API_ENDPOINT } from './config';

export default function RandomGraphFrom() {

const [isFetching, setFetching] = useState(false);
const [result, setResult] = useState('');


async function handleSubmit(event) {
  event.preventDefault();
  const formValues = Object.fromEntries(new FormData(event.target));
  const endpoint = new URL(`${API_ENDPOINT}/${formValues['graph-model']}`);
  endpoint.searchParams.append('nodes', formValues['nodes']);
  endpoint.searchParams.append('connection', formValues['connection']);
  endpoint.searchParams.append('steps', formValues['steps']);

  if ('download' in formValues) {
    endpoint.searchParams.append('download', 1);
    window.open(endpoint.toString());
    return;
  }

  setFetching(true);
  try {
    const result = await fetch(endpoint.toString(), {
      timeout: 5000,
    });
    const jsonData = await result.json();
    setResult(jsonData);
  } catch (error) {
    console.error(error);
  } finally {
    setFetching(false);
  }
}

  return (
    <>
    <h2>Generátor náhodného grafu</h2>
      <form onSubmit={handleSubmit} action={`${API_ENDPOINT}/ba`}>
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
    </>
  );
}
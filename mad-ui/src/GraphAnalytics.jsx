import React, { useState, useMemo } from "react";
import { API_ENDPOINT } from "./config";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  RadialLinearScale,
  ArcElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";
import DataTable from "react-data-table-component";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  RadialLinearScale,
  ArcElement
);

export default function GraphAnalytics() {
  const [isFetching, setFetching] = useState(false);
  const [graphData, setGraphData] = useState(null);
  const [tableData, setTableData] = useState(null);

  useMemo(() => {
    if (graphData) {
      const { vertices } = graphData.graph;
      const data = vertices.map((vertex) => ({
        id: vertex,
        rank: graphData.ranks[vertex],
        centrality: graphData.centralities.centralities[vertex],
        meanDistance: graphData.centralities.meanDistances[vertex],
      }));
      setTableData(data);
    }
  }, [graphData]);

  const tableColumns = [
    {
      name: "Uzel",
      selector: (row) => row.id,
    },
    {
      name: "Stupeň",
      selector: (row) => row.rank,
      sortable: true,
    },
    {
      name: "Centralita",
      selector: (row) => row.centrality.toFixed(4),
      sortable: true,
    },
    {
      name: "Průměrná vzdálenost",
      selector: (row) => row.meanDistance.toFixed(4),
      sortable: true,
    },
  ];

  async function handleSubmit(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    setFetching(true);
    try {
      const response = await fetch(`${API_ENDPOINT}/analytics`, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setGraphData(data);
      console.log(response);
    } catch (error) {
      console.error(error);
    } finally {
      setFetching(false);
    }
  }

  function downloadData() {
    if (!graphData) {
      return;
    }
    const blob = new Blob([JSON.stringify(graphData)]);
    const link = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.style.display = 'none';
    anchor.href = link;
    anchor.download = 'graph-info.json';
    document.body.appendChild(anchor);
    anchor.click();
    URL.revokeObjectURL(link);
    document.body.removeChild(anchor);
  }

  let graphs = null;
  if (graphData) {
    const barChartData = {
      labels: Object.keys(graphData.distributionsOfRanks),
      datasets: [
        {
          label: "Distribuce stupňů",
          data: Object.values(graphData.distributionsOfRanks),
          backgroundColor: "rgba(255, 99, 132, 0.5)",
        },
      ],
    };

    graphs = (
      <>
        <ul>
          <li>Průměrný stupeň: <b>{graphData.globalRank.toFixed(4)}</b></li>
          <li>Průměr grafu: <b>{graphData.diameter}</b></li>
          <li>Průměrná globální vzdálenost: <b>{graphData.globalMeanDistance.toFixed(4)}</b></li>
        </ul>
        <Bar
          style={{ minWidth: "500px" }}
          options={{ responsive: true }}
          data={barChartData}
        />
        <DataTable pagination columns={tableColumns} data={tableData} />
      </>
    );
  }

  return (
    <div style={{flex: 1}} className="analytics">
      <h2>Grafový analyzátor</h2>
      <form onSubmit={handleSubmit} action={`${API_ENDPOINT}/analytics`}>
        <label htmlFor="graph">Graf</label>
        <input type="file" name="graph" id="graph" />

        <button disabled={isFetching} type="submit">
          {isFetching ? "Probíhá analýza" : "Analyzovat"}
        </button>
        {graphData && 
          <button onClick={downloadData} type="button">Stáhnout data</button>
        }
      </form>

      

      {graphData && graphs}
    </div>
  );
}

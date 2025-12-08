import { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
} from "chart.js";

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement);

export default function LineChartCard({ service }: { service: string }) {
  const [metricValues, setMetricValues] = useState<number[]>([]);
  const [metricLabels, setMetricLabels] = useState<string[]>([]);

  useEffect(() => {
    async function load() {
      const res = await fetch(`http://localhost:8000/status/service/${service}`);
      const data = await res.json();

      if (!data.metrics) return;

      setMetricLabels(Object.keys(data.metrics));
      setMetricValues(Object.values(data.metrics).map((v: any) => Number(v)));
    }
    load();
  }, [service]);

  const chartData = {
    labels: metricLabels,
    datasets: [
      {
        label: `Métricas — ${service}`,
        data: metricValues,
        borderColor: "#e879f9",
        backgroundColor: "rgba(232,121,249,0.25)",
        borderWidth: 2,
        tension: 0.3,
      },
    ],
  };

  return (
    <div className="bg-black/50 p-4 rounded-xl border border-fuchsia-700">
      <Line data={chartData} />
    </div>
  );
}

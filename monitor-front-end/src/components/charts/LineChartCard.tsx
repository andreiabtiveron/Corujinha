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
  const [labels, setLabels] = useState<string[]>([]);
  const [values, setValues] = useState<number[]>([]);

  useEffect(() => {
    async function load() {
      const res = await fetch(`http://localhost:8000/metrics/latest/${service}`);
      const data = await res.json();

      // Extrair SOMENTE UMA métrica (ex: latency_ms)
      const metricName = data[0]?.metric_name ?? "";
      const filtered = data.filter((m: any) => m.metric_name === metricName);

      setLabels(filtered.map((m: any) => m.timestamp.slice(11, 19)));
      setValues(filtered.map((m: any) => m.value));
    }
    load();
  }, [service]);

  const chartData = {
    labels,
    datasets: [
      {
        label: service.toUpperCase(),
        data: values,
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

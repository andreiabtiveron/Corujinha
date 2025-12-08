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
  const [values, setValues] = useState<number[]>([]);
  const [labels, setLabels] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const res = await fetch(`http://localhost:8000/metrics/latest/${service}`);
        const data = await res.json();

        // data é uma LISTA → converter para formato {nome: valor}
        const metricMap: Record<string, number> = {};
        data.forEach((m: any) => {
          metricMap[m.metric_name] = m.value;
        });

        setLabels(Object.keys(metricMap));
        setValues(Object.values(metricMap));
      } catch (e) {
        console.error("Erro ao carregar métricas", e);
      } finally {
        setLoading(false);
      }
    };

    fetchMetrics();
  }, [service]);

  if (loading) {
    return (
      <div className="bg-black p-3 rounded-xl border border-purple-800 text-center text-purple-300">
        Carregando...
      </div>
    );
  }

  const chartData = {
    labels,
    datasets: [
      {
        label: `Métricas — ${service}`,
        data: values,
        borderColor: "#e879f9",
        backgroundColor: "rgba(232, 121, 249, 0.3)",
        borderWidth: 2,
        tension: 0.3,
        pointRadius: 2,
      },
    ],
  };

  return (
    <div className="bg-black p-3 rounded-xl border border-purple-800">
      <Line data={chartData} />
    </div>
  );
}

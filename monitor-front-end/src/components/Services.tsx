import { useEffect, useState } from "react";
import LineChartCard from "./charts/LineChartCard";

export default function Services() {
  const [services, setServices] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/status/dashboard/all")
      .then((res) => res.json())
      .then((data) => setServices(data));
  }, []);

  return (
    <section className="w-full py-20">
      <h2 className="text-4xl font-bold text-center mb-12">Status dos Serviços</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 px-10">
        {services.map((s: any) => (
          <div
            key={s.key}
            className={`p-6 rounded-xl border ${
              s.status === "green"
                ? "border-green-500"
                : s.status === "yellow"
                ? "border-yellow-500"
                : "border-red-500"
            } bg-black/50`}
          >
            <h3 className="text-xl font-semibold">{s.name}</h3>
            <p className="mt-2">
              Status:{" "}
              <span
                className={
                  s.status === "green"
                    ? "text-green-400"
                    : s.status === "yellow"
                    ? "text-yellow-300"
                    : "text-red-400"
                }
              >
                {s.status.toUpperCase()}
              </span>
            </p>

            {/* Gráfico */}
            <div className="mt-4">
              <LineChartCard service={s.key} />
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

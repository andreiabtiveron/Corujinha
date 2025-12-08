import { useEffect, useState } from "react";
import LineChartCard from "./charts/LineChartCard";

export default function Services() {
  const [services, setServices] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/status/dashboard/all")
      .then((r) => r.json())
      .then((d) => setServices(d));
  }, []);

  return (
    <section id="services" className="w-full py-20">
      <h2 className="text-4xl font-bold text-center mb-12 drop-shadow-lg">
        Status dos Serviços
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 px-10">
        {services.map((s: any) => (
          <div
            key={s.key}
            className="p-6 rounded-xl bg-black/40 border border-fuchsia-600/40 backdrop-blur-lg shadow-xl"
          >
            <h3 className="text-xl font-semibold mb-2">{s.name}</h3>

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

            <div className="mt-4">
              <LineChartCard service={s.key} />
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

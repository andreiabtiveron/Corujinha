import { useEffect, useState } from "react";

export default function Dashboard() {
  const [services, setServices] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/status/dashboard/all")
      .then((r) => r.json())
      .then((d) => setServices(d));
  }, []);

  return (
    <section id="dashboard" className="py-24 text-center">
      <h2 className="text-4xl font-bold mb-6 drop-shadow-xl">
        Visão Consolidada
      </h2>

      <p className="opacity-80 text-lg max-w-2xl mx-auto mb-10">
        Veja métricas, gráficos e alertas agrupados de forma clara e elegante.
      </p>

      {/* GRID DE VISÃO RESUMIDA */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 px-10">
        {services.map((s: any) => (
          <div
            key={s.key}
            className="p-6 bg-black/40 backdrop-blur-lg border border-purple-600 rounded-xl shadow-xl"
          >
            <h3 className="text-xl font-bold mb-2">{s.name}</h3>

            <p
              className={
                s.status === "green"
                  ? "text-green-400"
                  : s.status === "yellow"
                  ? "text-yellow-300"
                  : "text-red-400"
              }
            >
              {s.status.toUpperCase()}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}

import { useEffect, useState } from "react";
import LineChartCard from "./charts/LineChartCard";

export default function Services() {
  const [services, setServices] = useState([]);

  // Carrega lista básica de serviços + status
  useEffect(() => {
    fetch("http://localhost:8000/status/dashboard/all")
      .then((r) => r.json())
      .then(async (basicList) => {
        // Para cada serviço, buscar as métricas completas
        const enriched = await Promise.all(
          basicList.map(async (svc: any) => {
            const detail = await fetch(`http://localhost:8000/status/service/${svc.key}`)
              .then((r) => r.json())
              .catch(() => null);

            return {
              ...svc,
              metrics: detail?.metrics || {},
            };
          })
        );

        setServices(enriched);
      });
  }, []);

  return (
    <section id="services" className="w-full py-20">
      <h2 className="text-4xl font-bold text-center mb-12 drop-shadow-lg">
        Status dos Serviços
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 px-10">
        {services.map((s: any) => {
          const m = s.metrics || {};

          return (
            <div
              key={s.key}
              className="p-6 rounded-xl bg-black/40 border border-fuchsia-600/40 backdrop-blur-lg shadow-xl"
            >
              <h3 className="text-xl font-semibold mb-2">{s.name}</h3>

              {/* STATUS */}
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

              {/* SEGURANÇA */}
              <div className="mt-4 text-sm space-y-1">
                <p className="font-semibold">Segurança:</p>

                <p>
                  🔥 Anomalia:{" "}
                  <span className={m.traffic_anomaly == 1 ? "text-red-400" : "text-green-400"}>
                    {m.traffic_anomaly == 1 ? "SIM" : "NÃO"}
                  </span>
                </p>

                <p>
                  🔐 Falhas de Login:{" "}
                  <span className={m.auth_failures > 0 ? "text-yellow-300" : "text-green-400"}>
                    {m.auth_failures || 0}
                  </span>
                </p>

                <p>
                  ⚠ Mudança de Configuração:{" "}
                  <span className={m.config_change == 1 ? "text-yellow-300" : "text-green-400"}>
                    {m.config_change == 1 ? "SIM" : "NÃO"}
                  </span>
                </p>

                <p>
                  🛑 Vulnerabilidade:{" "}
                  <span
                    className={m.known_vulnerability == 1 ? "text-red-400" : "text-green-400"}
                  >
                    {m.known_vulnerability == 1 ? "SIM" : "NÃO"}
                  </span>
                </p>
              </div>

              {/* GRÁFICO */}
              <div className="mt-4">
                <LineChartCard service={s.key} />
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}

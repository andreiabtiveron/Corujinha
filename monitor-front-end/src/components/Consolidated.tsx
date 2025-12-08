import { useEffect, useState } from "react";

export default function Consolidated() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    fetch("http://localhost:8000/status/consolidado")
      .then((r) => r.json())
      .then((d) => setData(d));
  }, []);

  if (!data) return null;

  return (
    <section id="consolidado" className="py-20 text-center">
      <h2 className="text-4xl font-bold mb-6 drop-shadow-xl">
        Visão Consolidada
      </h2>

      <p className="opacity-80 text-lg mb-6">
        Média de latência: {data.media_latencia} ms
      </p>

      <p
        className={
          data.health === "green"
            ? "text-green-400 text-xl font-semibold"
            : data.health === "yellow"
            ? "text-yellow-300 text-xl font-semibold"
            : "text-red-400 text-xl font-semibold"
        }
      >
        Status geral: {data.health}
      </p>
    </section>
  );
}

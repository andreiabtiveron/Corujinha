import { useEffect, useState } from "react";

interface ServiceStatus {
  key: string;
  name: string;
  status: string; // green | yellow | red
}

export default function Dashboard() {
  const [data, setData] = useState<ServiceStatus[]>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/status/dashboard/all")
      .then((res) => res.json())
      .then((json) => setData(json));
  }, []);

  const colors = {
    green: "bg-green-600 shadow-[0_0_20px_rgba(0,255,0,0.4)]",
    yellow: "bg-yellow-500 shadow-[0_0_20px_rgba(255,255,0,0.4)]",
    red: "bg-red-600 shadow-[0_0_20px_rgba(255,0,0,0.4)]",
  };

  return (
    <section id="dashboard" className="w-full py-24 bg-black relative">
      <h2 className="text-4xl font-bold text-center mb-12">Dashboard Geral</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 px-10">
        {data.map((s) => (
          <div
            key={s.key}
            className={`
              rounded-2xl p-6 text-center border border-purple-700
              hover:scale-105 transition-all duration-300
              bg-opacity-20 backdrop-blur-md cursor-pointer
              ${colors[s.status]}
            `}
          >
            <h3 className="text-xl font-semibold mb-2">{s.name}</h3>
            <p className="text-sm opacity-90">Status:</p>
            <span className="text-lg font-bold uppercase">{s.status}</span>
          </div>
        ))}
      </div>
    </section>
  );
}

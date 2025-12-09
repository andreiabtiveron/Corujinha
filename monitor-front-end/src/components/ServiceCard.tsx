import React from "react";

interface ServiceCardProps {
  name: string;
  status: string; // "green", "yellow", "red"
  metrics: any;
  last_alert?: {
    level: number;
    message: string;
  } | null;
}

export default function ServiceCard({ name, status, metrics, last_alert }: ServiceCardProps) {

  const statusColor =
    status === "green"
      ? "bg-green-600"
      : status === "yellow"
      ? "bg-yellow-500"
      : "bg-red-600";

  return (
    <div className="bg-gray-900 p-5 rounded-xl shadow-xl border border-gray-700 w-full text-white">
      
      {/* Nome do Serviço */}
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold">{name}</h2>
        <span className={`px-3 py-1 rounded-lg text-sm font-bold ${statusColor}`}>
          {status.toUpperCase()}
        </span>
      </div>

    
      {last_alert?.message && (
        <div className="mt-4 p-3 rounded-lg bg-red-900/40 border border-red-700">
          <p className="text-red-300 font-semibold">⚠ Motivo do alerta:</p>
          <p className="text-red-200 text-sm">{last_alert.message}</p>
        </div>
      )}

      {/*  Métricas principais */}
      <div className="mt-4 text-sm">
        <p><span className="text-gray-400">Latência:</span> {metrics.latency_ms ?? 0} ms</p>
        <p><span className="text-gray-400">Erros 4xx:</span> {metrics.http_4xx ?? 0}</p>
        <p><span className="text-gray-400">Erros 5xx:</span> {metrics.http_5xx ?? 0}</p>
        <p><span className="text-gray-400">Conexões ativas:</span> {metrics.open_connections ?? 0}</p>
        <p><span className="text-gray-400">Disponibilidade:</span> {metrics.availability === 1 ? "UP" : "DOWN"}</p>
      </div>

      {/*  Seção Segurança */}
      <div className="mt-5 p-3 rounded-lg bg-gray-800 border border-gray-700">
        <h3 className="font-semibold mb-2">🔐 Segurança</h3>

        <p><span className="text-gray-400">🔥 Anomalia:</span> {metrics.traffic_anomaly === 1 ? "SIM" : "NÃO"}</p>
        <p><span className="text-gray-400">🔐 Falhas de Login:</span> {metrics.auth_failures ?? 0}</p>
        <p><span className="text-gray-400">⚠ Mudança de Configuração:</span> {metrics.config_change === 1 ? "SIM" : "NÃO"}</p>
        <p><span className="text-gray-400">🛑 Vulnerabilidade:</span> {metrics.known_vulnerability === 1 ? "SIM" : "NÃO"}</p>
      </div>
    </div>
  );
}

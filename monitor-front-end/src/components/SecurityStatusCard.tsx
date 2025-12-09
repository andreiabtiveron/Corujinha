export default function SecurityStatusCard({ metrics }: any) {
  return (
    <div className="mt-4 p-4 rounded-lg bg-black/40 border border-purple-600/40">
      <h4 className="text-lg font-semibold mb-2">Segurança:</h4>

      <p>🔥 Anomalia: {metrics?.traffic_anomaly == 1 ? "SIM" : "NÃO"}</p>
      <p>🔐 Falhas de Login: {metrics?.auth_failures ?? 0}</p>
      <p>⚠ Mudança de Configuração: {metrics?.config_change == 1 ? "SIM" : "NÃO"}</p>
      <p>🛑 Vulnerabilidade: {metrics?.known_vulnerability == 1 ? "SIM" : "NÃO"}</p>
    </div>
  );
}

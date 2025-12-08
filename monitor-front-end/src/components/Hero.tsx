export default function Hero() {
  return (
    <section
      id="hero"
      className="
        w-full h-screen relative flex flex-col items-center justify-center
        bg-gradient-to-r from-purple-900 via-fuchsia-700 to-purple-900 overflow-hidden
      "
    >
      {/* Glow animado */}
      <div className="absolute inset-0 bg-gradient-to-r from-fuchsia-600 via-pink-500 to-fuchsia-600 opacity-30 blur-[120px] animate-pulse"></div>

      <h1 className="text-5xl md:text-6xl font-bold tracking-wide drop-shadow-xl">
        DevOps Monitoring Dashboard
      </h1>

      <p className="text-lg mt-4 opacity-80 max-w-xl text-center">
        Monitoramento em tempo real de Web, Banco de Dados, DNS e SMTP — tudo em um só lugar.
      </p>

      <a
        href="#dashboard"
        className="
          mt-8 px-8 py-3 bg-black bg-opacity-40 border border-fuchsia-400
          hover:bg-fuchsia-600 hover:border-fuchsia-200 hover:shadow-[0_0_25px_rgba(255,0,255,0.6)]
          transition-all duration-300 rounded-xl text-lg
        "
      >
        Ver Dashboard
      </a>
    </section>
  );
}


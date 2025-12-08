export default function Hero() {
  return (
    <section
      id="hero"
      className="
        w-full h-screen flex flex-col items-center justify-center
        text-center relative
      "
    >
      <h1 className="text-5xl md:text-6xl font-bold tracking-wider drop-shadow-lg">
        DevOps Monitoring Dashboard
      </h1>

      <p className="text-lg opacity-80 mt-4 max-w-xl">
        Monitoramento em tempo real de Web, Banco de Dados, DNS e SMTP.
      </p>

      <a
        href="#dashboard"
        className="
          mt-8 px-8 py-3 border border-fuchsia-400 bg-black/40 rounded-xl
          hover:bg-fuchsia-600 hover:border-fuchsia-200 hover:shadow-[0_0_25px_rgba(255,0,255,0.6)]
          transition-all duration-300 text-lg
        "
      >
        Ver Dashboard
      </a>
    </section>
  );
}

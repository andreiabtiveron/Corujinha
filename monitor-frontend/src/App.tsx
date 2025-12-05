export default function App() {
  return (
    <div className="w-full min-h-screen bg-black text-white scroll-smooth">

      {/* Seção 1 — Landing Page */}
      <section
        id="home"
        className="w-full h-screen bg-gradient-to-r from-purple-900 via-fuchsia-700 to-purple-900 relative overflow-hidden"
      >
        {/* Glow */}
        <div className="absolute inset-0 bg-gradient-to-r from-fuchsia-600 via-pink-500 to-fuchsia-600 opacity-30 blur-3xl"></div>

        {/* Navbar */}
        <nav className="absolute top-6 right-10 flex space-x-10 text-white text-sm font-light tracking-wide">
          <a href="#home" className="hover:text-fuchsia-300 duration-200">Home</a>
          <a href="#dashboard" className="hover:text-fuchsia-300 duration-200 font-semibold">
            Dashboard
          </a>
        </nav>

        {/* Logo */}
        <div className="absolute top-6 left-10">
          <div className="flex items-center space-x-2">
            <div className="w-4 h-4 border-t-2 border-l-2 border-fuchsia-400 rotate-45"></div>
            <span className="text-white tracking-widest text-xs">REDES</span>
          </div>
        </div>

        {/* Título */}
        <div className="w-full h-full flex items-center justify-center">
          <h1
            className="text-white text-7xl md:text-9xl font-bold tracking-wide drop-shadow-2xl"
            style={{ textShadow: "0 0 30px #ff00c8, 0 0 60px #ff00c8" }}
          >
            FRONT TESTE
          </h1>
        </div>

        {/* Rodapé */}
        <div className="absolute bottom-10 w-full text-center text-white tracking-widest text-xs opacity-80">
          TRABALHO DE CONCLUSÃO DE REDES
        </div>
      </section>

      {/* Seção 2 — Dashboard */}
      <section
        id="dashboard"
        className="min-h-screen bg-gradient-to-r from-purple-900 via-fuchsia-700 to-purple-900 pt-20 pb-32 relative overflow-hidden"
      >
        {/* Glow */}
        <div className="absolute inset-0 bg-gradient-to-r from-fuchsia-600 via-pink-500 to-fuchsia-600 opacity-30 blur-3xl"></div>

        {/* Título Dashboard */}
        <h1
          className="text-white text-5xl font-bold text-center mb-16 tracking-wide relative z-10"
          style={{ textShadow: "0 0 25px #ff00c8, 0 0 45px #ff00c8" }}
        >
          Dashboard de Monitoramento
        </h1>

        {/* Grid Neon */}
        <div className="relative z-10 grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-8 px-12">

          {/* Card */}
          <div className="p-6 rounded-2xl bg-black/40 border border-fuchsia-500/50 shadow-lg hover:shadow-fuchsia-500/50 duration-300 backdrop-blur-md">
            <ServiceCard 
              title="Web Server"
              status={level}     // verde/amarelo/vermelho
              latency={150}      
              rps={20}
            />

          </div>

          <div className="p-6 rounded-2xl bg-black/40 border border-fuchsia-500/50 shadow-lg hover:shadow-fuchsia-500/50 duration-300 backdrop-blur-md">
            <h2 className="text-xl font-semibold text-white" style={{ textShadow: "0 0 10px #ff00c8" }}>
              Banco de Dados
            </h2>
            <p className="mt-2 text-sm text-fuchsia-200/80">QPS, conexões, lentidão…</p>
          </div>

          <div className="p-6 rounded-2xl bg-black/40 border border-fuchsia-500/50 shadow-lg hover:shadow-fuchsia-500/50 duration-300 backdrop-blur-md">
            <h2 className="text-xl font-semibold text-white" style={{ textShadow: "0 0 10px #ff00c8" }}>
              DNS
            </h2>
            <p className="mt-2 text-sm text-fuchsia-200/80">Resolução, falhas…</p>
          </div>

          <div className="p-6 rounded-2xl bg-black/40 border border-fuchsia-500/50 shadow-lg hover:shadow-fuchsia-500/50 duration-300 backdrop-blur-md">
            <h2 className="text-xl font-semibold text-white" style={{ textShadow: "0 0 10px #ff00c8" }}>
              SMTP
            </h2>
            <p className="mt-2 text-sm text-fuchsia-200/80">Fila, falhas, throughput…</p>
          </div>

        </div>
      </section>

    </div>
  );
}

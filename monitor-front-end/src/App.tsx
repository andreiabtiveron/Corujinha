import React from "react";
import Hero from "./components/Hero";
import Services from "./components/Services";
import Dashboard from "./components/Dashboard";
import Footer from "./components/Footer";

/* Fundo Cyberpunk com animações e gradiente */
const CyberpunkBackground = React.memo(() => {
  return (
    <div className="absolute inset-0 -z-10">
      {/* Gradiente vertical */}
      <div className="absolute inset-0 bg-gradient-to-b from-purple-900 via-fuchsia-800/40 to-black"></div>

      {/* Linhas neon diagonais */}
      <div className="absolute inset-0 overflow-hidden">
        {Array.from({ length: 12 }).map((_, i) => (
          <div
            key={i}
            className="absolute w-full h-px bg-fuchsia-500/30"
            style={{
              top: `${i * 8}vh`,
              transform: "rotate(45deg)",
              animation: `moveLines ${10 + i}s linear infinite`,
            }}
          ></div>
        ))}
      </div>

      {/* Pontos neon */}
      {Array.from({ length: 25 }).map((_, i) => (
        <div
          key={i}
          className="absolute bg-fuchsia-300/60 rounded-full blur-sm animate-ping"
          style={{
            width: "5px",
            height: "5px",
            top: `${Math.random() * 100}%`,
            left: `${Math.random() * 100}%`,
            animationDuration: `${2 + Math.random() * 3}s`,
          }}
        ></div>
      ))}
    </div>
  );
});

export default function App() {
  return (
    <div className="relative w-full min-h-screen text-white overflow-x-hidden">
      <CyberpunkBackground />

      <div className="relative z-10">
        <Hero />
        <Services />
        <Dashboard />
        <Footer />
      </div>

      <style>
        {`@keyframes moveLines {
          0% { transform: translateX(-100%) rotate(45deg); }
          100% { transform: translateX(100%) rotate(45deg); }
        }`}
      </style>
    </div>
  );
}

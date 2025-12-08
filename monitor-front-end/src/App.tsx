import Hero from "./components/Hero";
import Services from "./components/Services";
import Dashboard from "./components/Dashboard";
import Consolidated from "./components/Consolidated";
import Footer from "./components/Footer";

export default function App() {
  return (
    <div className="w-full min-h-screen text-white overflow-x-hidden bg-gradient-to-b from-purple-900 via-fuchsia-800/40 to-black">
      {/* Conteúdo principal */}
      <Hero />
      <Services />
      <Dashboard />
      <Consolidated />
      <Footer />
    </div>
  );
}

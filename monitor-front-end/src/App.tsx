import Hero from "./components/Hero";
import Services from "./components/Services";
import Footer from "./components/Footer";

export default function App() {
  return (
    <div className="w-full min-h-screen bg-black text-white scroll-smooth">
      <Hero />
      <Services />
      <Footer />
    </div>
  );
}

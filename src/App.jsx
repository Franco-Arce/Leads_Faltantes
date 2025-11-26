import React, { useState } from 'react';
import {
  LayoutDashboard,
  BarChart3,
  PieChart,
  LineChart,
  TrendingUp,
  Users,
  GraduationCap,
  Building2,
  X,
  ChevronRight,
  Activity
} from 'lucide-react';

// --- Mock Data ---

const universities = [
  {
    id: 'cesa',
    name: 'CESA',
    logo: '/assets/cesa.png',
    color: 'bg-blue-600',
    dashboards: [
      { id: 'd1', title: 'Cesa Admisiones', description: 'Análisis detallado de admisiones y estadísticas de aspirantes.', icon: <Users className="w-8 h-8 text-blue-600" />, url: 'https://app.powerbi.com/reportEmbed?reportId=109bdd63-f82f-4ed3-b9f4-52b7ff58ff34&autoAuth=true&ctid=8185a0e8-8820-49e3-afe3-940ab308e861' },
      { id: 'd2', title: 'Cesa Servicios', description: 'Visión general de los servicios institucionales y su utilización.', icon: <TrendingUp className="w-8 h-8 text-indigo-600" />, url: 'https://app.powerbi.com/reportEmbed?reportId=9efb2c3b-8efe-4837-bb9f-52961655bee7&autoAuth=true&ctid=8185a0e8-8820-49e3-afe3-940ab308e861' },
      { id: 'd3', title: 'Cesa Zoom', description: 'Métricas de uso de aulas virtuales y sesiones de Zoom.', icon: <Activity className="w-8 h-8 text-purple-600" />, url: 'https://app.powerbi.com/reportEmbed?reportId=bcd3318e-5657-430c-b72a-75fff0e134ea&autoAuth=true&ctid=8185a0e8-8820-49e3-afe3-940ab308e861' },
    ]
  },
  {
    id: 'andes',
    name: 'Universidad de los Andes',
    logo: '/assets/andes.png',
    color: 'bg-yellow-500',
    dashboards: [
      { id: 'd4', title: 'Ventas Nods Neotel', description: 'Reporte detallado de ventas y seguimiento de métricas comerciales.', icon: <BarChart3 className="w-8 h-8 text-yellow-600" />, url: 'https://app.powerbi.com/reportEmbed?reportId=eaf2a561-0504-4de8-803e-7627a9b77214&autoAuth=true&ctid=8185a0e8-8820-49e3-afe3-940ab308e861' },
    ]
  },
  {
    id: 'jala',
    name: 'Jala University',
    logo: '/assets/jala.png',
    color: 'bg-teal-500',
    dashboards: [
      { id: 'd6', title: 'Marketing Analytics', description: 'Análisis de campañas de marketing y métricas de conversión.', icon: <BarChart3 className="w-8 h-8 text-teal-600" />, url: 'https://app.powerbi.com/reportEmbed?reportId=05df31df-53e9-4d2c-aee5-263b0c5286c5&autoAuth=true&ctid=8185a0e8-8820-49e3-afe3-940ab308e861' },
      { id: 'd7', title: 'Reporte Budget', description: 'Seguimiento detallado del presupuesto y ejecución financiera.', icon: <TrendingUp className="w-8 h-8 text-cyan-600" />, url: 'https://app.powerbi.com/reportEmbed?reportId=60a3ba4f-bf73-4508-ae51-17bce9e67da0&autoAuth=true&ctid=8185a0e8-8820-49e3-afe3-940ab308e861' },
      { id: 'd8', title: 'Tablero General', description: 'Visión consolidada con bases de datos Azure.', icon: <LineChart className="w-8 h-8 text-emerald-600" />, url: 'https://app.powerbi.com/reportEmbed?reportId=69df3ce6-6bbe-4b4a-8295-749b31488d0a&autoAuth=true&ctid=8185a0e8-8820-49e3-afe3-940ab308e861' },
    ]
  },
  {
    id: 'uic',
    name: 'UIC',
    logo: '/assets/uic.png',
    color: 'bg-red-600',
    dashboards: [
      { id: 'd9', title: 'Performance Admisiones', description: 'Análisis de rendimiento de admisiones y métricas clave.', icon: <Building2 className="w-8 h-8 text-red-600" />, url: 'https://app.powerbi.com/reportEmbed?reportId=97fdce72-fe30-4be4-b03a-23c6409941d4&autoAuth=true&ctid=8185a0e8-8820-49e3-afe3-940ab308e861' },
    ]
  },
  {
    id: 'unab',
    name: 'UNAB',
    logo: '/assets/unab.png',
    color: 'bg-orange-500',
    dashboards: [
      { id: 'd11', title: 'Performance y estados', description: 'Análisis detallado de rendimiento y estados operativos.', icon: <PieChart className="w-8 h-8 text-orange-600" />, url: 'https://app.powerbi.com/reportEmbed?reportId=7bb2982d-9344-46f4-8ecd-76524ab78b15&autoAuth=true&ctid=8185a0e8-8820-49e3-afe3-940ab308e861' },
    ]
  },
];

// --- Components ---

const SidebarItem = ({ university, isSelected, onClick }) => (
  <button
    onClick={() => onClick(university)}
    className={`w-full flex items-center gap-3 px-4 py-3.5 transition-all duration-300 group relative overflow-hidden ${isSelected
      ? 'text-white'
      : 'text-slate-400 hover:text-slate-100'
      }`}
  >
    {isSelected && (
      <div className="absolute inset-0 bg-gradient-to-r from-blue-600/20 to-transparent border-l-4 border-blue-500 animate-in fade-in slide-in-from-left-2 duration-300"></div>
    )}
    <div className={`relative z-10 w-9 h-9 rounded-lg flex items-center justify-center bg-white p-1.5 shadow-lg overflow-hidden transition-transform duration-300 ${isSelected ? 'scale-105 ring-2 ring-blue-500/50' : 'group-hover:scale-105'}`}>
      <img src={university.logo} alt={university.name} className="w-full h-full object-contain" />
    </div>
    <span className={`relative z-10 font-medium text-sm tracking-wide text-left transition-colors duration-300 ${isSelected ? 'text-white font-semibold' : ''}`}>
      {university.name}
    </span>
    {isSelected && <ChevronRight className="relative z-10 w-4 h-4 ml-auto text-blue-400 animate-pulse" />}
  </button>
);

const DashboardCard = ({ dashboard, onOpen }) => (
  <div className="bg-white rounded-2xl shadow-sm hover:shadow-xl transition-all duration-300 overflow-hidden group flex flex-col h-full border border-slate-100">
    {/* Top Section - Dark Preview */}
    <div
      onClick={() => onOpen(dashboard)}
      className="h-48 bg-slate-900 relative overflow-hidden group-hover:scale-105 transition-transform duration-700 cursor-pointer"
    >
      {/* Abstract Dashboard UI Pattern */}
      <div className="absolute inset-0 opacity-20 pointer-events-none">
        <div className="absolute top-4 left-4 right-4 h-2 bg-slate-700 rounded-full"></div>
        <div className="absolute top-10 left-4 w-1/3 h-20 bg-slate-800 rounded-lg"></div>
        <div className="absolute top-10 right-4 w-1/2 h-20 bg-slate-800 rounded-lg"></div>
        <div className="absolute bottom-4 left-4 right-4 h-8 bg-slate-800 rounded-lg"></div>
      </div>

      {/* Overlay Gradient */}
      <div className="absolute inset-0 bg-gradient-to-t from-slate-900/80 to-transparent pointer-events-none"></div>

      {/* Centered Button */}
      <div className="absolute inset-0 flex items-center justify-center z-10">
        <button
          onClick={(e) => {
            e.stopPropagation();
            onOpen(dashboard);
          }}
          className="group/btn relative px-6 py-2.5 bg-slate-800/40 backdrop-blur-md border border-white/20 rounded-full text-white text-sm font-medium hover:bg-white hover:text-slate-900 transition-all duration-300 flex items-center gap-2 shadow-lg"
        >
          <span>Ver Dashboard</span>
          <LayoutDashboard className="w-3 h-3 group-hover/btn:translate-x-0.5 transition-transform" />
        </button>
      </div>
    </div>

    {/* Bottom Section - Content */}
    <div className="p-6 flex flex-col flex-grow relative">
      <div className="flex items-start justify-between mb-4">
        <div className="w-10 h-10 rounded-lg bg-blue-50 flex items-center justify-center text-blue-600">
          {dashboard.icon}
        </div>
        <span className="px-2 py-1 rounded bg-slate-100 text-[10px] font-bold text-slate-500 tracking-wider uppercase">
          Reporte
        </span>
      </div>

      <h3 className="text-lg font-bold text-blue-700 mb-2 leading-tight">
        {dashboard.title}
      </h3>

      <p className="text-slate-500 text-sm leading-relaxed line-clamp-3">
        {dashboard.description}
      </p>
    </div>
  </div>
);

const PowerBIModal = ({ isOpen, onClose, dashboard }) => {
  if (!isOpen || !dashboard) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6">
      <div
        className="absolute inset-0 bg-slate-950/70 backdrop-blur-md transition-opacity duration-300"
        onClick={onClose}
      ></div>
      <div className="relative w-full max-w-[90vw] h-[90vh] bg-white rounded-2xl shadow-2xl flex flex-col overflow-hidden animate-in fade-in zoom-in-95 duration-300 border border-slate-200/50 ring-1 ring-slate-900/5">
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100 bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/60 z-10">
          <div className="flex items-center gap-4">
            <div className="p-2.5 bg-slate-50 rounded-xl border border-slate-100 shadow-sm">
              {dashboard.icon}
            </div>
            <div>
              <h2 className="text-xl font-bold text-slate-900 tracking-tight">{dashboard.title}</h2>
              <p className="text-xs font-medium text-slate-500 uppercase tracking-wider">Reporte Power BI Integrado</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-slate-400 hover:text-slate-900 hover:bg-slate-100 rounded-full transition-all duration-200 transform hover:rotate-90"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        <div className="flex-grow bg-slate-50/50 p-0 relative">
          {dashboard.url ? (
            <div className="w-full h-full bg-white">
              <iframe
                title={dashboard.title}
                src={dashboard.url}
                className="w-full h-full border-0"
                allowFullScreen={true}
              />
            </div>
          ) : (
            <div className="w-full h-full bg-slate-50 flex flex-col items-center justify-center text-slate-400">
              <div className="w-20 h-20 bg-slate-100 rounded-full flex items-center justify-center mb-6 animate-pulse">
                <BarChart3 className="w-10 h-10 text-slate-300" />
              </div>
              <p className="text-xl font-semibold text-slate-700">Próximamente</p>
              <p className="text-sm text-slate-500 mt-2 max-w-md text-center">Este tablero está en desarrollo y estará disponible pronto.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// --- Main App Component ---

function App() {
  const [selectedUniversity, setSelectedUniversity] = useState(universities[0]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentDashboard, setCurrentDashboard] = useState(null);

  const handleOpenDashboard = (dashboard) => {
    setCurrentDashboard(dashboard);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setTimeout(() => setCurrentDashboard(null), 200); // Clear after animation
  };

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden font-sans selection:bg-blue-100 selection:text-blue-900">
      {/* Sidebar */}
      <aside className="w-72 bg-slate-950 flex flex-col shadow-2xl z-20 flex-shrink-0 border-r border-slate-800/50">
        <div className="h-24 flex items-center justify-center border-b border-slate-800/50 bg-slate-950 w-full px-6">
          <img
            src="/assets/nods-white.png"
            alt="NODS Technology"
            className="h-14 w-auto object-contain opacity-90 hover:opacity-100 transition-opacity duration-300"
          />
        </div>

        <div className="flex-grow py-8 overflow-y-auto custom-scrollbar">
          <div className="px-8 mb-4">
            <h3 className="text-[11px] font-bold text-slate-500 uppercase tracking-[0.2em]">Clientes</h3>
          </div>
          <nav className="space-y-1 px-4">
            {universities.map((uni) => (
              <SidebarItem
                key={uni.id}
                university={uni}
                isSelected={selectedUniversity.id === uni.id}
                onClick={setSelectedUniversity}
              />
            ))}
          </nav>
        </div>

        <div className="p-6 border-t border-slate-800/50 bg-slate-900/30">
          <div className="flex items-center gap-4 px-2 py-2 rounded-xl hover:bg-slate-800/50 transition-colors cursor-pointer group">
            <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-xs font-bold text-white shadow-lg ring-2 ring-slate-800 group-hover:ring-slate-700 transition-all">
              GN
            </div>
            <div className="flex flex-col">
              <span className="text-sm font-semibold text-slate-200 group-hover:text-white transition-colors">Grupo Nods</span>
              <span className="text-xs text-slate-500 group-hover:text-slate-400 transition-colors">Administrador</span>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-grow flex flex-col h-screen overflow-hidden bg-slate-50 relative">
        {/* Background Pattern */}
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px] pointer-events-none"></div>
        <div className="absolute inset-0 bg-gradient-to-tr from-slate-50 via-white to-blue-50/30 pointer-events-none"></div>

        {/* Header */}
        <header className="h-20 bg-white border-b border-slate-200 flex items-center justify-between px-10 flex-shrink-0 z-10 sticky top-0">
          <div className="flex items-center gap-4">
            <h1 className="text-2xl font-bold text-slate-900 tracking-tight">{selectedUniversity.name}</h1>
            <span className="px-3 py-1 rounded-full bg-emerald-100 text-emerald-700 text-[10px] font-bold tracking-wide uppercase">
              Activo
            </span>
          </div>
          <div className="flex items-center gap-6">
            {/* Icons removed as requested */}
          </div>
        </header>

        {/* Dashboard Grid */}
        <div className="flex-grow overflow-y-auto p-10 relative z-0">
          <div className="max-w-7xl mx-auto">

            {/* Hero Banner */}
            <div className="mb-10 relative overflow-hidden rounded-3xl bg-slate-900 text-white shadow-2xl">
              <div className="absolute top-0 right-0 -mt-20 -mr-20 w-96 h-96 bg-blue-600/20 rounded-full blur-3xl"></div>
              <div className="absolute bottom-0 left-0 -mb-20 -ml-20 w-80 h-80 bg-indigo-600/20 rounded-full blur-3xl"></div>
              <div className="relative p-10 md:p-12">
                <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
                  <div className="max-w-2xl">
                    <span className="inline-block text-blue-400 font-bold tracking-wider text-xs uppercase mb-3">Portal de Cliente</span>
                    <h2 className="text-3xl md:text-4xl font-bold text-white mb-4 tracking-tight">{selectedUniversity.name}</h2>
                    <p className="text-slate-400 text-lg leading-relaxed">
                      Acceda a los módulos de gestión, métricas en tiempo real y reportes consolidados para esta institución.
                    </p>
                  </div>
                  {/* Optional: Add a visual element or logo watermark here if needed */}
                </div>
              </div>
            </div>

            <div className="mb-8 flex items-center justify-between">
              <h2 className="text-xl font-bold text-slate-900 tracking-tight">Tableros Disponibles</h2>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 pb-10">
              {selectedUniversity.dashboards.map((dashboard) => (
                <DashboardCard
                  key={dashboard.id}
                  dashboard={dashboard}
                  onOpen={handleOpenDashboard}
                />
              ))}
            </div>
          </div>
        </div>
      </main>

      {/* Modal */}
      <PowerBIModal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        dashboard={currentDashboard}
      />
    </div>
  );
}

export default App;

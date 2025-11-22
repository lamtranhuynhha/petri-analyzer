import React from 'react';
import usePetriNetStore from '../../hooks/usePetriNet';
import PropertiesTab from './PropertiesTab';
import AnalysisTab from './AnalysisTab';
import SimulationTab from './SimulationTab';

/**
 * Right Sidebar Component - Container cho 3 tabs
 */
const RightSidebar = ({ onAnalyze }) => {
  const { activeTab, setActiveTab } = usePetriNetStore();
  
  const tabs = [
    { id: 'properties', label: 'Props', component: PropertiesTab },
    { id: 'analysis', label: 'Analysis', component: AnalysisTab },
    { id: 'simulation', label: 'Sim', component: SimulationTab },
  ];
  
  const ActiveComponent = tabs.find(t => t.id === activeTab)?.component || PropertiesTab;
  
  return (
    <div className="w-sidebar bg-white border-l border-gray-300 flex flex-col z-sidebar">
      {/* Tab Headers */}
      <div className="flex border-b border-gray-300">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`
              flex-1 py-3 text-sm font-medium transition-colors duration-200
              ${activeTab === tab.id
                ? 'text-primary-600 border-b-2 border-primary-600 bg-primary-50'
                : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50'
              }
            `}
          >
            {tab.label}
          </button>
        ))}
      </div>
      
      {/* Tab Content */}
      <div className="flex-1 overflow-hidden">
        {activeTab === 'properties' && <PropertiesTab />}
        {activeTab === 'analysis' && <AnalysisTab onAnalyze={onAnalyze} />}
        {activeTab === 'simulation' && <SimulationTab />}
      </div>
    </div>
  );
};

export default RightSidebar;



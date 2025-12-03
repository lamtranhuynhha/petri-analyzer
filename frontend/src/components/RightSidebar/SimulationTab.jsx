import React from 'react';
import { FaFire, FaRedo, FaPlay, FaPause, FaStepForward, FaTrash, FaFileExport } from 'react-icons/fa';
import usePetriNetStore from '../../hooks/usePetriNet';

/**
 * Simulation Tab - Mô phỏng firing transitions
 */
const SimulationTab = () => {
  const {
    currentMarking = {},
    initialMarking = {},
    simulationHistory = [],
    isSimulating,
    resetToInitialMarking,
    fireTransition,
    getEnabledTransitions,
    startAutoPlay,
    stopAutoPlay,
    places = [],
    exportTrace,
  } = usePetriNetStore();
  
  const [autoPlaySpeed, setAutoPlaySpeed] = React.useState(1000);
  
  const enabledTransitions = getEnabledTransitions() || [];
  
  const handleFire = (transitionId) => {
    fireTransition(transitionId);
  };
  
  const handleRandomFire = () => {
    if (enabledTransitions.length > 0) {
      const randomTransition = enabledTransitions[Math.floor(Math.random() * enabledTransitions.length)];
      handleFire(randomTransition.id);
    }
  };
  
  const handleAutoPlay = () => {
    if (isSimulating) {
      stopAutoPlay();
    } else {
      startAutoPlay(autoPlaySpeed);
    }
  };
  
  const markingVector = places.map(p => currentMarking[p.id] || 0);
  const stepCount = simulationHistory.length;
  
  return (
    <div className="p-4 space-y-4 overflow-y-auto h-full">
      
      {/* CURRENT STATE */}
      <div className="card p-3">
        <div className="font-semibold text-gray-800 mb-2"> CURRENT STATE</div>
        
        <div className="space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-600">Marking:</span>
            <span className="font-mono font-semibold">
              ({markingVector.join(', ')})
            </span>
          </div>
          
          <div className="flex justify-between">
            <span className="text-gray-600">Step:</span>
            <span className="font-semibold">{stepCount}</span>
          </div>
          
          {/* Vector view */}
          <div className="bg-gray-50 p-2 rounded mt-2">
            <div className="text-xs text-gray-500 mb-1">Vector view:</div>
            <div className="grid grid-cols-2 gap-1">
              {places.map(place => (
                <div key={place.id} className="text-xs flex justify-between">
                  <span className="text-gray-700">{place.id}:</span>
                  <span className="font-semibold">{currentMarking[place.id] || 0}</span>
                </div>
              ))}
            </div>
          </div>
          
          <button
            onClick={resetToInitialMarking}
            className="w-full btn-secondary btn-sm flex items-center justify-center gap-2 mt-2"
          >
            <FaRedo />
            Reset to M0
          </button>
        </div>
      </div>
      
      {/* ENABLED TRANSITIONS */}
      <div className="card p-3">
        <div className="font-semibold text-gray-800 mb-2">
           ENABLED TRANSITIONS ({enabledTransitions.length})
        </div>
        
        {enabledTransitions.length > 0 ? (
          <div className="space-y-2">
            {enabledTransitions.map(trans => (
              <div
                key={trans.id}
                className="flex items-center justify-between p-2 bg-green-50 rounded"
              >
                <span className="text-sm font-medium text-green-800">
                  ✅ {trans.label || trans.id}
                </span>
                <button
                  onClick={() => handleFire(trans.id)}
                  className="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700 text-sm flex items-center gap-1"
                >
                  <FaFire />
                  Fire
                </button>
              </div>
            ))}
            
            <button
              onClick={handleRandomFire}
              className="w-full btn-secondary btn-sm mt-2"
            >
               Random Fire
            </button>
          </div>
        ) : (
          <div className="text-sm text-gray-500 italic p-2 bg-gray-50 rounded">
            No enabled transitions (deadlock state)
          </div>
        )}
      </div>
      
      {/* AUTO PLAY */}
      <div className="card p-3">
        <div className="font-semibold text-gray-800 mb-2"> AUTO PLAY</div>
        
        <div className="space-y-2">
          <div className="flex gap-2">
            <button
              onClick={handleAutoPlay}
              className={`flex-1 btn-sm flex items-center justify-center gap-2 ${
                isSimulating ? 'btn-danger' : 'btn-primary'
              }`}
            >
              {isSimulating ? (
                <>
                  <FaPause />
                  Pause
                </>
              ) : (
                <>
                  <FaPlay />
                  Play
                </>
              )}
            </button>
            
            <button
              onClick={handleRandomFire}
              disabled={enabledTransitions.length === 0}
              className="btn-secondary btn-sm"
            >
              <FaStepForward />
            </button>
          </div>
          
          <div>
            <label className="text-xs text-gray-600">
              Speed: {autoPlaySpeed}ms
            </label>
            <input
              type="range"
              min="100"
              max="3000"
              step="100"
              value={autoPlaySpeed}
              onChange={(e) => setAutoPlaySpeed(parseInt(e.target.value))}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-gray-500">
              <span>Fast</span>
              <span>Slow</span>
            </div>
          </div>
        </div>
      </div>
      
      {/* FIRING HISTORY */}
      <div className="card p-3">
        <div className="flex items-center justify-between mb-2">
          <div className="font-semibold text-gray-800"> FIRING HISTORY</div>
          <button
            onClick={() => {
              resetToInitialMarking();
            }}
            className="text-xs text-red-600 hover:text-red-800"
            title="Clear history"
          >
            <FaTrash />
          </button>
        </div>
        
        {simulationHistory.length > 0 ? (
          <div className="space-y-1 max-h-48 overflow-y-auto">
            <div className="text-xs text-gray-600 p-1 bg-blue-50 rounded">
              M0: ({Object.values(initialMarking).join(',')})
            </div>
            {simulationHistory.map((entry, idx) => {
              const markingVector = places.map(p => entry.marking[p.id] || 0);
              return (
                <div key={idx} className="text-xs text-gray-700 p-1 hover:bg-gray-50 rounded">
                  <span className="text-blue-600">--{entry.transition}→</span> M{idx + 1}: ({markingVector.join(',')})
                </div>
              );
            })}
            <div className="text-xs text-green-600 font-semibold p-1 bg-green-50 rounded">
              ← Current: ({markingVector.join(',')})
            </div>
          </div>
        ) : (
          <div className="text-sm text-gray-500 italic p-2 bg-gray-50 rounded">
            No firing history yet
          </div>
        )}
        
        {simulationHistory.length > 0 && (
          <button
            onClick={() => exportTrace('txt')}
            className="w-full btn-secondary btn-sm mt-2 flex items-center justify-center gap-2"
          >
            <FaFileExport />
            Export Trace
          </button>
        )}
      </div>
      
    </div>
  );
};

export default SimulationTab;



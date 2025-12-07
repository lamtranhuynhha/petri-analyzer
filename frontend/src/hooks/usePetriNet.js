import { create } from 'zustand';

/**
 * Zustand store cho Petri Net state management
 * Quản lý toàn bộ state của ứng dụng: model, UI, simulation, analysis
 */
const usePetriNetStore = create((set, get) => ({
  // ============ PETRI NET MODEL ============
  places: [],
  transitions: [],
  arcs: [],
  weights: {},
  initialMarking: {},
  
  // ============ UI STATE ============
  selectedTool: 'select',
  selectedElement: null,
  activeTab: 'properties',
  firstSelectedNode: null,
  
  // ============ MODALS ============
  modals: {
    reachabilityGraph: false,
    coverabilityTree: false,
    export: false,
    confirm: false,
    welcome: false, // Đảm bảo có cái này để không lỗi WelcomeModal
  },
  confirmAction: null,
  
  // ============ SIMULATION STATE ============
  currentMarking: {},
  simulationHistory: [],
  isSimulating: false,
  autoPlayInterval: null,
  
  // ============ ANALYSIS RESULTS ============
  analysisResults: {
    reachability: null,
    deadlock: null,
    boundedness: null,
    liveness: null,
    siphonsTraps: null,
  },
  
  // ============ STATUS ============
  status: {
    isBounded: null,
    elementCount: { places: 0, transitions: 0 },
    stateCount: 0,
    hasWarning: false,
    warningMessage: '',
  },
  
  // ============ UNDO/REDO ============
  history: [],
  historyIndex: -1,
  maxHistory: 50,

  // ============ LOADING STATE ============
  loading: {
    reachability: false,
    boundedness: false,
    liveness: false,
    siphonsTraps: false,
    upload: false,
  },
  
  // ============ ACTIONS - Model Management ============
  
  addPlace: (place) => set((state) => {
    if (state.isSimulating) {
      console.warn('Cannot add place while auto play is running. Please pause first.');
      return state;
    }

    get().saveToHistory();

    const newMarking = { ...state.initialMarking, [place.id]: place.tokens || 0 };
    
    const shouldReset = state.simulationHistory.length > 0;
    
    if (shouldReset) {
      const resetPlaces = state.places.map(p => ({
        ...p,
        tokens: state.initialMarking[p.id] || 0
      }));
      
      resetPlaces.push({
        ...place,
        tokens: place.tokens || 0
      });
      
      if (state.autoPlayInterval) {
        clearInterval(state.autoPlayInterval);
      }
      
      return {
        places: resetPlaces,
        initialMarking: newMarking,
        currentMarking: newMarking,
        simulationHistory: [],
        isSimulating: false,
        autoPlayInterval: null,
        status: { ...state.status, elementCount: { ...state.status.elementCount, places: resetPlaces.length } }
      };
    }
    
    const newPlaces = [...state.places, place];
    
    return {
      places: newPlaces,
      initialMarking: newMarking,
      currentMarking: { ...state.currentMarking, [place.id]: place.tokens || 0 },
      status: { ...state.status, elementCount: { ...state.status.elementCount, places: newPlaces.length } }
    };
  }),

  updatePlace: (id, updates) => set((state) => {
    if (state.isSimulating) {
      console.warn('Cannot update place while auto play is running. Please pause first.');
      return state;
    }
    get().resetSimulationIfModelChanged();
    get().saveToHistory();

    const newPlaces = state.places.map(p => 
      p.id === id ? { 
        ...p, 
        ...updates,
        tokens: updates.tokens !== undefined ? Number(updates.tokens) : p.tokens
      } : p
    );
    
    const newInitialMarking = { ...state.initialMarking };
    const newCurrentMarking = { ...state.currentMarking };

    if (updates.tokens !== undefined) {
      const tokens = Number(updates.tokens);
      newInitialMarking[id] = tokens;

      if (state.simulationHistory.length === 0) {
        newCurrentMarking[id] = tokens;
      }
    }

    return {
      places: newPlaces,
      initialMarking: newInitialMarking,
      currentMarking: newCurrentMarking,
      selectedElement: state.selectedElement?.id === id && state.selectedElement?.type === 'place' 
        ? { 
            ...state.selectedElement, 
            data: { 
              ...state.selectedElement.data, 
              ...updates,
              tokens: updates.tokens !== undefined ? Number(updates.tokens) : state.selectedElement.data.tokens
            } 
          } 
        : state.selectedElement
    };
  }),

  deletePlace: (id) => set((state) => {
    if (state.isSimulating) {
      console.warn('Cannot delete place while auto play is running. Please pause first.');
      return state;
    }
    get().resetSimulationIfModelChanged();
    get().saveToHistory();

    const newPlaces = state.places.filter(p => p.id !== id);
    const arcsToRemove = state.arcs.filter(a => a.source === id || a.target === id);
    const newArcs = state.arcs.filter(a => a.source !== id && a.target !== id);

    const newWeights = { ...state.weights };
    arcsToRemove.forEach(arc => {
      const key = JSON.stringify([arc.source, arc.target]);
      delete newWeights[key];
    });

    const newMarking = { ...state.initialMarking };
    delete newMarking[id];

    const newCurrentMarking = { ...state.currentMarking };
    delete newCurrentMarking[id];

    const selectedElement = state.selectedElement?.id === id ? null : state.selectedElement;

    return {
      places: newPlaces,
      arcs: newArcs,
      weights: newWeights,
      initialMarking: newMarking,
      currentMarking: newCurrentMarking,
      selectedElement,
      status: { ...state.status, elementCount: { ...state.status.elementCount, places: newPlaces.length } }
    };
  }),

  addTransition: (transition) => set((state) => {
    if (state.isSimulating) {
      console.warn('Cannot add transition while auto play is running. Please pause first.');
      return state;
    }
    get().resetSimulationIfModelChanged();
    get().saveToHistory();

    const newTransitions = [...state.transitions, transition];
    
    return {
      transitions: newTransitions,
      status: { ...state.status, elementCount: { ...state.status.elementCount, transitions: newTransitions.length } }
    };
  }),

  updateTransition: (id, updates) => set((state) => {
    if (state.isSimulating) {
      console.warn('Cannot update transition while auto play is running. Please pause first.');
      return state;
    }
    get().resetSimulationIfModelChanged();
    get().saveToHistory();

    return {
      transitions: state.transitions.map(t => t.id === id ? { ...t, ...updates } : t),
      selectedElement: state.selectedElement?.id === id && state.selectedElement?.type === 'transition' 
        ? { ...state.selectedElement, data: { ...state.selectedElement.data, ...updates } } 
        : state.selectedElement
    };
  }),
  
  deleteTransition: (id) => set((state) => {
    if (state.isSimulating) {
      console.warn('Cannot delete transition while auto play is running. Please pause first.');
      return state;
    }
    get().resetSimulationIfModelChanged();
    get().saveToHistory();

    const newTransitions = state.transitions.filter(t => t.id !== id);

    const arcsToRemove = state.arcs.filter(a => a.source === id || a.target === id);
    const newArcs = state.arcs.filter(a => a.source !== id && a.target !== id);

    const newWeights = { ...state.weights };
    arcsToRemove.forEach(arc => {
      const key = JSON.stringify([arc.source, arc.target]);
      delete newWeights[key];
    });

    const selectedElement = state.selectedElement?.id === id ? null : state.selectedElement;

    return {
      transitions: newTransitions,
      arcs: newArcs,
      weights: newWeights,
      selectedElement,
      status: { ...state.status, elementCount: { ...state.status.elementCount, transitions: newTransitions.length } }
    };
  }),

  addArc: (arc) => set((state) => {
    if (state.isSimulating) {
      console.warn('Cannot add arc while auto play is running. Please pause first.');
      return state;
    }
    get().resetSimulationIfModelChanged();
    get().saveToHistory();

    const newArcs = [...state.arcs, arc];
    const weightKey = JSON.stringify([arc.source, arc.target]);
    const newWeights = { ...state.weights, [weightKey]: arc.weight || 1 };
    
    return { arcs: newArcs, weights: newWeights };
  }),

  updateArc: (id, updates) => set((state) => {
    if (state.isSimulating) {
      console.warn('Cannot update arc while auto play is running. Please pause first.');
      return state;
    }
    get().resetSimulationIfModelChanged();
    get().saveToHistory();

    const newArcs = state.arcs.map(a => a.id === id ? { ...a, ...updates } : a);
    const updatedArc = newArcs.find(a => a.id === id);
    if (!updatedArc) return { arcs: newArcs };
    
    const result = { arcs: newArcs };
    
    if (updates.weight !== undefined) {
      const weightKey = JSON.stringify([updatedArc.source, updatedArc.target]);
      result.weights = { ...state.weights, [weightKey]: updates.weight };
    }
    
    if (state.selectedElement?.id === id && state.selectedElement?.type === 'arc') {
      result.selectedElement = {
        ...state.selectedElement,
        data: { ...state.selectedElement.data, ...updates }
      };
    }
    
    return result;
  }),

  deleteArc: (id) => set((state) => {
    if (state.isSimulating) {
      console.warn('Cannot delete arc while auto play is running. Please pause first.');
      return state;
    }
    get().resetSimulationIfModelChanged();
    get().saveToHistory();

    const arc = state.arcs.find(a => a.id === id);
    const newArcs = state.arcs.filter(a => a.id !== id);
    if (arc) {
      const weightKey = JSON.stringify([arc.source, arc.target]);
      const newWeights = { ...state.weights };
      delete newWeights[weightKey];
      return { arcs: newArcs, weights: newWeights };
    }
    return { arcs: newArcs };
  }),

  // ============ ACTIONS - UI ============

  setSelectedTool: (tool) => set({ selectedTool: tool }),

  setSelectedElement: (element) => set({ selectedElement: element }),

  setActiveTab: (tab) => set({ activeTab: tab }),
  
  setFirstSelectedNode: (node) => set({ firstSelectedNode: node }),
  
  openModal: (modalName) => set((state) => ({
    modals: { ...state.modals, [modalName]: true }
  })),

  closeModal: (modalName) => set((state) => ({
    modals: { ...state.modals, [modalName]: false }
  })),

  setConfirmAction: (action) => set({ confirmAction: action }),

  // ============ ACTIONS - Simulation ============

  setCurrentMarking: (marking) => set({ currentMarking: marking }),

  resetToInitialMarking: () => set((state) => {
    const updatedPlaces = state.places.map(p => ({
      ...p,
      tokens: state.initialMarking[p.id] || 0
    }));
    
    return {
      places: updatedPlaces,
      currentMarking: { ...state.initialMarking },
      simulationHistory: [],
    };
  }),

  fireTransition: (transitionId) => set((state) => {
    const transition = state.transitions.find(t => t.id === transitionId);
    if (!transition) return state;

    const newMarking = { ...state.currentMarking };
    const inputArcs = state.arcs.filter(a => a.target === transitionId);
    const outputArcs = state.arcs.filter(a => a.source === transitionId);

    const isEnabled = inputArcs.every(arc => {
      const weightKey = JSON.stringify([arc.source, arc.target]);
      const weight = state.weights[weightKey] || 1;
      return newMarking[arc.source] >= weight;
    });

    if (!isEnabled) return state;

    inputArcs.forEach(arc => {
      const weightKey = JSON.stringify([arc.source, arc.target]);
      const weight = state.weights[weightKey] || 1;
      newMarking[arc.source] -= weight;
    });

    outputArcs.forEach(arc => {
      const weightKey = JSON.stringify([arc.source, arc.target]);
      const weight = state.weights[weightKey] || 1;
      newMarking[arc.target] = (newMarking[arc.target] || 0) + weight;
    });

    const updatedPlaces = state.places.map(p => ({
      ...p,
      tokens: newMarking[p.id] || 0
    }));

    const historyEntry = {
      marking: state.currentMarking,
      transition: transitionId,
      timestamp: Date.now(),
    }; 

    return {
      places: updatedPlaces,
      currentMarking: newMarking,
      simulationHistory: [...state.simulationHistory, historyEntry],
    };
  }),

  getEnabledTransitions: () => {
    const state = get();
    // FIX: Thêm bảo vệ state.transitions và arcs
    return (state.transitions || []).filter(t => {
      const inputArcs = (state.arcs || []).filter(a => a.target === t.id);
      return inputArcs.every(arc => {
        const weightKey = JSON.stringify([arc.source, arc.target]);
        const weight = state.weights[weightKey] || 1;
        return (state.currentMarking[arc.source] || 0) >= weight;
      });
    });
  },

  startAutoPlay: (interval = 1000) => set((state) => {
    if (state.autoPlayInterval) {
      clearInterval(state.autoPlayInterval);
    }

    const intervalId = setInterval(() => {
      const enabled = get().getEnabledTransitions();
      if (enabled.length > 0) {
        const randomTransition = enabled[Math.floor(Math.random() * enabled.length)];
        get().fireTransition(randomTransition.id);
      } else {
        get().stopAutoPlay();
      }
    }, interval);

    return { isSimulating: true, autoPlayInterval: intervalId };
  }),

  stopAutoPlay: () => set((state) => {
    if (state.autoPlayInterval) {
      clearInterval(state.autoPlayInterval);
    }
    return { isSimulating: false, autoPlayInterval: null };
  }),

  // ============ ACTIONS - Analysis ============

setAnalysisResult: (analysisType, result) => set((state) => {
    
    // 1. Viết logic ở đây
    if (analysisType === 'reachability') {
        console.log("🎯 Reachability Data:", result);
    }

    // 2. Sau đó mới return object state
    return {
      analysisResults: {
        ...state.analysisResults,
        [analysisType]: result,
      }
    };
  }),

  setLoading: (key, value) => set((state) => ({
    loading: { ...state.loading, [key]: value }
  })),

  updateStatus: (updates) => set((state) => ({
    status: { ...state.status, ...updates }
  })),

  // ============ ACTIONS - History (Undo/Redo) ============

  saveToHistory: () => set((state) => {
    const snapshot = {
      places: state.places,
      transitions: state.transitions,
      arcs: state.arcs,
      weights: state.weights,
      initialMarking: state.initialMarking,
    };

    const newHistory = state.history.slice(0, state.historyIndex + 1);
    newHistory.push(snapshot);

    if (newHistory.length > state.maxHistory) {
      newHistory.shift();
    }

    return {
      history: newHistory,
      historyIndex: newHistory.length - 1,
    };
  }),

  undo: () => set((state) => {
    if (state.historyIndex <= 0) return state;

    const newIndex = state.historyIndex - 1;
    const snapshot = state.history[newIndex];

    return {
      ...snapshot,
      historyIndex: newIndex,
      currentMarking: { ...snapshot.initialMarking },
    };
  }),

  redo: () => set((state) => {
    if (state.historyIndex >= state.history.length - 1) return state;

    const newIndex = state.historyIndex + 1;
    const snapshot = state.history[newIndex];

    return {
      ...snapshot,
      historyIndex: newIndex,
      currentMarking: { ...snapshot.initialMarking },
    };
  }),

  canUndo: () => {
    const state = get();
    return state.historyIndex > 0;
  },

  canRedo: () => {
    const state = get();
    return state.historyIndex < state.history.length - 1;
  },

  // ============ ACTIONS - Import/Export ============

  exportTrace: (format = 'txt') => {
    const state = get();

    if (format === 'json') {
      const placeIds = state.places.map(p => p.id).sort();
      
      const trace = {
        metadata: {
          netName: "Petri Net",
          exportDate: new Date().toISOString(),
          initialMarking: placeIds.map(id => state.initialMarking[id] || 0),
          places: placeIds,
          transitions: state.transitions.map(t => t.id),
          totalSteps: state.simulationHistory.length
        },
        trace: [
          {
            step: 0,
            marking: placeIds.map(id => state.initialMarking[id] || 0),
            transition: null
          },
          ...state.simulationHistory.map((entry, index) => {
            const entryKeys = Object.keys(entry.marking).sort();
            return {
              step: index + 1,
              transition: entry.transition,
              marking: entryKeys.map(id => entry.marking[id] || 0)
            };
          })
        ],
        currentState: {
          step: state.simulationHistory.length,
          marking: placeIds.map(id => state.currentMarking[id] || 0)
        }
      };
      
      const blob = new Blob([JSON.stringify(trace, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `petri-net-trace-${Date.now()}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      
      return trace;
    }

    if (format === 'txt') {
      let text = "";

      text += "Petri Net Execution Trace\n";
      text += "=========================\n";
      text += `Net: ${state.status.isBounded === false ? 'UNBOUNDED' : state.status.isBounded === true ? 'BOUNDED' : 'UNKNOWN'}\n`;
      text += `Places: ${state.places.length}P, Transitions: ${state.transitions.length}T\n`;
      
      const initialKeys = Object.keys(state.initialMarking).sort();
      const initialVector = initialKeys.map(id => state.initialMarking[id] || 0);
      text += `Initial Marking: M0(${initialVector.join(',')})\n\n`;

      if (state.simulationHistory.length > 0) {
        state.simulationHistory.forEach((entry, index) => {
          const stepNum = index + 1;
          const entryKeys = Object.keys(entry.marking).sort();
          const markingVector = entryKeys.map(id => entry.marking[id] || 0);
          text += `Step ${stepNum}: --${entry.transition}--> M${stepNum}(${markingVector.join(',')})\n`;
        });
        
        const currentKeys = Object.keys(state.currentMarking).sort();
        const currentVector = currentKeys.map(id => state.currentMarking[id] || 0);
        text += `\nCurrent: (${currentVector.join(',')})\n`;
      } else {
        text += "No firing history\n";
      }

      const blob = new Blob([text], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `petri-net-trace-${Date.now()}.txt`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      return text;
    }

    return null;
  },

  loadPetriNet: (data) => set((state) => {
    get().saveToHistory();
    return {
      places: data.places || [],
      transitions: data.transitions || [],
      arcs: data.arcs || [],
      weights: data.weights || {},
      initialMarking: data.initial_marking || data.initialMarking || {},
      currentMarking: data.initial_marking || data.initialMarking || {},
      status: {
        ...state.status,
        elementCount: {
          places: (data.places || []).length,
          transitions: (data.transitions || []).length,
        }
      }
    };
  }),

  resetNet: () => set((state) => {
    get().saveToHistory();
    return {
      places: [],
      transitions: [],
      arcs: [],
      weights: {},
      initialMarking: {},
      currentMarking: {},
      selectedElement: null,
      simulationHistory: [],
      analysisResults: {
        reachability: null,
        deadlock: null,
        boundedness: null,
        liveness: null,
        siphonsTraps: null,
      },
      status: {
        isBounded: null,
        elementCount: { places: 0, transitions: 0 },
        stateCount: 0,
        hasWarning: false,
        warningMessage: '',
      },
    };
  }),

  // ============ HELPERS ============

  getPetriNetData: () => {
    const state = get();
    return {
      places: state.places.map(p => p.id),
      transitions: state.transitions.map(t => t.id),
      arcs: state.arcs.map(a => [a.source, a.target]),
      weights: state.weights,
      initial_marking: state.initialMarking,
    };
  },
  
  getPetriNetDataGraphic: () => {
    const state = get();
    return {
      places: state.places.map(p => ({
        id: p.id,
        label: p.label,
        position: p.position || { x: 0, y: 0 },
      })),
      transitions: state.transitions.map(t => ({
        id: t.id,
        label: t.label,
        position: t.position || { x: 0, y: 0 },
      })),
      arcs: state.arcs.map(a => ({
        source: a.source,
        target: a.target
      })),
      weights: state.weights,
      initial_marking: state.initialMarking,
    };
  },

  resetSimulationIfModelChanged: () => set((state) => {
    if (state.simulationHistory.length > 0 || state.isSimulating) {
      const resetMarking = { ...state.initialMarking };
      
      const updatedPlaces = state.places.map(p => ({
        ...p,
        tokens: resetMarking[p.id] || 0
      }));
      
      if (state.autoPlayInterval) {
        clearInterval(state.autoPlayInterval);
      }
      
      return {
        places: updatedPlaces,
        currentMarking: resetMarking,
        simulationHistory: [],
        isSimulating: false,
        autoPlayInterval: null,
      };
    }
    return {}; // Trả về object rỗng nếu không có thay đổi để tránh lỗi
  }),

})); 

export default usePetriNetStore;
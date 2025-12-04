import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://127.0.0.1:8000/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response.data;
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message);
    
    // Format error message
    const errorMessage = error.response?.data?.message || 
                        error.response?.data?.detail || 
                        error.message || 
                        'Unknown error occurred';
    
    return Promise.reject(new Error(errorMessage));
  }
);

// ============ FILE OPERATIONS ============

/**
 * Upload PNML or JSON file
 * @param {File} file - File object to upload
 * @returns {Promise} - Parsed Petri Net data
 */
export const uploadPetriNet = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  return await apiClient.post('/net/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

/**
 * Convert between PNML and JSON formats
 * @param {string} inputFormat - 'pnml' or 'json'
 * @param {string} outputFormat - 'pnml' or 'json'
 * @param {string} data - Data to convert
 * @returns {Promise} - Converted data
 */
export const convertFormat = async (inputFormat, outputFormat, data) => {
  return await apiClient.post('/net/convert', {
    input_format: inputFormat,
    output_format: outputFormat,
    data,
  });
};

/**
 * Export Petri Net to specified format
 * @param {Object} netData - Petri Net data
 * @param {string} format - 'pnml', 'json', 'png', 'svg'
 * @returns {Promise} - Export result
 */
export const exportPetriNet = async (netData, format) => {
  return await apiClient.post('/net/export', {
    net_data: netData,
    format,
  }, {
    responseType: format === 'pnml' || format === 'png' || format === 'svg' ? 'blob' : 'json',
  });
};

// ============ ANALYSIS OPERATIONS ============

/**
 * Analyze Reachability Graph
 * @param {Object} netData - Petri Net data
 * @returns {Promise} - RG data with states and edges
 */
export const analyzeReachability = async (netData) => {

  return await apiClient.post('/analyze/reachability', netData);
};

/**
 * Detect deadlocks
 * @param {Object} netData - Petri Net data
 * @returns {Promise} - Deadlock information
 */
export const analyzeDeadlock = async (netData) => {
  return await apiClient.post('/analyze/deadlock', netData);
};

/**
 * Check boundedness
 * @param {Object} netData - Petri Net data
 * @returns {Promise} - Boundedness analysis result
 */
export const analyzeBoundedness = async (netData) => {
  return await apiClient.post('/analyze/boundedness', netData);
};

/**
 * Check liveness
 * @param {Object} netData - Petri Net data
 * @returns {Promise} - Liveness analysis result
 */
export const analyzeLiveness = async (netData) => {
  return await apiClient.post('/analyze/liveness', netData);
};

/**
 * Compute siphons and traps
 * @param {Object} netData - Petri Net data
 * @returns {Promise} - Siphons and traps
 */
export const analyzeSiphonsTraps = async (netData) => {
  return await apiClient.post('/analyze/siphons-traps', netData);
};

// ============ VISUALIZATION ============

/**
 * Get visualization of Reachability Graph
 * @param {Object} rgData - RG data (states, edges)
 * @param {string} format - 'png' or 'svg'
 * @returns {Promise} - Image data
 */
export const getReachabilityGraphImage = async (rgData, format = 'svg') => {
  return await apiClient.post(`/visualize/reachability`, {
    rg_data: rgData,
    format,
  }, {
    responseType: 'blob',
  });
};

/**
 * Get visualization of Coverability Tree
 * @param {Object} treeData - Coverability tree data
 * @param {string} format - 'png' or 'svg'
 * @returns {Promise} - Image data
 */
export const getCoverabilityTreeImage = async (treeData, format = 'svg') => {
  return await apiClient.post(`/visualize/coverability`, {
    tree_data: treeData,
    format,
  }, {
    responseType: 'blob',
  });
};

/**
 * Get visualization of Petri Net
 * @param {Object} netData - Petri Net data
 * @param {string} format - 'png' or 'svg'
 * @returns {Promise} - Image data
 */
export const getPetriNetImage = async (netData, format = 'svg') => {
  return await apiClient.post(`/visualize/petri-net`, {
    net_data: netData,
    format,
  }, {
    responseType: 'blob',
  });
};

// ============ SIMULATION ============

/**
 * Get enabled transitions at current marking
 * @param {Object} netData - Petri Net data
 * @param {Object} marking - Current marking
 * @returns {Promise} - List of enabled transition IDs
 */
export const getEnabledTransitions = async (netData, marking) => {
  return await apiClient.post('/sim/enabled', {
    net_data: netData,
    marking,
  });
};

/**
 * Fire a transition
 * @param {Object} netData - Petri Net data
 * @param {Object} marking - Current marking
 * @param {string} transitionId - Transition to fire
 * @returns {Promise} - New marking after firing
 */
export const fireTransition = async (netData, marking, transitionId) => {
  return await apiClient.post('/sim/fire', {
    net_data: netData,
    marking,
    transition_id: transitionId,
  });
};

// ============ HEALTH CHECK ============

/**
 * Check if backend is running
 * @returns {Promise} - Health status
 */
export const healthCheck = async () => {
  return await apiClient.get('/health');
};

export default {
  uploadPetriNet,
  convertFormat,
  exportPetriNet,
  analyzeReachability,
  analyzeDeadlock,
  analyzeBoundedness,
  analyzeLiveness,
  analyzeSiphonsTraps,
  getReachabilityGraphImage,
  getCoverabilityTreeImage,
  getPetriNetImage,
  getEnabledTransitions,
  fireTransition,
  healthCheck,
};



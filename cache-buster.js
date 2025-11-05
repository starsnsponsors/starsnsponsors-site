// Auto Cache Buster Utility
// Include this script to automatically handle cache busting in development

(function() {
  'use strict';
  
  // Detect if we're in development environment
  const isDev = window.location.hostname === 'localhost' || 
                window.location.hostname === '127.0.0.1' || 
                window.location.hostname === 'file' ||
                window.location.port !== '';
  
  if (isDev) {
    console.log('🔄 Cache busting enabled for development');
    
    // Update cache buster meta tag with current timestamp
    const cacheBusterMeta = document.querySelector('meta[name="cache-buster"]');
    if (cacheBusterMeta) {
      const timestamp = new Date().getTime();
      cacheBusterMeta.setAttribute('content', timestamp);
    }
    
    // Add cache buster to any dynamically loaded resources
    const originalFetch = window.fetch;
    window.fetch = function(url, options) {
      if (typeof url === 'string' && !url.includes('?')) {
        url += '?cb=' + Date.now();
      } else if (typeof url === 'string') {
        url += '&cb=' + Date.now();
      }
      return originalFetch(url, options);
    };
    
    // Optional: Show cache status in console
    window.addEventListener('load', function() {
      console.log('📄 Page loaded with cache buster:', 
                 document.querySelector('meta[name="cache-buster"]')?.content || 'none');
    });
  }
})();
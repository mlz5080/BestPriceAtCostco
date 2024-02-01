const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://142.198.226.38:5000',
      changeOrigin: true,
    })
  );
};
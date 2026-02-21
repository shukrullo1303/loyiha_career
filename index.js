const path = require('path');

// API endpointlaridan KEYIN, barcha boshqa so'rovlar uchun:
app.use(express.static(path.join(__dirname, 'frontend/dist')));

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'frontend/dist', 'index.html'));
});
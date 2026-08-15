import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { TelaLogin } from './pages/Login';
import { TelaAgenda } from './pages/Agenda'; 
import { TelaCriarConta } from './pages/CriarConta'; 
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';

const temaEscuro = createTheme({
  palette: { mode: 'dark' },
});

function App() {
  return (
    <ThemeProvider theme={temaEscuro}>
      <CssBaseline />
      
      {/* O BrowserRouter é o motor que entende a URL do navegador */}
      <BrowserRouter>
        {/* O Routes é o "mapa" */}
        <Routes>
          {/* Se a URL for exatamente "/", mostre o Login */}
          <Route path="/" element={<TelaLogin />} />
          
          {/* Se a URL for "/agenda", mostre a Agenda */}
          <Route path="/agenda" element={<TelaAgenda />} />
 
          {/* Se a URL for "/criarconta", mostre a Agenda */}
          <Route path="/criarconta" element={<TelaCriarConta />} />


          
        </Routes>
      </BrowserRouter>

    </ThemeProvider>
  );
}

export default App;
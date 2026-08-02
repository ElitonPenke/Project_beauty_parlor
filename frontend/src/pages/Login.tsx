import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { api } from '../services/api';
import type { LoginDados, RespostaLogin } from '../types/auth';
import { 
  Box, 
  Button, 
  Checkbox, 
  CssBaseline, 
  FormControlLabel, 
  TextField, 
  Typography, 
  Stack, 
  Card as MuiCard, 
  ThemeProvider, 
  createTheme 
} from '@mui/material';
import { styled } from '@mui/material/styles';

// 1. Criamos o Tema Escuro (Igual ao do Template)
const temaEscuro = createTheme({
  palette: { mode: 'dark' },
});

// 2. Copiamos o estilo do "Cartão" central do template deles
const Card = styled(MuiCard)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  alignSelf: 'center',
  width: '100%',
  padding: theme.spacing(4),
  gap: theme.spacing(2),
  margin: 'auto',
  [theme.breakpoints.up('sm')]: { maxWidth: '450px' },
  boxShadow: 'hsla(220, 30%, 5%, 0.5) 0px 5px 15px 0px, hsla(220, 25%, 10%, 0.08) 0px 15px 35px -5px',
}));

const SignInContainer = styled(Stack)(({ theme }) => ({
  minHeight: '100vh',
  padding: theme.spacing(2),
  [theme.breakpoints.up('sm')]: { padding: theme.spacing(4) },
  '&::before': {
    content: '""',
    display: 'block',
    position: 'absolute',
    zIndex: -1,
    inset: 0,
    backgroundImage: 'radial-gradient(ellipse at 50% 50%, hsl(210, 100%, 16%), hsl(220, 30%, 5%))',
    backgroundRepeat: 'no-repeat',
  },
}));

export function TelaLogin() {
  const navigate = useNavigate(); 
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');

  async function fazerLogin() {
    try {
      const dados: LoginDados = { email, senha };
      const resposta = await api.post<RespostaLogin>('/authentication/login', dados);
      
      const token = resposta.data.access_token;
      localStorage.setItem('@SalaoBeleza:token', token);
      
      
      navigate('/agenda');
      
    } catch (erro) {
      alert('Erro ao fazer login. Verifique as credenciais.');
    }
  }

  // 3. A estrutura visual baseada no template, limpa e funcional
  return (
    <ThemeProvider theme={temaEscuro}>
        
      <CssBaseline />
      <SignInContainer direction="column" sx={{ justifyContent: 'space-between' }}>
        <Card variant="outlined">
          <Typography component="h1" variant="h4" sx={{ width: '100%', fontSize: 'clamp(2rem, 10vw, 2.15rem)' }}>
            Sign in
          </Typography>
          
          <Box sx={{ display: 'flex', flexDirection: 'column', width: '100%', gap: 2 }}>
            <Box>
              <Typography variant="body2" sx={{ mb: 1 }}>Email</Typography>
              <TextField
                type="email"
                placeholder="seu@email.com"
                fullWidth
                variant="outlined"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </Box>

            <Box>
              <Typography variant="body2" sx={{ mb: 1 }}>Password</Typography>
              <TextField
                type="password"
                placeholder="••••••"
                fullWidth
                variant="outlined"
                value={senha}
                onChange={(e) => setSenha(e.target.value)}
              />
            </Box>

            <FormControlLabel
              control={<Checkbox value="remember" color="primary" />}
              label="Remember me"
            />

            <Button type="button" fullWidth variant="contained" onClick={fazerLogin}>
              Sign in
            </Button>
          </Box>
        </Card>
      </SignInContainer>
    </ThemeProvider>
  );
}       
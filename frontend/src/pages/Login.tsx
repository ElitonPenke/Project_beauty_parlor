import { useNavigate } from 'react-router-dom';
import { useState, type FormEvent } from 'react';
import { api } from '../services/api';
import type { LoginDados, RespostaLogin } from '../types/auth';
import {
  Box,
  Button,
  Checkbox,
  CssBaseline,
  FormControlLabel,
  IconButton,
  InputAdornment,
  TextField,
  Typography,
  Stack,
  type StackProps,
  Card as MuiCard,
  ThemeProvider,
  createTheme,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import EmailOutlinedIcon from '@mui/icons-material/EmailOutlined';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import VisibilityOutlinedIcon from '@mui/icons-material/VisibilityOutlined';
import VisibilityOffOutlinedIcon from '@mui/icons-material/VisibilityOffOutlined';

const temaEscuro = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#8b5cf6',
    },
    background: {
      default: '#020817',
      paper: '#0f172a',
    },
    text: {
      primary: '#f8fafc',
      secondary: '#94a3b8',
    },
  },
  shape: {
    borderRadius: 18,
  },
  typography: {
    fontFamily: 'Inter, system-ui, sans-serif',
  },
});

// StackProps reintroduz o generic que permite usar component="main" no PageShell
const PageShell = styled(Stack)<StackProps>(() => ({
  minHeight: '100vh',
  position: 'relative',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  background:
    'radial-gradient(circle at top, rgba(139, 92, 246, 0.22), transparent 30%), #020817',
  paddingLeft: 16,
  paddingRight: 16,
  paddingTop: 32,
  paddingBottom: 32,
}));

const Card = styled(MuiCard)(({ theme }) => ({
  width: '100%',
  maxWidth: 420,
  padding: theme.spacing(4),
  borderRadius: 24,
  background: 'rgba(15, 23, 42, 0.9)',
  border: '1px solid rgba(148, 163, 184, 0.18)',
  boxShadow: '0 28px 80px rgba(15, 23, 42, 0.8)',
}));

const BrandBadge = styled(Box)(() => ({
  width: 72,
  height: 72,
  borderRadius: 20,
  display: 'grid',
  placeItems: 'center',
  margin: '0 auto',
  background: 'linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%)',
  color: '#fff',
  fontWeight: 800,
  fontSize: '1.7rem',
  boxShadow: '0 20px 40px rgba(99, 102, 241, 0.4)',
}));

export function TelaLogin() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [mostrarSenha, setMostrarSenha] = useState(false);
  const [lembrar, setLembrar] = useState(true);
  const [carregando, setCarregando] = useState(false);

  async function fazerLogin(event?: FormEvent) {
    event?.preventDefault();

    if (!email || !senha) {
      alert('Preencha e-mail e senha.');
      return;
    }

    setCarregando(true);

    try {
      const dados: LoginDados = { email, senha };
      const resposta = await api.post<RespostaLogin>('/authentication/login', dados);

      const token = resposta.data.access_token;
      localStorage.setItem('@SalaoBeleza:token', token);

      if (lembrar) {
        localStorage.setItem('@SalaoBeleza:lembrar', 'true');
      } else {
        localStorage.removeItem('@SalaoBeleza:lembrar');
      }

      navigate('/agenda');
    } catch (erro) {
      alert('Erro ao fazer login. Verifique as credenciais.');
    } finally {
      setCarregando(false);
    }
  }

  return (
    <ThemeProvider theme={temaEscuro}>
      <CssBaseline />
      <PageShell component="main">
        <Card>
        <Box component="form" onSubmit={fazerLogin} noValidate>
          <Box sx={{ textAlign: 'center', mb: 1 }}>
            <BrandBadge>SB</BrandBadge>

            <Typography
              variant="h4"
              sx={{
                mt: 2,
                fontWeight: 700,
                letterSpacing: '-0.04em',
              }}
            >
              Bem-vindo
            </Typography>

            <Typography
              variant="body2"
              color="text.secondary"
              sx={{ mt: 1, lineHeight: 1.6 }}
            >
              Entre para acessar sua conta e gerenciar sua agenda de beleza.
            </Typography>
          </Box>

          <Stack spacing={2.5} sx={{ mt: 1 }}>
            <Box>
              <Typography variant="body2" sx={{ mb: 1, fontWeight: 600 }}>
                E-mail
              </Typography>

              <TextField
                type="email"
                placeholder="seu@email.com"
                fullWidth
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                slotProps={{
                  input: {
                    startAdornment: (
                      <InputAdornment position="start">
                        <EmailOutlinedIcon fontSize="small" color="action" />
                      </InputAdornment>
                    ),
                    sx: {
                      borderRadius: 2,
                      backgroundColor: 'rgba(15, 23, 42, 0.7)',
                      '& fieldset': {
                        borderColor: 'rgba(148, 163, 184, 0.2)',
                      },
                    },
                  },
                }}
              />
            </Box>

            <Box>
              <Box
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  mb: 1,
                }}
              >
                <Typography variant="body2" sx={{ fontWeight: 600 }}>
                  Senha
                </Typography>

                <Box
                  component="a"
                  href="#"
                  sx={{
                    color: 'primary.main',
                    textDecoration: 'none',
                    fontSize: 13,
                    fontWeight: 500,
                    '&:hover': {
                      textDecoration: 'underline',
                    },
                  }}
                >
                  Esqueceu a senha?
                </Box>
              </Box>

              <TextField
                fullWidth
                type={mostrarSenha ? 'text' : 'password'}
                placeholder="Digite sua senha"
                value={senha}
                onChange={(e) => setSenha(e.target.value)}
                slotProps={{
                  input: {
                    startAdornment: (
                      <InputAdornment position="start">
                        <LockOutlinedIcon fontSize="small" color="action" />
                      </InputAdornment>
                    ),
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton
                          aria-label={mostrarSenha ? 'Ocultar senha' : 'Mostrar senha'}
                          onClick={() => setMostrarSenha((prev) => !prev)}
                          edge="end"
                          size="small"
                        >
                          {mostrarSenha ? (
                            <VisibilityOffOutlinedIcon fontSize="small" />
                          ) : (
                            <VisibilityOutlinedIcon fontSize="small" />
                          )}
                        </IconButton>
                      </InputAdornment>
                    ),
                    sx: {
                      borderRadius: 2,
                      backgroundColor: 'rgba(15, 23, 42, 0.7)',
                      '& fieldset': {
                        borderColor: 'rgba(148, 163, 184, 0.2)',
                      },
                    },
                  },
                }}
              />
            </Box>

            <FormControlLabel
              control={
                <Checkbox
                  checked={lembrar}
                  onChange={(e) => setLembrar(e.target.checked)}
                  color="primary"
                />
              }
              label={
                <Typography variant="body2" color="text.secondary">
                  Lembrar por 30 dias
                </Typography>
              }
              sx={{
                ml: 0,
              }}
            />
          </Stack>

          <Button
            type="submit"
            fullWidth
            variant="contained"
            size="large"
            disabled={carregando}
            sx={{
              mt: 3,
              py: 1.5,
              borderRadius: 2,
              fontWeight: 700,
              textTransform: 'none',
              background: 'linear-gradient(135deg, #f66e5c 0%, #3b82f6 100%)',
              boxShadow: '0 18px 34px rgba(99, 102, 241, 0.35)',
              '&:hover': {
                background: 'linear-gradient(135deg, #7c3aed 0%, #2563eb 100%)',
              },
            }}
          >
            {carregando ? 'Entrando...' : 'Entrar'}
          </Button>

          <Typography
            variant="body2"
            align="center"
            sx={{ mt: 3, color: 'text.secondary' }}
          >
            Não tem conta?{' '}
            <Box
              component="button"
              type="button"
              onClick={() => navigate('/criarconta')}
              sx={{
                background: 'transparent',
                border: 'none',
                padding: 0,
                color: 'primary.main',
                fontWeight: 600,
                cursor: 'pointer',
                '&:hover': {
                  textDecoration: 'underline',
                },
              }}
            >
              Crie uma conta
            </Box>
          </Typography>
        </Box>
        </Card>
      </PageShell>
    </ThemeProvider>
  );
}
import { useNavigate } from 'react-router-dom';
import { useState, type FormEvent } from 'react';
import { api } from '../services/api';
import {
  Box,
  Button,
  IconButton,
  InputAdornment,
  MenuItem,
  TextField,
  Typography,
  Stack,
  type StackProps,
  Card as MuiCard,
  ThemeProvider,
  createTheme,
  CssBaseline,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import PersonOutlinedIcon from '@mui/icons-material/PersonOutlined';
import EmailOutlinedIcon from '@mui/icons-material/EmailOutlined';
import PhoneOutlinedIcon from '@mui/icons-material/PhoneOutlined';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import HomeOutlinedIcon from '@mui/icons-material/HomeOutlined';
import CakeOutlinedIcon from '@mui/icons-material/CakeOutlined';
import VisibilityOutlinedIcon from '@mui/icons-material/VisibilityOutlined';
import VisibilityOffOutlinedIcon from '@mui/icons-material/VisibilityOffOutlined';

// Espelha o UsuarioSchema do backend (campos ativo/admin ficam de fora,
// pois são definidos pelo servidor e não preenchidos no cadastro)
interface CriarContaDados {
  nome: string;
  email: string;
  telefone: string;
  senha: string;
  sexo: string;
  dataNascimento: string; // input type="date" envia string no formato AAAA-MM-DD
  endereco: string;
}

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

const PageShell = styled(Stack)<StackProps>(() => ({
  minHeight: '100vh',
  position: 'relative',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  background:
    'radial-gradient(circle at top, rgba(141, 246, 92, 0.82), transparent 30%), #020817',
  paddingLeft: 16,
  paddingRight: 16,
  paddingTop: 32,
  paddingBottom: 32,
}));

const Card = styled(MuiCard)(({ theme }) => ({
  width: '100%',
  maxWidth: 460,
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

const camposEstiloInput = {
  borderRadius: 2,
  backgroundColor: 'rgba(15, 23, 42, 0.7)',
  '& fieldset': {
    borderColor: 'rgba(148, 163, 184, 0.2)',
  },
};

export function TelaCriarConta() {
  const navigate = useNavigate();

  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [telefone, setTelefone] = useState('');
  const [senha, setSenha] = useState('');
  const [confirmarSenha, setConfirmarSenha] = useState('');
  const [sexo, setSexo] = useState('');
  const [dataNascimento, setDataNascimento] = useState('');
  const [endereco, setEndereco] = useState('');

  const [mostrarSenha, setMostrarSenha] = useState(false);
  const [mostrarConfirmarSenha, setMostrarConfirmarSenha] = useState(false);
  const [carregando, setCarregando] = useState(false);

  async function criarConta(event?: FormEvent) {
    event?.preventDefault();

    if (
      !nome ||
      !email ||
      !telefone ||
      !senha ||
      !sexo ||
      !dataNascimento ||
      !endereco
    ) {
      alert('Preencha todos os campos.');
      return;
    }

    if (senha !== confirmarSenha) {
      alert('As senhas não coincidem.');
      return;
    }

    setCarregando(true);

    try {
      const dados: CriarContaDados = {
        nome,
        email,
        telefone,
        senha,
        sexo,
        dataNascimento,
        endereco,
      };

      await api.post('/authentication/criar_conta', dados);

      navigate('/agenda');
    } catch (erro) {
      alert('Erro ao criar conta. Verifique os dados informados.');
    } finally {
      setCarregando(false);
    }
  }

  return (
    <ThemeProvider theme={temaEscuro}>
      <CssBaseline />
      <PageShell component="main">
        <Card>
          <Box component="form" onSubmit={criarConta} noValidate>
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
                Criar conta
              </Typography>

              <Typography
                variant="body2"
                color="text.secondary"
                sx={{ mt: 1, lineHeight: 1.6 }}
              >
                Preencha seus dados para agendar seus horários no salão.
              </Typography>
            </Box>

            <Stack spacing={2.5} sx={{ mt: 1 }}>
              <Box>
                <Typography variant="body2" sx={{ mb: 1, fontWeight: 600 }}>
                  Nome completo
                </Typography>

                <TextField
                  placeholder="Seu nome completo"
                  fullWidth
                  value={nome}
                  onChange={(e) => setNome(e.target.value)}
                  slotProps={{
                    input: {
                      startAdornment: (
                        <InputAdornment position="start">
                          <PersonOutlinedIcon fontSize="small" color="action" />
                        </InputAdornment>
                      ),
                      sx: camposEstiloInput,
                    },
                  }}
                />
              </Box>

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
                      sx: camposEstiloInput,
                    },
                  }}
                />
              </Box>

              <Box sx={{ display: 'flex', gap: 2 }}>
                <Box sx={{ flex: 1 }}>
                  <Typography variant="body2" sx={{ mb: 1, fontWeight: 600 }}>
                    Telefone
                  </Typography>

                  <TextField
                    placeholder="(00) 00000-0000"
                    fullWidth
                    value={telefone}
                    onChange={(e) => setTelefone(e.target.value)}
                    slotProps={{
                      input: {
                        startAdornment: (
                          <InputAdornment position="start">
                            <PhoneOutlinedIcon fontSize="small" color="action" />
                          </InputAdornment>
                        ),
                        sx: camposEstiloInput,
                      },
                    }}
                  />
                </Box>

                <Box sx={{ flex: 1 }}>
                  <Typography variant="body2" sx={{ mb: 1, fontWeight: 600 }}>
                    Data de nascimento
                  </Typography>

                  <TextField
                    type="date"
                    fullWidth
                    value={dataNascimento}
                    onChange={(e) => setDataNascimento(e.target.value)}
                    slotProps={{
                      input: {
                        startAdornment: (
                          <InputAdornment position="start">
                            <CakeOutlinedIcon fontSize="small" color="action" />
                          </InputAdornment>
                        ),
                        sx: camposEstiloInput,
                      },
                    }}
                  />
                </Box>
              </Box>

              <Box>
                <Typography variant="body2" sx={{ mb: 1, fontWeight: 600 }}>
                  Sexo
                </Typography>

                <TextField
                  select
                  fullWidth
                  value={sexo}
                  onChange={(e) => setSexo(e.target.value)}
                  slotProps={{
                    input: {
                      sx: camposEstiloInput,
                    },
                  }}
                >
                  <MenuItem value="Feminino">Feminino</MenuItem>
                  <MenuItem value="Masculino">Masculino</MenuItem>
                </TextField>
              </Box>

              <Box>
                <Typography variant="body2" sx={{ mb: 1, fontWeight: 600 }}>
                  Endereço
                </Typography>

                <TextField
                  placeholder="Rua, número, bairro, cidade"
                  fullWidth
                  value={endereco}
                  onChange={(e) => setEndereco(e.target.value)}
                  slotProps={{
                    input: {
                      startAdornment: (
                        <InputAdornment position="start">
                          <HomeOutlinedIcon fontSize="small" color="action" />
                        </InputAdornment>
                      ),
                      sx: camposEstiloInput,
                    },
                  }}
                />
              </Box>

              <Box>
                <Typography variant="body2" sx={{ mb: 1, fontWeight: 600 }}>
                  Senha
                </Typography>

                <TextField
                  fullWidth
                  type={mostrarSenha ? 'text' : 'password'}
                  placeholder="Crie uma senha"
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
                      sx: camposEstiloInput,
                    },
                  }}
                />
              </Box>

              <Box>
                <Typography variant="body2" sx={{ mb: 1, fontWeight: 600 }}>
                  Confirmar senha
                </Typography>

                <TextField
                  fullWidth
                  type={mostrarConfirmarSenha ? 'text' : 'password'}
                  placeholder="Repita a senha"
                  value={confirmarSenha}
                  onChange={(e) => setConfirmarSenha(e.target.value)}
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
                            aria-label={
                              mostrarConfirmarSenha ? 'Ocultar senha' : 'Mostrar senha'
                            }
                            onClick={() => setMostrarConfirmarSenha((prev) => !prev)}
                            edge="end"
                            size="small"
                          >
                            {mostrarConfirmarSenha ? (
                              <VisibilityOffOutlinedIcon fontSize="small" />
                            ) : (
                              <VisibilityOutlinedIcon fontSize="small" />
                            )}
                          </IconButton>
                        </InputAdornment>
                      ),
                      sx: camposEstiloInput,
                    },
                  }}
                />
              </Box>
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
              {carregando ? 'Criando conta...' : 'Criar conta'}
            </Button>

            <Typography
              variant="body2"
              align="center"
              sx={{ mt: 3, color: 'text.secondary' }}
            >
              Já tem conta?{' '}
              <Box
                component="button"
                type="button"
                onClick={() => navigate('/')}
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
                Entrar
              </Box>
            </Typography>
          </Box>
        </Card>
      </PageShell>
    </ThemeProvider>
  );
}
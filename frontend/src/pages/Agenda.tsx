import { Typography, Container, Box } from '@mui/material';

export function TelaAgenda() {
  return (
    <Container>
      <Box sx={{ mt: 10, textAlign: 'center' }}>
        <Typography variant="h3">Bem-vindo à Agenda do Salão!</Typography>
        <Typography variant="subtitle1">Aqui ficarão os agendamentos dos clientes.</Typography>
      </Box>
    </Container>
  );
}
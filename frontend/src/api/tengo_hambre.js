import api from './client'

export const sugerirRecetas = (idHogar, soloCriticos, limite) =>
  api.get(`/tengo-hambre/${idHogar}`, {
    params: { solo_criticos: soloCriticos, limite },
  })

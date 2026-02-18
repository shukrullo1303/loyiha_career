import React from 'react'
import { useQuery } from 'react-query'
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Chip,
  Button,
} from '@mui/material'
import { Videocam } from '@mui/icons-material'
import apiClient from '../api/client'

function Cameras() {
  const { data: cameras, isLoading } = useQuery('cameras', async () => {
    const response = await apiClient.get('/cameras/')
    return response.data
  })

  if (isLoading) {
    return <Typography>Yuklanmoqda...</Typography>
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Kameralar
      </Typography>
      <Grid container spacing={3} sx={{ mt: 2 }}>
        {cameras?.map((camera: any) => (
          <Grid item xs={12} sm={6} md={4} key={camera.id}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Videocam sx={{ fontSize: 40, mr: 2 }} />
                  <Box>
                    <Typography variant="h6">{camera.name}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      {camera.ip_address}
                    </Typography>
                  </Box>
                </Box>
                <Chip
                  label={camera.is_active ? 'Faol' : 'Nofaol'}
                  color={camera.is_active ? 'success' : 'default'}
                  size="small"
                  sx={{ mb: 2 }}
                />
                <Button
                  variant="outlined"
                  fullWidth
                  onClick={() => {
                    // Таҳлилни бошлаш
                  }}
                >
                  Tahlilni boshlash
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  )
}

export default Cameras

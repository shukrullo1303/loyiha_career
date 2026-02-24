import React, { useState } from 'react'
import { useQuery } from 'react-query'
import {
  Box,
  Typography,
  Paper,
  Grid,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from '@mui/material'
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import apiClient from '../api/client'

function Analytics() {
  const [locationId, setLocationId] = useState<number | ''>('')

  const { data: locations } = useQuery('locations', async () => {
    const response = await apiClient.get('locations/')
    return response.data
  })

  const { data: analytics } = useQuery(
    ['analytics', locationId],
    async () => {
      if (!locationId) return null
      const response = await apiClient.get(`/analytics/locations/${locationId}`)
      return response.data
    },
    { enabled: !!locationId }
  )

  const { data: riskScore } = useQuery(
    ['risk', locationId],
    async () => {
      if (!locationId) return null
      const response = await apiClient.get(`/analytics/locations/${locationId}/risk`)
      return response.data
    },
    { enabled: !!locationId }
  )

  const chartData = analytics?.map((item: any) => ({
    date: new Date(item.date).toLocaleDateString(),
    real: item.real_customers,
    reported: item.reported_revenue / 50000, // Ўртача чек
    discrepancy: item.discrepancy,
  })) || []

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Аналитика
      </Typography>
      <FormControl fullWidth sx={{ mt: 3, mb: 3, maxWidth: 300 }}>
        <InputLabel>Локацияни танланг</InputLabel>
        <Select
          value={locationId}
          onChange={(e) => setLocationId(e.target.value as number)}
        >
          {locations?.map((loc: any) => (
            <MenuItem key={loc.id} value={loc.id}>
              {loc.name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      {riskScore && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Риск баҳоси
          </Typography>
          <Typography variant="h3" color={riskScore.risk_level === 'critical' ? 'error' : 'warning'}>
            {riskScore.risk_score.toFixed(1)}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Даража: {riskScore.risk_level}
          </Typography>
        </Paper>
      )}

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Мижозлар ва тушум таҳлили
            </Typography>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="real" stroke="#8884d8" name="Реал мижозлар" />
                <Line type="monotone" dataKey="reported" stroke="#82ca9d" name="Хисоботдаги мижозлар" />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  )
}

export default Analytics

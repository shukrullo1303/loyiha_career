import React from 'react'
import { useQuery } from 'react-query'
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
} from '@mui/material'
import {
  LocationOn,
  People,
  TrendingUp,
  Warning,
} from '@mui/icons-material'
import apiClient from '../api/client'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

function Dashboard() {
  const { data: locations } = useQuery('locations', async () => {
    const response = await apiClient.get('/locations/')
    return response.data
  })

  const { data: analytics } = useQuery('dashboard-analytics', async () => {
    // Содда статистика
    return {
      totalLocations: locations?.length || 0,
      totalEmployees: 0,
      riskLocations: 0,
      revenue: 0,
    }
  })

  const chartData = [
    { name: 'Душанба', customers: 120, revenue: 6000000 },
    { name: 'Сешанба', customers: 150, revenue: 7500000 },
    { name: 'Чоршанба', customers: 180, revenue: 9000000 },
    { name: 'Пайшанба', customers: 200, revenue: 10000000 },
    { name: 'Жума', customers: 250, revenue: 12500000 },
    { name: 'Шанба', customers: 300, revenue: 15000000 },
    { name: 'Якшанба', customers: 280, revenue: 14000000 },
  ]

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Дашборд
      </Typography>
      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <LocationOn color="primary" sx={{ fontSize: 40, mr: 2 }} />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Локациялар
                  </Typography>
                  <Typography variant="h4">
                    {analytics?.totalLocations || 0}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <People color="primary" sx={{ fontSize: 40, mr: 2 }} />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Ходимлар
                  </Typography>
                  <Typography variant="h4">
                    {analytics?.totalEmployees || 0}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Warning color="error" sx={{ fontSize: 40, mr: 2 }} />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Рискли локациялар
                  </Typography>
                  <Typography variant="h4">
                    {analytics?.riskLocations || 0}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <TrendingUp color="success" sx={{ fontSize: 40, mr: 2 }} />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Тушум
                  </Typography>
                  <Typography variant="h4">
                    {(analytics?.revenue || 0).toLocaleString()} сум
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Ҳафталик статистика
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="customers" stroke="#8884d8" name="Мижозлар" />
                <Line type="monotone" dataKey="revenue" stroke="#82ca9d" name="Тушум (сум)" />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  )
}

export default Dashboard

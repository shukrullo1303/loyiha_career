import React from 'react'
import { useQuery } from 'react-query'
import {
  Box,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  IconButton,
} from '@mui/material'
import { Edit, Delete } from '@mui/icons-material'
import apiClient from '../api/client'

function Locations() {
  const { data: locations, isLoading } = useQuery('locations', async () => {
    const response = await apiClient.get('/locations/')
    return response.data
  })

  if (isLoading) {
    return <Typography>Юкланмоқда...</Typography>
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Локациялар
      </Typography>
      <TableContainer component={Paper} sx={{ mt: 3 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Номи</TableCell>
              <TableCell>Манзил</TableCell>
              <TableCell>Тури</TableCell>
              <TableCell>ИНН</TableCell>
              <TableCell>Статус</TableCell>
              <TableCell>Амаллар</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {locations?.map((location: any) => (
              <TableRow key={location.id}>
                <TableCell>{location.name}</TableCell>
                <TableCell>{location.address}</TableCell>
                <TableCell>{location.location_type}</TableCell>
                <TableCell>{location.tax_id || '-'}</TableCell>
                <TableCell>
                  <Chip
                    label={location.is_active ? 'Фаол' : 'Нофаол'}
                    color={location.is_active ? 'success' : 'default'}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <IconButton size="small">
                    <Edit />
                  </IconButton>
                  <IconButton size="small">
                    <Delete />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  )
}

export default Locations

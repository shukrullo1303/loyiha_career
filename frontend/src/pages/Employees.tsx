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
} from '@mui/material'
import apiClient from '../api/client'

function Employees() {
  const { data: employees, isLoading } = useQuery('employees', async () => {
    // Содда версия - локация ID керак
    return []
  })

  if (isLoading) {
    return <Typography>Юкланмоқда...</Typography>
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Ходимлар
      </Typography>
      <TableContainer component={Paper} sx={{ mt: 3 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ФИО</TableCell>
              <TableCell>Лавозим</TableCell>
              <TableCell>Телефон</TableCell>
              <TableCell>Рўйхатдан ўтган</TableCell>
              <TableCell>Статус</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {employees?.map((employee: any) => (
              <TableRow key={employee.id}>
                <TableCell>{employee.full_name}</TableCell>
                <TableCell>{employee.position || '-'}</TableCell>
                <TableCell>{employee.phone || '-'}</TableCell>
                <TableCell>
                  <Chip
                    label={employee.is_registered ? 'Ҳа' : 'Йўқ'}
                    color={employee.is_registered ? 'success' : 'error'}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  <Chip
                    label={employee.is_active ? 'Фаол' : 'Нофаол'}
                    color={employee.is_active ? 'success' : 'default'}
                    size="small"
                  />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  )
}

export default Employees

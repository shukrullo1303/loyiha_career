import React, { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from 'react-query'
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
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  CircularProgress,
  Alert,
  MenuItem,
} from '@mui/material'
import { Edit, Delete, Add as AddIcon } from '@mui/icons-material'
import apiClient from '../api/client'

interface Location {
  id: number
  name: string
  address: string
  tax_id?: string | null
  is_active: boolean
  location_type: string
}

interface LocationFormValues {
  name: string
  address: string
  tax_id?: string
  location_type: string
}

function Locations() {
  const queryClient = useQueryClient()
  
  // Modal oynasi va tanlangan qator uchun statelar
  const [open, setOpen] = useState(false)
  const [selectedLocation, setSelectedLocation] = useState<Location | null>(null)

  // 1. GET - Ma'lumotlarni o'qish
  const { data: locations, isLoading, isError } = useQuery<Location[]>(
    'locations',
    async () => {
      const response = await apiClient.get('locations/')
      return response.data
    }
  )

  // 2. POST (Yaratish) va PUT (Yangilash) uchun umumiy mutatsiya
  const saveMutation = useMutation<any, any, LocationFormValues>(
    (data) => {
      if (selectedLocation) {
        // Agar selectedLocation bo'lsa - PUT (Update)
        return apiClient.put(`/locations/${selectedLocation.id}/`, data)
      } else {
        // Agar selectedLocation bo'lmasa - POST (Create)
        return apiClient.post('locations/', data)
      }
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries('locations') // Jadvalni yangilash
        handleClose()
      },
      onError: (err: any) => {
        alert(err?.response?.data?.detail || 'Xatolik yuz berdi')
      }
    }
  )

  // 3. DELETE - O'chirish
  const deleteMutation = useMutation<void, any, number>(
    (id) => apiClient.delete(`/locations/${id}/`),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('locations')
      }
    }
  )

  // Modalni ochish (Yangi yoki Tahrirlash uchun)
  const handleOpen = (location: Location | null = null) => {
    setSelectedLocation(location)
    setOpen(true)
  }

  const handleClose = () => {
    setOpen(false)
    setSelectedLocation(null)
  }

  const handleDelete = (id: number) => {
    if (window.confirm("Ushbu lokatsiyani o'chirishni xohlaysizmi?")) {
      deleteMutation.mutate(id)
    }
  }

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const formData = new FormData(event.currentTarget)
    const raw = Object.fromEntries(formData.entries()) as Record<string, FormDataEntryValue>
    const data: LocationFormValues = {
      name: (raw.name as string) || '',
      address: (raw.address as string) || '',
      tax_id: (raw.tax_id as string) || undefined,
      location_type: (raw.location_type as string) || 'other',
    }
    
    // Checkbox yoki status bo'lsa shu yerda convert qilinadi
    saveMutation.mutate(data)
  }

  if (isLoading) return <Box sx={{ display: 'flex', justifyContent: 'center', p: 5 }}><CircularProgress /></Box>
  if (isError) return <Alert severity="error">Ma'lumotlarni yuklashda xatolik!</Alert>

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Lokatsiyalar</Typography>
        <Button 
          variant="contained" 
          startIcon={<AddIcon />} 
          onClick={() => handleOpen()}
        >
          Yangi qo'shish
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead sx={{ backgroundColor: '#f5f5f5' }}>
            <TableRow>
              <TableCell>Nomi</TableCell>
              <TableCell>Manzil</TableCell>
              <TableCell>INN</TableCell>
              <TableCell>Status</TableCell>
              <TableCell align="right">Amallar</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {locations?.map((loc: Location) => (
              <TableRow key={loc.id} hover>
                <TableCell>{loc.name}</TableCell>
                <TableCell>{loc.address}</TableCell>
                <TableCell>{loc.tax_id || '-'}</TableCell>
                <TableCell>
                  <Chip 
                    label={loc.is_active ? "Faol" : "Noactive"} 
                    color={loc.is_active ? "success" : "default"} 
                    size="small" 
                  />
                </TableCell>
                <TableCell align="right">
                  <IconButton color="primary" onClick={() => handleOpen(loc)}>
                    <Edit fontSize="small" />
                  </IconButton>
                  <IconButton color="error" onClick={() => handleDelete(loc.id)}>
                    <Delete fontSize="small" />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Qo'shish va Tahrirlash Modali */}
      <Dialog open={open} onClose={handleClose} fullWidth maxWidth="sm">
        <form onSubmit={handleSubmit}>
          <DialogTitle>
            {selectedLocation ? 'Lokatsiyani tahrirlash' : 'Yangi lokatsiya qo\'shish'}
          </DialogTitle>
          <DialogContent dividers>
            <Box sx={{ display: 'grid', gap: 2, pt: 1 }}>
              <TextField
                name="name"
                label="Lokatsiya nomi"
                fullWidth
                required
                defaultValue={selectedLocation?.name || ''}
              />
              <TextField
                name="address"
                label="Manzil"
                fullWidth
                required
                defaultValue={selectedLocation?.address || ''}
              />
              <TextField
                name="tax_id"
                label="INN (Tax ID)"
                fullWidth
                defaultValue={selectedLocation?.tax_id || ''}
              />
              <TextField
                select
                name="location_type"
                label="Turi"
                fullWidth
                required
                defaultValue={selectedLocation?.location_type || 'other'}
              >
                <MenuItem value="cafe">Kafe</MenuItem>
                <MenuItem value="restaurant">Restoran</MenuItem>
                <MenuItem value="tea_house">Choyxona</MenuItem>
                <MenuItem value="hair_salon">Sartaroshxona</MenuItem>
                <MenuItem value="car_wash">Avtoyuvish</MenuItem>
                <MenuItem value="service_center">Servis markaz</MenuItem>
                <MenuItem value="household_service">Maishiy xizmat</MenuItem>
                <MenuItem value="other">Boshqa</MenuItem>
              </TextField>
            </Box>
          </DialogContent>
          <DialogActions sx={{ p: 2 }}>
            <Button onClick={handleClose} color="inherit">Bekor qilish</Button>
            <Button 
              type="submit" 
              variant="contained" 
              disabled={saveMutation.isLoading}
            >
              {saveMutation.isLoading ? 'Saqlanmoqda...' : 'Saqlash'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Box>
  )
}

export default Locations
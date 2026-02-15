import React from 'react'
import { View, Text, StyleSheet, FlatList } from 'react-native'
import { useQuery } from 'react-query'
import axios from 'axios'
import { useAuthStore } from '../store/authStore'

const API_URL = 'http://localhost:8000/api/v1'

export default function LocationsScreen() {
  const { token } = useAuthStore()

  const { data: locations } = useQuery(
    'locations',
    async () => {
      const response = await axios.get(`${API_URL}/locations/`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      return response.data
    },
    { enabled: !!token }
  )

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Локациялар</Text>
      <FlatList
        data={locations}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text style={styles.cardTitle}>{item.name}</Text>
            <Text style={styles.cardSubtitle}>{item.address}</Text>
            <Text style={styles.cardType}>{item.location_type}</Text>
          </View>
        )}
      />
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 15,
    marginBottom: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  cardSubtitle: {
    fontSize: 14,
    color: '#666',
    marginBottom: 5,
  },
  cardType: {
    fontSize: 12,
    color: '#1976d2',
  },
})
